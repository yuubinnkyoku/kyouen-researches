# 11×11：S5共有証明DAGの増分統合と証人選択

K0376の「既知LOSS 31 classすべてが117手被覆に必要」という最小値は、S5証明の
節点最小値や計算時間を意味しない。ここではK0375にある既に独立検証済みのS5根だけを
扱い、solver-trustedな新規LOSSを証拠に加えない。

## 範囲

K0375に保存された、互いに異なるS4配下の三根S5 LOSS証明を二組読み込み、
既存のKYPRFDG v1形式と独立検証規則のまま6根へ段階的に統合する。新しい証明書は
`.local/`へ出力し、元JSONや過去の証明書は変更しない。solver、cache、未解決S5の
探索結果は読み込まず、探索・probeも起動しない。

K0372の証拠隔離、元先手視点のAND/OR極性、全合法手の完全性、終局のみの葉という
信頼境界を保持する。`{60,27}`、S4の完全境界、未解決S5の独立証明はこの成果に
含まれない。

## 入力の固定と現在境界

入力はK0375が独立検証済みとしてSHA-256を記録した次の二つだけである。

| 群 | 根 | 入力節点 / 辺 | JSON gzip | SHA-256 |
|---|---:|---:|---:|---|
| latest S4 | 3 | 2,337,747 / 3,484,437 | 72,771,052 B | `48edffe570591e7196c2021353342a05ba058d70b141f05128bd17c207d4e922` |
| previous S4 | 3 | 1,002,511 / 1,517,437 | 29,607,918 B | `9f55e6997f62ee2bae31d286b98ad2b89b6306e18df5091eac081b05d5d10af6` |

入力ごとにK0375の証明書・検証receipt hash、根の極性、節点・辺数、trusted leaf 0を
照合してから、JSONを逐次SQLiteへ読み込む。current leading S4
`(1297036692683752448,0)` の最新106子境界は LOSS 40 / WIN 0 / UNKNOWN 66、
二石root `{60,27}` の既知クラスcoverは117/119で残りは`{100,108}`である。
境界値は [20 S5 LOSS更新の監査](../n11-reply27-20more-20261011/README.md) にある。
20件はsolver-trustedのexact結果であり、本experimentへ証拠として取り込んでいない。

## 統合・最適化方法

`scripts/integrate.py` は各局面maskを主キーとして候補表へ入れ、全合法手を要する
節点の全辺と、存在証人を選ぶ節点の候補辺を区別する。候補証人は入力DAG内に
既にある閉じた同極性の子に限定する。入力二組に同じmaskがあれば一つへinternし、
根を追加する順で証明閉包の限界追加量を測る。S5 root間で既に到達可能な大きな
証人閉包がある場合、それを優先する。

比較対象は順に、入力順union、既知の3根K0377 witness switchを固定して根を追加する
増分greedy、共有後の到達unionを評価する局所改善、候補数上限付きの厳密root-level
列挙である。厳密列挙の保証範囲はrootの証人選択だけで、下位節点の証人選択全体や
全合法証明の大域最小ではない。

## 測定結果

3根のstage 1はK0377を再現した。証明書SHA-256は
`478fc29e51ffd7e18158f74f0032b7e7756446e11c5d0819b000e19e79474fc2`、
1,718,259節点 / 2,547,576辺 / 16,080,927 bytesで一致した。これは既知のS6 witness
move 11を、別rootが既に使うmove 46へ変える既存の26.5%節点縮約を再現する。

6根への増分統合では、二入力の節点総数とintern後の候補局面数が共に3,340,258で、
入力間の重複局面は0だった。K0377の3根最適variantを維持して三根を追加した結果、
全体は2,720,770節点 / 4,065,013辺 / 25,446,729 bytesとなった。増分前の入力順
unionからは619,488節点減るが、この差は3根K0377の既知witness switchに由来する。
二つのS4群の間では局面共有がなく、6根化そのものによる追加の節点・辺削減は0。

二つの出力 (`six-root-incremental` と `six-root-joint-optimized`) は同じSHA-256と
同じ内容だった。既存unionに含まれるroot子の候補を再調査しても、新しい証人候補は
0件だった。greedyは各追加根の限界閉包を測定し、局所改善は1個の可変rootを調べたが
変更なし。厳密列挙は2通りを評価し同じ選択を最適とした。従ってこの入力群では、
共同最適化によるK0377以外の追加縮約は観測されない。10根への拡張に使える、既存の
独立終局閉包済みS5 rootは入力にないため、10根計測は行わない。

