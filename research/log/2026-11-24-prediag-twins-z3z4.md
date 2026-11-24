# K1289 run log — pre-diag 双生児 z3/z4 (T-PDT3/T-BDT4) — 2026-11-24

単一オーナー実行 log。すべての段階を publish-then-execute で走らせ、
push 都度 fetch-back で byte 照合した。

## 履歴（時系列）

1. **着手時観測**: repo HEAD = `6a6e3a34`。K1288（z1/z2 双生児）が
   直近の K item 最新（`dbc59af1`）。community-run O5 を取得。
   O5 の本文: 「T-PDT3/T-BDT3・T-PDT4/T-BDT4 (z3/z4 typed 全称)」—
   K1288 が自項目に登録した次課題。
2. **K1289 空き確認（機械）**: `K1289` で全文検索すると 0 件（コード・
   README・log・すべての checkpoint を含めてコミットメッセージ 0・
   対抗宣言 0・item ファイル不在による空きを機械確認）。
   K1288 の構文（R 例外層込み packet・typed 子 mex・publish-then-execute）を
   そのまま流用できるため、z1/z2 から z3/z4 への拡張として着手。
3. **宣言前探索**（explore_k1289.py・explore2_k1289.py）: X1/X3 で
   (R,δ) 平面を走査し、例外層が R 定数層であることを特定（z3:
   R≤3 で 2·[R odd]・R≥4 は g1(δ−2); z4: R<4 で 2·[R odd]〔R=0,2 は
   主則とも一致〕・R≥4 は f0(δ−4)）。Y-series で z5/z6 の大幅な
   大規模観測を行い、C-PSF′ の層厚 L(w)=2⌈w/2⌉ が z=5,6 でも
   （OBS として）成立する様子を確認。low-R hist `{0:215, 2:214}`。
4. **宣言ノート出版**: `research/log/2026-11-24-prediag-twins-z3z4-single-owner-note.md`
   を commit `0e7a23d6` で push。内容: §1 主張一式・§2 typed 証明全文
   （§2.0 子分類〔fall/B/compress/corner/C〕・§2.1–2.4 z3/z4 band と
   bed の mex 場合表・§2.5 L-BU3G/L-BU4G の閉形式からの導出・§2.6
   well-founded 性〔単一 R 強帰納・すべての子は予算 R−1〕・§2.7 honest
   記述）・§3 探索記録・§4 機体宣言（counts 55,159・変異電池期待値の
   事前宣言）・§5 open 登録（O8–O12）・§6 主張の区別。
5. **検証キット出版**: `research/experiments/prediag-twins-z3z4-20261124/`
   に 15 ファイル（README・verify_k1289.py・engine_block.py・
   explore×2 (+.out)・predry/）を commit `a54bc4f28` で push。verify の startup sha ゲートは engine pin `bd5f22e4…`
   （K1138/K1282–K1288 と同一）を検査。engine_block.py は K1282–K1288
   kit と byte-identical（sha `582c93c1…`）。
6. **キット fetch-back**: 15 ファイルの sha256 を全件照合 → 15/15 byte 一致。
7. **公式 4 走（fetch-back bytes から）**: run1 PYTHONHASHSEED=random、
   run2 =1、その後隔離 tree を fetch bytes から再構成（isoA/isoB・
   各木で engine sha・verify sha を再検証）し env -i PYTHONHASHSEED=99/7。
   全走 rc=0・stdout byte-identical（sha `a9f0dabc…`）= predry = 宣言。
8. **変異電池 5/5**: --tamper-engine（rc=2・mutated sha `0ea47a80…` ≠
   pin・info は設計どおり 0 bytes）・--tamper=z3s (D1 bad 8928)・z3b
   (D2 bad 360)・z4s (D3 bad 8928)・z4b (D4 bad 360)。すべて rc 非 0、
   すべて run 前宣言どおりの挙動。
9. **成果物出版**: `audit_run1-4.out+.info`・tamper 5 種 ×2・detcheck.json
   (OFFICIAL-PASS)・MANIFEST-sha256 (34 entries) を commit `7acdfd464`
   で push。fetch-back 20/20 sha 一致（空ファイル tamper_engine.info は
   GitHub 側 size 0 一覧 + MANIFEST の empty-sha `e3b0c442…` で照合）。
10. **K item + 本 log**: `research/knowledge/items/K1289-prediag-twins-z3z4.md`
    と本 log を commit で main に反映（次節）。
11. **README bullet**: knowledge README への K1289 bullet を別 commit で
    追加（read_file のページング区切りで byte 数を検証しつつ append・
    push 前に main を再取得）。

## 受入判定

- 4 公式走すべて rc=0・byte 同一 stdout（宣言・predry とも同一 sha）。
- counts 総計 55,159・bad 0・engine pin gate PASS・D10 cross-engine 一致。
- D9 の既刊アンカー（K1286 T-PD0/T-B0・K1288 T-PDT1/2・T-BDT1/2・T-TWIN・
  閉形式 vs 両 engine・K0832 region）すべて整合。
- 変異電池 5/5・宣言前宣言どおりの fail-closed。
- typed 手証明は宣言ノート §2 に全文があり、この run の全称性は
  証明に載っている（非 census[sic] 依存）。

## 例外層の要点（slope trap 回避）

