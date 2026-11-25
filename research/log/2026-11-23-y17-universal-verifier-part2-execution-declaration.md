# 単一オーナー宣言: y=17 全称検証器 part2（C1d+C11r・K1240 昇格パイプライン）の着手（先行出版）

- 宣言時刻: push 時刻で確定する。
- 宣言時点の観測 HEAD: `83234a16`（2026-11-23T01:18:49Z・push 直前の最新 main 再取得で確認し、
  push 成功後の fetch-back で着地を確認する）。
- 宣言者: 高速レーン（vertical-fiber 系・別実行）。

## 前提: part1 の出版済み正本の採用

y=17 族全称の part1 は、同一の先行宣言スコープ
（実証宣言 `9be89a9` + amendment `03ca97a` + 検証器宣言 `b099a97`）の下で
並走実行が出版済みである（実験dir `33e0a062` / K1241 item `02a95e01` /
knowledge README bullet `83234a16`・2026-11-23T01:17-18Z）。本レーンは
part1 を重複出版せず、下記の独立複製による交叉検証の結果を以て
出版機体を正本として採用する。

- 併記（part1 独立複製の交叉検証結果）: 本レーンは part1 を別系統
  （builder 主義: 出版済み y16 part1 検証器と出版 cand17.py から
  count-asserted span/rename で組立・3回再生成 byte-identical・
  verify_y17_universal.py 37,606 B・SHA-256 `76a73b6e...`）で独立複製し、
  全12チェック PASS・6,312,890 点 bad 0 に到達していた。
  出版機体（6,343,825 点 bad 0）と全共有主張が一致し、census part ファイル
  （ordered SHA-256 `12234496...` / canonical SHA-256 `1ca205a5...`）は
  両機体で byte-identical、点数差 +30,935 は掃引広がり
  （C1 +285 / C1b +2,150 / C2 +6,174 / C3 +267 / C8 +22,059）に完全分解
  される（出版機体の掃引が全域で本機の上位集合）。C4t の 1,300 violations
  first (60,98,98) も一致。よって出版 part1 は第二独立機体による交叉検証済み
  であり、part2 はこの正本（fetch-back SHA-256 `2110ecbb...`・37,970 B）に
  in-place で接ぐ。

## part2 の範囲（先行宣言 `9be89a9` の予約事項を変更なく実行する）

- `scripts/preflight_c1d_y17.py`: 出版固定 z スライスアンカー
  （K0999/K1000・K1001・K1011 スコープ・K1065・K1077・K1087）の y=17 行を
  組込み前に三方 fail-closed 事前検査（生 H_ordered / 生 H_canonical /
  cand17・z0 ∈ {8,9,10,15,16,17}・x=17..45・R<=x+z0+30）。
  低 R 単一トークン還元の事前検査（z0 ∈ {15,16,17}・x=17..159・
  R<=z0+6 で cand17 == single_token(x+17,z0,R)）。
  アンカー関数ブロックは y=10 part2 検証器の transcribed block から
  verbatim（y=13/y14/y15/y16 part2 と同一の出版ブロック）。
- C1d: 上記アンカーの y=17 行評価 x=17..159・R<=x+61 の cand17 照合 +
  低 R 単一トークン還元 R<=z+6（z=15..17）。y=7..y16 part2 と同一掃引定数。
- C11r: `census_rows.py` 第三実装（独立生二重回帰・ZHI=80・XMIN=17・
  XMAX=70・RBUF=19・LRU cap 1,600,000・tail 主張 R>=x+z+18 ⇒ (x+17)%2 の
  行内 assert）が書く `output/census.txt`（80*54=4,320 行）を cand17 から
  行ごとに再導出照合（T/P 集合・Thue-Morse index・tail）。ledger の欠落・
  重複行・不揃いは FAIL-CLOSED。
- 既存12チェック本体は byte-invariant（出版 part1 の docstring 約束）。
  main() のチェック集合は14チェックに拡張、STAGE 文字列は part 2 に更新。
- 品質ゲート: preflight PASS 後にのみ組込み。14チェックフル実行
  （C11ordered + C11canonical census part 生成を含む）3回 byte-identical
  （同一 cwd 2回 + 隔離 tree/cwd/HOME・PYTHONHASHSEED=random 1回・隔離側で
  census part/census.txt 再生成）・fail-closed 改ざん電池（part1 の
  7種に加え preflight json・census.txt 行改ざん・欠落・重複の追加種）。
- PASS 条件成立時に **K1240 を observed → proved に昇格**する
  （K1141/K1152/K1231/K1233/K1235/K1237 と同一手続き）。併せて K1241 item に
  part2 を追記、log note `2026-11-23-y17-universal-verifier-part2.md`、
  knowledge README bullet を更新する。

## 対抗確認（宣言前の最新 main で実施）

- 観測 HEAD `83234a16`: part2 の宣言・実験要素・K1242 以降の y=17 part2 系
  item は存在しない。search_code 'y17-universal-part2' / 'y=17 universal
  part 2' total_count 0。research/log の y17 系 notes は既知の 5 本
  （fit・part1・proof single-owner・verifier single-owner・two-token skeleton）
  のみで part2 着手宣言はなし。実験dirに census_rows.py / preflight は未存在。
- 実験dir `vertical-fiber-two-token-y17-parametric-allz-proof-20261123` は
  part1 出版構成（verify + scripts/check_transcriptions_y17.py +
  output/audit.json + census part 2本 + transcriptions-check + published_run）
  のみ。

## 範囲外

3トークン以上、y>=18 族、固定幅・q点版の安定化長、標準 11x11 空盤・
二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本宣言の範囲外。
