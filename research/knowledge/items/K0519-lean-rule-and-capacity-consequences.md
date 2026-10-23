---
id: K0519
title: 共円ルールと一様終端ゲームの一般帰結47補題をLean形式検証
kind: verification
status: verified
topics: [rules, formalization, grundy, strategy-length]
aliases: []
relations: []
artifacts:
- path: Kyouen/StructuralConsequences.lean
  role: lean
  note: 47個の一般補題。有限盤面の全数探索や追加公理に依存しない
- path: .github/workflows/lean-foundations.yml
  role: verifier
  note: repository指定のLean toolchainで新規moduleも検査するCI
scope: SquareBoardの任意の辺長・任意のlist局面と、UniformTerminalを満たす任意の有限rankゲーム
evidence: Lean 4.30.0のlake build Kyouen.StructuralConsequencesが成功
---

47個の補題を既存の実行可能ルールと一般ゲーム定義から証明した。
証明名と厳密な仮定はartifactの各theoremを正本とする。

- Winningは敗北子の存在、Losingは全子の勝利と同値。
  終局はLosingでWinningではなく、唯一の子を持つ局面の勝敗も特徴づける。
- 禁止四点の存在は4点の明示的証人と同値。占有集合の拡大で禁止性は保存され、
  安全性と合法性は占有集合の縮小で保存される。
- 合法手の出発・到着局面は安全。重複なし局面への合法追加は重複なしを保つ。
  既占有点・既禁止局面には合法着手できない。
- 同じ点を含むlistは順序や重複数にかかわらず同じ禁止性・合法性を持つ。
  1・2・3要素listは安全で、1石・2石局面の合法性は未占有性だけで決まる。
- 実装のmovesに属する子は、合法な点1個を追加したlistであることと同値。
  各遷移は長さを厳密に1増やし、安全性・重複なし・親の包含を保つ。
  自己ループと2周期は存在せず、禁止局面には子がない。
- UniformTerminalの下では、終局・容量到達・残り手数0は同値。
  1手ごとに残り手数は1減り、2手では2減る。
  容量到達時はLosingかつGrundy数0、残り1手はWinning、残り2手はLosing。

再現: `lake build Kyouen.StructuralConsequences`。
ローカルでは利用可能なLean 4.30.0で確認した。repository指定の4.35.0は
ローカルに未導入で、取得要求がHTTP 403となったため、同版でのローカル検査は未実施。
CIはrepositoryのlean-toolchainを使用する。新たな具体盤の勝敗や未解決盤の解決は主張しない。
