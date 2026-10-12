# 11×11 central-reply frontier for the 19 unresolved opening orbits

## Result

This analysis starts from K0414's solver-trusted LOSS proof for `{60,27}` and K0415's 21-orbit opening partition. The K0414 baseline was independently regenerated here: 119 legal third moves, 3,384 canonical S4 classes, 367,228 S4→S5 boundary edges, 121,088 unique canonical S5 children, and 5,613 current exact-cache hits. Its 119/119 LOSS-S4 response coverage matches K0415.

For each of the other 19 first-move D4 representatives, the pair `{first,60}` has 119 legal third moves. Independent integer geometry reconstructs every S3→S4 boundary, then derives each S4 status from the current exact S5 cache: an S4 is WIN if any S5 child is exact WIN, LOSS if every S5 child is exact LOSS, and UNKNOWN otherwise. All 19 pair roots remain UNKNOWN. Existing LOSS-S4 responses cover between 4 and 10 of 119 third moves; no new first-move orbit is classified.

| Initial D4 orbit | First representative | Orbit size | Third-move D4 orbits | Third moves with known LOSS-S4 response | S4 classes | Unique S5 children | Exact S5 hits (LOSS/WIN) | Validated saved S5 raws |
|---|---:|---:|---:|---:|---:|---:|---:|
| `[0,4]` | 16 | 4 | 64 | 10 | 3,402 | 123,066 | 1,112 / 56 | 3 |
| `[0,2]` | 38 | 4 | 64 | 10 | 3,400 | 122,756 | 759 / 14 | 3 |
| `[0,1]` | 49 | 4 | 64 | 10 | 3,374 | 119,917 | 730 / 32 | 1 |
| `[3,3]` | 24 | 4 | 64 | 8 | 3,384 | 121,108 | 458 / 34 | 0 |
| `[5,5]` | 0 | 4 | 64 | 7 | 3,396 | 122,953 | 493 / 1 | 65 |
| `[1,3]` | 26 | 8 | 119 | 7 | 6,542 | 234,600 | 938 / 14 | 3 |
| `[1,1]` | 48 | 4 | 64 | 7 | 3,377 | 120,191 | 918 / 61 | 0 |
| `[4,4]` | 12 | 4 | 64 | 6 | 3,389 | 121,758 | 1,002 / 67 | 65 |
| `[2,3]` | 25 | 8 | 119 | 6 | 6,585 | 238,948 | 808 / 3 | 7 |
| `[2,5]` | 3 | 8 | 119 | 6 | 6,612 | 242,082 | 1,061 / 20 | 7 |
| `[3,4]` | 13 | 8 | 119 | 6 | 6,586 | 239,298 | 758 / 9 | 6 |
| `[3,5]` | 2 | 8 | 119 | 6 | 6,594 | 240,450 | 856 / 12 | 6 |
| `[2,4]` | 14 | 8 | 119 | 6 | 6,577 | 238,259 | 899 / 5 | 4 |
| `[0,5]` | 5 | 4 | 64 | 6 | 3,385 | 121,444 | 622 / 8 | 0 |
| `[1,4]` | 15 | 8 | 119 | 5 | 6,590 | 239,477 | 736 / 20 | 7 |
| `[1,5]` | 4 | 8 | 119 | 4 | 6,588 | 239,510 | 505 / 7 | 7 |
| `[4,5]` | 1 | 8 | 119 | 4 | 6,615 | 242,823 | 636 / 4 | 6 |
| `[1,2]` | 37 | 8 | 119 | 4 | 6,546 | 234,876 | 505 / 13 | 2 |
| `[2,2]` | 36 | 4 | 64 | 4 | 3,388 | 121,391 | 275 / 9 | 0 |

The table ranks `{16,60}` first for a future cache-aware continuation: it ties the maximum existing LOSS-S4 coverage at 10/119 and has the most exact S5 hits (1,168). `{38,60}` and `{49,60}` tie coverage but have fewer current-cache hits. This ranks boundary reuse; it does not say those pair roots are LOSS or estimate solver runtime.

## Other second moves and reuse limits

The exact S5 cache has 5,851 rows (5,692 LOSS and 159 WIN); 65 rows have a nonzero solver-node field. The active main cache is the only cache used to derive S4 labels. A scan of 485 tracked `.cache` files found no standalone S4 exact cache. Reverse-indexing all current S5 rows reconstructs 32 cache-derived S4 LOSS classes, exactly the 32 used in K0414's root proof.

The saved-raw audit was rechecked: all 23 source receipts and 176 unique raw files match their SHA-256 and replay fields; the audit records 202 raw references and zero untracked-local raw references. The table's raw column counts direct exact S5 raw keys that also occur below that pair root. The 65 raw hits at first moves 0 and 12 are reused records from K0414's already-closed boundary; they do not provide broad coverage for the remaining third moves.

All 120 legal second moves after each unresolved first-move representative were grouped under that first move's D4 stabilizer and ranked by existing LOSS-S4 coverage. The best noncentral candidate is `{0,63}`: three known LOSS-S4 classes cover 4/119 third moves, versus 7/119 for `{0,60}` after first move 0. No alternative reply reaches a complete LOSS response table. The central response remains the strongest current reply candidate across the 19 orbits.

Across the 20 analyzed roots (the 19 candidates plus `{60,27}`), 34,869 canonical S4 classes and 968,263 canonical S5 children occur in more than one root boundary. The known `{60,27}` boundary shares 3,383 of its 3,384 S4 classes and all 121,088 of its S5 children with at least one candidate boundary. This is reusable geometry and cache coverage, not independent proof of the unknown S5 outcomes.

## Small-search decision

The top three central roots `{16,60}`, `{38,60}`, and `{49,60}` contain 9,517 distinct S4 classes: 9 known LOSS, 186 known WIN, and 9,322 UNKNOWN. Among UNKNOWN S4 classes in these roots, the fewest missing exact S5 children for any one class is 51; none can be closed with three or fewer new exact results. The best shared candidate S4 classes still have 98–99 missing S5 children, despite potentially adding coverage to 12 unresolved root/third-move pairs if all those children eventually prove LOSS.

No new solver exploration was started: a small number of exact S5 results cannot close even one currently UNKNOWN S4 boundary. The best next pair to revisit remains `{16,60}`, but it requires a broader exact boundary plan. The saved missing-child counts and legal-move counts are prioritization features only, not solver-node or runtime guarantees.

## Trust boundary and reproduction

S3/S4 geometry is rebuilt with the independent integer-geometry `Board`. Cache-derived S4 labels use only the current solver-trusted exact S5 cache. The raw checks bind to K0414's audited artifacts. No new terminal-only proof DAG was generated; K0414's solver-trusted leaf dependency and K0416's 2,992 unclosed S5 roots remain unchanged. A WIN result for any two-stone root would not by itself classify the opening first move.

```powershell
uv run --locked python research/experiments/n11-central-reply-frontier-20261012/scripts/analyze_central_reply_frontier.py
uv run --locked python research/experiments/n11-central-reply-frontier-20261012/scripts/rank_cached_second_replies.py
uv run --locked python research/experiments/n11-central-reply-frontier-20261012/scripts/select_small_s5_probe.py
```

`output/central-reply-frontier.json` stores all 119 third moves for each of the 19 roots, S3/S4 boundary counts, cache/raw reuse, cross-root sharing, and the cost-proxy ranking. `output/cached-second-reply-ranking.json` stores the global S4 reverse index and per-opening second-reply candidates. `output/small-s5-probe-readiness.json` records the unknown S4 completion gaps. The three JSON files contain input SHA-256 values and leave every unsupported verdict as UNKNOWN.
