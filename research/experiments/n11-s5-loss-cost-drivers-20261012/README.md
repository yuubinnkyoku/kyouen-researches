# S5 LOSS証明費用の分解

## 結論

K0375・K0378でterminal-onlyかつtrusted leaf 0として独立検証された6根から、保存済みのS6 LOSS証人と閉包サイズを抽出した。代表3根では、証明DAGから確定済みのS6 LOSS証人を知った状態での探索も、S5直接探索も、同一の完全探索部品でLOSSを再計算できた。

S5直探索のS6子ごとの増分節点を追加計測した結果、決定的S6 LOSSの前に調べた子は全てS6 WINだった。各根の探索費用は次のように分かれた。

| S5根 | 直探索合計 | 先行S6 WINの確認 | 決定的S6 LOSSの証明 | LOSS証明比率 |
|---|---:|---:|---:|---:|
| `9904729241291607129994559488` | 2,335,333 | 344,344（4子） | 1,990,988（5番目） | 85.3% |
| `10412322338480590849` | 5,416,337 | 2,679,846（5子） | 2,736,490（6番目） | 50.5% |
| `1297036692750861312` | 5,026,776 | 1,168,545（2子） | 3,858,230（3番目） | 76.8% |

したがって、S6証人を見つける費用も大きいが、この標本では少なくとも2根で、証人候補の全S7子を閉じてLOSSを示す費用がより大きい。legal-count降順・canonical key順・6候補の合法手数順位・S6間TT共有では、証人発見の節点削減を確認できなかった。既定の探索順は変更しない。

## 対象・独立証明の確認

最新main上のS4 `(1297036692683752448,0)` は106子中LOSS 40 / WIN 0 / UNKNOWN 66、未解決第三手は100・108。根状態は固定済み監査 `n11-reply27-20more-20261011/output/audit.json`、SHA-256 `87b155e3b18fa7f9456d8513b7edd5b43ced94872226943ee9c0ec31368c8e5e` から再確認した。未知S5は探索していない。

既存DAGから抽出した6根は以下の通り。DAG節点・辺は、証明の共有・圧縮後サイズであり、solver探索節点数ではない。`過去S5 raw` はK0380で参照された完了rawの節点数。

| S5分類 | canonical S5 | 選択S6 LOSS | S7子数 | S6閉包DAG 節点 / 辺 | 過去S5 raw節点 |
|---|---:|---:|---:|---:|---:|
| latest/legal94 | `1301540292311122944` | `10412392707224768513` | 67 | 792,830 / 1,178,931 | 3,454,253 |
| latest/legal92 | `1297036692750861312` | `1297036692750926848` | 73 | 925,426 / 1,368,642 | 5,026,776 |
| latest/legal84 | `10412322338480590849` | `10412322338480592897` | 66 | 666,475 / 1,004,605 | 5,416,337 |
| previous/third | `9903520315472555450773274624` | `9903520317778398459986968576` | 64 | 520,472 / 786,253 | 2,457,938 |
| previous/second | `9904729241291607129994559488` | `9904729241291607130128777216` | 67 | 482,036 / 731,181 | 2,335,333 |
| previous/first | `9903520317777835510033547264` | `9903520317778398459986968576` | 64 | 520,472 / 786,253 | 3,981,449 |

latest/legal84には別の保存済みS6 LOSS `10412392707224768513` もある（合法S7子67、DAG 792,830節点 / 1,178,931辺）。選択証人は合法S7子66で、DAGが126,355節点小さい。単独探索も2,691,081節点で、別証人の3,454,252節点より22.1%少なかった。latest/legal84とlatest/legal94の証人閉包には46,987節点の共有があり、previous/firstとprevious/thirdは同一S6証人閉包を共有する。異なるK0375 bundle間に同一canonical局面はなかった。

DAG抽出元のcurrent-S4証明は2,337,747節点 / 3,484,437辺、別bundleは1,002,511節点 / 1,517,437辺。各受領書でtrusted leaf 0を確認した。6根の統合監査はK0378を参照。証明DAGは既存のものだけを読み、書き換えやsolver結果の独立証明への昇格はしていない。

## 探索条件

- 事前固定した3根：previous/second（6根中最小の証人DAG）、latest/legal84（2証人を保存）、latest/legal92（current S4で最大の証人DAG）。
- 主要比較A・B・C1・C2は同一build、`g++ -O3 -std=c++20 -DNDEBUG`、盤11、memo power 22、`exact-order=count`、外部cacheなし。
- AはS5直接exact replayで各根6M節点まで。Bは保存済みS6 LOSSをそれぞれ独立rootとして6M節点まで。latest/legal84の2候補は別々に測定。
- C1/C2は合法S7子数昇順・canonical key順で先頭6 S6子を各1M節点まで。C1は候補ごとに空TT、C2は根内で初期空TTを共有。UNKNOWNでも費用を推定していない。
- 候補順序追試は保存済みS6 LOSS 4候補すべてにCOUNTD・KEY順を各6M節点まで適用し、COUNT順の完了値と比較した。
- 追加した `--exact-replay-profile` は既定OFF。層別呼出し/展開/TT countersに加え、プロファイル有効時に直近S5 rootの各S6子の増分節点数を記録する。4×4完全解析fixtureで旧binary・新binary既定・新binary profile-onの勝敗と節点数を照合した。

## 高予算のA/B結果

全て完全解決LOSS。時間はWindows上の単発測定であり、node countより強い性能主張には使わない。RSSは各プロセスの最大値。

