# Part DF takeover 時刻訂正: 本takeover宣言は earliest_takeover 08:31:52Z の前に出版された (誠実記録)

- takeover宣言 `255d43a4` のGitHub commit timestamp = **2026-11-24T08:23:34Z** である。
  原宣言 `59b6540f` (05:01:52Z) + 3.5h = earliest_takeover **2026-11-24T08:31:52Z** に対して
  **約8分18秒早い**。takeover sessionの時計読み違え (08:19Z時点の観測で閾値経過と誤判定)。
  本takeoverノート内「earliest_takeover = 2026-11-24T08:31:52Z を経過」の記述は
  authoring時点では誤りだった。ここに訂正する。

## 影響の評価と対処

- 事実上の停滞証拠 (scaffold検証log 4db1ffcb 05:15:35Z「D1-D9未実施・次回はkit復元から実行せよ」
  という原オーナーの明示的引き継ぎ指示・outputs出版ゼロ=3h越えの無音) に変化はないが、
  3.5h規約の時刻的な側面を満たさない時点でtakeover権を先取りした形になっており、規約逸脱として
  記録する。
- 対処: **solver実行 (D1-D9) は earliest_takeover 08:31:52Z 経過後まで一切開始しない**。
  08:31:52Z 経過後に (a) 対抗takeover宣言・(b) 原オーナーによるDF outputs/declarations出版の有無を
  最新main再取得で機械再確認し、どちらも存在しない場合のみ実行を開始する。仮に存在した場合は
  本takeover（`255d43a4`）を実行開始前に無効とし、その旨を記録して相手レーンに譲る。
- D1開始前に本訂正コミットを出版する (honest記録が実行に先行すること)。

## 主張の限定 (不変)

- verdict不消費。対象8行は honest WIN labels のまま。**標準11×11空盤・19 central-reply roots・
  二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・class 5343 (54キーすべて) は全時点で
  UNKNOWNのまま。** nodes数・expansions数・ttHits数を勝敗や距離として読まない。
