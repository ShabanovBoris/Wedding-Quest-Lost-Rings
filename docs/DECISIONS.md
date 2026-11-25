# Decision log

| ID | Decision | Status / rationale |
| --- | --- | --- |
| D001 | Browser 2D platformer; Phaser + TypeScript strict + Vite; Arcade Physics | Proposed baseline in GAME_SPEC; exact versions and compatibility to verify in stage 0 |
| D002 | Static client, local progress storage, no backend for gameplay | Baseline scope; private hosting can still require access control |
| D003 | Graybox and vertical slice before full campaign; separate external art production may proceed independently | Baseline to reduce rework |
| D004 | Three chapters; two protagonists; two cats and bulldog; both rings in guest's jacket | Narrative baseline; detailed fictional scenes and mechanics are provisional |
| D005 | 15–25 minutes, forgiving difficulty, keyboard and landscape touch | Proposed targets to test, not verified |
| D006 | Public repository, no personal input committed | Initial repo metadata checked; recheck before release; private deployment undecided |

| D007 | Owner + separate AI produce ready art/audio; developer integrates only | Owner requirement, 2026-11-24. ASSET_PRODUCTION.md + ASSET_HANDOFF.md. Geometry and silence only for dev placeholders. |
| D008 | Versioned manifest and gitignored asset-delivery/ | Proposed technical handoff; confirm exact dimensions, IDs and schema at stage 0 before mass production. |
| D009 | `npm run qa:capture` per docs/QA_HARNESS.md is a stage 2 deliverable and the evidence source for level QA | Decided 2026-11-24. Problem: level look, feel and frame timing cannot be verified from code alone. Alternatives: agent-driven manual screenshots (not reproducible), no visual gate. Rationale: GAME_SPEC §11 already requires Playwright E2E and a read-only `__GAME_TEST__` snapshot; the harness makes that evidence deterministic. Impact: headless numbers are a regression signal, not a device FPS claim (QA14 stays manual). |
| D010 | Level production: design doc (docs/levels/TEMPLATE.md) → independent critique → owner approval → build → feel polish → QA Gate (`scripts/kent/qa-gate.py`) → independent review | Decided 2026-11-24. Problem: level design, responsiveness and atmosphere are the owner's top priorities and had no gate. Rationale: the approved doc is the single source of truth; the gate is deterministic. Impact: a level task ends gameplay-ready, or through the owner-approved `accept_defects` exit when the owner accepts known gate defects (decided 2026-11-25; recorded in the task with `known_defects`); release DONE still requires stages 3, 7 and 8. |
| D011 | In a Kent task worktree agents commit on the task branch; push and merge stay with the owner | Decided 2026-11-24. Problem: parallel level tasks need isolated branches, while the owner's default rule forbids agent commits without explicit permission. Alternatives: uncommitted worktrees (owner commits every task), direct work on `main` (no isolation). Impact: scoped to task branches; `main` and other owner branches keep the old rule. |
| D012 | Level feel and atmosphere are level data (event-to-VFX/SFX bindings, zone ambience, camera bounds, music cues); shared systems stay level-agnostic | Decided 2026-11-24. Problem: parallel level tasks editing shared systems would conflict and blur ownership. Alternatives: engine edits inside level tasks (merge conflicts), engine-only feel (no per-level atmosphere). Impact: stages 1–2 must expose these data hooks; a missing hook is a question to the owner, not a level-task edit. |

For new decisions record date, status, problem, alternatives, rationale, impact, and evidence. Do not silently change P0 requirements.
