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


## 追記: 第3水平配置 offX=−1 と剛体配置全12通りカバー (同日)

等変性で既存 2走査 (offX=0/1) から鏡映導出を試みたところ、seed 列幅 [1,19] に対し
水平 3配置目 offX=−1 が未走査であることを発見 (σ は H/V 非対称のため鏡映では
導けない)。検証済み第2実装で (2,2)/(3,3) を走査:
- (2,2): nP 2,415・pruned 1,277・leaves 12,588・witness 0・T′ 2点 {(19,3),(20,3)}
- (3,3): nP 54,809・pruned 20,811・leaves 1,252,862・witness 0

両者とも完全列挙負。等変性補題 (D₂ 鏡映で surgery 球・safety・maximality・
行欠損が保存される) と合わせ、m=20 witness の剛体配置全 12通り
(水平 3 × 対称 4像) の sd≤6 球が空であることが確定した。
実験 README 追記2に詳細。surgery_verify5.js は負の offX を取れるため再現可能。


## 追記2: 列挿入埋め込み族 (内部分割21位置) の safe 判定と surgery 走査 (同日)

剛体配置 (追記1) の次に、witness の「内部列挿入」埋め込み
(位置 c に空列を挿入・x≥c の石を +1 シフト・c=0..20 の21位置) を全走査した。
safe 判定: 12位置 safe (6 distinct 配置)・9位置 unsafe (5石円の出現・
witness の密な左中央領域では分割が安全性を破壊)。
新規4配置 (c=3,6,8,15) を (2,2)・(3,3) とも完全列挙: すべて witness 0
((2,2): c=3 11,320 / c=6 10,360 / c=8 11,067 / c=15 12,431・
(3,3): c=3 1,252,781 / c=6 1,247,430 / c=8 1,274,014 / c=15 1,271,303)。
よって列挿入埋め込み族の safe 全6配置の sd≤6 球が空と確定
(剛体配置全12通り (追記1・等変性) と合わせ、列挿入埋め込みの全配置から
sd≤6 で ≤15石 witness には到達不能)。実験 README 追記3に詳細。
