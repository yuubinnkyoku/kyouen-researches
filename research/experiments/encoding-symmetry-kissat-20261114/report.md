# 拡張符号化（totalizer・lex対称性打破）と長時間バックグラウンド実行による外部SAT境界 — 6×12 q=8 最小極大サイズ=37（確定）

date: 2026-11-14
solver: kissat 4.0.4 公式 linux-amd64 リリースバイナリ（--time=長時間予算）
base encoding: K0810 encode()/toDimacs verbatim（sat.js = research/experiments/row-deficient-sat-witnesses-20261114/scripts/row_deficient_sat.js のコピー）

## 動機

K0815 第1〜3弾で、固定幅の open 境界は単発 260〜280 秒の kissat で未決着だった
（6×12 q=8 cap=36・6×30 q=5・6×23 q=6・5×22 q=6・6×21 q=7・6×19 q=8・5×20 q=7）。
第3弾レジュームの「符号化改良か分割統治」を本実験で実行した。
加えて、コマンド境界を越えて生存するバックグラウンド実行
（`setsid nohup … &`・検証済み）により 275 秒の単発制限を突破した。

## 新符号化（sat2.js — K0810コアの上に3点を追加）

1. **totalizer**（Bailleux–Boufkhad）: maxStones 全体石数上限の sequential counter を
   totalizer に置換（`--counter=tot`）。葉は x↔>=1、マージは (a_i∧b_j)→o_{i+j} と
   o_{t+1}→(a_{i+1}∨b_{j+1})、根で ¬o_{K+1}。
2. **lex-leader 対称性打破**（`--lex=H,V,HV`）: 盤面の等距変換 H（列反射）・
   V（行反射）・HV（180°回転）に対し S ≤lex σ(S) を節符号化。
   健全性: 解集合（極大安全配置・cap・欠損制約込み）はこれらの反射で不変であり、
   各 orbit の lex-min は全 σ で S* ≤lex σ(S*) を満たすため SAT 性は保存される。
3. **欠損行単一節モード**（`--deficient`・K0810 デフォルトと同一・DIMACSバイト一致を確認）:
   欠損極大（石数 < w(q−1)）⟺「ある行が ≤q−2 石」（各行は安全制約で ≤q−1 石に既に上限）。
   cap=w(q−1)−1 相当のインスタンスは全体計数器なしの単一節で表せる。
   m≥q が必要（行直線がcensusに現れる条件; 4×4 q=6 で検出）。

## 検証プロトコル

- sat2.js `--deficient` 出力は K0810 `encode()` デフォルトと DIMACS バイト一致（2×8 q=4）。
- validate.js: 小盤面 6種（2×7 q4・2×8 q4・3×5 q5・4×4 q6・3×6 q4・2×9 q4）で
  **全列挙 ground truth** と全符号化変種（deficient・deficient+lex・rowfixed+lexH・
  cap tot/seq ±lex）の SAT/UNSAT が完全一致（ALL OK）。
  （初回実行は環境リセットで消失したため再実行; 再実行も ALL OK。初回の失敗検出は
  4×4 q=6 の m<q での行不在 — 仕様として文書化）
- 制御: 2×9 q=4 UNSAT（M_{2,4}=9）・2×8 q=4 SAT（K0796 5石再現・2系統検証 PASS）。
- SAT witness は全て JS census不使用検証器（verifyConfig）と Python 別実装
  （verify_input.py = verify_py.py safe_maximal の verbatim 移植・Fraction 厳密）の
  2系統で safe+maximal PASS。
- **決定性**: L1（6×12 cap=36 tot+lex UNSAT・10,225,097 conflicts）は実行環境リセット後に
  同一CNFで再実行し conflicts まで bit-exact 再現（L1re）。

## 主結果: 6×12 q=8 最小極大サイズ = 37（確定）

| run | 符号化 | 予算 | 結果 | conflicts | 備考 |
|---|---|---|---|---|---|
| L1 | cap=36, totalizer+lex(H,V,HV)・4,285 vars/18,851 clauses | 600s | **UNSAT** | 10,225,097 | 408秒で完了・exit 20 |
| L1re | 同一CNF（環境リセット後の再実行） | 600s | **UNSAT** | 10,225,097 | bit-exact 再現 |
| X1 | cap=36, **K0810元符号化**（seq・lex無し・5,574 vars/20,568 clauses・dump.js） | 1500s | **UNSAT** | 20,469,242 | 1155秒で完了・独立符号化での交叉確認 |
| ctrl | cap=37, totalizer+lex | 240s | SAT | 383,522 | 37石 witness・行構成 7,7,2,7,7,7・2系統検証 PASS |

- cap=36 UNSAT（2符号化で一致）+ cap=37 SAT（本実験のtot+lexでも再現）→
  **6×12 q=8 の最小極大サイズは 37 に確定**（従来 ≤37・cap=36 未決着; K0815のopen項目）。
