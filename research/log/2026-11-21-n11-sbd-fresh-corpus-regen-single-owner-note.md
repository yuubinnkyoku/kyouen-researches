# 2026-11-21 n11 S4 (1297036692683752448,0) corpus fresh regeneration (JS replica): single-owner declaration

- Declaration time: 2026-11-21T15:39Z. HEAD at declaration: `904e7b40b2f8bf7f4e06b19d9f3de13a47124028`. This declaration claims the following 101 S5 keys so that no other agent starts the same exact searches.
- Background: the 2026-11-21 union-audit/reconciliation measurement lane
  (`research/experiments/n11-s5-frontier-census-20261121`, outputs sha256 `7280376d...`, `cd7631a5...`)
  identified 108 backward-only rows (107 LOSS + 1 WIN) that are absent from the current
  reply27 JS-replica chain (probe-13, 5,756 rows, sha256 `60e0dc34...`) and not quarantined,
  and deputed their adoption to the evidence owners. **This lane does NOT adopt them.**
  It re-executes the load-bearing part from scratch, chain-native, under the same
  recipe/evidence norms as reply27 probe #1-#13, so that dhe decided-class corpus is
  re-established in the live chain lineage by fresh computation instead of by adoption.
  Historical verdicts are used only as post-hoc comparison material; any disagreement
  (including a fresh WIN where history recorded LOSS) is published and blocks the class
  closure claim, exactly as the reply27 acceptance conditions require.
- Claimed targets (deterministic, machine-checkable selection):
  1. The 99 canonical S5 children of S4 `(1297036692683752448,0)` that are absent from the
     probe-13 chain cache (= 106 children - 7 already in chain; identical to the 99
     backward-only rows the union audit attributed to this S4). Includes
     `(1152921504607899649,536870912)` (the historically S6-derived child; handled per
     acceptance condition 5).
  2. The 2 unclaimed backward-only LOSS rows outside that S4's child set:
     `(1152921504606851072,805306370)`, `(1188950301626859520,671088640)`.
  Explicit exclusions (never started by this lane): the 7 focus-class-lane-declared
  backward-only rows (incl. the WIN row `1188950301626859520:603979776`, whose evidence
  stays with the focus lane and K0374/K0379), all reply27-two-target-declared supply probes,
  and all quarantined keys. Overlap with the reply27 13 published targets is empty by
  construction (their targets are in the chain; these keys are not).
- Execution medium: Node.js replica of the pinned exact-replay path of
  `cpp/solvers/kyouen_dfpn_root.cpp` at commit `154f3b7a67`
  (source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`),
  identical bytes to the reply27 probe publications (`scripts/jsreplay.js`, sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`). This host has no
  C++ toolchain. CPU use: at most 2 workers (host has 2 cores), fresh 2^22 PnTT per row,
  one solver per row, publish=ALL, exact-order=count, <= 15,000,000 node budget.
