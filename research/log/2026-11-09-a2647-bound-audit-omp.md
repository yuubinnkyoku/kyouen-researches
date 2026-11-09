# 2026-11-09 A(2647) 上下界の証拠連鎖の独立監査（omp ワーカー）

タスクW1。sparse checkout上で既存ファイルのみを読み、主張と証拠の対応を照合した。
ソルバ・検証器の起動は行っていない（軽い集計・`git show` のみ）。
作成ファイルは本log 1件のみ。

## 対象の主張（タスク文から）

- 下界: A(2647) >= 1296
- 上界: A(2647) <= 1322（サイズ1323全形状UNSAT、サイズ1322は3形状UNSATで (1,1,3) のみ未決）

## 観点1: 下界1296の構成 — **verified（一部はsparse欠落につきgit経由で確認）**

- 証人は `research/experiments/parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt`
  に実在する。ヘッダ `2647 1296`、2行目はソート済み・重複なしの**ちょうど1296個**のパラメータ
  （0以上2645以下）であることを直接数えた。
- SAT探索の記録 `run.json`（target=1293, clauses=142992, SAT 11.233秒, size 1296）と
  `result.json`（p=2647, d=1323, target=1293, empty_bound=32）が一致する。
- 独立幾何検査 `geometry.json`: `2647 1296 117002820060 44277012`、終了コード0、
  選択四点117,002,820,060を必要合同式で絞り44,277,012候補をgeneric 4×4整数行列式で検査し禁止四点0件。
  検証器ソースSHA-256 `c817e78...`（K0711 artifact `parabola-local-repair-20261109/verify_subset.cpp`）。
- K0711（`research/knowledge/items/K0711-p2647-safe-lower-bound-1292.md`）の数値
  （1296点、117002820060、44277012、28.903秒）はすべて実ファイルと一致。
- 初回1292点証人（`parabola-local-repair-20261109/`）はsparse checkoutに欠落しているが、
  `git show HEAD:` で実在を確認: candidate.txt 2行目1296でなく**1292点**、
  geometry.json は `2647 1292 115563355055 43730623`、verify_subset.cpp のSHA-256は
  `c817e780...` でK0711記載と一致。初回証人の一次記録はK0711記述どおり。
- 結論: 1296 <= A(2647) は、保存証人を整数幾何検証器が独立に検査した有限計算として
  K項目・log・実験出力で一貫している。

## 観点2: サイズ1323の全形状クラス UNSAT — **discrepancy（重大）**

- ログ `research/log/2026-11-09-p2647-near-miss-and-size-1323.md` はサイズ1323の
  4クラス (0,0,0), (0,1,1), (1,0,1), (1,1,2) すべてUNSATと主張する。
- しかし実ファイル `research/experiments/parabola-p2207-no-equality-witness-20261107/output/shape_class_2647_1323.json`
  には **(1,1,2) の1レコードしかない**（sat=false, 611.5秒, 85619節）。
  クラス (0,0,0), (0,1,1), (1,0,1) のreceiptsはrepo内に存在しない。
  `git log --all` でも同ファイルに (1,1,2) だけが記録されており、過去に存在した形跡もない。
- クラス列挙のコード `search_shape_class.py`（80–105行目）は
  `x + c + h - e = size` から (x,c,e)∈{(0,0,0),(0,1,1),(1,0,1),(1,1,2)} の4クラスを列挋する
  （x∈{0,1}、c∈{0,1}、e=x+c+h−size）。クラス数4はログどおり。ただしスクリプトは
  結果を `results` に追記し全クラス終了後に書き出す構造（140–148行目）であり、
  中断すれば最後の1クラスだけが残る。3クラス分が欠けた状態はこの挙動と整合するが、
  欠落した3レコードを再構成する材料はrepo内にない。
- K0711 のartifactノートはこのファイルを「サイズ1323の4形状クラスすべてUNSATの記録
  （上界1322の根拠）」と説明しているが、これは**ファイルの実内容と食い違う**。
  同様に K0711 のscope/evidence本文は「サイズ1324・1323の全形状クラスのUNSAT（A<=1322）から従う」
  と書くが、サイズ1323側は4クラス中1クラス分のreceiptしかない。
