# 子局面再利用とexact/P/Nの併用回帰

速度ではなく、同じ設定のcache OFFと初回移譲ONで勝敗・探索量・予算・cache状態が一致するかを検査する。
新しい未知11×11探索は行わない。

## C++

既存の`cpp/tests/test_kyouen_frame_children.cpp`を拡張した。
全安全4×4局面の独立幾何・直接部分集合DPに加え、4局面、memo5/12、両tie順序、
exact publish全3方式、残余なし/SG6/PN6/PN16 cap8の192条件を比較する。
native exactは合法手8・予算8・retry2、cap8のroot quotaは23、それ以外は128。
同じsolverで7 work中断の後2,000 workへ上げて再開し、元手番の独立勝敗と全計数を照合する。
ON側はfresh-list監査も有効にする。

## Release CLI

`-O2 -DNDEBUG`のproduction binaryで以下を検査する。

- 3 publish × 4残余設定 × 3 work上限(0/7/2000) × 3根 × OFF/ON = 216評価。
- 各publish/残余/OFF・ONで、奇数石と偶数石の既知終盤をそれぞれ同根2回。計96根評価。
- ごく短いwall guardでOFF/ONともTIME_BUDGETとなる2評価。

- 既知11×11終盤の両石数parity各1根で、publish all/separate・残余なし/PN6・OFF/ONの16評価。

計258 process・330根評価。出力CSV全文、設定、ヘッダ、解析行は単一`records.json`へ保持する。
publish実設定はlogヘッダで確認し、勝敗、通常/native exact仕事量、P/N使用数・残量、
重複試行抑制、rootごとのreset、生成回数の置換を厳密に比較する。
時間差や深いrootの性能は推論しない。

```sh
g++ -std=c++20 -O2 -DNDEBUG cpp/solvers/kyouen_dfpn_root.cpp -o /tmp/dfpn-combined
python research/experiments/dfpn-combined-options-20261022/study.py freeze
# 固定protocolをcommit
python research/experiments/dfpn-combined-options-20261022/study.py run
python research/experiments/dfpn-combined-options-20261022/study.py verify
python -m unittest discover -s research/experiments/dfpn-combined-options-20261022 -p 'test_*.py'
```

記録を上書きしない。CIは記録の再検査とC++小盤回帰だけを行い、このRelease CLI matrix全体は再実行しない。
