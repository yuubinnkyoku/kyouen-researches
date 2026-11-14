# 2026-11-15 N11 class2-lane: 69f fold 予測の第三手法による独立監査

## 背景
- 監査対象: class2-lane-next-fold-marginal-prediction-20261115.json（schema v2、baseline 1154 head、cost-69f 9 bits + cost-70c bits 3/42/86/103）および class2-lane-cost70c-warm-batch3-records-20261115.json（warm batch-3 claim b9822fb0）。
- 69f の残り4証明書（bits 2/94/109/119）の公開と fold 実行は並走レーンが担当。本監査は予測の列挙・算術の独立検証。

## 手法
- 独立D4正規化（8変換、bit index 11*b+a、BigInt）による lift 再生成、4x4行列式による共円判定（退化=4点共線も検出）、3x3直線判定、parent-orbit membership による per-S5 serve 関係。repo verifier / solver / cache 不使用、入力は main (30c638d5) の manifest 6分割・ranking 175行・予測/batch-3 JSON。

## 結果: 予測の全監査項目が第三手法で再現
1. root恒等式 root == child|1<<bit は13/13、records・prediction の root_hex と全件一致。popcount 7/6 全件。covers=7 全件。
2. 全rootで4点共円・退化4点組 0件。3点共線はrootあたり2〜3件（bit 118のみ3件）存在するが、共円の勝利条件（4点の円/直線）には該当せず安全。
3. 69f 9 bits の marginal_manifest_hexes は全て当該rootのlift軌道かつmanifest行。growing union marginal の再計算 [2,0,1,1,1,1,1,1,1] は予測と完全一致。distinct union 9、solved increment 9。
4. D の9 hex の manifest cost 合計 669 = 予測の sum drop（527,949→527,280）と一致。
5. 第三class-2 target 80910200000000000000: 8/588 →（Cの影響なし）→ 7/519。予測と完全一致。最安未sweep子 00000000000000809102000000002000 は manifest 行・cost 69 を確認。
6. batch-3（gain-0）の構造整合: 4 bits とも in-manifest lift 3件 + non-manifest 4件。bits 42/86 の主張 marginal=4 は再生成された non-manifest 4件と完全一致。bits 3/103 の marginal=0（全事前カバー）とも整合。batch-3 の in-manifest lift は warm6 C 集合・69f D 集合のいずれとも交差しない。

## 新規の構造発見
- D の9 hex はそれぞれ恰好2つの open S5 に serve する。うち S5 00000000000000801202000000000080（class 2, 68 orbits / 5093）が全9 hex を含み、fold 後は 59 / 4424 になる（条件付き予測）。
- 同様に warm6 C の6 hex は全て S5 00000000000000801242000000000000（class 2, 70/5517 → warm6 fold 後 64/5043）に serve。
- per-S5 rem の総和は多重計上（1148時点 12,773 / 1,007,211）であり、distinct orbit の head 値（4,963 / 391,672）とは別物。fold で per-S5 総和は −18、distinct demand は −9。どちらも distinct-count 帳簿の下で整合。

## 未解決・要確認
- 最安未sweep子 00000000000000809102000000002000 の予測noteの c1=0,c2=2,c4=2（4 serve）に対し、実測では ranking 175行 Open S5 中3 S5 のみ。endpoint 算術には無影響（当該 hex は D 外）だが、非open serve の計上かクラス集計の要確認。
- D の9 hex の「1154時点で未解決」は予測のsolved setに基づく主張で、本監査では独立再計算不能（per-S5整合で代替検証済み）。

## 状態
- 11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 すべて UNKNOWN（不変）。
- 成果物: class2-lane-next-fold-prediction-independent-audit-20261115.json（同階層 output/）。
