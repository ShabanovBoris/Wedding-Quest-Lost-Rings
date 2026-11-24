# Instructions for coding agents

## Read first

Read docs/GAME_SPEC.md completely, then docs/IMPLEMENTATION_PLAN.md and docs/STATUS.md. The specification is the source of truth for game requirements; this file defines the work protocol. Record conflicts or material deviations in docs/DECISIONS.md and resolve them before marking affected work done.

## Work protocol

- Begin at the first unfinished, unblocked stage. Inspect git status, existing code, available tools and dependency compatibility; preserve unrelated changes.
- Deliver small runnable increments. Graybox movement and a playable vertical slice precede bulk asset production and full campaign construction.
- Preserve the two sequential protagonists, all three pets, the search for both rings, and the non-malicious guest/jacket resolution. No invented real-life details. P0 before P1; P2 only with owner approval.
- Use explicit placeholders while inputs are missing; never label placeholder content as final. Obtain owner approval for character likenesses, personal texts, paid services, external transfer of personal references and deployment.
- At each stage run relevant checks and exercise actual browser input, document the commands, environment, results and evidence. Build success alone is not gameplay acceptance. Do not invent test results, generated assets or deployment.
- Update docs/STATUS.md, docs/IMPLEMENTATION_PLAN.md, docs/DECISIONS.md, docs/ASSET_MANIFEST.md and docs/QA.md as applicable. Commit coherent increments if permitted. At context boundaries record exact next action and known blockers. Do not mark incomplete or unverified acceptance gates DONE.
- Target scripts after bootstrap: npm ci; npm run dev; npm run typecheck; npm run lint; npm run test; npm run test:e2e; npm run validate:assets; npm run build; npm run preview. Until scripts exist, report them as not available.
- No backend, analytics, multiplayer or unnecessary dependencies. Prioritize reliable movement, save/restore, checkpoint reachability and accessible controls.
- Repository is public as of initialization. Never commit personal source or derived likeness assets, recordings, identifying texts or secrets without explicit owner approval. Keep private-input/ and private runtime staging out of Git and build inputs by default. Do not deploy private content without real access controls and explicit permission.
- Generated assets must have documented provenance and permissions. No unlicensed music. Never use arbitrary third-party assets as final without checking license.

## Starting task

Stage 0: validate environment, pin compatible dependencies, initialize TypeScript/Vite/Phaser and tests, establish dev/build smoke checks, document actual commands and decisions. Then stage 1: graybox movement. Do not start mass generation.