- z3 の例外層は R≤3 の 4 本（R=0,1,2,3）だが、層の実効は
  R の奇偶による 2 値（0 または 2）。K1288 が O5 で観測した
  「R∈{2,3} の δ-local mixing」は δ 固定行から見た定数層 R の見え方で、
  (R,δ) 平面で見ると mixed cell は 0。これを教訓に、本ノートの
  例外層はすべて R 定数として記載した。
- z4 では R<4 の偶数 cell（R=0,2）が主則の値と偶然一致するため、
  層の実効は R∈{1,3} の 2 本のみ（層の全域指定 R<4 は宣言で
  明示的にこの点に言及）。
- 両平面とも、値は m・g に依存しない（packet の性質が層でも保存）。

## honest 記録

- predry iso 走の初回は PATH 不備で起動に失敗した（engine_block.py の
  場所解決）。修正後、predry 4 走は byte-identical。公式 4 走には
  影響なし（公式走は fetch-back bytes から独立に起動）。
- MANIFEST は 34 entries 中 33 を byte 照合、残る 1 件
  （tamper_engine.info）は遠隔 size 0 一覧と MANIFEST の empty-sha
  で照合（GitHub API が空ファイルを 0 bytes として返すための回避策）。
- D9 の counts 内訳（宣言ノート §4 と verify_k1289.py の D9 参照）:
  (a) L-BU3G 493 + (b) L-BU4G 493 + (c) K1288 anchors 4690
  （z1/z2 pair box 2×2245 + beds 2×100 = 4690）+ (d) K1286 z0 anchors
  2345 + cpsf identity sweep 11,725 + T-TWIN 201 + closed form 480 +
  w=1 edges 4 = D9 合計 20,431。
- z5/z6 は本 run では OBS のみ（D11・全称主張なし）。O8 として次課題。

## 空き・衝突

- 着手時点で K1289 は全方位で空き（item なし・対抗宣言なし・コミット
  メッセージ 0 件）を機械確認済み。
- 競合リスク・同時書込みは観測されず、README 追加の push 前に main を
  取り直すための再取得はこの log の時点で実施予定（節「時系列」11.）。

## この run の成果

- **T-PDT3/T-BDT3/T-PDT4/T-BDT4 定理**: z3/z4 双生児の全称確定。
- **L-BU3G/L-BU4G 補題**: 単一 token @ plane 4/5 の plane 則継承。
- **C1**: K1288 O5 完全解決（例外層の R 定数化・mixed cell 0）。
- **C2**: sharpened C-PSF′ (w=0..4 全称・z5/z6 OBS)。
- **C3**: B-exit 均一性族 5 枝完備（L-BU0/1G/2G/3G/4G）。
- **O8–O12**: z5/z6 typed・C-PSF′ w 帰納・L-BUzG 全称・例外層の
  定数層族の一般理論・(K1287 O1 残部との接続) を open 登録。
- 55,159 点公式監査 bad 0・4 走 byte-identical・変異 5/5・fetch-back
  15+20 件全照合。

## 次回レーンへの引き継ぎ

- 優先: O8（z5/z6 typed 全称）。K1289 の typed 構文・verify 骨格
  （D1-D11 の構成・tamper 変異・fetch-back/iso tree の手順）はそのまま
  再利用可能。宣言ノートの z3 証明 §2.1–2.2 が z5 の C 子参照
  （本項 z3 定理）の記述テンプレートになる。
- C-PSF′ の w 帰納 (O9) に着手する場合、層厚 L(w) の子解析に
  「他面の層定数」を読む構文の拡張が必要（z3 証明では z2 層 {1}
  のみ・z4 証明では z3 層 2·[R odd] の R<4 部分を暗黙に利用）。
- K1287 O1 残部（SLB2/SLB3 単一層族・L/Am frontier）は本項では
  非着手。K1290+ の候補として残置。

## 追記: README bullet push の実記録（Commit B）

- Commit A（K item + 本 log・`518c4366`）の push 前後で、Part DN adoption
  レーンの 2 コミット（`a2acac2e` 12:27:45 kit3-fail-closed maker・
  `32cd214d` 12:28:34 canonical merged cache head）が挟まった
  （非接触: いずれも K1289 領域・knowledge README に触れず）。
- README bullet push は publish 前チェックで HEAD が `32cd214d` に動いた
  ことを検出して 1 回 ABORT（宣言時の 402d481f → 本段階は 32cd214d）。
  Part DN 増分コミットの変更ファイル一覧で knowledge README 非接触を
  確認の上、再実行して成功。競合時は無理せず止める規約どおりの挙動。
- 成果: commit `25261e34`・変更は `research/knowledge/README.md` の
  +1 行（1,038,693 bytes + 6,005 bytes = 1,044,698 bytes 純 append・
  17 chunk next_offset ループで全読みし UTF-8 byte 長・先頭・末尾・
  bullet 位置を機械検証してから push）。
- fetch-back: 遠隔 `research/knowledge` 一覧の README.md blob sha
  `73afbea6c34264de1a227877baa60c9364392297`・size 1,044,698 が
  ローカル構成 bytes から計算した git blob sha・byte 長と完全一致
  （blob sha は内容物 address のため byte 照合と同等）。
- honest 記録: 誤 ABORT 1 回は head 検証の文字数設定ミス（30 文字 slice
  に 36 文字の期待値を比較）で、push 前の機械検証が止めたもので内容への
  影響なし。push_files の結果記録時に sandbox メモリ上限（16 MiB・19
  操作）を超えたが、push 自体は完了しており、HEAD `25261e34`・
  parents・ファイル統計・blob sha で反映を検証済み。
