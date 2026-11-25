# n11 残余72行候補供給正本の独立第二検証（whole-record経路）: single-owner declaration

K1075（残余72行のfull cache-join候補供給再構築）の出版正本に対する独立第二検証のうち、
本ノートは **whole-record経路**（生probe corpus再構成・resolve6値同一性・fold鎖数値・
クロスレーン整合・row_demand再集計）を本実行の管轄とする。

- **担当レーン**: 本実行（2026-11-20）。
- **前提（幾何レーンとの役割分担）**: 並走レーンが K1075 正本に対する幾何経路の独立第二検証
  （D4変換・厳密整数Bareiss・witness 36根とretired 38根の被覆幾何再導出・44 gate）を
  出版済み（`research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/candidate-supply-second-verification-20261120.json`、
  単一オーナー宣言
  `2026-11-20-n11-residual72-candidate-supply-second-verification-single-owner-note.md`）。
  本レーンは幾何の再導出を重複して行わず、幾何では到達できない出版記録同一性の経路のみを担う。
  両レーンは同一正本に対する互補検査である。
- **目的**: 出版済み正本のみを用い、(1) K1069 live sweep の分類・node統計を生worker probe
  記録corpus（98行・一意(root,ordering)78対・重複20行）から自前dedup/agreement実装で再構成、
  (2) K1059 dead sweep の REFUTED-D10 39/39 を sweep39dead 正本の witness_records.probe_runs
  から再構成し resolve6.base_state.dead_roots_39 と照合、(3) resolve6 正本の
  verdict_join stats/universe_hits と K1075 stage-1 複製の全数値一致、+38 refuted/+1 win
  delta 算術（7,493+39=7,532・6,707+38=6,745・786+1=787・conflict 0）、
  universe78=7,969 / universe72=7,448 の恒等式、(4) fold鎖（78→fold9 −4→fold10 −2→72）の
  集合算術・frontier数値（491,497/6,206/1,642・閉鎖40/112）・resolve6 WIN被覆4行=fold9
  target 4行、(5) 72行 row_demand 再集計（fresh-safe 52/76/4,678・judged_refuted 4/13/638・
  judged_win全0・deficit全false）、witness 36根の72行ちょうど1回被覆と matching ≤ ⌊72/2⌋=36
  の上限・36本の全行ペアで maximum=36 を記録のみから証明、(6) resolve7 正本および
  76-gate resolve7 第二検証正本とのクロスレーン整合。
- **入力pin（SHA-256）**:
  - K1075正本 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`
  - resolve5 `5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e`
  - resolve6 `e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a`
  - fold9（windfall4） `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2`
  - fold10（第17） `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`
  - sv17 `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc`
  - sweep39 live（K1069） `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc`
  - sweep39 dead（K1059） `f8608d0a04a132012f0aa692099cebe851cdf261a3ea916dc4c15d6841fc5246`
  - resolve7 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`
  - resolve7第二検証正本 `4286100804d82376418066da89167c50017244f2c6f02b81ad76a07b45bd91d6`
  - 生probe記録 w0/w1/w2/w3 `6b045eae…`/`4aaa4d0a…`/`2d4ff7dd…`/`e04e20bd…`（正確なSHA-256は機械内PINSに固定）
  - roots.json `9f0161a8a61d311534fd3a4035b1c367426691c72ad5eb44efd01a5fae37e0cc`
- **管轄外**: corpus/cache joinの再実行、候補根の新規判定、depth-10 sweepの実行
  （36-root fresh-witness掃引は既存の宣言
  `2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md` に属し本検証は実行・変更しない）、
  証明書抽出、receipt fold、幾何の再導出（既出版の幾何レーンが担当済み）、add-two-stones、
  depth>10探索。
- **解釈**: REFUTED-D10 は LOSS 証明ではない。matching・被覆は条件付き探索計画の簿記であり
  証明書ではない。標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 の
  勝敗は本検証では一切判定せず UNKNOWN のまま。

検証完了後、再現機械・機械可読結果・README・研究logを新規の独立experimentとして
`research/experiments/n11-residual72-candidate-supply-whole-record-second-verification-20261120/`
に追加する。branch/PRは作らず main に直接反映する。