- なおサイズ1324（h+1）の3形状は別系統で完全に揃っている:
  `parabola-hplus1-drat-20261109/output/shape-{a,b,c}/` に各audit.json
  （VERIFIED, checker source SHA `34249932...`）・solver.json・proof.drat.gz が存在し、
  3形状とも target_size=1324, SOLVER_UNSAT。旧ファイル shape_b_single_2647.json /
  shape_c_2647.json も target_size=1324 のUNSAT記録で、訂正済みログ
  `2026-11-09-p2647-no-size-h1-set-corrected.md` と一致する（A<=1323, ソルバ主張）。
- 結論: 「A(2647) <= 1322」の証拠連鎖は**現時点で不完全**。1323の4クラス中3クラス
  ((0,0,0),(0,1,1),(1,0,1)) のUNSATはログの表（0.3秒/12.1秒/0.7秒）ではあるが
  machine-readableなreceiptsが欠けており、独立監査としては採用できない。
  K0711が上界1322を採用しているのは証拠に先行している。

## 観点3: サイズ1322の3形状 UNSAT と (1,1,3) 未決 — **verified**

- `shape_class_2647_1322.json` に3レコード: (0,0,1) 0.6秒, (0,1,2) 618.4秒,
  (1,0,2) 7.8秒。いずれも sat=false, unknown=false。クラス列挙コードから
  サイズ1322の取り得るクラスは (x,c)∈{(0,0),(0,1),(1,0),(1,1)} に対し
  e=x+c+1323−1322=x+c+1 で (0,0,1),(0,1,2),(1,0,2),(1,1,3) の4つであり、
  記録されている3つ + 未決の (1,1,3) で漏れなく対応する。
- (1,1,3) 未決の記述は `2026-11-09-p2647-near-miss-and-size-1323.md` 40行目以降:
  1.5時間以上+3M衝突予算で完了せず中断、Glucose4 で71分以上でも未完（52–57行目）。
  (1,1,3) に対応するreceiptsファイルは存在しない（未決なので当然）。
- 従ってサイズ1322の安全集合の不存在は**証明されておらず**、上界1321は未確定
  （ログ本文も「A(2647) <= 1321 は未確定」と明記）。これは正しく記録されている。

## 観点4: K項目・ログ・results 間の数値・status の食い合わせ

一致しているもの:

- K0706（`K0706-p2647-no-parabola-equality-witness.md`, status: computed）:
  全1323 d UNSAT・修正版DRAT 1323/1323 VERIFIED。receipts
  `drat_audit_full_2647_34249932790a9e9d.json` を直接集計し、1323レコード・
  d=1..1323重複なし・全件 verified・UNSAT・checker_rc 0 を確認。
  `parabola-equality-refutation-20261109/receipt_coverage.json`
  （1323 verified / 0 failures, 証明総行数8,038,838）および
  `parabola-audit-coverage-20261109/inventory.json`（2647: full_verified_coverage=true,
  missing 0）とも一致。上界 A(2647)<=1324 は三方面で一貫。
- K0101（status: refuted）の論理は `parabola-equality-refutation-20261109/README.md` どおり。
- K0097 92行目 `1296<=A(2647)<=1324` と K0706 74行目の記述は一致
  （両者とも上界として独立DRAT監査済みの1324を採用）。
- 2026-11-08ログ `2026-11-08-p2647-third-no-equality-prime.md` の数値（UNSAT 1323・
  2,899秒・A<=1324）はK0706と一致。旧commit `666a778c` の「A<=1103」混同は
  `2026-11-09-ternary-1296-and-shape-bound-arithmetic.md` が記録どおり訂正済み。

食い違い:

