# 標準11×11・第9回の6石親に対する極性監査（2026-10-23）

標準q=4、完全指摘、通常プレイ。勝敗は**元の先手固定視点**。空盤は **UNKNOWN**。

第9回の6個の8石LOSSから44個の7石LOSSを逆向きに導く部分は妥当である。一方、44個の7石LOSSを一手戻した139個の6石親を `WIN` とするのは不正な伝播である。偶数石（6石）はOR節点なので、**WINには少なくとも一つの7石WIN子**、LOSSには**全合法7石子のLOSS**が必要。7石LOSS子が一つあるだけでは勝敗は決まらない。

旧資料 `n11-s8-round9-global78-20261020/verify_s7_s6.py` の `139 S6 WIN parents` という出力と、`round9_s6_win_parents.txt` のファイル名は**勝敗証明ではない**。歴史的入力は書き換えず、139件を「7石LOSS子を持つ6石親の候補集合」としてのみ扱う。既存の他の独立証明を否定するものではない。

独立整数幾何の検証器 `audit.py` は、6個の8石LOSS根→44個の7石LOSS親→139個の6石親の列挙を再計算し、固定先手のOR/AND集約の負例を検査する。旧2,232件の7石LOSSと17件の7石WINの凍結一覧を渡した場合、139件はこの**指定した証拠集合に限って**すべてUNKNOWNであることも検査する。終局葉の勝敗そのものは再計算しないため、別途第9回の終局証明を検証する必要がある。

```sh
python3 research/experiments/n11-round9-s6-polarity-audit-20261023/audit.py \
  --round9 research/experiments/n11-s8-round9-global78-20261020 \
  --old-loss research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_loss_2232.txt \
  --known-win research/experiments/n11-targeted-terminal-lift-20261015/data/all_s7_win_17.txt
```

K0371の既存極性訂正と同型の再発であり、この139件をWIN verdictとして共有cacheに取り込んではならない。7石LOSSの44件と8石LOSS根の証明はこの誤りによって撤回されない。