6根の二variantはバイト単位で同一なので一つを既存独立検証器へ一度通す。測定後の
最大RSS、wall time、temporary scratch、全6根のLOSS、terminal count、trusted leaf数は
[`output/integration-audit.json`](output/integration-audit.json) に記録する。検証前の
局面数やbyte数だけを独立証明完了とは扱わない。検証費用の増加率は、同日・同一
Windows環境と同じ250ms process-tree/RSS samplerで測ったK0377三根compact結果とも
比較する。統合処理そのもののwall time、process-tree peak RSS、出力・一時DBを含む
peak storageも `benchmark_integration.py` が別に記録する。

| 検証対象 | 根 | 節点 / 辺 | compact bytes | wall time | peak RSS | peak scratch |
|---|---:|---:|---:|---:|---:|---:|
| K0377 witness-switch baseline | 3 | 1,718,259 / 2,547,576 | 16,080,927 | 1,366.687 s | 193,683,456 B | 454,351,644 B |
| 増分統合・共同最適化 | 6 | 2,720,770 / 4,065,013 | 25,446,729 | 1,793.031 s | 200,245,248 B | 731,814,768 B |

3根から6根に増やした際、検証節点は58.345%、辺は59.564%、compact bytesは
58.242%、wall timeは31.195%、peak RSSは3.388%、peak scratchは61.068%増えた。
統合処理全体は707.328秒、peak process-tree RSS 553,791,488 B、出力と一時DBを
含むpeak storageは1,489,753,019 Bだった。current S4側3根の入力処理は112.481秒、
その3根最適化は100.328秒、追加S4証明のインポートは42.887秒、6根段階全体は
438.025秒。JSON gzip入力2本（計102,378,970 B）とcompact出力のbyte数は形式も
witness選択も異なるため、容量率だけを圧縮効果として切り分けない。

## 再現手順

以下の出力先は新規ディレクトリで実行する。`.local/n11-proof-dag-incremental-20261011/`
はGit ignore対象であり、大容量証明書は通常のGit履歴へ入れない。

```powershell
uv run --locked python research/experiments/n11-proof-dag-incremental-20261011/scripts/benchmark_integration.py `
  --output-dir .local/n11-proof-dag-incremental-20261011/run-replay
uv run --locked python -m unittest discover -s research/experiments/n11-proof-dag-incremental-20261011/tests -v
uv run --locked python research/experiments/n11-proof-compact-20261011/scripts/benchmark_verifier.py `
  --format compact `
  --certificate .local/n11-proof-dag-incremental-20261011/run-replay/artifacts/six-root-joint-optimized.kpd.gz `
  --out-dir .local/n11-proof-dag-incremental-20261011/verify-replay
uv run --locked python research/experiments/n11-proof-dag-incremental-20261011/scripts/build_audit.py `
  --plan .local/n11-proof-dag-incremental-20261011/run-replay/integration-plan.json `
  --benchmark .local/n11-proof-dag-incremental-20261011/verify-replay/benchmark.json `
  --three-root .local/n11-proof-dag-incremental-20261011/run-replay/artifacts/three-root-start.kpd.gz `
  --incremental .local/n11-proof-dag-incremental-20261011/run-replay/artifacts/six-root-incremental.kpd.gz `
  --optimized .local/n11-proof-dag-incremental-20261011/run-replay/artifacts/six-root-joint-optimized.kpd.gz `
  --optimizer-benchmark .local/n11-proof-dag-incremental-20261011/run-replay/benchmark.json `
  --output .local/n11-proof-dag-incremental-20261011/integration-audit-replay.json
```

`build_audit.py` は検証receiptが6根全てのLOSS、terminal-only、trusted leaf 0を示し、
証明書hashが統合計画・両variantと一致した場合にのみ監査JSONを出す。現行mainに
固定した小さな集計だけをGitへ記録する。大きい証明書の公開時はcompact-format version、
source JSON SHA-256、compact SHA-256、receiptを同時に配布する。

## 限界

この計算は6つの既知S5根の証明をまとめただけで、親S4の全106子や二石rootの119手を
閉じていない。別群の証明DAGに同じcanonical局面が現れず、追加で使える既存閉包内の
root証人も無かったため、全体最適化の改善は得られなかった。証明節点の全体最小性、
別root集合での増加率、10 root以上の費用、`{60,27}` の独立勝敗は未確定である。
現在のS4境界とK0372の隔離状態は変更していない。