1. **K0711 のみ上界1322を採用**（title・本文・evidence）。K0097・K0706は上界1324。
   K0711自身115行目は「本項で独立監査済みとして採用した上界は1324。単一CNFのDRAT監査による
   強化は今後の課題」と書いており、内部的に矛盾している（観点2のとおり1322の根拠receiptsが不完全）。
   handoff summary（`2026-11-09-parabola-equality-handoff-summary.md`）は上界を
   K0706の1324として扱い、サイズh+1の形状(c)を「未決」としており、K0711の1322と食い違う。
   なおhandoff summaryの「サイズ h+1（=(p+3)/2−1）の形状 (c) は単一CNFが難しく未決」
   という記述は p=2207 の形状(c) に関するもので、p=2647 の3形状は
   `parabola-hplus1-drat-20261109` でVERIFIED済みであり、pの別を明記していない点は紛らわしい。
2. K0711のartifactノート「shape_class_2647_1323.json = 4形状クラスすべてUNSATの記録」は
   ファイル実内容（1レコードのみ）と食い違う（観点2）。
3. K0711の依存ノート「shape_b_single_2647.json …（形状(a),(c)は別記録）」について、
   形状(c)は shape_c_2647.json に実在するが、**形状(a)の1324記録は
   shape_b_single/shape_c の2ファイルにはなく**、`parabola-hplus1-drat-20261109/output/shape-a/`
   （audit VERIFIED, target_size=1324）にある。K0711のartifactsにはこのパスが登録されておらず、
   上界1323/1322の議論でこの後続実験への依存が明示されていない。

## (1,1,3) 形状について現在 repo が言えることの正確な範囲

- クラス (1,1,3) はサイズ1322（原点を含む x=1、完全対1つ c=1、空対3つ e=3、
  |S|=h+x+c−e=1323+1+1−3=1322）の4クラスのうちの1つで、他3クラスはreceipts付きUNSAT。
- (1,1,3) 単体CNFのUNSATは**証明されていない**。CaDiCaL（1.5時間+3M衝突予算）と
  Glucose4（71分以上）がともに完了せず、SAT・UNSATいずれの確定もない。
  したがって「サイズ1322の安全集合は存在しない（A<=1321）」も
  「(1,1,3) 型のサイズ1322の安全集合が存在する」も主張できない。
  上界1322を支えるのはサイズ1323不存在（観点2のとおり証拠不全）のみであり、
  (1,1,3) の決着はそれとは独立に必要。
- 現在の監査済み上界として確実なのは A(2647) <= 1324（K0706全d監査）。
  1323（サイズ1324の3形状UNSAT+DRAT監査、ただし後続実験のlogs/logエントリは未参照）
  および1322（K0711採用）は、それぞれreceiptsの完全性に上記の問題を残す。

## sparse checkout による未確認事項（unverifiable）

- `research/experiments/parabola-local-repair-20261109/` は作業treeに欠落。
  初回1292点証人・geometry receipt・検証器ソースは `git show HEAD:` で確認したが、
  walkの一次出力の完全な再検査は行っていない。
- サイズ1323のクラス (0,0,0), (0,1,1), (1,0,1) のUNSAT receiptはgitの全履歴にも見つからず、
  「sparse欠落」ではなく「そもそもcommitされていない」可能性が高い。欠落理由の確定はこの
  checkoutでは不可能。
- `parabola-hplus1-drat-20261109` に README がなく、K項目・log もこの実験を参照していない。
  3形状auditの作成経緯・承認状態はこのcheckoutからは追跡できない（audit.json自体の
  SHA-256整合は確認済み）。

## 総括

| 主張 | 判定 |
|---|---|
| A(2647) >= 1296 | verified（candidate.txt・geometry.json・run/result.json・K0711整合） |
| A(2647) <= 1324 | verified（全d DRAT receipts 1323/1323、coverage・inventory整合） |
| A(2647) <= 1323 | 条件付きverified（h+1 3形状のaudit実在。ただしK0711はこの実験を未参照） |
| A(2647) <= 1322 | **discrepancy**（サイズ1323の4クラス中3クラスのreceipts欠落。K0711の採用は証拠に先行） |
| サイズ1322の3形状 UNSAT | verified（shape_class_2647_1322.json、3/4クラス） |
| (1,1,3) 未決 | verified（未決であることの記述は正確。UNSAT/SATは未証明） |
