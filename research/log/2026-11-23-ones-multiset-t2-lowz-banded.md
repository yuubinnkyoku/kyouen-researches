# run log: {1}^t z=1 分離（T2）昇格 K1269・低z banded window extension K1270（2026-11-23）

Vibe 高速レーン（定時自律実行・1セッション）。 reclaim 元: 前回セッションの
高速レーンレジューム「(a) T2 の独立 K 昇格」が最有力候補と指定していた課題を
着手し、その裏付け計算から新定理（低z banded window extension）が生えたため
1宣言で両方を出版した。

## 選定（着手前の最新 main 確認）

- observed HEAD `85d26a2c4e`（Part CK completion・長期レーン・非接触）。直近
  コミット走査で統合窓宣言 `cf299bdd` 完了以降に高速レーン系の対抗宣言なし。
- K 項目最高番号は K1268（items commit `7a9ed19f5c`）で K1269/K1270 空きを確認。
- AGENTS.md・SCHEMA.md・統合窓 report・出版検証器 byte 事前検証
  （verify_unified_window_sharpness.py SHA-256 0ab66665… が出版記述と一致・
  engine block 2,508B SHA-256 bd5f22e4… が出版 report 記述と一致）を確認。
- K1267 item が「T2 の K 昇格は次回」と明記・K1268 report が予想 C1 を open
  problem として登録済み。y=23 レーン（仮採番 K1266・宣言 `474ec50b`）は非接触。

## セッションの流れ

1. **紙面作業（宣言前・エンジン実行 0 回）**: T2 の証明（出版済み・再確認）に
   加え、選択肢集合一致の手法で C1 の z=0 行・z=1 行が帰納で落ちることを
   紙面で発見した:
   - z=0 slice: min>=2 で B/C 手が不在になり、全 A手子が K1264 窓端か帰納
     （底は K0832）で単一値 v(Σ−1,0,m) に縮約、親も単一側も mex{同一个値}。
   - z=1 slice（m>=3）: 親子の値集合 {v(Σ−1,1,m+1)} ∪ {1 XOR v(Σ,0,m+1)} が
     単一側の選択肢と完全一致（C手は z=0 slice による）。
   - 底 m=2: min=1・ちょうど1個の 1・予算 3 の z=1 分類（補題 LW）で H=2 一様、
     親の mex が 1 に一致（2 は吸収）。X={2} 辺境は直接計算。
   これが M2/K1270。宣言ノートに証明全文を開示して先行出版した。

2. **単一オーナー宣言**（publish-then-execute・commit `9ceb96d0`）:
   research/log/2026-11-23-ones-multiset-t2-lowz-banded-single-owner-note.md
   ・M1（K1269・T2 の昇格）と M2（K1270・新証明）・LW・境界の鋭さ・機械 protocol
   D0-D5・紙面予想値を事前登録・fetch-back byte 一致を確認。

3. **機体構成**: build_lowz_banded_verifier.py が出版統合窓検証器から
   engine block を SHA pin 付き機械抽出（PROVENANCE PASS・byte-identical・
   手転写ゼロ）。template + 埋め込みで機体を生成
   （初版 SHA-256 c1e6ad75…→訂正版 dda422f2…）。

4. **run 1（AUDIT FAIL→訂正の誠実記録）**: 総照合 64,200 比較のうち D0c が
   bad=2。原因は宣言前紙面予想値の 1 件「H(3;(1,2);0)=0（K0832 帯と注記）」が
   誤りで、K0832 の R<=2 条款は R=3 を束縛しない（正値は 2・
   mex{B:v(2,1,2)=1, A:v(2,0,2)=0}）。fail-closed 設計が機能した最初の捕捉例。
   M1/M2 の証明はこの値を使用していない。初回監査正本を
   output/audit-pre-correction.json として保存・機体の当該エントリを正値 2 と
   導出コメントに訂正（宣言ノート本文は一次資料として不変・訂正は本 log と
   report の記録による）。

5. **run 2 以降（AUDIT PASS）**: 総照合 64,200 比較 bad 0
   （D0 52,234・D0b 85・D0c 182・D1 868・D2 3,652・D3 3,816・D3b 63・D4 3,300）。
   決定性 4 実行（同一 cwd×2・隔離 cwd・env -i 別 HOME/PYTHONHASHSEED=random）で
   output/audit.json byte-identical
   （SHA-256 ea5467c3198931e16691efccf4eeeb118de50aed96845cb6870250550b5e0a27）。
   変異電池 7/7 捕捉（mut1..mut7・output/tamper.txt）。wall 約35秒/実行。

6. **census 記録（beyond・判定外）**:
   - z=0 の窓+2: 332 beyond 点すべて無分離（z=0 では窓+2 までの拡張候補が
     存在する可能性。次課題）。
   - z=1・m=2 の窓+2=5: 23 点中 16 点で分離・すべて親2 vs 単一0（m=2 行の
     窓+2 は分離帯・parent 2 一様の一般則は未解決）。
   - 深部（m=15..25・乱数 300 点）も含めて slice 主張 bad 0。

7. **出版**（fetch-back byte 照合）:
   - Commit A `6f24d49f` 実験dir 7 ファイル
     （report・機体 dda422f2…・template・build f88f6da3…・audit ea5467c3…・
     audit-pre-correction 8bef4cd2…・tamper.txt）7/7 byte 一致。
   - Commit B 本 commit: K1269 item・K1270 item・本 run log。
   - README bullet は別 commit（3 bullet・K1269・K1270）。

## K番号

K1269（T2 昇格・proved）・K1270（低z banded・proved）は AGENTS.md 規約により
仮採番として採番（main 上の K1268 までと衝突なし・items コミット履歴で確認）。
統合時に衝突があれば再採番する。

## 未解決・次課題（次回実行の候補）

1. **z=0 の窓+2 の全称化**: census 332 点無分離。M2 z=0 と同型の帰納で
   H(m+2;X;0)=v(Σ,0,m+2) が証明できる可能性が高い（a=m 子の予算 m+1 が
   M2(z=0, m−1) の帯式 (m−1)+1 に丁度一致する）。単一オーナー宣言→機体→の
   publish-then-execute で着手可能。
2. **C1 の z>=2 帯**: バンド内 a=m 子の形状拘束（ちょうど1個の m−1・他>=m）の
   値制御が帰納の鍵。前線 witness 一意性（d=0/1）と E6 の L1/L2 親値 2 が
   手がかり。
3. **z=1・m=2 の窓+2 分離帯の一般則**（parent 2 一様性の全称化）。
4. **{1}^t の z>=2 疎パターンの一般則**（E5・K1268 課題 4）。
5. y23 機体出版後の C4t 予測照合（clip47 違反182・first (60,110,110)・
   clip48 0違反・types 465,939。予測資材は前々回セッションが work/ に作成）。

標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4 は常にUNKNOWNのまま。nodes 数等を勝敗として読まない。
11×11巨大探索・y>=23族・3トークン一般構造・固定幅・q点版は本レーンの範囲外。
