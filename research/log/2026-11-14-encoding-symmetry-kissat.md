# 2026-11-14 高速レーン: 拡張符号化と長時間バックグラウンド実行 — 6×12 q=8 最小極大=37確定

repo最新main（HEAD 453acdf6 → 31e11245）・AGENTS.md・knowledge README・K0815/K0816確認。
並走は n11 class2-lane（cost-69帯）・five-row-q7-m20 enumeration lane（K0816で5×20完了）・
素数census lane — 本レーンの主題（固定幅SAT境界・符号化）と衝突なし。

## 実施内容

1. **sat2.js 開発**（K0810 encode/toDimacs コア verbatim + 3拡張）:
   totalizer符号化（maxStones上限）・lex-leader対称性打破（H/V/HV・orbit-min健全性）・
   欠損行単一節モード（K0810デフォルトとDIMACSバイト一致を確認）。
2. **検証**: 小盤面6種の全列挙ground truthと全符号化変種（deficient/deficient+lex/
   rowfixed+lexH/cap tot/seq ±lex）が完全一致（validate.js ALL OK・2回）。
   2×9 q=4 UNSAT・2×8 q=4 SAT（K0796再現）制御。SOLVED: m<qでは行直線が
   censusに現れず欠損行単一節モードは定義不能（4×4 q=6で検出）。
3. **setsid バックグラウンド実行の確立**: `setsid nohup … &` で起動した
   プロセスはコマンド境界を越えて生存（nohup単体ではnodeラッパーが境界でkill
   される場合あり — L1初回をこれで喪失し、決定的再実行で復元）。
   これにより275秒の単発制限を突破（600〜1800秒予算）。
4. **主結果: 6×12 q=8 最小極大サイズ = 37（確定）**:
   cap=36 UNSATを totalizer+lex（10,225,097 conflicts・408s・リセット後bit-exact再現）
   と K0810元符号化（20,469,242 conflicts・1155s）の2独立符号化で確認。
   cap=37 SATはtot+lexでも再現（383,522 conflicts・37石・2系統検証PASS）。
   K0815第1弾の残項目「cap=36」を決着。
5. **符号化の非対称効果（負の結果・有意な観測）**:
   6×18 q=8 既知41石witnessは欠損行単一節lex無しで15.9秒発見・
   **lex付きでは240秒でも非発見**（5.08M conflicts）。旧拡張符号化（全体計数器32秒）
   に対し単一節lex無しは15.9秒 — witness探索には「欠損行単一節・lex無し」、
   UNSAT証明には「totalizer+lex」のポートフォリオが正解。
6. 単発275秒の抵抗: 6×12 cap36 tot+lex 6.96M・6×19 q8 def+lex 5.86M・
   6×21 q7 def+lex 4.55M（いずれも旧符号化よりconflict/秒は改善・未決着）。

## 反省・運用

- 実行環境リセット（Koyeb）が1回 — /tmp・workspace全滅。push前の成果消失を
  決定的再実行と会話内記録で復元。以後「run完了ごとに数値を記録→即push」。
- CSV更新でstatus/source列のindex取り違えを1回起こしかけた（assertで事前に防止）。
- GitHub api の release探索はrepo名変更（arlencox→arminbiere/kissat）に注意 —
  web_searchで当たるのが速い。

## レジューム

1. フロンティア長時間実行（実行中/未実行）: (6,5) 6×30 q=5 欠損行単一節・
   (6,6) 6×23 q=6・(5,6) 5×22 q=6・(6,7) 6×21 q=7・(6,8) 6×19 q=8 —
   SATなら下界+1・UNSATなら現下界が最終確定。どちらも成果。
2. (5,7) 5×19 q=7 cap=29 のSAT交叉確認（K0738–K0759のoccupancy列挙UNSATの
   第二系統確認・欠損行単一節+lex・UNSAT期待）と 5×20 q=7（K0816確認）。
3. 6×12 q=8 のDRAT証明の生成と検証ツール整備（今のUNSATは2符号化一致のみで
   DRAT未検証 — 素数レーンのDRAT VERIFIED方式に揃える価値）。
4. cap=36の第3符号化（tot無しlex）での三重確認は任意。

## 11×11空盤・二石root {49,60}・S2 {59,60}・class 2・class 4 はいずれも UNKNOWN

（本レーンの固定幅成果は無盤面勝敗に無関係）
