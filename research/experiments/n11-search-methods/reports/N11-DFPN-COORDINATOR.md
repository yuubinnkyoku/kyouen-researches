> **実験一次資料**：本文の判定・数値・計画は記録時点のものです。現在の結論・未解決・検証境界の唯一の正本は[knowledge](../../../knowledge/README.md)です。この資料を現在知識の正本として並行更新しません。

# adaptive coordinator: 最初の class 証明

**11x11: UNKNOWN**

- base commit: `1da3db9`
- script: `dfpn_coord_pilot.sh`
- 対象: first=60, r2=0

## coordinator の構造

LOSS=cost 0 / UNKNOWN=cost 1 / WIN=禁止 として、
每次 verdict ごとに optimistic cover を解き直す。
**cover に含まれる UNKNOWN だけを worker に渡す**ので、
3395 個全部を触る必要がない。

## 実測（pilot, 1 class）

```
# COVER optimistic=35 in_cover=119 secured=4/119 min_additional=34
coord,481,6,4,LOSS,419287160,2316875,win=0 loss=424 unk=0
# COVER optimistic=35 in_cover=119 secured=10/119 min_additional=33 worked=1
```

| 指標 | 値 |
|---|---:|
| 対象 class | 481 |
| coverage size | 6 |
| 着手前の unknown s5 | 4 |
| verdict | **LOSS** |
| s5 children | 424 個すべて LOSS |
| exact nodes | 419,287,160 |
| wall | 2,316,875 ms（約 39 分）|

**secured が 4 → 10 に増え、min_additional が 34 → 33 に減った。**
つまり 1 個の class 証明で 6 頂点のうち 2 頂点が新たに確定し、
残りの class 必要数が 1 減った。progress metric が正しく動いている。

## 重要な観察: unknown s5 の数と coverage の関係

この class は **coverage 6 なのに unknown s5 は 4 個しかなかった**。
残りの 4 個だけが未決であり、だから 39 分で完了した。

この class の 424 個のうち **既に 420 個が cache で LOSS 決まっていた**。
これが coordinator の「少ない unknown s5 を優先」則が効く状況であり、
**coverage 6 優先」だけでは無駄な仕事が多い**ことを示唆する。

ただし 1 class だけなので一般化はできない。
**5〜10 class の pilot で rule を決める**必要がある。

## 実測時間から分かること

1 class の証明に 39 分かかった。OPT が 31 なので全部で
**31 x 39 分 で約 20 時間**の換算になる。
これは「20 返信すべてを 31 class で埋める」場合の
**1 返信あたりの所要時間の目安**である。

**20 返信すべては 400 時間超**になるので、
並列化（worker ごとの cache 分離）が必須である。

## soundness

- ASan + UBSan で 1 class 完走を確認、**エラー 0**
- hybrid 回帰: n=4 LOSS / n=5 WIN / n=6 WIN / n=7 LOSS（不変）
- adaptive 回帰: 全条件 pass

**注意**: 「in_cover=119」は optimistic cover が全頂点を含むという意味で、
**secured=10/119 が真の確定状況**である。
optimistic cover を refutation と誤読しないよう、
secured を別 column として報告している。

## 現状

- LOSS class **2 個**（1 個は前回、1 個は今回 class 481）
- secured **10 / 119**
- 二石 root は 1 個も閉じていない

**11x11: UNKNOWN**
