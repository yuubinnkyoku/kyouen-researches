# blocker類1の条件付き閉鎖

三石位置 `{59,60,61}` から手5または115で得られる四石位置は、K0675スイープと公開証明書の既存監査記録を前提に、いずれも先手WIN。手5には71、手115には49と応じると、どちらも五石位置 `00000000000000803082000000000000` の対称像になる。

その五石位置の合法手80個は、盤の対称性により40個の六石軌道に分かれる。`audit_class1_closure.py` は全てを列挙し、既存スイープによる先手WIN 2軌道、既存WIN7監査記録からの先手WIN 25軌道、新規WIN7証明書による先手WIN 13軌道に分ける。五石位置では第二手が指すため、全六石子が先手WINならこの五石位置も先手WIN。各四石位置では先手がこの五石位置へ動けるので、四石位置も先手WIN。

新規七石局面の証明書は先手WIN13件・先手LOSS2件。`scripts/verify_priority_certificates.py` は同梱された圧縮証明書を展開し、別実装の4×4整数行列式による合法性と終局までの戦略木を検証する。検査結果と元データのSHA-256は `output/priority-certificates-verified.json`、六石軌道と対応証人は `output/class1-s6-proof.csv` を参照。

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_priority_certificates.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_class1_closure.py
```

既存スイープと既存WIN7監査記録の証明書本体の一部は別保管で、今回それらを再検証していない。したがって本結論はそれら公開監査記録を前提とする。blocker類2・4、二石rootおよび空盤の勝敗は未確定。
