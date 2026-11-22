# 7×7・8×8の最大安全サイズSAT単独確定、n=7〜9の極大行スペクトル拡張、双対Sinzカウンタのv2修正 (2026-11-22)

## 位置づけ

単一オーナー宣言 (commit `46efd957`・宣言時HEAD `9e10cd06`・[宣言ノート](../../../log/2026-11-22-n8n9-rows-k10-exactlyk-sat-single-owner-note.md)) の元、exactly-k極大安全行判定 (pinned enc_sat2 v2.1 + 新規双対Sinz at-least-kリフト) とsafe集合at-least-k閉包 (S1安全性のみ+LX lex-leader+双対Sinz) を実行した。同日並走レーンの [K1228](../../knowledge/items/K1228-n3-n6-safe-size-histograms-sat-crosscheck.md) (n3..n6のSAT単独確定) と方法論を共有し、**n≥7側の拡張としてスコープ非重複** (K1228本文も「n7のsafe行サイズ別分布・n8・n≥9盤面は未着手」と明示)。

主張の正確な範囲:

- **K_7 = 14 と K_8 = 15 をSAT単独で確定** (既知値 [K0029](../../knowledge/items/K0029-n1-n9-maximum-safe-sizes.md) 表の値更新ではなく、CYCLE5完全最大探索・[K1169](../../knowledge/items/K1169-n8-ge16-partition-fresh-complete-search-verification.md) 分割完全探索に続く**第三の独立手法**による再確定。値は不変)。
- n=7〜9の極大安全行 (石数exactly-k) の非空行witnessを増加 (n7: k=9..14 / n8: k=10..15 / n9: k=10..17、計20行×2ショット、全witness復号+独立整数検証PASS)。
- n9のat-least-18/19は本レーンではINDET (240s)。**K_9上界・K_9=18確定への主張は一切しない**。ge19判定は[2026-11-20のn9-ge19レーン](../../../log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md)が所有する。
- 全判定は有限盤のみ・実装/符号化/kissat 4.0.4のtrust込み・形式証明ではない。標準11×11空盤・二石root・S2・closure classは非接触 (UNKNOWNのまま)。

## 主結果

### 1. safe集合 at-least-k閉包 (enc_safe_atleast v2)

| 盤面 | 判定 | verdict | 根拠 |
|---|---|---|---|
| 7×7 | ≥15石安全集合 | **UNSAT** ×2 (default 4.86s/200,082 conflicts・s42 5s) | K_7 ≤ 14。k=14 witnessと合わせ **K_7=14 SAT単独確定** |
| 8×8 | ≥16石安全集合 | **UNSAT** ×2 (default 199.2s/5,646,514・s42 181.96s/5,245,460) | K_8 ≤ 15。k=15 witnessと合わせ **K_8=15 SAT単独確定**。K1169分割閉鎖の別手法交叉確認 |
| 8×8 | ≥15石安全集合 | SAT (1.18s, 15石witness復号+検証) | 陽性対照 |
| 9×9 | ≥17石安全集合 | SAT (3.85s, 17石witness復号+検証) | 陽性対照 (K0029のrepo内証明書17石レベルの機材内再現) |
| 9×9 | ≥18石安全集合 | INDET (240s, 6,118,159 conflicts) | fresh探索ではW9スケールのwitnessに240sで到達不能。W9注入対照で符号化健全性は確認 |
| 9×9 | ≥19石安全集合 | INDET (240s, 6,166,925 conflicts) | 上界主張なし (ge19レーン所有インスタンス) |

- s42ショット = `--shuffle=42` のFisher-Yates変数置換による同型独立符号化。CNF生成は決定的 (全生成2回byte-identical検査、`determinism=byte-identical` 記録)。UNSATの2ショット一致を独立性根拠とする。

### 2. W9細部注入陽性対照 (n9 ge18)

18石証人 W9 (cells p=x+9y): `[5,6,8,9,11,18,24,31,44,47,50,52,54,55,70,73,75,79]` ([2026-11-15実験](../n9-k9-upper-sat-20261115/README.md)・第三系検証済み) の8つのD4像について、全81セル変数を単位節で固定してkissatで解いた (**CNFバイトは改変せずunit節を追記**)。

- 恒等像 (d4_1): **SATISFIABLE** — 符号化+S1+LXが既知の18石witnessを受容
- 他7像: すべて **UNSATISFIABLE** — LX lex-leader鎖が非正準形の軌道コピーを正しく棄却
- 含意: n9 ge18 CNFはSAT (W9で充足される)、n9スケールの符号化は健全、fresh探索のINDETは探索能力の限界であって符号化の問題ではない。

### 3. exactly-k極大安全行

pinned enc_sat2 v2.1 (at-most-k極大安全+LX) + 新規atleast_lift (双対Sinz) によるexactly-k極大安全行の判定。

| 盤面 | 非空行 (witness数) | 空行判定 |
|---|---|---|
| 4×4 (較正) | k=5,6,7 (2^16全数と一致) | k=1..4, k=8: UNSAT (2ショット) |
| 6×6 (較正) | k=11 (K1225出版行464の陽性対照) | k=12: UNSAT ×2 (K1225零行再導出) |
| 7×7 | **k=9..14** (12 witness) | k=6: UNSAT ×2 (K1224/s_7=7整合)・k=15: UNSAT ×2 (行閉包) |
| 8×8 | **k=10..15** (12 witness) | 行≥16はge16閉包で一括 |
| 9×9 | **k=10..17** (16 witness; k=17は証明書レベル) | k≥18: K_9上界に依存、非主張 (W9から行18非空・行≥19はge19判定待ち) |

