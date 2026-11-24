# Instructions for coding agents

Read docs/GAME_SPEC.md, docs/IMPLEMENTATION_PLAN.md, docs/STATUS.md and docs/ASSET_HANDOFF.md. GAME_SPEC defines gameplay; this file defines the work protocol. docs/ASSET_PRODUCTION.md is a brief for the owner's separate asset AI, NOT a coding task.

## Responsibility boundary
- Owner and separate external AI supply finished graphics, animation frames, backgrounds, UI, music, SFX and approved personal content. Do not generate, draw, repaint, extend, search for or substitute artwork/audio, synthesize sound or invent personal details. Do not send private inputs to external services.
- Validate supplied files and manifest, stable IDs, approval/rights, import, configure animations, timing and anchors, test in browser. Deterministic atlas packing, format conversion/optimization and runtime effects using supplied resources are allowed; creative corrections are not.
- Missing/invalid resources: list exact ID, expected format, defect and blocked gate; request owner correction. Continue independent mechanics with explicitly marked geometric dev placeholders and silence. No placeholders in release. Complete ready packs may be integrated as soon as relevant systems exist.

## Work protocol
- Begin at first unfinished, unblocked stage; inspect git status, environment, compatibility and existing code. Preserve unrelated changes.
- Deliver small runnable increments; graybox and playable vertical slice before full campaign. External asset production may precede or parallel development.
- Preserve sequential protagonists, three pets, two rings, non-malicious guest/jacket resolution. P0 before P1, P2 only with owner approval.
- At each stage run checks and test actual browser input; record real evidence, commands, environment and results. Build success alone is not gameplay acceptance. Never invent results.
- Update STATUS, IMPLEMENTATION_PLAN, DECISIONS, ASSET_MANIFEST and QA. Commit coherent increments if permitted; at context boundaries record exact next action. Distinguish gameplay-ready and asset-ready; do not mark incomplete gates DONE.
- Target scripts: npm ci; npm run dev; npm run typecheck; npm run lint; npm run test; npm run test:e2e; npm run validate:assets; npm run build; npm run preview. Report unavailable scripts honestly. Asset validation distinguishes dev from production.
- No gameplay backend, analytics, multiplayer or unnecessary dependencies. Prioritize controls, reliable saves, checkpoint reachability and accessibility.
- Repository was public at initialization. Keep asset-delivery/, private-input/, private-runtime/ outside Git/build inputs by default. Never commit private inputs, derived likenesses, recordings, identifying texts or secrets without explicit permission. No deployment without owner approval and verified appropriate access. Document rights and provenance.

## Starting task
Stage 0: inspect repo and environment, pin compatible dependencies, bootstrap Phaser/TypeScript/Vite and tests, verify dev/build, confirm ASSET_HANDOFF contract and ID mapping and inventory delivered files. Then stage 1 graybox. Missing art/audio does not block independent mechanics.
