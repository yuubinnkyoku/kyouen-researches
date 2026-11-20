# 研究log: WIN8-D10証明書抽出 root 8005021（2026-11-20）

単一オーナー宣言（commit `7ffddc66`・先行出版）に基づく実行記録。

## 経緯

fold11（K1105・root `…8003180` のWIN8 receipt fold・残余72→68行）の直後に着手。
K1097の残務「WIN16候補の証明書抽出」のうち、並走宣言済み2根
（`…8180000`・`…0810000a`）と抽出済み1根（`…8003180`）を除く
greedy計画順最上位の未着手根 `00000000000000003800000008005021`（主張3行）を選定した。
選定基準: (1) K1086 greedy計画順2位・fold11後の残余68行に主張3行が全て残存、
(2) 並走が着手していないroot（実験dir・宣言ノートの走査で確認）、
(3) loser mobility 41と抽出候補中で最安価。

## 実行

1. **宣言ノートの先行出版**: `research/log/2026-11-20-n11-residual72-win8-cert-extract-root8005021-single-owner-note.md`（commit `7ffddc66`）。着手権確定後に計算開始。
2. **probe再現**: K1086出版値（andclose1 619,138・andclose0 751,581・両方 loss=true uncapped・terminal [14,18]）を本環境のrunner v17（git blob pin `c132cc64…`一致確認）で再現。各順序2回・pilot_d6 3,402 nodes 4回ともnode-exact一致（計時msのみ変動）。
3. **抽出一式**: root legal 41手の独立再導出（純Python 4×4行列式）→ A1（41プロセス・総nodes 3,272,039・fbt_drops 0）→ A2完全再実行（初手単位node/nRows完全一致・行bytes一致）→ B（単一プロセス・総nodes 2,876,091・戦略行26,083不変）。3実行の行集合byte一致。
4. **三重検証**: BigInt 3×3（41/41 sub-root・union 0/0）・Bareiss 4×4（root-check stones 8・mobility 41・consumed 26,083 0/0）・python第三方法（監査機械・全木再走査）。3方法が全集計値で一致: visited 59,594・winner 38,442・loser 10,961・応手辺 53,352・terminal 10,191・[14,18]。
5. **監査機械**: K1096出版機械（`assemble_win8_audit_20261120.py`）のroot定数差し替え+g19追加版 `assemble_win8_audit_root8005021.py`。**19/19 gate PASS**・同一cwd 2回+別cwd別プロセス1回で監査JSON byte-identical（SHA-256 `0bd2dd10…`）。g19でK1086 greedy被覆3行 == K1097 win16 footprint claimed == intrinsic の三点一致を機械確認。
   - 実装上の注記: Bareiss検証器のfilename guard（`endsWith('verify_win8_cert_bareiss.ts')`）のためローカルで一時縮約名を使った際に一度起動しないことがあった（guardは予期どおりfail-closedで、検証器自体の阳性を変えない）。出版時は原名のまま同梱。
6. **証明書**: `certs/win8-root-00000000000000003800000008005021-20261120.n11`・945,298 bytes・26,083行・SHA-256 `69f32661d80ae0887ecf385cb690e0d4300c5ad28686ec42fc83e93da79ac6f5`。

## 意味と限界

- この証明書は当該8石rootのゲーム木のみを証明する。S6親行の被覆幾何・fold（fold12候補）は別工程であり、行の閉鎖claimは本項では一切行わない。
- REFUTED-D10はLOSS証明ではない。node数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手

- fold12候補: この証明書のreceipt fold（残余68行・主張3行）。着手時に単一オーナー宣言ノートを先行出版する。
- 残るWIN8候補12根（並走宣言済み2根を除く）の証明書抽出・fold。
