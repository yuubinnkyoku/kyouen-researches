# 研究log: WIN8-D10証明書抽出 root 9090022（2026-11-20）

単一オーナー宣言（commit `0202057295a20f3c3c3e99036014697f34eecb58`・先行出版）に基づく実行記録。

## 経緯

K1108（root 9840004 証明書抽出・README弾丸まで出版完了）の直後に着手。
残るWIN8候補のうち、並走宣言済み2根（`…8180000`・`…0810000a`）と抽出・fold済み
2根（`…8003180`・`…8005021`）と前段抽出根（`…9840004`）を除く次安価の未着手根
`00000000000000909002200080100000`（主張4行・K1086探査nodes 512,590/614,246）を
選定した。選定基準: (1) fold12後の残余65行に主張4行が全て残存、
(2) 並走が着手していないroot（宣言note 48件の走査で確認）、(3) 探査nodesが
残る候補中最小（9840004の半分弱）。

## 実行

1. **宣言ノートの先行出版**: `research/log/2026-11-20-n11-win8-cert-extract-root9090022-single-owner-note.md`（commit `02020572`）。着手権確定後に計算開始。
2. **probe再現**: K1086出版値（andclose1 512,590・andclose0 614,246・両方 loss=true uncapped・terminal [14,18]）を本環境のrunner v17（git blob pin `c132cc64…`一致確認）で再現。各順序2回・pilot_d6 3,402 nodes 4回ともnode-exact一致（計時msのみ変動）。
3. **抽出一式**: root legal 50手の独立再導出（純Python 4×4行列式・石 [20,31,45,49,60,63,68,71]・quadruple-free・LSB bit 20・child `…80000000`）→ A1（50プロセス・総nodes 6,102,650・最大初手 bit 10 の 476,446・fbt_drops 0）→ A2完全再実行（初手単位node/nRows完全一致・行bytes一致）→ B（単一プロセス・別cwd・総nodes 6,102,650・戦略行29,942不変）。3実行の行集合byte一致。9840004と異なりBのnodes会計がA1と同一だった（chunk/単一プロセスの差が本rootでは現れない。戦略行の不変性が本質でありnode会計は証明内容に影響しない）。
4. **三重検証**: BigInt 3×3（50/50 sub-root・union 0/0）・Bareiss 4×4（root-check stones 8・loserMobility 50・50 sub-root全PASS・union 0/0）・python第三方法（監査機械・全木再走査）。3方法が全集計値で一致: visited 65,134・winner 42,115・loser 12,780・応手辺 58,084・terminal 10,239・[14,18]。
5. **監査機械**: K1108出版機械（`assemble_win8_audit_root9840004.py`）のroot定数差し替え版 `assemble_win8_audit_root9090022.py`（g05 mobility 50・g07主張4行・g08 bit 20・g17/brc等の57→50・g19の `len(fp["claimed"]) == 3` → `== 4`）。**19/19 gate PASS**・同一cwd 2回+別cwd別プロセス1回（EXPERIMENT_ROOT）で監査JSON byte-identical（SHA-256 `00836a6e…`）。g19でK1086 greedy被覆4行 == K1097 win16 footprint claimed == intrinsic の三点一致を機械確認。
   - 実装上の注記: 移行時にg19の主張行数定数（9840004の`== 3`）を`== 4`へ書き換え忘れた状態では g19 が PASS せず fail-closed した。監査機が期待値不一致を正しく拒否した実証として記録する。
6. **証明書**: `certs/win8-root-00000000000000909002200080100000-20261120.n11`・1,082,873 bytes・29,942行・SHA-256 `b8a15f9aac5e5f802f85459318247cb20bc983e3b2372167917ba8138cbc7a54`。

## 意味と限界

- この証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold は別工程であり、行の閉鎖claimは本項では一切行わない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2{59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold13/14候補: K1108 root 9840004証明書と本root 9090022証明書のreceipt fold（残余65行・着手時に単一オーナー宣言ノートを先行出版する）。
- 残るWIN8候補12根の証明書抽出（K1086 per_root上の次候補）と残余65行のrefsolve第6ラウンド。