- 全45のSAT witness (20行×2ショット+較正) はdecode→verify_witness.py (独立整数4×4行列式実装) で **verdict SAFE+MAXIMAL・石数k一致・違反0** を確認済み (publish時に `output/verify/` へ収録)。
- 単石除去tamper対照 (受入条件3): 20 default witness × k通りの単石除去が全て **SAFE かつ NOT-MAXIMAL** (viol=0, uncovered≥1) であることを機械確認 (計208除去)。証明: S∖{p}が極大なら攻撃三つ組T⊂S∖{p}と T∪{p} が禁止四点組となり、それはS内の禁止四点組となってSの安全性に矛盾する。

### 4. n4全数較正 (2^16地面真理)

カタログのみ (行列式不使用) による2^16全列挙 (`scripts/brute_truth_n4.mjs`):

- safe合計 5,811 (K1228/archived round4_f・K0004と一致)・サイズ別 {0:1, 1:16, 2:120, 3:560, 4:1626, 5:2360, 6:1064, 7:64}
- 極大ヒストグラム {5:176, 6:688, 7:64} (K1225全77行と一致)
- fixed符号化の全判定一致: sa ge-k は k=1..12 で SAT⇔k≤7 (両ショット)、exactly-k は k=1..8 で SAT⇔5≤k≤7 (両ショット)

### 5. 双対Sinzカウンタのv2修正 (訂正記録)

- **発端**: n7 ge15のs42ショット追加実行が0秒でSATISFIABLEを返した (既知のK_7=14と矛盾)。
- **原因**: 双対Sinz逐次カウンタに **j=1開始節 (x_i, U(i,1)) (i≥1) が欠落** していた。セル0が石のときカウンタが起動せず、at-least-k半束縛が空文化する。atleast_lift.mjsにも同一の欠落があった。
- **機械確認**: n7 ge15 (no-lex) pre-fix CNF上で、11石/38空点の割当が全9,629節を0違反で充足することを直接評価した (CNF全文 vs modelの全節スキャン)。
- **帰結の非対称**: models(pre-fix) ⊇ models(post-fix) の純緩和。ゆえに **pre-fixのUNSAT判定はすべてa fortiori有効**。pre-fixのSAT判定は単独では無価値 (ただし全SAT witnessは復号後verify_witness.pyで独立検証済みなので、行非空の**証明書としては符号化に依存せず有効**)。
- **修正**: 両スクリプトにSTART節を追記 (v2)。全UNSAT閉包 (n4k8・n6k12・n7k6・n7k15exactly・ge15/ge16) をv2で2ショット再実行し、n4全数較正で受入言語照合した。
- **較正を透過した理由**: n4では最小極大サイズが5でat-most-k底が効くため、欠落があってもexactly-k結果が Lucky に一致した。**「SAT側の較正はwitness復号+k一致まで」「at-least束縛は実質化するサイズでも注入対照を必須とする」** を規約として記録する ([K1221](../../knowledge/items/K1221-sat-lex-leader-orbit-coverage-rule.md) の「受入言語照合」と同種の事故)。

## 機材 (pinned)

- census.mjs・decode_model.mjs・enc_sat2.mjs (v2.1)・verify_witness.py: git blob shaでpinned (出版物 `output/run_records.json` の `pinned_tools` にsha256を記録)。
- kissat 4.0.4: md5 `3a5eba830aa6008a604fcc9bbe99a325` (binary非刊行)。
- atleast_lift.mjs v2・enc_safe_atleast.mjs v2: sha256を run_records.json に記録、`scripts/` に全文掲載。
- 運用: 実行環境リセット3回 (11:47Z頃・13:35Z頃・14:5xZ頃)。永続マウントの作業キットに成果物を全保存し復旧。「1回のbash呼び出し ≤ 1ソルバ実行 (cap ≤250s)」を厳守。バルク出力 (witness/verify/tamper/records/scripts) は環境復旧後に続刊 (2段階出版・session logに記録)。

## 再現

```bash
# exactly-k行 (pinned base + v2 lift)
bash scripts/run_case.sh <n> <k> default|s42 <cap秒> <tag>
# safe集合 ge-k (v2)
bash scripts/run_safe_atleast.sh <n> <k> default|s42 <cap秒> <tag>
# 単位節注入対照
bash scripts/inject_cells.sh <cnf> <n> <cells_csv> <cap秒> <tag>
# 単石除去tamper対照
bash scripts/tamper_removals.sh <witness.json> <tag>
# n4全数地面真理
node scripts/brute_truth_n4.mjs 4
# 出版レコード統合
node scripts/collect_records.mjs
```

CNF本体は非刊行 (宣言でshaピン運用)。CNFは決定的再生成可能 (byte-identical検査済み) で、sha256は meta/run_records に記録。

## 関連

[K0029](../../knowledge/items/K0029-n1-n9-maximum-safe-sizes.md) (最大安全サイズ表)・[K0031](../../knowledge/items/K0031-n7-minimum-maximal-size.md) (s_7=7)・[K0032](../../knowledge/items/K0032-n8-minimum-maximal-size.md) (s_8=8)・[K1169](../../knowledge/items/K1169-n8-ge16-partition-fresh-complete-search-verification.md) (n8-ge16分割閉鎖)・[K1225](../../knowledge/items/K1225-small-board-maximal-rows.md) (小盤全行)・[K1228](../../knowledge/items/K1228-n3-n6-safe-size-histograms-sat-crosscheck.md) (n3-n6 SAT単独確定)・[K1221](../../knowledge/items/K1221-sat-lex-leader-orbit-coverage-rule.md) (lex鎖受入規約)・[n9-k9-upper-sat-20261115](../n9-k9-upper-sat-20261115/README.md) (W9)・[2026-11-20 n9-ge19レーン宣言](../../../log/2026-11-20-n9-ge19-k9-upper-decision-single-owner-note.md)
