# 単一オーナー宣言: eight-row (8,12) band closure takeover — genfam12 再構築 + q12 帯掃引 17..882（2026-11-22）

- 宣言時刻: 2026-11-22T09:55Z（Vibe sandbox UTC）
- 観測 HEAD-before-push: d0518787b25145ae0c3f15c3fabe503848827d05
- スコープ（単一オーナー）: `research/experiments/eight-row-q11-q12-band-closure-20261115/`（閉包レーン正本）の (8,12) 側。元レーンの README・claim が「q12 掃引 231..882 残・records/sweep-q12.jsonl はローカル喪失・genfam12.js は格納前喪失」と記録した引き継ぎ債務の執行。8×m・q=12 の def-mode UNSAT 掃引 m=17..882（214幅の旧ローカル分 17..230 も正本記録が存在しないため本セッションで再実行して新規正本化する）。
- 作業内容: (1) 喪失した genfam12.js を README 仕様から再構築し、publish 済み三系統の oracle（sat2 全三つ組 8×11..16 q11/q12 計11幅・genfast 弦対 8×17/20/26/40/60 q11/q12 計10幅・sweep-q11.jsonl の CNF md5/vars/clauses を帯全域から8幅サンプル）で byte-identity を検証してから使用する。(2) kissat 4.0.4（公式 linux-amd64・md5 3a5eba83…）def-mode 単一節で幅ごとに UNSAT 判定・records/sweep-q12.jsonl を追記型（resume-safe・1幅1行・CNF md5 付き）で掃引。(3) 全幅 UNSAT なら M_{8,12}=17 exact を K0843・CSV へ反映、SAT 発見なら即座に Honest に HALT して witness を2系統検証。
- 受入条件:
  1. genfam12 再構築は三系統較正の全部（計29対照）が byte-identical でなければ掃引に進まない。
  2. sweep 記録は幅ごとに (status, conflicts, proc_s, cap, rc, cnf_md5, vars, clauses, tag, solver) を持ち、INDET 幅は cap 昇格の再実行で決着させる（決着不能は INDET のまま記録して閉包主張しない）。
  3. 決定性: 掃引完了後に代表幅（難・易・端）を再実行して conflicts bit-exact を確認する。
  4. M=17 exact 主張は「族census のもとで・m ≤ 984・kissat 4.0.4 正しい」までの有限機械検証として出版する（全称数学定理として過大主張しない）。UB U_{8,12}=883（K0318 substitution・w7_upper_bounds.json）は引用のまま。
  5. 出版は branch/PR なし・main 直接・push ごとに HEAD 再取得・競合したら押し進めず記録して中断。
- 非目標（non-goals）: 11×11 空盤・二石 root・S2・class 1/2/4 は非接触（UNKNOWN のまま）。(8,9) 8x29 frontier・(8,10) 26..39・(5,7) m=38..157・(6,8) m=60..370 の各レーン領域には着手しない。q11 側の既刊成果（K0843・sweep-q11.jsonl）は 1 byte 変更しない。nodes/conflicts を勝敗として読まない。
