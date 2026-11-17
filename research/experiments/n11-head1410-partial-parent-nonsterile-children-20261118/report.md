# n11 head-1410 partial-STERILE parent の非STERILE remaining child 列挙 (2026-11-18)

## 目的

K0863（STERILE行は自出行・cross-coverを問わずどのdepth-10 WIN7 receipt rootにもcoverされない）
とK0865（head-1410の174 open S5 parentを114 own_closable / 57 partial_sterile /
3 all_remaining_sterileにorbit-level集計）に対して、**57 partial-STERILE parent
（cross_cover_required）の非STERILE remaining S6行のidentityを初めて全数列挙**する。
K0865はper-parentの集計値（rem・cost・sterile refs）を出版したが、非STERILE行の
hexは出版していなかった。K0863により、これらのparentが自前行集合から受けられる
depth-10 receipt証拠は列挙された非STERILE行に限られる。本auditはjoining自体を
raw worklistから独立再導入し、既出版の全集計値を再現した上で、cross-cover候補表
（per-parentの最小cost行・共有行のmultiplicity・全体の最小cost行）を生成する。

## 方法

`audit_partial_parent_nonsterile_children_20261118.py`（blob `6e4e0dfb942841d352a8a62be2504d74443e0cc5`）。
engine実行なし・浮動小数点なし。関連判定はK0865と同じorbit-level定義
（∃σ∈D4: σ(P) ⊆ R、121-bit 11×11 mask・8 transform）をpythonで独立実装。
出力は `output/n11-head1410-partial-parent-nonsterile-children-20261118.json`
（blob `30c8fdc4e7212bafe271662d8dcf0bbbde35b63b`・schema v1・16 checks all PASS・二重実行byte-identical）。

入力4ファイル（全てgit blob pin検証・commit `c63d9c86`時点のmain）:

- K0865 census `9c251da3138c5cb0516e097be5e5d0427dfaf5f0`
- head-1410 S6 worklist CSV `2fee1d0718547a62e346d35f5858d7913e37c097`
- head-1410 S5 closability CSV `65215b6582de6efedfed8d77d91630edd883a2cb`
- closability ranking JSON `c39c547d2ab21b8cd4f0b1f098738cc027bd9d3a`

## 検証（16 checks all PASS）

- **A. pin**: 4入力のgit blob sha1一致。
- **B. worklist shape**: 6,438行・カテゴリ計数 unswept 6390 / sterile 35 /
  win_receipt_scheduled 9 / transfer_partial 2 / win_pending 2・ranking JSONの
  counts・sterile hex list一致。
- **C. global incidence**: 行側のopen_parents総和 == parent側のrem総和 == 12,274。
- **D. row-level join再現**: 全6,438行で、census 174 parentへのorbit-related数が
  出版open_parents値と一致（不一致0）。
- **E. parent-level join再現**: 174 parent全てで children数 == remaining_s6_orbits・
  cost総和 == remaining_s7_edge_cost・sterile数 == sterile_refs_count・sterile hex集合 ==
  census sterile_refs・sterile cost総和 == sterile_cost・effRem == rem − sterile・
  effective_cost == cost − sterile_cost・S5 CSVの5カテゴリ計数
  （rows_sterile/win_pending/win_receipt_scheduled/transfer_partial/unswept）全一致・
  分類名の対応（partial_sterile ↔ cross_cover_required等）も全一致（不一致0 parent）。
- **F. sterile_row_registry**: 35行全てがworklistのsterile集合内で、各entryの
  open_parents listが本joinの再導出と一致。
- **G. 91 sterile refsの構造**: 各refがparentの1石拡張のD4正準形
  （ref hex == canon(P | 1<<b)、σ≠identityでもframe-freeに成立）・cost一致・
  worklist上sterile分類（不一致0・計91 refs）。crosscheck (2026-11-18)の18 refs
  チェックの全91 refsへの拡張に相当。
- **H. effective_worklist_top16**: 16 entry全ての hex・effective_cost・
  effective_remaining・sterile_refs_count・remaining_s6_orbits を本joinから再現。
