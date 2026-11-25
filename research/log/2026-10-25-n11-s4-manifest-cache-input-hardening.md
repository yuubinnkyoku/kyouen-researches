# 2026-10-25：S4証明書検証器のS5入力をfail-closed化

作業開始時のmainは `e5eb877cc465499cf6db590cdcb2370e81ddbec1`。
`AGENTS.md`、`research/knowledge/README.md`、K0023/K0329/K0426、
11×11終局被覆の直近実験・研究記録と、S5共有merge・S4証明書検証器を確認した。
標準11×11空盤の勝敗は **UNKNOWN**。

## 発見した証明境界の穴

`research/experiments/n11-search-methods/scripts/dfpn_s4_manifest_verify.py`
の旧 `load_s5_cache` は、同じ正準S5鍵についてWIN/LOSSが重複すると
**最後の行で無警告に上書き**した。また不正形式の行を黙って無視し、
鍵の正準性・5石安全性・隔離対象の検査を行っていなかった。
このため、入力が汚染されたときに、S4証明書の子の勝敗を独立検査する
という目的に対してfail-openになり得た。既存の特定の証明書が
誤っていたと示したものではない。

修正後は全入力行の形式・数値範囲・5石数・D4正準鍵・共円禁止条件を
独立に検査し、同一鍵の異なる確定勝敗を`CONFLICT`として拒否する。
UNKNOWNは証明に使用せず、現在の`results/n11-s5-evidence-quarantine.json`
でactiveな鍵は証明の根拠から除外する。隔離対象を必要とするS4証明書は
未証明として拒否される。

旧 `dfpn_s5_merge_test.sh` は `/mnt/d/...` の機種依存パスを使い、
入力鍵 `100,0` などが5石安全正準鍵でなかった。
「正常なmerge」が失敗しても最後まで実行され得たため、
この試験の`MERGE_GUARD_OK`は有効な回帰証拠になっていなかった。
既存の凍結cacheに実在する4個の安全正準鍵を使う試験へ置き換え、
正常merge・異極性衝突・UNKNOWN除外・既存出力の保護・
同時書込の和集合・不正幾何の拒否をそれぞれassertするようにした。

## 確認範囲と限界

新しいS5入力検査と同等の関数をローカルPythonで実行し、
正常重複・異極性重複・不正形式・UNKNOWN・隔離・
非正準鍵・禁止四点を含む鍵の7種類を確認した。
テスト用4鍵は整数幾何で5石安全・D4正準であることを別途確認した。
`test_dfpn_s4_manifest_verify_cache.py`を追加し、上記の検査を
repo内で再実行できるようにした。

ただし**repo内の新しいunittestとmergeの同時書込試験は
この実行環境で実行できていない**。CI・knowledge整合性検査の
完了も未確認。これは検証器の入力信頼境界の重要修正であり、
新しいS5/S4の勝敗証明や被覆増分ではない。
二石rootの新規閉鎖0、**標準11×11空盤UNKNOWN**。

再現コマンド（repo root）：

```sh
python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
bash research/experiments/n11-search-methods/scripts/dfpn_s5_merge_test.sh
```
