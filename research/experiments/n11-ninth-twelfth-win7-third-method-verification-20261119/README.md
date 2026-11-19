# 第9〜第12 WIN7-D10証明書の第三方法独立検証と sweep43/census・fold/resolve5 の静的交差監査（2026-11-19）

K1057（`../n11-stranded86-add-one-stone-expansion-d10-sweep-20261119/`）が出版した
第9〜第12 WIN7-D10証明書4枚・43-witness掃引と86行census・4-receipt fold・resolve5を、
repoの出版物のみを入力として**第三環境・第三の代数経路**で検証した記録。
K1057の `verify/REPLICA-2026-11-19.md`（same-pipeline byte再現）に対し、
本検証は検証器自体が別実装・別経路であり、戦略木の状態流量のみならず
sweep43/census/fold/resolve5の静的主張（被覆関係・行集合・基数）を第三再導出で監査する。
検証器はpython3標準ライブラリのみで、repoコードは読まない。

## 方法（第三の代数経路）

- 3点 (a,b,c) を通る円 `x²+y²+Dx+Ey+F=0` をCramer則で厳密に解き、分母 W で
  交差乗算した整数判定式 `W*(s_d-s_1) + DD*(x_d-x_1) + EE*(y_d-y_1) == 0`
  （s=x²+y²）で第4石 d のbanned判定を行う。W==0（共線3点組）は直線外積式
  `dx*(y_d-y_1) - dy*(x_d-x_1) == 0` に分岐。除算・浮動小数点なし。
- 既存2検証器（BigInt 3×3余因子展開 `verify_bit7_win7_cert.ts`、4×4整数Bareiss
  `verify_win7_certificate_bigint_independent.mjs`）とは独立の導出経路であり、
  ラン内で512サンプル三つ組について lifted-cofactor 法（昇格行列式
  [x²+y²,x,y,1] の余因子展開）とのbannedセル完全一致を照合（不一致0）。
- replay規約は出版検証器と同じ: rootの各合法loser応手が1 subroot（深さ0）から
  開始、偶数深さは証明書行に厳密追随、奇数深さは全合法応手を展開、
  loser詰み（>=13石）で終端、winner詰みなし、fbtドロップなし。

## 再生方法

```sh
sh research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119/scripts/run_third_method_verification_20261119.sh <repoRoot>
```

- 入力はrepoのK1057/K1046実験dirのファイルのみ（下記の入力一覧）。
  第9証明書テキストは出版 `.n11.gz.b64` から `base64 -d | gunzip` で復元し、
  SHA-256 が出版pin 503ff9da… と一致することをgateで検証する。
- 出力は `output/` に6 JSON。速い環境で全6成果物の生成は約19秒（逐次1プロセス）。
- 2回実行で `wall_s` を除きbyte一致（`cert_path` は出版ファイル名のみを記録し
  スクラッチ位置に依存しない）。

## 入力（すべてrepo出版正本）

- `n11-stranded86-...-20261119/cert-9th/..12th/`: 第9〜第12 `.n11`（第9は
  `.n11.gz.b64`）・extraction-summary・independent-verification（BigInt）・
  bareiss-subroots jsonl
- `n11-stranded86-.../sweep43/output/witness-43-root-depth10-sweep-20261119.json`・
  `probe-records-w0/w1.jsonl`・`sweep43/roots.json`
- `n11-stranded86-.../fold/output/ninth-twelfth-win7-receipt-fold-20261119.json`・
  `post-twelfth-receipt-cover-resolve5-20261119.json`
- `n11-117pool-...-20261119/foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json`

## 結果（全6 JSON・全gate合格・failed_gates空）

### 証明書4枚の第三方法検証（各39 gate）

| 証明書 | root | 合法手 | strategy行 | subroot | visited | terminal | 終局石 | wall |
|---|---|---:|---:|---:|---:|---:|---|---:|
| 第9 | 00000000000000801202000001040200 | 72 | 84,928 | 72 | 171,066 | 27,410 | [13,17] | 9.1s |
| 第10 | 00000000000000821082040200000000 | 56 | 45,450 | 56 | 96,862 | 15,936 | [13,17] | 4.5s |
| 第11 | 00000000000000821092200000000000 | 47 | 24,375 | 47 | 56,207 | 8,516 | [13,17] | 2.4s |
| 第12 | 00000000001020003800000048000000 | 51 | 26,756 | 51 | 61,065 | 9,191 | [13,17] | 2.8s |

- 証明書SHA-256・行数・root（7石・D4正準・safe・mobility）は出版extraction・BigInt・Bareiss
  サマリと全一致。winner/loser状態・loser応手edge・terminal数・終局石rangeは出版BigInt流量と
  全一致、per-subroot統計は出版Bareiss（72/56/47/51 subroot）と全件一致、
  strategy行とvisited集合のunion欠損・過剰はいずれも0。

### sweep43/census 静的監査（`audit_sweep43_census.py`、17 gate）

- 43 pair witnessが86 stranded行を**各行ちょうど1回**被覆（被覆集合==resolve4残余86行）。
- 43根すべて: 7石・D4正準・safe・RAW maxbit child（added_bit一致）・被覆関係
  （rootの8-D4像から1石引いた正準形が被覆行）を第三実装で再導出し完全一致。
- probe 86件（両AND順序）のnodes・cap・loss・pilot_d6（3,402 nodes）が出版witness記録と
  全件一致。分類（WIN 4・REFUTED 39・CAPPED 0・conflict 0）とnodes総計173,165,148を
  raw probe記録から再導出し一致。WIN 4根は第9〜第12証明書rootと完全一致。

### fold/resolve5 交差監査（`audit_fold_resolve5.py`、62 gate）

- 4 receiptが閉じる5親target 8行を第三再導出で一致、9 S6行閉鎖（8 target行＋第10の
  extra行 `00000000000000801082080400000000` cost 80）の被覆関係をrootの8-D4像−1石から
  独立再導出で確認。closed_edge_cost総計667 == 163+227+133+144。
- S6保存則・frontier変化（6,222行/492,688 → 6,213行/492,021・solved S6 1,626→1,635）・
  parent incidence·5親target 26→34/112（残余78行）を出版fold記録と照合。
- resolve5: 残余78行==86行−fold閉鎖8行の再計算一致、add-one-stone universe 7,969を
  再列挙一致（in_pool 93・既知REFUTED 46・fresh = safe 4,728 + unsafe 3,102）、
  39 witnessの7石・D4正準・safe・被覆から78行完全1回被覆を再構築、43 sweep根・
  4 receipt根との不交、verdict pool 379 REFUTED/168 WIN、matched 78/stranded 0/witness 39。

## スクリプト

- `scripts/verify_third_method.py` — 証明書1枚の第三方法検証器。
  `verify_third_method.py <cert.n11> <extraction-summary.json> <bigint-verification.json> <bareiss-subroots.jsonl> <out.json>`
- `scripts/audit_sweep43_census.py` — sweep43/census静的監査（workdir入力）。
- `scripts/audit_fold_resolve5.py` — fold/resolve5交差監査（workdir入力）。
- `scripts/run_third_method_verification_20261119.sh` — 入力のsymlink工作と上記全実行を行う
  wrapper（workdir入力名とrepo出版名の対応はこの中に一元化）。

## 解釈規約（既存レーンと同一）

- 本検証はK1057出版事実の検証強化であり、**勝敗の進展ではない**。
- REFUTED-D10はLOSS証明ではなく、foldは行被覆の簿記、resolve5の39 witnessは
  次回掃引の条件付き計画である。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
