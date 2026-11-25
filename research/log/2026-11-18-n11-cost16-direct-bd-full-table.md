# 2026-11-18 N11 cost-16 parent direct mode B_d 全31行独立再計算（published b_slices 全行一致・総和==B16）

## 成果

31行 cost-16 parent `00000000000000003800000008001000` の **direct mode B_d（行d二重被覆型の寄与）を全31行独立再計算し、published per-d slice表（`cost16-b-phase-total-20261118.json`・commit `9b2747f0`）と全行一致（0不一致）・総和が B16 = 660,663,050,386,546,968 と厳密一致**した。B16の検証経路はこれで (i) per-doubled-row d-slice（published・shared memo）、(ii) per-pair-type groups分解（`a5ca4443`・恒等式 sum(b_part)/16==B16）、(iii) direct mode全行（本run・各行fresh memo）の3経路となり、**per-d行レベル・per-pair-typeレベル・総和レベルのすべてが独立に一致**した。

- JSONL: `output/cost16-b-direct-20261118.jsonl`（31 records。前回出版時はd=18,2の2行spot check → 本runで31行に拡張）
- 完了検証script: `verify_cost16_phaseb_groups_completion_20261118.py` のdirect部を spot check（rows [2,18]）から全表照合（rows 0..30・各行==published b_d・sum==B16）へ拡張し再実行。**25 checks all PASS・二重実行byte-identical（verification JSON sha256 `addcf891c…`）**。

## 主要数値

1. **全31行一致**: d=0〜30の B_d が published `b_slices` と0不一致（最小 d=18: 18,319,351,945,126,110（bottleneck行）・最大 d=2,3,13: 23,475,415,507,703,040（対称類ハブ3行））。行2・行3・行13の対称類（同B_d・同pair degree 30）も直接確認。
2. **総和恒等式**: Σ_d B_d = 660,663,050,386,546,968 == B16（exact）。
3. terms数（=N(d)の2-組み合わせ数）は276（d=18,19・最小）〜435（d=2,3,13・最大）で、published sliceのanchors 276〜435と一致。

## 実験的事実

- 各行は1 invocation・fresh memo（STATE_CAP 8M・実測memo 3,522,873〜3,524,540状態・RSS ~450MB・33〜40秒/行）。cgroup 1.04GB上限内で全行安全圏。
- invocationごとにknowledge scratchへsnapshot（環境リセット1回発生したが0レコード喪失）。
- 本日の転記誤り2件（設計log (4,29) b_part・groups進捗log d=2 B_d）に続く全行照合で、published b_slices側に同種の誤りがないことを機械確認。

## 次課題

1. top-10 joint membership（上位pair root 45組み合わせ・単純和top-10 44.23%に対する真のkill（包含排除）の確定）。行共有pairのjointはB型coverのみで非ゼロ（23行・29行parentと同一構造）。
2. ban生存曲線（31行版・A位相40秒+31 d-slice ~19分/k点）。
3. membership上位rootの実際のverdict評価は並走sweep-lane管轄のまま。

## 解釈上の注意

B_d・membershipは代替最小cover計画の組合せ数であり探索コストでもverdictでもない。REFUTED-D10・STERILEはLOSS証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
