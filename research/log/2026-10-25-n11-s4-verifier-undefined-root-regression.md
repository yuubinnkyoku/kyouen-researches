# 2026-10-25：S4証明書の実行経路で未定義の二石root集合を修正

開始時main `53bf3f01914c0bb2b2ead2ecf4001389d376b903`。AGENTS.md、knowledge README、K0023/K0329/K0414/K0426/K0433、11×11の直近log、S4 manifest検証器・回帰・coordinator記録を確認。11×11空盤勝敗はUNKNOWN。

## 発見と修正

`research/experiments/n11-search-methods/scripts/dfpn_s4_manifest_verify.py` の `main()` は、S4 classのraw edgeを検証するループで `occ4 = base | {a, b}` としていた。しかし索引再利用を導入した後の `main()` に `base` の定義がなく、証明書に実在するclassがあれば `NameError` で停止する。入力構造だけを検査する既存回帰と索引単体の全辺比較は、この実行経路を通らないため見逃す。

二石rootを検査行から読み取った直後に `base = {first, r2}` を定義した。S4 classのD4索引・合法五石子集合・勝敗伝播の意味は変更しない。

## 回帰の拡充

`test_dfpn_s4_manifest_verify_cache.py` に、`main()` そのものを呼ぶ回帰を追加した。二石root `{60,0}` と安全な四石 `{60,0,1,2}` の合法五石子を整数幾何から列挙し、単一raw edgeの合成manifestを組み立てる。S4 class索引とS5 cacheの入力のみ差し替え、次の三条件を検査する。

- 全五石子がLOSSとして与えられた場合はS4 LOSSを受理する。
- 一つのWIN子が証人として与えられた場合はS4 WINを受理する。
- LOSS manifestの五石子を一つ欠落させた場合は拒否する。

これらのcacheラベルは**テスト用の合成入力**であり、実際の局面勝敗の新規証明ではない。合法手生成と証明書の実行経路を回帰する目的に限定する。

再現コマンド：

```sh
python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
```

変更をmainに直接反映した。今回の実行環境からGitHub Actionsの結果を取得できず、上記リポジトリ回帰の実行完了・全体CI成功は未確認。**新規二石rootの閉鎖なし、11×11空盤はUNKNOWN**。
