# 2026-10-30：独立LOSS7→S6逆向き監査にS8終局証人の出自を結合

開始時main `05f20ff1527930709e16244866656cd886cc110c`。AGENTS.md、knowledge README、K0023/K0414/K0415/K0426/K0485/K0486/K0528、固定37個の8石終局証明、固定14個の7石伝播、6石逆向き監査と直近のlogを確認した。標準11×11空盤は **UNKNOWN**。

## 独立監査器の信頼境界

`audit_loss7_to_s6_frontier.py` は従来、固定済み `lift_result.json` のSHAと、13個の元先手LOSS7に関する局面・極性・逆向き辺を検査していた。しかし、**7石行に記載された8石証人が実際にLOSS8の終局証明を持つか**は、この独立監査器単体では検査していなかった。別の `audit_s7_polarity_and_s6_coverage.py` は既にこの条件を検査するが、逆向き監査器は固定された伝播結果への依存を残していた。

## 修正

- 37個の8石終局証明書をGit blob `48d691da7e272c61be02cd2c3d8fe0de7c3d7c6e` に固定して読み込む。8 WIN / 29 LOSS、局面の正準化・安全性・重複なしを独立の4×4整数行列式で確認する。
- 29個のLOSS8から石を1個ずつ除去して7石親を逆算し、固定14根の `knownLoss8Children` と各 `witness` が証明済みLOSS8に実際に接続しているかを検査する。29個のLOSS8に未使用の根があれば拒否する。
- 実際に合法で、しかしWIN8と証明済みの `00000000000000821080000001040120` を7石LOSS証人として差し込む負例を追加し、逆向き監査器自身が拒否するようにした。

これは**独立監査の出自保証の改善**であり、既存の7石勝敗が誤っていたという意味ではない。8石終局葉の再帰計算は既存の `verify.js --full` と `verify.py --negative` に委ねる。凍結2,232個の7石LOSS集合は歴史的な比較集合であり、今回全件の終局再計算を行っていない。6石局面の未被覆数は指定集合に対する値で、真のUNKNOWN数ではない。

変更はmainへ直接反映（`3f29345d925004e2c1178fda417eb38952ad7706`）。branch/PRは作らず。新たな6石・二石rootの閉鎖は0、空盤の勝敗は **UNKNOWN**。

## 再現

```sh
python3 research/experiments/n11-s8-fixed37-terminal-closure-20261030/audit_loss7_to_s6_frontier.py
```

CI：`n11-loss7-s6-frontier.yml` と `n11-s8-fixed37-terminal-closure.yml`。変更後の成功・失敗は実行結果を確認してから判定する。
