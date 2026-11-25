# cost64h fold receipt vs preregistration agreement check (2026-11-17)

## 背景

cost64h（child `00000000000000403800000008100000`）の23 WIN7-D10 receipt fold receiptが
並走レーンにより `828c595c` でmain着地した（`class-frontier-cost64h-receipts-recompute-20261117.json`、
git blob `1633be292f6f1862c895009eac29d398d0be7738`）。本レーンはfold receipt着地**前**に
preregistration（`c64579b4`・blob `5074a8a0cbb75fcc91b5b999a3135fac06d42400`）と
machine agreement checker（`check_cost64h_fold_receipt_agreement_20261116.py`、self-test 18/18、`637c2e98`/`c8a658f8`）
を出版済みであり、resume計画どおり着地後の全フィールド照合を実行した。

## 実行

- 入力は着地済みmain（commit `665c115f`）からraw CDNで取得し、git blob SHAを照合:
  prereg `5074a8a0...` 一致、fold receipt `1633be292f...` 一致。
- `--selftest` 18/18 PASS を実行後に、着地fold receiptに対してcheckerを実行。
- 2回実行で出力byte-identical（md5 `12eb73f2780945779db9ea24a3ef3b90`）。

## 結果（19/19 checks PASS、mismatch 0・note 0）

- C1/C2/C2b: fold record読み取り可・receipts 23・baseline head 1452一致。
- C3: projected head 6数値 `[1472, 174, 6376, 504672, 4649, 368586]` 完全一致。
- C4/C5: demand histogram（open-only 9バケット）とdeltas完全一致。
- C6/C7: total marginal 111・marginal_in_manifest 20一致。
- C8/C9: closed manifest row 20件の集合完全一致・child row閉鎖（bit 4）確認。
- C10/C10b: affected parents 17件の集合とrows_before/after・lost_rows完全一致。
- C11/C12: parent row incidences 42・edge cost delta 3090一致。
- C13/C14: WIN bit 23件の集合一致・**fold順序がpreregの昇順bit順と同一のためper-receipt marginal/mimが全bitでbit-exact一致**。
- C15/C16: conflict census 0・全root hexが `child|1<<bit` 再構成と一致。

着地fold receiptはpreregistrationの事前投影と全数量で一致した。並走のfold audit
（`class2-lane-cost64h-fold-audit-20261117.json`・145 checks PASS）とも矛盾なし
（prereg blob pin `5074a8a0` を両者が参照）。

## 制限

- agreement checkはbookkeeping照合であり、engine search・新規verdictは存在しない。
- solved 1472はmanifest被覆の簿記。WIN7-D10証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明する。
- REFUTED-D10はLOSS証明ではない。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれもUNKNOWN。

## 成果物

- `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64h-fold-receipt-agreement-20261116.json`
- checker（事前出版済み・本実行で改変なし）: `.../scripts/check_cost64h_fold_receipt_agreement_20261116.py`

## 次の一手

- head-1472 cover-multiplicity監査（preregistration prediction `d4f5044f` との照合）は同一セッションで実行
  （別log `2026-11-17-n11-class2-lane-head1472-cover-multiplicity-audit.md`）。
- cost76c fold receiptは未着地（並走claim済み・着手禁止）。着地後は本checkerの76c版を同様に実行。
- cost66i receipt foldは76c fold着地まで着手禁止（依存は64h着地で解消済み・`41e15e5a`）。
