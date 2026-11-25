# 研究log: WIN8-D10証明書抽出 root 8890020（2026-11-20）

単一オーナー宣言（commit `60e2940cf079c8e98efc9c0e72150835b87e5184`・先行出版）に基づく実行記録。

## 経緯

K1111（fold14 root 9090022・README弾丸まで出版完了）の直後に着手した。
残るWIN8候補のうち、並走宣言済み2根（`…8180000`・`…0810000a`）と抽出・fold済み
4根（`…8003180`・`…8005021`・`…9840004`・`…9090022`）を除く最安価の未着手根
`00000000010000889002000080100000`（主張4行・K1086探査nodes 409,407/575,570）を
選定した。選定基準: (1) fold14後の残余58行に主張4行が残存
（`…8890020…`の主張行はK1097 win16 footprintでintrinsic==claimedを確認済み）、
(2) 並走が着手していないroot（list_commits直近60件の宣言走査で確認）、
(3) 探査nodesが残る候補中最小。

## 実行

1. **宣言ノートの先行出版**:
   `research/log/2026-11-20-n11-win8-cert-extract-root00010000889002000080100000-single-owner-note.md`
   （commit `60e2940c`）。着手権確定後に計算開始。
2. **root幾何の事前確認**: 8石 [20,31,49,60,63,67,71,88]・quadruple-free
   （C(8,4)=70組の4×4リフト行列式が全て非零）・D4正準（8対称像中最小hexがroot自身）・
   LSB bit 20・child = root − bit20 = `00000000010000889002000080000000`。
3. **probe再現**: K1086出版値（andclose1 409,407・andclose0 575,570・両方
   loss=true uncapped・terminal [14,18]）を本環境のrunner v17（git blob pin
   `c132cc64…`一致確認）で再現。各順序2回・pilot_d6 3,402 nodes 4回とも
   node-exact一致（計時msのみ変動）。
4. **抽出一式**: root legal 50手の独立再導出（純Python 4×4行列式）→
   A1（50プロセス・総nodes 4,424,758・最大初手 bit 14 の 937,490・fbt_drops 0）→
   A2完全再実行（初手単位node/nRows完全一致・行bytes一致）→ B（単一プロセス・
   総nodes 4,424,758・戦略行21,446不変）。3実行の行集合byte一致。
   9090022と同じくBのnodes会計がA1と同一だった（chunk/単一プロセスの差が本rootでも
   現れない。戦略行の不変性が本質でありnode会計は証明内容に影響しない）。
5. **三重検証**: BigInt 3×3（50/50 sub-root・union 0/0）・Bareiss 4×4
   （root-check stones 8・loserMobility 50・50 sub-root全PASS・union 0/0）・
   python第三方法（監査機械・全木再走査）。3方法が全集計値で一致:
   visited 48,855・winner 31,320・loser 9,882・応手辺 43,837・terminal 7,653・[14,18]。
6. **監査機械**: K1109出版機械（`assemble_win8_audit_root9090022.py`）のroot定数
   差し替え版 `assemble_win8_audit_root8890020.py`（ROOT_HEX・CERT_RELPATH・
   probe nodes 409,407/575,570・実験名。g05 mobility 50・g07主張4行・g08 bit 20・
   g19の`== 4`は9090022と同じ4行構成のため不変）。**19/19 gate PASS**・
   同一cwd 2回+別cwd別プロセス1回（EXPERIMENT_ROOT）で監査JSON byte-identical
   （SHA-256 `b8c264e6…`）。g19でK1086 greedy被覆4行 == K1097 win16 footprint
   claimed == intrinsic の三点一致を機械確認。
7. **証明書**:
   `certs/win8-root-00000000010000889002000080100000-20261120.n11`・775,317 bytes・
   21,446行・SHA-256 `105e1e2ad59f4f6baa85f37dde7306b98fc96d2164edf5b5d12205b1c71e2bc4`。

## 環境リセットを跨いだ決定的再現（運用記録・重要）

上記工程の初回実行終了直後（監査19 gate PASS・直前まで）に、実行環境
（Koyeb sandbox・503 upstream reset）が消失し、作業dirを喪失した。
本出版に先行して、repo出版正本のK1109実験dir機材（commit `9ca77ca60a`・
K1086/K1097入力のSHA pin照合込み）を再取得し、全工程
（probe再現 → A1/A2/B → 証明書化 → BigInt/Bareiss/監査19 gate → 3実行
byte-identical確認）を再実行した。結果: **証明書SHA-256（105e1e2a…）・
総nodes 4,424,758・全行集合21,446・三重検証の全数値が初回記録と完全一致**。
抽出パイプライン全体（証明書bytesから監査JSON再構成まで）が環境リセットを
跨いでbyte-exact再現した2例目（K1036の証明書SHA再現が第1例）であり、
「再現不能なローカル状態に重要証拠を残さない」規約の実効性を実証した。

## 意味と限界

- この証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は
  別工程であり、行の閉鎖claimは本項では一切行わない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2{59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold15候補: 本root 8890020証明書のreceipt fold（残余58行・着手時に単一オーナー
  宣言ノートを先行出版する）。
- 残るWIN8候補の証明書抽出: K1086 per_root上の残る未抽出根は
  `00000000000200003800200008180000`（主張2行・261,294/288,448・並走宣言済み
  commit 4496c888・着手禁止）と `00000000012000003800080009000000`
  （主張3行・657,152/825,127・並走宣言済み commit 26c88746b2・着手禁止）の
  2根のみで、K1086掃引の23根の（WIN8 uncappedの）未着手根は本rootで枯渇。
  次の抽出候補はK1089/K1091/K1095系の代替根（着手時に宣言とnodes確認が必要）。
- 残余58行のrefsolve第6ラウンド（宣言不要の未着手領域）。

## 採番記録

- 当初K1112で準備していたが、出版直前の最新main再取得で並走のy=4パラメトリック
  全称証明（K1112・commits 3a3f48f950〜280f1155ce・README弾丸着地済み）が使用済み
  と判明。衝突側再採番規約により**K1113**に再採番した（README grep・list_commits
  ・items 404の3点でK1113空きを確認）。
