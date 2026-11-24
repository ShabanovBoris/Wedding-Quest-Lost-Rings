# Implementation plan

Detailed mandatory acceptance criteria: GAME_SPEC.md sections 10–11. All stages below are initially TODO. Documentation handoff is not stage 0 completion.

| Stage | Work | Dependencies | Status |
| --- | --- | --- | --- |
| 0 | Bootstrap, version checks, dev/build, tooling inventory | — | TODO |
| 1 | Graybox: both heroes, movement, jump, collision, camera, touch | 0 | TODO |
| 2 | Vertical slice: bride, combat, cat, pickups, checkpoint, HUD | 1 | TODO |
| 3 | Integrate and validate owner-supplied slice assets, animation and audio | 2 + external A1 package | TODO |
| 4 | Full chapter 1, clue and transition | 2 for gameplay; approved assets for DONE | TODO |
| 5 | Chapter 2, groom, second cat, bulldog | 4 route | TODO |
| 6 | Chapter 3, hero switching, cooperative pet abilities, rings | 4–5 routes | TODO |
| 7 | Personalization, epilogue, approved audio/photos | 3, 6 | TODO |
| 8 | QA, accessibility, performance, balancing | 4–7 | TODO |
| 9 | Release candidate and owner-authorized release | 8, owner approval | TODO |

## Execution checklist
- [ ] Stage 0: inspect repo and agent capabilities, select/pin versions, initialize package and lockfile, verify dev and build, record commands.
- [ ] Stage 1: verify both heroes, keyboard/touch, coyote time, jump buffer, collision and focus recovery in browser.
- [ ] Stage 2: ordinary-input 2–3 minute playable slice, pet, pickup, combat, death/reload/exit; E2E evidence.
- [ ] Stage 3: accept owner-supplied A1/full pack; validate manifest, atlas/pivots/alpha, browser animation and sound. No creative generation or sourcing.
- [ ] Stages 4–6: full playable route, no softlocks, optional secrets, checkpoints, two rings granted once.
- [ ] Stage 7: licensed/approved content; no placeholder personal data in release.
- [ ] Stage 8: all P0 QA gates, first-play duration, mobile/desktop checks, privacy and production asset validation.
- [ ] Stage 9: owner-approved mode of access, anonymous access checks if private, smoke test, delivery instructions.

External production A0–A5 belongs to owner and separate AI (ASSET_PRODUCTION.md). Stage 0 records contract and inventory. Stages 1–2 and independent gameplay 4–6 continue while integration 3 is BLOCKED. Separate gameplay-ready and asset-ready; no DONE for stages requiring missing P0 assets. A complete ready pack can be integrated as soon as relevant systems exist. Prefer cutting P2/P1 and excess map length before removing P0 requirements. Record evidence and next action in STATUS.md.
