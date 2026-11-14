# blocker類2の条件付き閉鎖

三石位置 `{59,60,61}` から手27または93で得られる四石位置では、先手はそれぞれ手49または71により、五石位置 `00000000000000003802000008000000` の対称像へ移れる。

この五石位置の合法手82個は盤の対称性により41六石軌道に分かれる。`audit_closure.py` は全合法手を再生成し、41軌道それぞれについて、先手WINの七石子を公開監査記録と照合する。内訳は既存六石スイープ1軌道、旧WIN7監査記録4軌道、保存済み終局証明書4軌道、cost-60/61/61b/64/65/68 のWIN7証明書32軌道である。複数軌道が同じ証明書を共有する。41軌道の一覧と勝ち手は `s6-witnesses.csv` にある。

五石位置では第二手が指す。どの合法手の後も先手が勝てるため、この五石位置は先手WIN。四石位置では先手がこの五石位置に移れるため、blocker 27・93も先手WIN。判定は、列挙した公開WIN7証明書の監査記録、既存スイープ、および戦略証明書検証器の正しさを前提とする。照合器は必要な保存済み証明書のハッシュ・根の一致と、全軌道の幾何・合法手を検査するが、全戦略木を再走査しない。

使用したcost-68の証明書2件は、既存TS監査とは別にPythonの整数行列式検査器で全戦略木を再検証した。結果とハッシュは `key-certificates-audit.json` に収録する。

```sh
python research/experiments/n11-class2-blocker-closure-20261114/audit_closure.py
python research/experiments/n11-class2-blocker-closure-20261114/audit_closure.py --determinant
python research/experiments/n11-class2-blocker-closure-20261114/verify_key_certificates.py
```

これにより閉じるのは類2のみ。類4、二石root `{59,60}`、11×11空盤は未解決。
