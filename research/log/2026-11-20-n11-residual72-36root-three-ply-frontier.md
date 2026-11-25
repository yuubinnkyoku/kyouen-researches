# 2026-11-20 n11 残余72行36-rootの三手先D4重複監査

## 着手判断

最新main `b8eec25ccc69192d0e9dd4edbe5b1b4b6ce8d82a`、`AGENTS.md`、`research/knowledge/README.md`、K1057/K1059/K1063/K1069〜K1075と11/20のsingle-owner noteを確認した。残余72行の36-root depth-10 sweepは `2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md` で別レーンの単一オーナー作業として宣言済みであり、同一probeの再実行・重複出版はしない。

K1075の候補供給第二検証は44/44 gate PASS済み、36-root sweep準備物も40/40 gate PASS済み。掃引結果はまだmainに出版されていない。したがって本レーンは探索を起動せず、並列worker設計に関係する独立の幾何測定を行った。

## 入力と方法

- 入力: `research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
- SHA-256: `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`
- Git blob SHA-1: `45744d8255f454eae3e0d59b0e2246df80e98667`
- 入力main: `b8eec25ccc69192d0e9dd4edbe5b1b4b6ce8d82a`

K1075の `witness_full` 36根を入力順のまま読み、全rootの7石・D4正準形・安全性を再検査した。3項余因子展開と6項Leibniz展開によるBigInt行列式を独立に計算し、各三点組の121点を照合した。rootから合法な1手・2手・3手を列挙し、10石局面をD4正準化してroot内・root間の重複を数えた。

4-workerの割当は、公開driverの `roots[W::4]` に合わせた。これは幾何類の重複配置であり、DFPNの共有表命中率ではない。

## 結果

- 36 root、合法初手49〜74。
- 9石局面56,597。
- raw 10石局面733,855、root別D4類733,800。
- root内D4併合55、全root横断の一意D4類728,370。
- root間重複membership 5,430（0.739984%）、共有root組221。
- 多重度2が5,420類、多重度3が5類。最大共有pairは146類。
- 9石局面の終局0。合法な第三手の延べ数は2,201,565。
- 4 workerのraw 10石負荷は178,547〜190,756で、各9 root。pairwise overlap 5,435のうち4,193（77.148114%）がworker境界をまたぐ。

12/12 gate PASS。全221共有pairとroot別集計をJSONに保存した。

## 判断

三手先の幾何重複は0.74%と小さい一方、その重複の約77%は現在のstrided分割でworkerをまたぐ。ただし、共有D4類が実探索の同一TTキー・同一深さ・再利用可能な証明境界になるとは限らない。重複絶対数も5,430 membershipであり、共有表の複雑化を直ちに正当化するほど大きいとは言えない。

現行36-root sweepの単一オーナー作業には介入していない。掃引結果が出版された後、実測TT hit率が得られるなら、この幾何上限との比較ができる。現時点ではworker分割の変更を提案せず、実測を待つ。

## 成果物

- `research/experiments/n11-residual72-36root-three-ply-frontier-20261120/audit_36_root_three_ply_frontier_20261120.mjs`
- `research/experiments/n11-residual72-36root-three-ply-frontier-20261120/output/36-root-three-ply-frontier-20261120.json`
- `research/experiments/n11-residual72-36root-three-ply-frontier-20261120/README.md`

標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はUNKNOWNのまま。REFUTED-D10はLOSS証明ではなく、receipt被覆も行の簿記である。
