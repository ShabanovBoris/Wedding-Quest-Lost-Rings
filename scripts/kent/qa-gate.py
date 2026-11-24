#!/usr/bin/env python3
"""Kent QA Gate for one level: mandatory project checks plus the level's automated capture.

Input (stdin): the `level_id` workflow parameter and Kent metadata. Output
(stdout): a Kent completion JSON for the `passed` or `failed` transition.
Command output goes to qa-artifacts/<level_id>/round-<N>/logs/, the capture
lands in .../round-<N>/capture/.

The script runs under the Kent service with a minimal PATH, so it stays
stdlib-only (system Python 3.9) and resolves Node through fnm or Homebrew.
"""

import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path


LEVEL_ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
STATIC_STEPS = ("typecheck", "lint", "test", "build")
RUNTIME_STEPS = ("test:e2e", "qa:capture")
DEFAULT_TIMEOUT_SECONDS = 600
TIMEOUTS = {"test:e2e": 1200}
LOG_TAIL_LINES = 40
LOG_LINE_WIDTH = 400
ARTIFACTS_DIR = "qa-artifacts"

# The active step's process group, so an interrupted gate does not leave a dev server behind.
active_process = None


def stop_active_process(signum, _frame):
    if active_process is not None and active_process.poll() is None:
        os.killpg(active_process.pid, signal.SIGKILL)
    sys.exit(128 + signum)


def run(command, cwd, env, log_path, timeout):
    global active_process
    with log_path.open("wb") as log:
        process = subprocess.Popen(
            command, cwd=str(cwd), env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True
        )
        active_process = process
        started = time.monotonic()
        try:
            process.wait(timeout=timeout)
            status = "ok" if process.returncode == 0 else "failed"
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            status = "timeout"
        finally:
            active_process = None
        elapsed = time.monotonic() - started
        if status == "timeout":
            log.write(f"\n[qa-gate] killed after {timeout}s\n".encode())
    return {"command": command, "status": status, "seconds": round(elapsed, 1), "log": log_path}


def tail(log_path, lines=LOG_TAIL_LINES):
    if not log_path.is_file():
        return ""
    content = log_path.read_text(encoding="utf-8", errors="replace").splitlines()[-lines:]
    return "\n".join(line[:LOG_LINE_WIDTH] for line in content)


def pinned_node_version(root):
    nvmrc = root / ".nvmrc"
    return nvmrc.read_text(encoding="utf-8").strip().lstrip("v") if nvmrc.is_file() else None


def find_npm(root):
    """Return npm's absolute path: PATH first, then the fnm Node matching .nvmrc (or newest), then Homebrew."""
    candidates = []
    fnm_versions = Path.home() / ".local/share/fnm/node-versions"
    if fnm_versions.is_dir():
        installed = sorted(
            (p for p in fnm_versions.iterdir() if (p / "installation/bin/npm").is_file()),
            key=lambda p: [int(part) for part in re.findall(r"\d+", p.name)],
        )
        wanted = pinned_node_version(root)
        installed = [p for p in installed if p.name.lstrip("v") == wanted] or installed[-1:]
        candidates += [str(p / "installation/bin") for p in installed]
    candidates += ["/opt/homebrew/bin", "/usr/local/bin"]
    path = os.pathsep.join(candidates + [os.environ.get("PATH", os.defpath)])
    npm = shutil.which("npm", path=path)
    if npm is None:
        raise SystemExit("qa-gate: npm is not found in PATH, fnm node-versions or Homebrew directories")
    return npm, path


def read_level_id(stream):
    try:
        data = json.load(stream)
    except ValueError as exc:
        raise SystemExit(f"qa-gate: stdin must be the workflow parameter JSON ({exc})")
    level_id = str(data.get("level_id") or "").strip()
    if not LEVEL_ID.fullmatch(level_id):
        raise SystemExit("qa-gate: level_id is required and must match [a-z0-9][a-z0-9_-]{0,63}")
    return level_id


def load_scripts(root):
    package = root / "package.json"
    if not package.is_file():
        raise SystemExit("qa-gate: package.json is not found; stage 0 (bootstrap) is not done")
    scripts = json.loads(package.read_text(encoding="utf-8")).get("scripts", {})
    missing = [step for step in STATIC_STEPS + RUNTIME_STEPS if step not in scripts]
    if missing:
        raise SystemExit(
            "qa-gate: package.json has no script(s) " + ", ".join(missing)
            + "; see docs/QA_HARNESS.md and the target scripts in AGENTS.md"
        )
    return scripts


def dependencies_current(root):
    lock = root / "package-lock.json"
    installed = root / "node_modules/.package-lock.json"
    if not lock.is_file():
        raise SystemExit("qa-gate: package-lock.json is not found; stage 0 (bootstrap) is not done")
    # A linked node_modules is managed by the owner's worktree setup and is trusted as is.
    if (root / "node_modules").is_symlink():
        return True
    return installed.is_file() and installed.stat().st_mtime >= lock.stat().st_mtime


def next_round_dir(root, level_id):
    level_dir = root / ARTIFACTS_DIR / level_id
    level_dir.mkdir(parents=True, exist_ok=True)
    existing = [int(m.group(1)) for p in level_dir.iterdir() for m in [re.fullmatch(r"round-(\d+)", p.name)] if m]
    number = max(existing, default=0) + 1
    while True:
        round_dir = level_dir / f"round-{number}"
        try:
            (round_dir / "logs").mkdir(parents=True)
            return round_dir, number
        except FileExistsError:
            number += 1


