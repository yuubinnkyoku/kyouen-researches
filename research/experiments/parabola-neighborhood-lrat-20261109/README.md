# 有界交換の保存DRATをLRATへ変換して独立検査

前回の1303点要求のRUP-only監査は120秒でtimeoutした。
今回は同じ探索を再起動せず、Git管理された同じ入力とDRATを別の経路で検査した。
現在の知識は[K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md)を参照する。
旧experimentのsolver主張とtimeout receiptは変更しない。

対象はp=2647、原点と完全対d=1323を固定し、保存1302点から除去3点以下で1303点以上を求めたCNF。
36457変数・126721節、入力SHA-256は
`4848c54905cd9f97020fdded1168e4fd0b3324bbf44149851caeabd7a060c2e2`。
元DRATは325093行、SHA-256は `7803e9d948b49d60f51eb4ab7f92796e31f3670a4c1daa64aec9e7d5a8e2d149`。

`audit.py` は既存vendorのDRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` を使う。
出典・MIT license・checkout bytes・build flagsは既存provenanceへ照合する。
`-U` による検査は11.891秒でVERIFIEDとなり、LRATを抽出した。
coreには25007 lemmas、0 RAT lemmas、10914690 resolution stepsがある。
この変換器の判定とは別に、空節処理を修正した既存lrat-checkで元の全CNFに対し再生した。
43074行・80008871 bytesのLRATを6.201秒で受理（終了コード0、`c VERIFIED`）。
LRATのSHA-256は `af1214d3c8eb33246b19a56ace712c137df89d034c2b311d7e5626f967797cfe`。

採用したLRAT本体は `output/target1303-remove3/core.lrat` にローカル保持し、Git対象から除外した。
Git管理の `result.json` にraw hash・サイズ・行数・所在がある。
別checkoutでは、Git管理された元DRATと同じ固定ソースからLRATを再生成して再生できる。
LRAT本体がGitに同梱されるとは主張しない。変換と再生には新しいSAT探索が不要である。

`verify_saved.py` は元の凍結符号化から実入力をbyte再生成し、追加counterの変数領域が
点選択変数または先行予約上限32569より上であることを確認した。
元DRAT・採用LRAT・ソース・二つの受理receiptもhash照合した。
DRAT-trimの6制御と修正LRATの5制御も実行した。
K0707の4偽証明、直接偽空節、K0714のvacuous-RAT空節経路を拒否した。
原版LRATの偽受理も再現し、原版の判定を証拠に採用していない。

この結果はその有界近傍CNFの独立反駁検査である。
固定完全対・除去上限を外した1303点の不存在、全体の最大性、上界の改善、一般の局所最適性は主張しない。
符号化の再生成や有限制御は検証器の一般健全性の証明ではなく、Lean形式証明とも区別する。

rootのuv環境で、毎回新しい出力先を指定する:

```sh
uv run --locked python research/experiments/parabola-neighborhood-lrat-20261109/audit.py --saved research/experiments/parabola-bounded-exchange-20261109/output/target1303-remove3-budget100000 --output FRESH-audit --timeout 180
uv run --locked python research/experiments/parabola-drat-trim-20261109/controls.py --output FRESH-trim-controls.json
uv run --locked python research/experiments/parabola-drat-trim-20261109/lrat_controls.py --output FRESH-lrat-controls.json
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-neighborhood-lrat-20261109/verify_saved.py --output FRESH-saved-verification.json
```

最後の保存監査は今回の採用raw LRATの存在を要する。別checkoutでは最初の変換を行い、
新しい出力先のraw LRATを、既存manifestが指す採用場所へ復元してhashを照合する。
Git管理された既存のreceiptや出力ディレクトリは上書きしない。
