# 2026-11-14 six-row q=8 m=20 class-split sweep (K0819)

高速レーン第8回。K0818（並走）が 6x19 q=8 の全35正準欠損クラス UNSAT で (6,8) の
witness-free prefix を {19} に伸ばした直後の前線 6x20 を、同一機構で直接攻撃した。

- 機構: K0818 lane の sat3.js（K0810 census + sat2.js counter core + class-split unit 節）
  を verbatim 再取得し、公式 kissat 4.0.4 linux-amd64 で決着。制御は 2x8 q=4 SAT・
  2x9 q=4 UNSAT・6x18 class {1} SAT 511,895 conflicts（K0818 と bit-exact）。
- 結果: **全35正準クラス UNSAT・合計 16,446,081 conflicts**（最難関 {2} 2,763,766 /
  128.9s、{1} 2,289,935 / 119.5s、{1,2} 2,729,150 / 120.4s）。INDET 0。
- 交叉確認: 最難関シングルトン {1},{2} を --lex=H 独立符号化で再び UNSAT
  （2,038,080 / 2,331,073 conflicts）。
- 正制御: 6x18 の SAT モデルを decode し 41石 rows (7,6,7,7,7,7) census不使用
  verifyConfig PASS — K0815 witness盤を符号化→ソルバ→検証の同一経路で再発見。
- 帰結: 6x20 に row-deficient maximal は存在しない。witness-free width set は
  {19,20}、**M_{6,8} ∈ {19,20} or ≥ 22**（上界371不変）。前線は 6x21 へ。
- 手続き: クラスは2並列worker（各 timeout 285）で走査。6x19（K0818）と比べて
  合計 conflicts は 15.5M→16.4M とほぼ横ばい（幅+1で難度は実質不変）。
  正則化・生成物の再構築は views 統合レーンに委ねる（本項目 K0819 追加と
  mwq_stabilization.csv の (6,8) 行更新のみが正本側変更）。
- 限界: 有限機械検証（K0810 census・class-split 符号化・kissat 4.0.4 の正しさまで）。
  m≥21 の persistence は未解決のまま。11x11 は無関係・UNKNOWN。

レジューム: (1) 6x21 q=7 の35クラス witness 探索が (6,7) の最前線（6×20 witnessは
rows 6,6,5,6,6,6・シングルトン{2}）。(2) 5x21 q=7 の19クラスが (5,7) の最前線。
(3) (6,8) 6x21 以降は全幅でなく tail 論証が現実的。
