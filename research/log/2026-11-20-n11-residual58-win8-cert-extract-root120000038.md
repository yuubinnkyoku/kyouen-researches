# 研究log: WIN8-D10証明書抽出 root 120000038（2026-11-20）

単一オーナー宣言（commit `26c88746b24dc510cb42f3cd64ec0ee746f6da06`・先行出版）に基づく実行記録。

## 経緯

K1113（並走レーン・root 00000000010000889002000080100000 証明書抽出）の出版と
ほぼ同時に着手。残るWIN8候補のうち、並走宣言済み3根（`…8180000`（4496c888）・
`…0810000a`・`…889002…80100000`（60e2940cf0））と抽出・fold済み4根
（`…8003180`・`…8005021`・`…9840004`・`…9090022`）を除く次安価の未着手根
`00000000012000003800080009000000`（主張3行・K1086探査nodes 657,152/825,127）を
選定した。選定基準: (1) fold14後の残余58行に主張3行が全て残存（fold14正本の
residual_row_hex_after照合）、(2) 並走が宣言していないroot（log最新走査で確認）、
(3) 探査nodesが残る候補中最小。

## 実行

1. **宣言ノートの先行出版**: `research/log/2026-11-20-n11-win8-cert-extract-root00000000012000003800080009000000-single-owner-note.md`（commit `26c88746`）。着手権確定後に計算開始。
2. **probe再現**: K1086出版値（andclose1 657,152・andclose0 825,127・両方 loss=true uncapped・terminal [14,18]）を本環境のrunner v17（git blob pin `c132cc64…`一致確認）で再現。各順序2回・pilot_d6 3,402 nodes 4回ともnode-exact一致（計時msのみ変動）。
3. **抽出一式**: root legal **53手**の独立再導出（純Python 4×4 Bareiss行列式・石 [24,27,43,59,60,61,85,88]・quadruple-free・LSB bit 24・child `…80000000`）。A1（53プロセス・4並列・総nodes 2,723,200・最大初手 bit 110 の 223,518・fbt_drops 0）→ A2完全再実行（初手単位node/nRows完全一致・行bytes一致）→ B（単一プロセス・別cwd・総nodes 2,141,807・戦略行32,470不変）。3実行の行集合完全一致。Bのnodes会計はA1 chunk合計(2,723,200)より小さい（9840004型のmemo温存差。戦略行の不変性が本質でありnode会計は証明内容に影響しない）。
   - 実行中に誤った--root引数での起動を1回行った（30進hex欠損盤）。抽出器は fatal=0・ok:false で行出力を一切拒絶した（fail-closed作動の追加実例）。正しいrootで再実行して完走。
4. **三重検証**: BigInt 3×3（53/53 sub-root・union 0/0・期待mobility 53・期待[14,18]をCLI pin）・Bareiss 4×4（root-check stones 8・loserMobility 53・53 sub-root全PASS・union 0/0）・python第三方法（監査機械・全木再走査）。3方法が全集計値で一致: visited 69,115・winner 44,580・loser 13,197・応手辺 61,058・terminal 11,338・[14,18]。
5. **監査機械**: K1109出版機械（`assemble_win8_audit_root9090022.py`）のroot定数差し替え版 `assemble_win8_audit_root120000038.py`（g05 mobility 53・g07主張3行・g08 bit 24・g17/root_mobility/subroots/bareiss数/loserMobilityの50→53・g19の `len(fp["claimed"]) == 4` → `== 3`）。**19/19 gate PASS**・同一cwd 2回+別cwd別プロセス1回（EXPERIMENT_ROOT）で監査JSON byte-identical（SHA-256 `ab8cd535…`）。g19でK1086 greedy被覆3行 == K1097 win16 footprint claimed == intrinsic の三点一致を機械確認。
   - 実装上の注記: 移行時にg17の `brc == {"stones": 8, "loserMobility": 50}` 定数を53へ書き換え忘れた状態では g17 が PASS せず fail-closed した（K1109のg19 len(claimed)教訓と同型）。監査機が期待値不一致を正しく拒否した実証として記録する。
6. **証明書**: `certs/win8-root-00000000012000003800080009000000-20261120.n11`・1,171,958 bytes・32,470行・SHA-256 `5a1359033325e918cf5d9cd2d60ff63fc2fd45e30b926e79330560a7a3a23c4c`。

## 意味と限界

- この証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は別工程であり、行の閉鎖claimは本項では一切行わない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2{59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold15/16候補: 本root 120000038証明書とK1113 root `…889002…80100000`証明書のreceipt fold（着手時に単一オーナー宣言ノートを先行出版する）。
- 残るWIN8候補の証明書抽出: K1086由来の7根は今回で全て出版・宣言済みとなった。未宣言の残りはK1089（3根）・K1091（3根）・K1095（3根）由来の9根から選定（着手時に単一オーナー宣言必須）。残余58行のrefsolve第6ラウンドは宣言不要の未着手領域。
