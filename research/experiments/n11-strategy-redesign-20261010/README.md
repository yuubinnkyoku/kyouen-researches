# reply27 strategy redesign: 2026-10-10 checkpoint

開始mainは `52239697a6a65b11889669725f8599604d53656f`。この文書は実験当時の一次記録であり、現在の結論の正本は K0355 / K0371。A・Bの比較後、正しい極性に基づく直接S6増額、reverse propagation、共有S5 probeを実行した。root LOSS certificateは未完成で、`{60,27}` と11×11 emptyはUNKNOWNを維持した。

## 極性と撤回

命題は全層で「元の先手が勝つ」。偶数石ORは `WIN iff ∃ WIN child` / `LOSS iff ∀ LOSS child`、奇数石ANDは `WIN iff ∀ WIN child` / `LOSS iff ∃ LOSS child`。空の子集合もこの式に従う。終局の手番側敗北を基底に、増加する石数で逆向きに帰納すれば健全性が得られる。D4はゲーム規則と合法遷移を保つのでcanonical子への商も健全。UNKNOWNは確定証人または完全全子条件がない限り残す。

旧S7 helper群には `S7 LOSS -> S6 WIN` の不正な反転があった。その経路だけによるS5 WIN `(1152925911243358208,536870912)` と `(10448351135499552768,128)` を隔離した。直接S5 rawは両方15M UNKNOWNで、支持する別のexact replayは見つからなかった。局面のWINを反証したのではなく根拠撤回である。過去cache/raw/logは改変していない。`results/n11-s5-evidence-quarantine.json` と主要cache loaderの隔離規則で旧unionからの再流入を防ぐ。

## A・B・Cの比較

AMD Ryzen 7 5800HS、8 cores / 16 threads、Windows。変更していないC++ exact solverをg++ 15.2.0 / O3でコンパイルした。比較pilotはfresh process / memo22 / count order / 1 worker / 2M nodes、各4件。後続増額も同じbinary/order/memoで、次classのpilot/completionのみ4 workers。秒数は各process elapsedの合計で、並列batchの経過時間ではない。

| 指標 | A: 現classのS7境界 | B: 他classのS5 | C: 極性を使ったhybrid |
|---|---|---|---|
| 開始時未確定 | 2 S5、6 S6、512 S7 | 全115候補中44 WIN除外、71 UNKNOWN。最初の候補98 S5 | 6 S6の上限15M増額、共有8 S5、次classの8+91 S5 |
| 同条件pilot nodes | 290,045、4/4 S7 LOSS | 7,289,601、1 LOSS / 3 UNKNOWN | pilot後の適応方針なので同条件比較値はない |
| 実行nodes | 上記290,045 | 最初のclass 14,831,422。次class 89,225,167 | S6 20,056,308、共有S5 44,544,197 |
| pilot process秒 | 4.845 | 41.035 | S6合計55.608、共有S5合計172.485 |
| 追加計算量の扱い | 既存S6境界をLOSSへ閉じる最小二親S7 unionは175。ただし実際にS4 WINが判明し、このclassからLOSSは得られない | 最初534.94M、次545.22M nodesは15M打切り平均の加算proxy。両classはWINで棄却。完了上界ではない | S4反証に必要だったS6は実際には1件・2,214,318 nodes。他のS6からLOSS再利用も得た |
| 再利用 | 104 S5 LOSS、140 S6 WIN、exact S7は0 | 最初9 S5 LOSS、saved exact S6交差16/5,079、派生S5は0 | 保存済み50 S6 WINでS5 WINの完全境界を閉じ、1 S6 LOSSから5新S5 LOSS |
| 共有 | 521 S7 incidences / 512 keys、共有は9キー（各2親） | 最初S6は9,412 incidences / 5,079 keys。S5共有probeの最後2件は各2 classに関連 | 上位境界をDAGとして集約。fresh replay間のnative TT共有は使っていない |
| メモリ | pilot peak約165.25 MiB/process | 同程度 | 全実行の観測max約165.34 MiB/process。4 workersは約662 MiBのsolver合計見積り、全将来入力への上界ではない |
| 早期停止 | 一つのS5 WINでclass棄却 | 最初7件、次79件を未dispatchで停止。active workはdrain | 一つの未確定S6を閉じるだけで第二S5 WINが成立する極性・境界を優先すべき |
| LOSS完了条件 | 全106 S5 LOSS。現在WIN子があるため不可 | 選んだclassの全canonical S5 LOSS。今回選んだ二classは不可 | correct exact leaves＋完全AND/OR境界、LOSS証人のreverse reuse、最新coverage再計算 |
| 独立検証 | geometry＋完全境界。再帰的exact葉はsolver信頼 | 同左 | 新43 raw rowsと完全上位境界を別determinant/D4実装で監査。全探索木の独立certificateではない |

全実行は168,947,139 nodes。固定dispatch node capはpilot16M、S6増額90M、最初のB増額120M、共有probe120M、次pilot120M、次completion1,365M。これらはdispatch上限であり証明完了の上界ではない。各targetには180秒watchdogもある。watchdog中断・UNKNOWN・未dispatchをcache verdictにしない。

### Aの選択を再評価した理由

