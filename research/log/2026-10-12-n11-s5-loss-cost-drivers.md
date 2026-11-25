# 2026-10-12 S5 LOSS証明費用の分解

## 問い

K0375/K0378で独立検証済みのS5 LOSSについて、S5直探索の費用のうち「S6 LOSS証人を見つける費用」と「候補S6をLOSSと証明する費用」を分離する。未知S5の計算はしない。

## 作業順

1. `main`先端のcurrent S4監査を確認。106子はLOSS 40 / WIN 0 / UNKNOWN 66、第三手100・108が未解決。探索プロセスはなく、計測対象も独立証明済み六根に限定した。
2. 六根のterminal-only証明DAG、検証receipt、K0375 raw hashを照合し、S5/S6 key、合法S7子数、閉包節点・辺、他root共有、過去S5 raw nodeを抽出した。六root統合監査でtrusted leaf 0。
3. 250kの小予算実験はK0380ですでに全UNKNOWNだった。過去完了raw 2.335M–5.416Mを参考に、対象を3根に固定し、S5/S6 root 6M、blind候補1Mずつ・6候補の共通比較を事前入力に記録した。
4. 同じprofile binary、fresh TT、memo power 22、count orderでS5直、保存済みS6証人単独、blind legal-count prefix、root内TT共有を順次実行。保存証人rootは全てLOSS、直S5 rootも3つ全てLOSS。
5. プロファイルを拡張し、S5直探索における各root child S6の増分node数・結果を計測。4×4完全解析fixtureでbase binary、profile off、profile onの勝敗・node一致とroot-child出力を回帰確認した。
6. profileを加えた同一v2 binaryでS5/S6再測定を行い、直探索内の決定S6 child deltaとS6単独root costの近似一致を確認した。legal-count降順とcanonical key順を同じv2 binaryで比較し、順序によるnode削減は確認しなかった。

## 発見

- 直探索で決定LOSSに至る前のS6子は、対象3根で4・5・2子。全てWIN判定まで完了し、費用は344,344・2,679,846・1,168,545 nodes。
- 決定S6 LOSS子に費やした増分は1,990,988・2,736,490・3,858,230 nodes。S5直探索総数の85.3%・50.5%・76.8%で、証人そのものの証明が大きい。
- 同じS6を空TTのrootとして再計測した費用は2,006,805・2,691,081・3,837,541 nodes。直探索内増分との差は0.8%・1.7%・0.5%。これはTT context差が小さいこの標本での観測であり、一般保証ではない。
- 1つのS5根には保存済みS6 LOSSが2つあり、より小さいDAG証人（666,475 vs. 792,830 nodes）も、単独探索が小さい証人（2,691,081 vs. 3,454,252 nodes）も一致した。節点削減22.1%は既知根の参考差で、未知S5に適用できる順位法ではない。
- blind ranked prefix C1/C2は各18行でLOSS 0、WIN 12、UNKNOWN 6。TT共有C2はC1より2.75%少ないnodeだったが、LOSS証人未解決のままで、 solve cost reductionとは扱わない。
- COUNTD/KEYの順序追試は各4証人に6M上限、両順序ともLOSS 0 / WIN 0 / UNKNOWN 4。COUNT基準では全4証人を最大3.84Mで解決していた。node削減がないため既定順を変えない。
- 14石層が各S6単独探索の約30–31% nodes。直接S5ではTT容量4,194,304 entryがlegal84/92で満杯となり、resolved evictionが約123万/86万。TT churnは存在するが、プロファイルの最深大負荷部分はS14前後の反復・分岐処理。

## 解釈の境界

計測したのはK0380と同じ `exact_prop` exact replay再帰展開であり、`solve_root` のDFPN expansion数ではない。DAG node数とも別単位である。全てのsolver runは測定に限り、勝敗の独立根拠は入力時点で既に検証済みのterminal-only DAGのまま。

unknown S5、定型探索担当が調べる局面、cache merge、S4再分類、第三手被覆の更新は行わなかった。改善が確認できなかったため、現行S4には適用せず探索順序も変更しない。次はS6決定証明内で高負荷となるS13–S15探索のTT pressureと共通子再利用を、既知閉包でさらに測るのが具体的な次候補。

再現方法、raw、hash、限定と数値表は`research/experiments/n11-s5-loss-cost-drivers-20261012/README.md`と`output/final-sha256.json`を参照。
