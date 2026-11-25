# Four-row q=7 stabilization closure — 2026-11-21

本 dir は K1177 four-row q6/q7 frontier レーンの直接後続（closure レーン）で、**M_{4,7} = 13 の閉包**を成立させる検証材料（宣言・スクリプト・監査 JSON・生ログ）を出版する。実行の委任宣言は `note.md`（fail-closed 受理条件つき）。知識項目としては K1182 に昇格。

## なぜ M_{4,7} = 13 か（责任的な根拠の分担）

- **一般上界（解析的・全域）**: K0318 の証明済み curve-packing 安定化定理により U_{4,7} = 81。すなわち全 m ≥ 81 で def-mode UNSAT。`u_recompute.js` は K0318 の整数最適化（curve_packing_fixed_width 閾値 JSON）を独立実装で再計算し、全 30 エントリ一致（`mismatches: 0`、`U_4_6 = 103, U_4_7 = 81` を含む。`output/u_recompute.json`, `output/k0318_regen_full.json`）。
- **有限排除（機械的・帯 [13,85]）**: K1177 が出版した q=7 全幅掃引 13..85 の def-mode UNSAT（`output/records_audit.json` が records.jsonl 108 レコードを機械監査: q=7 witness band {7..12} すべて SAT（3系統検証 witness つき）、witness-free band {13..85} すべて UNSAT rc=20・INDET 0、q=6 witness {6..15} SAT / {16..29} UNSAT）。
- **下界証人**: m=12 に row-deficient 極大安全配置（rows [6,6,5,6]・23石・3系統検証 PASS）が存在（K1177 witness。本レーンでも m=7..12 witness の JS 再検証を実施、`output/live/witness_*.json`）。

3 つを併合すると [13,85] の有限排除と [81,∞) の解析上界が全幅 m ≥ 13 を被覆し、M_{4,7} = 13。K0077/K0071 で確立した「解析上界＋有限排除＋下界証人」パターンの w=4 q=7 適用。

## genfast3 census の w=4 移植と較正

sat2.js 全三つ組 census は m=86 で生成段階のメモリ壁に到達していた（K1177 記録どおり）。本レーンは six-row-q8-band-closure-22-370-20261114 出版の `genfast3.js`（弦対抽象円 census、q ≥ w+2 で完全性論つき・K1134 レーンで確立済み）を byte-identical（md5 `12c2bd9c…`）で移植し、q=7 ≥ w+2 = 6 で w=4 に適用した。

較正（`output/live/` の生ログ）:

- CNF byte 一致: (4,13,7)→`80663be5…`、(4,20,7)→`6f882012…`、(4,16,6)→`3ce3a8fa…`、(4,85,7)→`2f78307d…`（いずれも sat2.js 出版値と同一 CNF md5）。
- pinned kissat 4.0.4 conflicts bit-exact: 5446 / 3359 / 1980648 / 3759（出版 records 値と一致）。

## 壁の先の掃引（m=86..88、支持証拠）

m=86..88 の 3 幅を genfast3 census で生成し pinned kissat で判定: すべて **UNSAT**（conflicts 5930 / 5191 / 6072、0.16..0.23s/幅、rc=20）。さらに (4,86,7) def-mode の `--lex=H` 交差符号化も UNSAT（conflicts 3677）。閉包自体は K0318 が [81,∞) を担うためこれらは支持的だが、sat2.js の壁が原理的なものでないことの直接確認になる。records への反映（108→112 レコード）は K1177 dir の `output/records.jsonl` に本レーン `scripts/append_records.js` が追記した（`output/records_extended.jsonl` がその正本のスナップショット、`output/records_audit_ext88.json` が追記後 112 レコードの再監査）。

## 結果の要約

$$
M_{4,7} = 13 \ \text{(closed)}
\qquad
M_{4,6} = 16 \ \text{or} \in [30,103] \ \text{(open, U_{4,6}=103)}
$$

ゲーム版の帰結（全 m ≥ 13 で全安全局面が g(S) = (24 − |S|) mod 2、空盤 second-player-win）は K1182 に記載。

## ファイル

- `note.md` — レーン宣言（first-published-priority・fail-closed 受理条件）。md5 `12b08bd25cd0a6544b2573527858d766`
- `scripts/genfast3.js` — 弦対抽象円 census 生成器（six-row レーンから byte-identical、core は four-row sat2.js と同一 md5）。md5 `12c2bd9cb3b24887fc3896f7ea9bcadf`
- `scripts/u_recompute.js` — K0318 整数最適化の独立再実装。md5 `1b8954305a3b2b9cb59c973c71c49d44`
- `scripts/audit_records.js` — records.jsonl 機械監査。md5 `51b02c990f89015d5d22858600854569`
- `scripts/append_records.js` — K1177 dir records.jsonl 形式への追記器。md5 `470f29e01c55cc2666ea3ea9ebb83140`
- `output/u_recompute.json` — 再計算結果（30 エントリ全一致）。md5 `86e5deb9292c579c3c6d8fa930e05c05`
- `output/k0318_regen_full.json` — 再生 K0318 閾値の全文。md5 `e7c9f4512215a27e2df64d1ffbc07055`
- `output/records_audit.json` — 出版 108 レコード監査（problems 0）。md5 `29587ec591c9189a19c3be064267a52b`
- `output/records_audit_ext88.json` — 追記後 112 レコード再監査（problems 0）。md5 `bfc94e7efd3c222c649129b4b02b8174`
- `output/records_extended.jsonl` — 112 レコード正本スナップショット。md5 `fd43f36ea49106c46829551694e3b15e`
- `output/live/gen_4x86q7_def.json` 他 3 本 — genfast3 生成メタログ（86/87/88 def + 86 lexH）
- `output/live/solve_*.txt`（7 本）— pinned kissat 生ログ。m=86/87/88 の def 3 幅は `solve_4xNNq7.txt` と `solve_4xNNq7_def.txt` の 2 回ずつの独立実行で conflicts bit-exact（5930/5191/6072）、(4,86,7) lexH 交差は 1 本（3677）。全ログ exit 20
- `output/live/witness_4x{7..12}q7.json`（6 本）— m=7..12 witness の JS 再検証メタ

CNF ファイルは容量の関係で掲載しない（records の cnf_md5 と生成スクリプト・生ログで再生成可能）。

## 再現方法

```
node scripts/u_recompute.js <k0318 curve_packing json> output/u_recompute.json   # 独立再計算（all entries must match）
node scripts/audit_records.js <records.jsonl> output/records_audit.json [mMaxQ7]
node scripts/genfast3.js 4 86 7 c_4x86q7_def.cnf        # DIMACS 生成（--lex=H 等のフラグも可、def は既定）
KISSAT_BIN=<pinned kissat 4.0.4> <solver> c_4x86q7_def.cnf   # exit 20 = UNSAT
node scripts/append_records.js <K1177 records.jsonl> <out.jsonl> output/live     # 4 レコード追記
```

pinned kissat: kissat 4.0.4 linux-amd64, md5 `3a5eba830aa6008a604fcc9bbe99a325`。

## 他レーンへの観察（本レーンでは作業しない）

(5,7) にも同一パターンが適用可能: five-row レーンの witness-free 帯掃引 19..157 が完了すれば、証明済み一般上界 U_{5,7} = 158（K0332/K0024 の置換、K0821 で引用）と併せて M_{5,7} = 19 が同一の K0077 型論法で閉じる。所有権は five-row レーンに移譲済み（`note.md` 参照）。