- 符号化の効果: 元符号化 20.5M conflicts/1155s に対し totalizer+lex は
  10.2M conflicts/408s — UNSAT証明は約2倍の効率（conflict数・実時間とも）。

## 負の結果（符号化の非対称効果・重要な観測）

- **lex は witness 発見を阻害する場合がある**: 6×18 q=8 欠損極大 witness（41石・既知）
  は `--deficient`（lex無し）では **15.9秒/492,432 conflicts で発見**（行構成 7,7,7,7,6,7・
  2系統検証 PASS）するが、`--deficient --lex=H,V,HV` では 240秒/5,084,165 conflicts でも
  未発見。単一節欠損モード自体は旧「拡張符号化」（全体計数器）より速い
  （6×18: 32秒/697k → 15.9秒/492k）。
- 教訓: SAT（witness探索）には lex 無し単一節、UNSAT（不在証明）には totalizer+lex を
  使い分けるポートフォリオが正解。対称性打破が探索順を悪化させる実例。
- 単発275秒: 6×12 cap=36 tot+lex 6.96M・6×19 q=8 def+lex 5.86M・6×21 q=7 def+lex 4.55M
  いずれも未決着 → バックグラウンド長時間実行が決着の鍵。

## フロンティア攻撃（結果は output/ の JSON）

バックグラウンド 1500〜1800 秒で (6,5) 6×30・(6,6) 6×23・(5,6) 5×22・(6,7) 6×21・
(6,8) 6×19 の欠損極大有無（欠損行単一節モード・SAT側はlex無し）と (5,7) 5×19 の
SAT交叉確認（occupancy完全列挙 K0738–K0759 は UNSAT と主張 — 独立系統での確認）を
実行した。各結果の verdict は output/*.json の result フィールド参照。

## フロンティア攻撃の結果（第1報・2026-11-14 12:00 UTC）

| run | 盤 | 符号化 | 予算 | 結果 | conflicts | 備考 |
|---|---|---|---|---|---|---|
| L2 | 6×30 q=5 | def単一節・lex無し | 1800s | **SAT** | 4,001,401 | 23石 witness・行構成 4,4,4,4,4,3・2系統検証 PASS・output/L2_c630_def.json |
| L3 | 6×23 q=6 | def単一節・lex無し | 1500s | **SAT** | 919,243 | 29石 witness・行構成 4,5,5,5,5,5・2系統検証 PASS（2分弱で判明） |
| L4 | 5×22 q=6 | def単一節・lex無し | 1500s | **未決着（中断）** | 14.7M+ | 約1330秒進行時に実行環境アウテージで中断・verdict なし |

- L2/L3 ともに並走の extend6 深除去レーン（第5弾）が同日に同じ盤で発見した
  witness とは**別系統の独立確認**。かつ H/V/HV 全等距変換での正準形比較により
  既知 witness（6×30: 2件・6×23: 8件）のいずれとも非同型の**新同型類**
  （第3・第9）である。境界はすでに extend6 で [31,658]・[24,495] に更新済みのため
  本実験は交叉確認と探索空間の相違の実証（K0815 第6弾参照）。
- 観測: プール相対列挙（base近傍・rem/add形式）は直接SATの探索空間のごく一部しか
  覆っていない。直接SATは両盤で列挙到達範囲外の同型類を発見した。
- L4 は 5×22 q=6 で歴代最長の 14.7M+ conflicts を投入したが環境アウテージで
  verdict は未取得（非不在）。次回レジューム: L4再実行（1500s）→
  L9 6×31 q=5（1800s）→ L10 6×24 q=6（1500s）→ L5 6×21 q=7・L6 6×19 q=8（各1200s）→
  L7 5×19 q=7 def+lex（K0738–K0759交叉確認・1200s）→ L8 5×20 q=7 def+lex
  （K0816交叉確認・1500s）→ L11 5×23 q=6（gap check・1200s）。
  詳細は research/log/2026-11-14-encoding-symmetry-frontier-runs.md。

## 運用（第1報で追加）

- 実行環境は本セッション中に約20分以上の完全なアウテージ（bash/file_system全滅・
  GitHub API系のみ生存）に入った — 進行中のkissatとバックグラウンドキューは失われる。
  完了済み結果は即pushが唯一の保護手段（L2/L3のsummaryはlogに記録済み）。
- pgrep は環境に無い — バックグラウンド待機は /proc スキャンで実装。
- 複数runの逐次実行は待機チェーン付きシェルスクリプト（前runの /proc 消失 or
  done marker を待って次を起動）で自動化できる。

## 運用（本セッションの知見）

- `setsid nohup … &` で起動したプロセスはコマンド境界を越えて生存する
  （nohup 単体では node ラッパーが境界でkillされる場合あり — L1初回がこれで喪失）。
- 実行環境リセット（Koyeb）で /tmp も消滅 — 完了成果は即push、
  進行中の log はこの README/repo に数値を逐次記録して二重化。
- kissat は同一CNFで bit-exact 決定的 — リセット後の再実行で node-exact 復元可。
