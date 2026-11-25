# 研究log: WIN8-D10証明書抽出 root 9840004（2026-11-20）

単一オーナー宣言（commit `45920e13edb746f4867524e7160baf3f0ff15492`・先行出版）に基づく実行記録。

## 経緯

fold12（K1107・root `…8005021` のWIN8 receipt fold・残余68→65行・open 8行閉鎖）の直後に着手。
残るWIN8候補のうち、並走宣言済み2根（`…8180000`・`…0810000a`）と抽出・fold済み2根
（`…8003180`・`…8005021`）を除く最安価の未着手根
`00000000000000003800000009840004`（主張3行・K1086探査nodes 512,590/614,246）を選定した。
選定基準: (1) fold12後の残余65行に主張3行が全て残存、(2) 並走が着手していないroot
（実験dir・宣言ノートの走査で確認）、(3) 候補中最小の探査費用と主張行の費用効率。

## 実行

1. **宣言ノートの先行出版**: `research/log/2026-11-20-n11-win8-cert-extract-root9840004-single-owner-note.md`（commit `45920e13`）。着手権確定後に計算開始。
2. **probe再現**: K1086出版値（andclose1 1,143,198・andclose0 1,528,656・両方 loss=true uncapped・terminal [14,18]）を本環境のrunner v17（git blob pin `c132cc64…`一致確認）で再現。各順序2回・pilot_d6 3,402 nodes 4回ともnode-exact一致（計時msのみ変動）。
3. **抽出一式**: root legal 57手の独立再導出（純Python 4×4行列式）→ A1（57プロセス・総nodes 4,109,768・最大初手 bit 94 の 294,494・fbt_drops 0）→ A2完全再実行（初手単位node/nRows完全一致・行bytes一致）→ B（単一プロセス・別cwd・総nodes 3,075,922・戦略行45,286不変）。3実行の行集合byte一致。
4. **三重検証**: BigInt 3×3（57/57 sub-root・union 0/0）・Bareiss 4×4（root-check stones 8・loserMobility 57・57 sub-root全PASS・union 0/0）・python第三方法（監査機械・全木再走査）。3方法が全集計値で一致: visited 103,531・winner 66,627・loser 19,571・応手辺 91,337・terminal 17,333・[14,18]。
5. **監査機械**: K1106出版機械（`assemble_win8_audit_root8005021.py`）のroot定数差し替え版 `assemble_win8_audit_root9840004.py`（g19継承）。**19/19 gate PASS**・同一cwd 2回+別cwd別プロセス1回（EXPERIMENT_ROOT）で監査JSON byte-identical（SHA-256 `2e453a76…`）。g19でK1086 greedy被覆3行 == K1097 win16 footprint claimed == intrinsic の三点一致を機械確認。
   - 実装上の注記: Bareiss検証器のfilename guard（`endsWith('verify_win8_cert_bareiss.ts')`）のためファイル名は出版名と同一に保つ（K1106と同一のfail-closed運用）。BigInt検証器はローカルでは `verify_bigint.mjs` で作業したがK1106 repo版 `verify_win8_certificate_bigint_independent.mjs` と byte-cmp 同一を確認し、出版名で同梱する。
6. **証明書**: `certs/win8-root-00000000000000003800000009840004-20261120.n11`・1,640,220 bytes・45,286行・SHA-256 `5b114b9e739b7a0a300434afb7ec5326564fc54b0d234df5e3d61abc44541143`。n11-terminal-strategy-v1全証明書中で最大行数（K1106の26,083行の1.74倍・45,286行）。

## 意味と限界

- この証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold（fold13候補）は別工程であり、行の閉鎖claimは本項では一切行わない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold13候補: この証明書のreceipt fold（残余65行・主張3行+coverage_of82内在行）。着手時に単一オーナー宣言ノートを先行出版する。
- 残るWIN8候補13根の証明書抽出（次の最安価 `00000000000000909002200080100000`・探査 nodes 512,590/614,246・claims 4）と残余65行のrefsolve第6ラウンド。
