# six-row (6,6) 6×26 frontier probe — session log（2026-11-22）

- 01:55:27Z 単一オーナー宣言 publish（commit `05785cdf`・宣言時 HEAD `a37a4825`）。
  対象: 6×26 q=6 class{2} krow=2:4+minpos=11 分解の初回走査（cap 260s 単一 probe）。
- 01:55:38Z CNF 生成（vars 58,722・clauses 205,674・sha256 `cc150fa0…`）。
  機材 pin 照合: sat3.js `e04581eb…`（K1215/K1217 出版正本）・kissat 4.0.4 官 `21da5d98…`。
- 01:55:38-01:59:59Z probe 260s → **INDET・3,555,947 conflicts**（6×25 の同一 H-split の
  SAT 3,574,244 に肉薄する値）。
- 宣言スコープ外の延長を 02:00:08Z に追加（同一インスタンス・cap 1200s）。理由: 壁の直後で
  SAT する可能性を放置しないため。追加走査であることを records.jsonl note と実験READMEに明記。
- 02:00:08-02:20:08Z extended 1200s → **INDET・14,704,926 conflicts**（RSS 85 MB・SIGTERM）。
  同一 H-split 単体では 6×26 の壁はこの予算では越えられない、という第1 datapoint として確定。
- 出版: 宣言（済み）→ 実験 dir（enc meta・生ログ2件・records.jsonl・README・session log・MANIFEST）。
  CSV (6,6) 行・knowledge README は値更新がないため不変。
- 知見: frontier 1幅ごとに同一分解の費用は乗る。次回は分解の細分化（minpos 掃引・krow 行位置追加
  分割）か witness 側アプローチ（bounded surgery・並進 census）から入るのが合理的。

標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーン非接触で UNKNOWN のまま。
conflicts 数を勝敗として読まない。