| S5根 | A: 直接S5 nodes / 時間 / RSS | B: 保存済みS6 LOSS nodes / 時間 / RSS | 決定S6のDAG節点 |
|---|---:|---:|---:|
| previous/second | 2,335,333 / 7.66s / 172.8MB | 2,006,805 / 6.87s / 172.8MB | 482,036 |
| latest/legal84 選択 | 5,416,337 / 18.53s / 173.3MB | 2,691,081 / 9.68s / 172.8MB | 666,475 |
| latest/legal84 別候補 | 同左 | 3,454,252 / 12.23s / 172.8MB | 792,830 |
| latest/legal92 | 5,026,776 / 17.28s / 173.3MB | 3,837,541 / 12.98s / 173.3MB | 925,426 |

決定S6子をS5直探索内で測った増分は、同じbinaryを使った追試で1,990,988 / 2,736,490 / 3,858,230節点。独立rootにしたBの費用との差は、各根で約0.8% / 1.7% / 0.5%。S5直探索の費用を「先行WIN証明」と「決定LOSS証明」に分けた内訳は上表のとおりで、節点合計はroot自身1節点を含めて直探索総数に一致する。

層別では各S6 LOSS探索の約30–31%が14石層で展開された。大きい直接S5探索では4,194,304-entry TTが満杯になり、resolved evictionがlegal84で1,230,506、legal92で862,575、平均probeはそれぞれ約9.92・8.51だった。S6単独探索は大半のentryを表内に保持できた（legal92だけ105,240 resolved eviction、平均probe約4.00）。TT churnは高費用の一因だが、今回の内訳では決定S6の中層探索の方が支配的だった。

## 証人順位付けと順序追試

C1/C2は各18候補を調べ、いずれもLOSS 0 / WIN 12 / UNKNOWN 6。各根の節点はC1が1,838,012 / 3,404,066 / 4,730,087、C2が1,649,594 / 3,404,066 / 4,644,899。合計は9,972,165 / 9,698,559節点で、C2は2.75%少ないが各根6Mの上限以内で既知LOSS証人を解決しなかった。wallはC1 33.66s / C2 32.14s、最大RSSは約173.4MBだった。UNKNOWNに完了費用を割り当てない。

決定S6 4根に対するCOUNTD・KEY順は、同じv2 binaryで各順序24M節点、LOSS 0 / WIN 0 / UNKNOWN 4。COUNT順は対応する4根を2,006,805〜3,837,541節点で解決済み。したがって本標本では別順序は6Mまでに勝たず、節点削減を示していない。単発wallはCOUNTD 177.65s、KEY 175.91sで、上限到達後の打切り比較のため解決費用の比較には使えない。

## 解釈と限界

計測対象はsolverの `exact_prop` によるexact replay再帰探索で、`solve_root` のDFPN expansion counterではない。K0380と同じ探索部品・同じ再生方式を用いる。したがって、ここで特定した支配費用はこのexact replayに対するもので、11×11の未解決S5全般やDFPN本体への一般化はしていない。

既知のS6証人をroot指定するBは、未知S5に対する証人順位付けの改善を示さない。証人発見を未知局面で速くする手法は確認できず、現行S4のUNKNOWNには適用しなかった。数値の似たDAG閉包サイズと探索node countを同じ費用として扱わない。

## 再現

リポジトリrootから、まず現行profile binaryをbuildする。

```powershell
New-Item -ItemType Directory -Force .local/n11-s5-loss-cost-drivers-20261012 | Out-Null
g++ -O3 -std=c++20 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe
```

build manifestのsource/binary SHA-256と照合し、次を順に実行する。

```powershell
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/check_profile_regression.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/profile-regression-recheck
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/benchmark_cost_drivers.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --build research/experiments/n11-s5-loss-cost-drivers-20261012/input/child-profile-build.json --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/stage1-recheck
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/benchmark_direct_s5_children.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/direct-s5-child-profile-recheck
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/benchmark_known_s6_costs_v2.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/known-s6-costs-recheck
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/freeze_known_witness_order_schedule.py --benchmark research/experiments/n11-s5-loss-cost-drivers-20261012/output/stage1-recheck/summary.json --out research/experiments/n11-s5-loss-cost-drivers-20261012/input/known-witness-order-schedule-recheck.json
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/benchmark_known_witness_orders.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --schedule research/experiments/n11-s5-loss-cost-drivers-20261012/input/known-witness-order-schedule-recheck.json --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/known-witness-order-recheck
uv run --locked python research/experiments/n11-s5-loss-cost-drivers-20261012/scripts/audit_results.py --solver .local/n11-s5-loss-cost-drivers-20261012/dfpn-profile-child.exe --out research/experiments/n11-s5-loss-cost-drivers-20261012/output/audit-recheck.json
```

順序研究の事前登録comparison scheduleを読み、六候補の幾何順位を再計測したい場合は上記 `benchmark_cost_drivers.py` を実行する。profile回帰receiptを再実行する場合は、baseline executable `.local/n11-s5-loss-witness-20261012/dfpn.exe` が別途必要で、そのSHAは `input/build.json` に固定している。元のA/B/C1/C2・COUNTD/KEY試行のraw、schedule、各run SHA、境界の入力SHA、profile回帰receiptは `output/` と `input/` にある。`scripts/audit_results.py` はrun manifest、trusted-leaf数、A/B/C結果、子費用合計、順序比較、同一binaryを横断照合する。`output/final-sha256.json` はこの実験の各ファイルおよびsolver sourceのhash manifestであり、自身のSHAはmanifest外である。
