# 2026-11-15 four-row (4,5) m21 — surgery (2,2)/(3,3) の独立検証 (第2実装・全カウンタ EXACT 一致)

four-row-q5-m21-surgery-20261115 の bounded-edit surgery 主張 (m=20 witness
両埋め込みから sd≤6 編集球内の 4×21 witness 不在・有限局所負) を、TS sandbox 上の
独立第2実装 (三重計数センサス + 独自列挙 DFS・surgery4.js のコード不使用) で検証した。

- (2,2) offX=0/1: nP 2,415・nPpruned 1,269/1,272・leaves 12,754/12,816・witness 0
- (3,3) offX=0/1: nP 54,809・nPpruned 20,478/20,619・leaves 1,250,587/1,256,103・witness 0

全カウンタが surgery4.js の記録と EXACT 一致。T′={(20,3)}/{(0,3)}・nEmpty 69・
seed safe check も一致。陽性対照として 4×20 (seed = 既知 witness −2石) で
既知 m=20 witness を再発見 (nMaximal=nWitness=1・full verify ok) し、
witness 検出経路を実証。L2 補題 (Rm ⊆ 赤字曲線上の石) の証明も独立確認
(除去石の穴の再ブロック曲線は赤字正)。

検証実装は scripts/surgery_verify5.js として実験 dir に push 済み (Node 再実行可能・
RNG 不使用で bit 再現可能)。詳細は実験 README の追記。
実行環境は 13:41Z 以降依然全面停止 (bash/file_system)・GitHub API + TS sandbox のみで実施。
4×21 全体の不在決着は class-split 掃引 (c0k3p0/p1・sat5.js blocker 円分割と
較正3点は環境復旧後) が担う。

注記: 初回 push が non-fast-forward (並走実行の同時コミット) で失敗したため
最新 main 再取得後に再 push した。