- **I. census totals**: 174/3/57/114/91/12,274/12,183 をjoinから再現。

## 新規成果（既出版のどこにも無い内容）

- **per-parent非STERILE行表**（`parents_by_min_child_cost`・57 parent全て・
  [hex, cost]対をcost昇順）: 計4,297 child-incidence / 3,555 distinct行
  （unswept 3,542・win_receipt_scheduled 9・transfer_partial 2・win_pending 2）。
- **per-parent最小cost行**: min 57・median 66・max 76。最小は
  `00000000000000003800000001800000`（class 4・rem 75・sterile 1・非STERILE 74行）の
  cost 57行 `00000000000000003800001001800000`。なおK0865 effective worklist第1位の
  `00000000000000801202000040000000`（effCost 229・effRem 3）はmin child cost 76で
  57 parent中最下位: effective cost順位とmin-child-cost順位は別の測度である。
- **共有候補**: 709行が複数のpartial parentに所属（2 parent 676行・3 parent 33行）。
  最小の共有行は cost 59 `00000000000080809002000020000000`（2 parent）。
  33行の3-parent行は単一sweepで3 parentのD10候補に同時に入る。
- **special 13行**（`special_nonsterile_rows`）: win_receipt_scheduled 9・
  transfer_partial 2・win_pending 2（うち4行が2 partial parentに所属）。

## 解釈と境界

non-STERILEはdepth-10 receipt coverの必要条件でしかない（その行のsweepがWIN7-D10を
返す保証は無い）。本表は候補列挙・簿記であり、receiptでもverdictでもない。parent分類
（own_closable / cross_cover_required / fully_sterile）にゲーム理論的値の主張は無い。
solved数はmanifest被覆の簿記である。**REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明
ではない。** 11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれも
**UNKNOWN** のまま。trust境界は出版STERILE scanのengine depth-10 verdict健全性とD4不変性
（全出版lane verdictと同一）。本auditはengine証拠を追加しない。

## 再現

```
python3 research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/audit_partial_parent_nonsterile_children_20261118.py
```

repo rootから実行。入力はrepo内の既出版4ファイル（pin検証込み）。出力は決定的で
（sort込み）、二重実行でbyte-identicalであることを確認済み。

## フォローアップ: own_closable parentとの重複 (同日)

`audit_nonsterile_own_closable_overlap_20261118.py`（blob `4419fb9d984b662c5ede106ece308ad0a4de94e2`）が、
3,555行のそれぞれについて114 own_closable (no_sterile) parentとのorbit重複を計算する
（出力 `nonsterile-own-closable-overlap-20261118.json`・blob `92056ad9fb23a8d390e3a0d735b5558336f8b003`・
6 checks all PASS・二重実行byte-identical）。チェックは3入力のpin検証・出版集合との一致
（57 parent / 3,555行）・全3,555行でjoin再現（関連parent数 == worklist open_parents・
partial所属 == 出版membership）・parent分類の分割健全性。

- **2,609行 (73.4%) が少なくとも1つのown_closable parentにも所属**: partial parentの
  D10候補作業の大部分は、own-closable閉鎖経路が消費し得る行と重なる。
- **946行がpartial-only候補**: どのown_closable parentにも属さず、own-closable経路だけを
  進めても触れない行。profile histogramは np1_no1 2,454 / np2_no0 612 / np1_no0 301 /
  np1_no2 91 / np2_no1 64 / np3_no0 33（np = partial所属数・no = own所属数）。
  **33行の3-parent行は全てpartial-only**である。
- per-parentのown-share中央値は60.9%（最低33.3% = effCost 229第1位parentの3行中1行、
  最高82.1%）。**57 parent中45 parentで最小cost候補行がown_closableと共有**、
  12 parentの最小候補はpartial-only。
- special 13行のprofileも出版（win_receipt_scheduled 9行中のown所属等）。

own_closableとの共有は「行が両方のparent型の行集合に乗っている」ことであり、sweep予定の
保証ではない。本フォローアップも候補の簿記であり、closure・coverage・verdictの主張を
含まない。