- Acceptance conditions (all must hold before any verdict is used or published):
  1. Node-exact validation gate (already passed on this host this session, fresh): the
     replica reproduces all 4 published raw replay rows of
     `research/experiments/n11-two-target-design-20261010/output/raw`
     (at2m x2: result 0, nodes 2,000,000, legal 98/99; 15M rows: result 2,
     nodes 3,651,923 and 5,040,200) with identical stones/legal/is_or/budget/result/nodes.
  2. Cold runs only: fresh TT (2^22) per row, deadline 0, exact-order=count, 15,000,000
     node budget per pass; a second independent pass re-runs every settled row for the
     determinism gate (identical result and node count), mirroring probe #13's twice-run
     15M gate and the Oct 12 batch norms. Budget-exhausted UNKNNUSÝÜÈ\HÙ\\ÈÛ\Ý]ÜË]\ÜÙY[\H\ØØ[]YÛHHHØÝ[Y[Y\]][ÛÝ]HÜB]\[KË]\H]È\XÝ\ÈÙ[ÛY]K]\YYYÚ]H\ËZ[\[[[YÙ\Ù[ÛY]B
\ÙX\ÚÙ^\[Y[ËÛLKZ[\[[Y^XÝX]Y]LLLÜØÜ\ËÚ[\[[XÚLMMMØLLÌMÌÙXMXÎXYMØMMÙYXÌÍMØÍMLNY
NHÝÛ\ËØ[ÛXØ[ØYH
ÈÜY[]XY\JKYØ[ÛÝ[KY\]YÍ\[Y[X\Ú\[HÞ[ËÎXÛ\ÜÈÙ[ÛY]H
ÚLMMNMÎMÌNNÙÍÍMMÍÌÍYNXÌMLLLM
KXÙ[ÙHÛBHØKLLÈÚZ[\ÙH[H]X\[[HYÚ\ÝH
ÚLMYÌMØLMXÌLMLLÍYLXØLÎLÙNÙLXXYMMØXNXØÍÙMÙNX
NÂÒSÓÔÔÈÛÛXÝYØZ[ÝH\ÙHZ[ÈÛÜÙYH\ÚÒS\XÝÛ[HÛÜ\ÈÙ^H[ÈHÛ\ÜÈÛÜÝ\HÛZ[NHÚ]\ÜÈ\ÂX\ÚYHÛÜ\ÜÛ[ÈÛ\ÜÙ\È\H[X\ÙY\ÝØÛÛ
Û\ÜÈÛÛ\][ÛXÜY
HÛHÚ]Z\ÝÛXXÚ[HÚXÚË[ÈÍÛ\ÜÈÙ\È[H\ÈX\ÙYÔÔÈ[\ÜÈHÛ\ÜË]ÚYH[XÚ[[SÔÔÈÛÛ][Û\ÈXXÚ[KXÚXÚÙYYØZ[ÝÙ[ÛY]KÈ\[[ÝHÛÝ\YÙHÛZ[HÚ]Ý]HYÙ[\]Y[ÝKXK[[ÝHÙ\YXØ]KKÜ
LMLLMLÎNMKLÍÌLLX\XÝMSH[[\ÜÈH
\ÝÜHØ^\È]Ý^\ÂSÓÕÓ\JNÈ]ÈÔÔËYKY\ÝX\ÚY\È\]YÛHÝYÚH\ÚÛÛKY^XÝ][ÛÙHÚ[ÛHX\ÚYÍÔÔÈÚ]\ÜÈ
LMLLMLÍLMLÍLÍÌLLX
ÝÛ\ËYØ[Ë^XÝYKNKÙ\È]MSKÚXÙK\[Ü]\Z[\ÛJH\ÂXXÚ[KXÚXÚÙYY[X\Ú\
[\[[Ø\YÙ[\]\ÈHÍKOÍÝ[\H[BÚ]\ÜÈ]\ÝHÛHÙHØ[ÛXØ[Ú[[H[Ù\ÝÛHSÛ\]NÈHØXÚBÝÈ\ÈÜ][Ú]Ù\ÏL\HØÝL\]Y\ÝÈXÙY[
]LK\ÍXÝ[\KY\XÝLÌLL
KÈÍÔÍÈ^Ü][Û^[Û\ÈÛHÚ]\ÜÈÙ^KÛ\ÜË]ÚYHÛÜÝ\KÛÝ\YÙK[HÛÝÙ\YXØ]H\HÙXÙYÛHHBX\ÚYØÝL]Y]\[[H
Y\YÛÜY\ÈÚ]ØÝ[Y[Y][ÛHYÊN]Y]ÙÛY\X
[ËÎÍÝ[\Y\ÈYÙ[\]YÛHH]ÈY\ÙYØXÚJK]Y]ÜÛÝÛÜÜËX
[ÝKXK[[ÝHLNKÌLNHÙ\YXØ]KÜÚ[È[Ý\ÈLÌLÈ\ÂÍ
KXÛ\ÜÚYWÌLMWØØ[Y]\ËXØXÚWØ]Ø\WÜ\L×ØØ\[[]KX[[[^KXÝ\H]ÈØXÚKHÛÝÍßXÝ][Y[\ÈÛH\Ý]YÚ]\ÈYÙ[\]YÙ\YXØ]NÈ]YÈÚZ[[]]H]Y[ÙHÈÌM
ÚXÚÙY\È]Â^\Ý[ÈÝ]\ÊH[Ù\ÈÝÝXÚH[\HØ\ËXXØ][Û]È[]ÛÝ][\È\Ù^H[\\ÜÈ
ÈX[Y\Ý
ÈØ]HÓÓ
È]ÈY\ÙYØXÚH[H
]È[NÈ\ÙHØKLLÈØXÚH]K\\Ù\Y
H
È[[\Ú\ÂÝ]]ÈYÙ[\]YÛHHÞ[Ù[ÛY]NÈ]\ÝXZ[KY]ÚYYÜH]\B\ÚÈ]ÚXXÚÈ]H\YXØ][ÛÛX\ÚY[Ý\YÙ[	ÜÈÛÛÝ\[XXØ][ÛÝXÚ\ÈHØ[YHÙ^\Ë]\Ù]\ÈÚÚ\Y[XÛÜY\B\LÈÝØÛÛÈØXÚHÛÛXÝ]XÝY[]Ú\HZ[ÈÛÜÙY[ÝÜÈXXØ][ÛH]Y[ÙH\N\ÚÛÛ\]\ÝY^XÝÝÜÈ
\XØHÚ]ÙKY^XÝ]È[Y][Û[[\[[Ù[ÛY]H]Y]
NÈÕ\Z[[[ÛHZ[[X^H\ÉÜÈ[YÊÊÈ[\B[XZ[ÈHY\[ÙH[\[Y[][ÛÈ[H]\ÊÊÈ\ÙXÝ[Û\ØYÜYZ[ÈÚ]\ÙBÝÜÈZ[ÈÛÜÙY[]ÜÙ\ØØ\[ÈH[Ü[Y[HÛYÛØ[ÎÈYÜ[ÛÙ\ÝÜXØ[ÝÜËÈØÝ\ËXÛ\ÜË[[HÙ^\ËÈÍÔÍÈ[[Y\][Û^[ÛHÚ[ÛHÚ]\ÜÈÙ^KÈ][K\ÛÝÜ[\KXØ\ÛZ[\ËÈ\Ý\ÙBÍ\ÛÝ\LLÝÙY\È[ÙYXØ][ÛÙX\ÚY[\ÈÙÝ\[\ËHÝ]\ÈÝX\HÝ[\L^LH[\HØ\[XZ[ÈSÓÕÓÙ\ËÛÛYÛÝ[Ë[Þ^X[Y\È\H]\\XÝË[[]\HØ]HÙXØÙ\[ÙHÛÛ][Û\ÜÙ\È[\ÂX\ÚYHÛË\ÝÛHÛÝÍßHÙY\È]ÈÝ\[ÝX\YX]Y[[[BØÝ[Y[][ÛÈ\È[HKY\ÝX\Ú\È]Y[ÙK]Ù\ÈÝÚÚ\\YXØ][ÛÝ\Ë