def npm_command(npm, script, *arguments):
    return [npm, "run", script] + (["--"] + list(arguments) if arguments else [])


def show(value):
    """JSON-ish values as compact text for the metrics summary line."""
    return str(value).lower() if isinstance(value, bool) else str(value)


def summarize_metrics(capture_dir):
    """Return (summary line, violations beyond the harness verdict) from capture/metrics.json."""
    path = capture_dir / "metrics.json"
    try:
        metrics = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, [f"capture/metrics.json is unreadable ({exc}); see docs/QA_HARNESS.md"]
    frame = metrics.get("frameMs") or {}
    latency = metrics.get("inputLatencyFrames") or {}
    beats = metrics.get("beats") or []
    summary = (
        "frame p50/p95/p99/max: {p50}/{p95}/{p99}/{max} ms; long tasks: {long}; "
        "input latency p50/max: {lp50}/{lmax} frames; console/page errors: {console}/{page}; "
        "failed requests: {requests}; softlock: {softlock}; beats: {ok}/{total}; verdict: {verdict}"
    ).format(
        p50=show(frame.get("p50")), p95=show(frame.get("p95")), p99=show(frame.get("p99")), max=show(frame.get("max")),
        long=show(metrics.get("longTasks")), lp50=show(latency.get("p50")), lmax=show(latency.get("max")),
        console=show(metrics.get("consoleErrors")), page=show(metrics.get("pageErrors")),
        requests=show(metrics.get("failedRequests")), softlock=show(metrics.get("softlock")),
        ok=sum(1 for beat in beats if beat.get("ok")), total=len(beats), verdict=show(metrics.get("verdict")),
    )
    violations = []
    if metrics.get("verdict") != "pass":
        listed = [str(item) for item in metrics.get("violations") or []]
        violations += listed or ["capture verdict is {!r} without listed violations".format(metrics.get("verdict"))]
    return summary, violations


def main():
    for signum in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signum, stop_active_process)

    level_id = read_level_id(sys.stdin)
    root = Path(os.environ.get("KENT_EXECUTION_ROOT") or os.getcwd()).resolve()
    load_scripts(root)
    npm, path = find_npm(root)
    env = dict(os.environ, PATH=path)
    round_dir, number = next_round_dir(root, level_id)
    capture_dir = round_dir / "capture"
    logs = round_dir / "logs"

    def announce(message):
        print(message, file=sys.stderr, flush=True)

    def execute(name, command, timeout=DEFAULT_TIMEOUT_SECONDS):
        announce(f"[qa-gate] {name}")
        step = run(command, root, env, logs / f"{name.replace(':', '-')}.log", timeout)
        step["name"] = name
        announce(f"[qa-gate] {name}: {step['status']} in {step['seconds']}s")
        return step

    if not dependencies_current(root):
        install = execute("npm ci", [npm, "ci"], 900)
        if install["status"] != "ok":
            raise SystemExit("qa-gate: npm ci failed; environment problem, not a level defect:\n" + tail(install["log"]))

    steps = [execute(step, npm_command(npm, step)) for step in STATIC_STEPS]
    static_failed = any(step["status"] != "ok" for step in steps)
    for step in RUNTIME_STEPS:
        if static_failed:
            steps.append({"name": step, "status": "skipped", "command": [], "log": None})
            continue
        if step == "qa:capture":
            arguments = ("--level", level_id, "--out", os.path.relpath(capture_dir, root))
            steps.append(execute(step, npm_command(npm, step, *arguments)))
        else:
            steps.append(execute(step, npm_command(npm, step), TIMEOUTS.get(step, DEFAULT_TIMEOUT_SECONDS)))

    violations = [step["name"] for step in steps if step["status"] != "ok"]
    metrics_summary = None
    capture_ok = any(step["name"] == "qa:capture" and step["status"] == "ok" for step in steps)
    if capture_ok:
        metrics_summary, capture_violations = summarize_metrics(capture_dir)
        violations += capture_violations

    artifacts_dir = os.path.relpath(round_dir, root)
    headline = "QA Gate, level {}, round {}: {}".format(
        level_id, number, "passed" if not violations else "FAILED (" + ", ".join(violations) + ")"
    )
    result = {"transition": "failed" if violations else "passed", "commentary": headline,
              "gate_round": str(number), "artifacts_dir": artifacts_dir}
    if violations:
        report = [headline, "", "Steps:"]
        report += ["- {}: {} ({}s)".format(step["name"], step["status"], step.get("seconds", "-")) for step in steps]
        for step in steps:
            if step["status"] in ("failed", "timeout") and step.get("log"):
                report += ["", "--- {} (last {} lines) ---".format(step["name"], LOG_TAIL_LINES), tail(step["log"])]
        if metrics_summary:
            report += ["", "Metrics: " + metrics_summary]
        if capture_dir.is_dir():
            report += ["Frames and video: " + os.path.relpath(capture_dir, root)]
        result["failure_report"] = "\n".join(report)
    else:
        report_path = capture_dir / "report.md"
        result.update(
            qa_report_path=os.path.relpath(report_path if report_path.is_file() else capture_dir / "metrics.json", root),
            metrics_summary=metrics_summary,
        )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
