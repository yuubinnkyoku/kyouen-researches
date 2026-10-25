# 2026-10-25：11×11四石LOSS証明書のD4同値な五石子列挙を共通化

開始時main: `98da192c2b11e24994b6dedd2be4dc77a740f891`。AGENTS.md、knowledge README、K0023・K0329・K0414、11×11のcoordinator・S4検証器・直近log・CIを確認した。空盤勝敗はUNKNOWN。K0414の二石root `{60,27}` の既存solver-trusted LOSSと、terminal-only独立証明の未完了を区別する。

## 観察と変更

従来の `dfpn_s4_manifest_verify.py` はLOSS classを検証する際、同じD4正準鍵に属する**全raw edge**について、合法五石子をそれぞれ列挙・正準化していた。しかし、同じD4 classの四石局面にはD4変換による全単射があり、合法な五石追加と正準化はこの変換で不変。したがって、**正準五石子集合は全raw edgeで完全一致**する。

この性質を利用し、LOSS classごとに最初のraw edgeだけから全五石子を再列挙するよう変更した。四石classの全raw edge、被覆頂点、完全子集合、S5 cacheの全子LOSS検査、矛盾検出は維持する。WIN証明の一証人検査は変更しない。

| 二石root | 四石raw edge | 四石D4 class | 全classをLOSS検証する場合の合法五石子列挙回数 |
|---|---:|---:|---|
| `{60,0}` | 6,894 | 3,396 | 6,894 → 3,396（50.74%減） |
| `{60,27}` | 6,871 | 3,384 | 6,871 → 3,384（50.75%減） |

この表は**全classをLOSSとして検証する仮想上限**の操作回数であり、実際のmanifestの構成や実行時間の計測ではない。索引構築とcache照合の負担は別に残る。

## 独立確認と回帰

別実装の整数4×4行列式とD4変換による局所検査で、上記二石rootそれぞれ最初の12 classについて全raw edgeの合法五石子集合を再生成した。**計24 class、不一致0**。rootごとの全raw edge・class数もそれぞれ6,894/3,396、6,871/3,384で一致した。

リポジトリの `test_dfpn_s4_manifest_verify_cache.py` に、両rootの各12個の複数raw edge classで子集合の完全一致を確認する回帰を追加した。既存の実盤面索引・実S5 cache入力を通すLOSS/WIN検証も維持する。

再現：

```sh
python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
```

独立局所検査は成功。リポジトリ内の追加回帰およびCIの完了は別途確認する。新しい勝敗証明・terminal-only二石root閉鎖は得ていない。**標準11×11空盤勝敗はUNKNOWN。**
