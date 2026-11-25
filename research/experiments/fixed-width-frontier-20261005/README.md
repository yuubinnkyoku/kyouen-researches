# 五行q点版の安定化フロンティア

現在の結論はknowledgeを正本とする。この実験には厳密閾値の証明、有限CNFの
生成・DRAT監査、独立の円生成、下界証人、未完probeを保存する。

- [q8の証明](reports/q58-exact-threshold.md): M5,8=16。全510有限除外と一般末尾を接続。
- [q7の境界](reports/q57-bounds-and-encoding.md): 19≤M5,7≤200。厳密値は未解決。
- [scripts](scripts/): 定式化と独立検算。
- [output](output/): 境界CNF/DRAT、全有限検査manifest、具体blocker、probe。

再現コマンドと外部SATツールの固定versionは各reportに記載する。
repoの依存宣言とlockfileは変更しない。UNSATはDRAT検査の有無を区別し、
UNKNOWNを有限除外や安定化の根拠にしない。