4 S7 WIN証人が全6 S6をWINにすればS5をWINへ導く。S4 LOSSの証明とは逆向きである。全6親を棄却する必要もなく、S4のWINには一つのS5 WINで十分だった。第二S5の完全51 S6子では50件が既知WIN、UNKNOWNは1件だけであり、その直接S6 WINが2,214,318 nodesで解決した。

条件付き4証人 / 245 S8 / 122 S9 / 3,734 S10遷移はexact判定ではない。選ばれた4 S7は今回すべてLOSSだったため、その選択をWINにする下位境界は実現しない。S7 AND WINには全S8 WIN、S8 OR WINには一つのS9 WINが必要である。一方S6 LOSSには全S7 LOSSが必要。単に小さいcoverや合法手数を最適化しても目的の極性やexact costは最適化されない。

個数を4へ固定することを止めれば、class棄却の上位境界は一つの未確定S6への直接探索で足りた。S4 LOSS方向の175 S7という最小値は、開始cacheの6 UNKNOWNを正しい全子条件で閉じる二親選択についての有限列挙値であり、任意の証明アルゴリズムの無条件下界ではない。S8の共有率は高くても、exact葉のコスト・極性を確認しない分解は採用しない。

solverは任意のS7を `--exact-replay --only=7` で処理できる。旧runnerの境界固定が制約だった。新しい汎用runnerで十分だったため、専用workflowは追加していない。既存native shared-TT機能は今後比較できるが、今回は正しさ未確認の枝刈りやsolver性能変更を導入していない。

### Bと選択モデル

完全S4/S5境界は独立integer-circle geometryで全6,871 raw edgesの代表不変性も確認して再構成した。115候補を全列挙し既知WINを除外。保存済みS6の全子/存在条件から候補71件への新規S5導出はなかった。raw historyのdeduplicated 15M S5は2,629キー。legal 70台の観測WINは13/79、80台55/765、90台5/1,241。これらは選択バイアスと打切りを含み、未知classの校正された確率ではない。

加算UNKNOWN数だけでなく、legal帯の打切りnode平均によるcompletion proxyと、WIN棄却の記述的頻度/コストによる情報獲得probeを分けた。共有8 S5の結果は4 WIN / 4 LOSS。しかし次classのpilotは8/8 LOSSだった後、completionでWINが出た。LOSS標本だけからclass LOSSへ昇格できない具体例である。

旧誤伝播を除外したbaselineはWIN 149 / LOSS 5,549、S4 LOSS31 / WIN260 / UNKNOWN3093。実行後の実験checkpointはexact S5 5,734（WIN156 / LOSS5578 / UNKNOWN excluded / conflict0）、S4 LOSS31 / WIN268 / UNKNOWN3085、secured117/119、remaining `{100,108}`、minimum additional classes1 = rational dual1。

direct S5 exactは30件（6 WIN / 24 LOSS）、S6 exact6件（5 WIN / 1 LOSS）、S7 exact4件（全LOSS）。加えてS6の正しい伝播から6新S5（1 WIN / 5 LOSS）。新cacheは旧5,700から根拠不十分2行を除外して36行を追加した。S5 UNKNOWN raw3件はcacheに含めない。今回のA six-S6境界は全解決したが、旧二つのS5境界等のUNKNOWNは残る。

最後のrankは `(1297036692683751424,16)`、108 S5中LOSS9 / UNKNOWN99、coverage `{26,28,100,108}`。約549.79M nodesのcapped proxyであり証明上界ではない。`next-boundary.json` は未dispatchのschedule。再開前にorigin/main、隔離registry、全raw/saved S6/S7交差を更新監査する。

## 再現・信頼境界

`compile-manifest.json`、各 `*-plan.json`、各runの `summary.json` とinput/output/logを保存した。過去rawをhash監査し、証明で再利用したrawは `reused-raw/` へbyte-identical copyした。独立監査は一般4×4 determinantからの行操作と、solverとは別に実装したD4を使う。`geometry.json.gz` は全3,384 S4の完全子境界。`upper-boundary-certificate.json` はS5/S6の上位certificateで、solver exact葉をopaqueに扱う。

`audit.py` はsource hashes、rawのtarget/budget/verdict、全canonical境界、reverse incidence、exact-only merge、全119第三手coverageを検査する。最小class数1は、残る頂点へのdual重み1と、それらを両方覆うUNKNOWN classの存在で厳密に確認した。UNKNOWN classの選択は勝敗証明ではない。再帰的minimax葉の独立検証コストは未測定で、node数からcertificateサイズを推測していない。

読み取りによる再監査:

```powershell
uv run --locked python research/experiments/n11-strategy-redesign-20261010/scripts/audit.py
uv run --locked python research/experiments/n11-strategy-redesign-20261010/scripts/report.py
uv run --locked python research/experiments/n11-strategy-redesign-20261010/scripts/verify_certificate.py
```

`study.py` とschedule生成を既存の凍結入力へ再実行しない。新しい探索は別plan/outputを作り、既存exactおよび同以上budget UNKNOWNを除外する。Python本体のlogic/geometry regression5件は既存SciPy optimizer環境、boundary regressions58件とfrontier recovery6件はroot uv環境で実施した。同じcompiled solverの既知空盤回帰はn4 LOSS（154 exact nodes）・n5 WIN（4,586 exact nodes）。knowledgeの必須checksと最終artifact hash検査は統合時に実施する。
