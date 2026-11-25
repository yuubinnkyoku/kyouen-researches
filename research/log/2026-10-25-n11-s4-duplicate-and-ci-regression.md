# 2026-10-25：S4証明書の重複主張を拒否し、S5共有統合試験を通常CIに組み込む

作業開始時mainは `afd8587f5a5f338dba95e0efa6f16c9b70d1baeb`。AGENTS.md、research/knowledge/README.md、K0023/K0105/K0329/K0355/K0415、11×11の直近logと、S4 manifest検証器・S5 merge・証拠隔離方針・回帰試験を確認した。空盤勝敗はUNKNOWN。

## 発見と修正

`dfpn_s4_manifest_verify.py` は同一の `(first,r2,key_lo,key_hi)` を二度書いた証明書を、勝敗が同じなら受理していた。子の列が異なる二つの行も個別に検査したうえで、`classes verified` を2と表示し得る。これは**証明された異なるclass数を水増しする**入力を許すもので、同じ行を二度書くことが新たな証明を生むわけではない。異なる二石rootが同じ四石D4鍵を参照することはあり得るので、重複判定は鍵単独ではなくrootとの組で行う。

`load_manifest` に重複検査を追加し、盤面全子列挙前に拒否する。回帰には「同一行の二重化」「同じroot・classで勝敗だけ変更」の拒否と、「rootの順序を変えた別の証明義務」の受理を追加した。既存の合法手・cache・終局勝敗判定は変更しない。

また、直近二回の修正で追加・改訂した `test_dfpn_s4_manifest_verify_cache.py` と `dfpn_s5_merge_test.sh` は、従来の通常CIでは実行されていなかった。`.github/workflows/ci.yml` に両方を実行する手順を追加した。これによりS5のWIN/LOSS矛盾拒否・UNKNOWN除外・並行writer和集合・S4の不正入力拒否が、以後の通常pushで検査対象になる。

## 再現・検証範囲

```sh
python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
bash research/experiments/n11-search-methods/scripts/dfpn_s5_merge_test.sh
```

この作業環境ではGitHub接続を介してmainに直接修正し、上記コマンドのローカル実行は行っていない。CIの完了と試験結果は別途確認が必要であり、コード追加だけをPASSと呼ばない。新たな局面の勝敗確定・二石rootの閉鎖は0。標準11×11空盤の勝敗は**UNKNOWN**。
