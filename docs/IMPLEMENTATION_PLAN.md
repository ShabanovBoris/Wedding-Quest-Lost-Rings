# Implementation plan

Detailed mandatory acceptance criteria: GAME_SPEC.md sections 10–11. All stages below are initially TODO. Documentation handoff is not stage 0 completion.

| Stage | Work | Dependencies | Status |
| --- | --- | --- | --- |
| 0 | Bootstrap, version checks, dev/build, tooling inventory | — | TODO |
| 1 | Graybox: both heroes, movement, jump, collision, camera, touch | 0 | TODO |
| 2 | Vertical slice: bride, combat, cat, pickups, checkpoint, HUD | 1 | TODO |
| 3 | Art direction, character approvals, asset pipeline, sound | 2 | TODO |
| 4 | Full chapter 1, clue and transition | 2; art approval for final | TODO |
| 5 | Chapter 2, groom, second cat, bulldog | 4 route | TODO |
| 6 | Chapter 3, hero switching, cooperative pet abilities, rings | 4–5 routes | TODO |
| 7 | Personalization, epilogue, approved audio/photos | 3, 6 | TODO |
| 8 | QA, accessibility, performance, balancing | 4–7 | TODO |
| 9 | Release candidate and owner-authorized release | 8, owner approval | TODO |

## Execution checklist
- [ ] Stage 0: inspect repo and agent capabilities, select/pin versions, initialize package and lockfile, verify dev and build, record commands.
- [ ] Stage 1: verify both heroes, keyboard/touch, coyote time, jump buffer, collision and focus recovery in browser.
- [ ] Stage 2: ordinary-input 2–3 minute playable slice, pet, pickup, combat, death/reload/exit; E2E evidence.
- [ ] Stage 3: owner-approved reference sheets before bulk generation; validated atlas/pivots, manifests, sound test.
- [ ] Stages 4–6: full playable route, no softlocks, optional secrets, checkpoints, two rings granted once.
- [ ] Stage 7: licensed/approved content; no placeholder personal data in release.
- [ ] Stage 8: all P0 QA gates, first-play duration, mobile/desktop checks, privacy and production asset validation.
- [ ] Stage 9: owner-approved mode of access, anonymous access checks if private, smoke test, delivery instructions.

Independent graybox work may proceed while personal art is blocked; do not mark personal art complete. Prefer cutting P2/P1 and excess map length before removing P0 requirements. Record evidence and next action in STATUS.md.
