# 2026-11-20 n11 残余72行 代替9根 depth-10掃引（K1146）whole-record独立第二検証（第二検証レーン）

- 実験: `research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/`
- item: K1151（replace9 whole-record独立第二検証。番号は、K1149二重採番の後着six-rowレーンがAGENTS.md再採番規則で空き番号へ再採番する際の移動先としてK1150を協調的に空けてある）
- 単一オーナー宣言ノート: `research/log/2026-11-20-n11-residual72-replace9-whole-record-second-verification-single-owner-note.md`（commit `edc231213f`・先行出版）
- 状態: 検証機実行完了・334/334 gate PASS・出版済み

## 目的

K1146（残余23行代替9根depth-10掃引・出版正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）の
whole-record独立第二検証。DFPNエンジンの全再実行は行わず、出版正本と
18 probe記録のみをSHA-256 pinで読み、**別実装の照合機**で5掃引横断の
帳簿整合・被覆幾何・verdict censusを検証する。K1102・replace16第二検証・
candidate-supply whole-record第二検証と同じ第二検証の枠組みの継続。

## 手法

`scripts/verify_replace9_whole_record_20261120.py`（stdlibのみ・fail-closed・
検証機 SHA-256 `e92fb7556a6f12c6e3cee06477e5387ddb6214cb58875e4ee3385010f9043e8a`）。
10入力をSHA-256 pinで固定（K1085/K1086/K1089/K1091/K1095/K1097/K1146正本・
probe記録・8根被覆判定正本・K1147監査正本）。334 gate:

1. **probe経路**: 18 probes × 両AND順序の per_root 全数値照合（nodes/loss/capped/
   terminalStoneRange・ms/wall_s除く）・pilot_d6制御（nodes 3,402・loss=false・
   capped=false）・生child hex規約（child==root−最低セットビット）・
   verdict再分類（WIN⇔両順序loss=true uncapped）・nodes総計 3,574,172・
   terminal union [14,18]。
2. **残余宇宙連鎖の独立再導入**: 72→49→40→30→23→20行。各ラウンドのWIN主張+REFUTED
   主張が当時の残余宇宙の disjoint exactly-once 分割であることを行ごとに機械検証。
   20行のうち12行はK1147監査の残余着手12行hexと一致。
3. **被覆幾何（新規実装）**: 9根すべて popcount 8・D4 min-canonical・quadruple-free
   （C(8,4)=70組の4×4行列式・Bareiss）・主張行6石⊂rootのD4像・27主張が残余23行の
   exactly-once被覆・gains hist {3:6, 2:2, 1:1}。
4. **5掃引横断census（本検証の独立成果物）**: 75根D4正準形一意・quadruple-free再検証・
   累積WIN17根（52主張行）とREFUTED58根の正準形空間衝突スキャン（**衝突0**）・
   pool算術 120,474−50=120,424〔P‴〕・−58=**120,416〔P⁗〕**・
   K1097除外50根リスト恒等・宇宙簿計の独立再計算
   （150,765==23×C(115,2)・137,959==45,263+92,696・45,219==45,263−44・
   50==44+6・50,670==40,065·1+4,857·2+297·3）。
5. **win16 intrinsic footprint**: K1097 win16のintrinsicを独立再計算（15根
   intrinsic==主張・1根〔K1095第3根〕は主張1行+余剰1行を正確に再現）。
6. **新WIN候補のintrinsic初計測**: K1146 root `00000000010000809002000040002001`
   のbase72宇宙上intrinsic == 主張3行（余剰なし）。round-5 refsolve計画
   （commit `ace38772d9`）の需要構造の定量基礎。

## 結果

**334/334 gate PASS**。監査正本
`output/replace9-whole-record-second-verification-20261120.json`
（115,002 bytes・SHA-256
`5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4`・
残余宇宙72/49/40/30/23/20行hex全リスト・75根census表・17+58 verdict表・
interpretation_guard 5文言同梱）。3実行（同一cwd×2・隔離cwd/HOME×1・
PYTHONHASHSEED=random）でbyte-identical。実行 <0.2秒/回。

## trust境界・解釈

- 出版記録の二次照合であり、DFPN探索器自体の健全性は対象外（再実行は
  bulk re-executionレーン `3f34046621`）。
- WIN8-D10 candidateは証明書ではない（receipt fold・抽出は別宣言
  `63877ffd2e`）。REFUTED-D10はLOSS証明ではない。本検証は行を1行も閉じない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。**

## 補足

- 並走レーンの全probe再実行第二検証（K1149・commit 23ff55a181 出版済み）は
  エンジン出力の再実行で正本再現を確定した。本検証はその補完として
  出版記録の帳簿・幾何・censusを独立実装で照合した。両レーンの全体像:
  再実行（エンジン事実）+ whole-record照合（記録事実）。
- 同レーンが単一オーナー宣言ノート（commit `edc231213f`）のK1146掃引正本
  SHA-256転写に1文字誤り（`…bf3eefbf…`・正しくは `…bf3eebf…`）が
  knowledge README K1146 bulletから引き写されていることを指摘した。
  正しい値は入力pin `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`
  （本検証の `.input-replace9.json` がoriginal byteで固定）。宣言ノートは
  探索の実行に影響しないため、原文を保持し本ログで訂正を記録する
  （宣言時刻・範囲・その他文言は不変）。

