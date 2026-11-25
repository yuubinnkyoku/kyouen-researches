# n11 残余72行 代替9根 depth-10掃引（K1146）whole-record独立第二検証の単一オーナー宣言（2026-11-20）

本レーンは K1146（残余23行代替9根depth-10掃引・出版正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3feefbf7f912cccc88ded1e`）の
**whole-record独立第二検証**（出版済み正本・probe記録のみをSHA-256 pinで読み、
元の掃引機械とは別実装で照合する）について単一オーナーとして着手する。
並走レーンは本宣言項目に着手しないこと。宣言時刻: 2026-11-20T14:29:00Z。

## 他宣言との区別

- 探索エンジン再実行（18 probes x 2 passes + pristine reassemble）は別レーンが
  単一オーナー宣言済み（commit `3f34046621`・2026-11-20T14:16:41Z）。本宣言は
  DFPNエンジンの再実行を行わず、出版記録の整合性照合のみを対象とする
  （K1102・replace16独立第二検証・candidate-supply whole-record第二検証と同じ枠組み）。
- round-5 refsolve計画簿記（commit `ace38772d9`）・WIN8証明書抽出
  （commit `63877ffd2e`）・fold26 receipt fold（commit `23bffdd4e4`・先行レーン所有）は
  いずれも本宣言と不競合。

## 範囲

- 入力: 6正本（K1085 `5fdd342d…`・K1086 `3045e152…`・K1089 `808fbda1…`・
  K1091 `edd7ac84…`・K1095 `335eca5e…`・K1097 `2896deb0…`）+
  K1146掃引正本（`e8f5d674…`）+ K1146 18 probe記録JSONL +
  K1147外部検証監査正本（`17dbd6ab…`）。すべてSHA-256 pin fail-closed。
- 検査: (1) 18 probe記録と掃引正本per_rootの照合・pilot_d6制御・順序整合、
  (2) 残余72→49→40→30→23行宇宙の連鎖独立再導入とK1097帳簿・K1147監査23行との一致、
  (3) 9根の被覆幾何（D4正準形・quadruple-free・exactly-once・gains hist {3:6,2:2,1:1}）
  の整数幾何再実装、(4) K1097 greedy選定==K1146掃引9根、(5) 5掃引横断verdict census:
  累積WIN候補17根・REFUTED 58根のD4正準形衝突0・pool算術（safe8 120,474−50−8==120,416）・
  WIN17根の72行宇宙上intrinsic被覆と主張の関係の独立再現。
- 決定性: stdlibのみ・乱数・時刻記述なし。同一cwd2回+別cwd別HOME1回の計3実行で
  監査正本JSON byte-identical必須。

## やらないこと

- 新規probe・掃引・行の閉鎖claim・receipt fold・証明書抽出は一切行わない。
- greedy/witness選定を証明書として読まない。REFUTED-D10をLOSS証明として読まない。
  node数・solved数を勝敗として読まない。

## 解釈規約

本検証は出版記録の二次照合であり行を1行も閉じない。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて
UNKNOWN のまま。**
