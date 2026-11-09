# 保存した形状証明のupstream監査とcore抽出

長い112形状の証明をSATで再生成せず、独立の実装で監査し、再生しやすい証拠へ縮める実験。
現在の数学的結論は [K0711](../../knowledge/items/K0711-p2647-safe-lower-bound-1292.md) を参照する。

使用する [DRAT-trim](https://github.com/marijnheule/drat-trim) はcommit
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985` に固定した。
`vendor/` にdrat-trim.c、lrat-check.cとMIT licenseの原文を保存し、
`provenance.json` に出典・commit・Windows checkoutのSHA-256と元Git blobのSHA-256を置いた。
checkout時のCRLF化をLFへ戻すと、元Git blobとbyte一致することも確認した。
コンパイルしたCRLF版のbyteをそのまま保持し、ソース本文は変更していない。
Windowsではgetc_unlockedが使えなかったため、ソースは変更せず
`-Dgetc_unlocked=getc` をコンパイル時に指定した。

`controls.py` はK0707の充足可能な4入力に対する偽UNSAT証明を拒否し、
小さいresolution反駁を受理することを検査する。一般健全性の証明とは区別する。

`audit.py` は修正後の形状入力とのbyte一致を確認し、原証明のhashを調べてから、
`-U`（RUPのみ）で後ろ向きの監査を行う。core DRATとLRATも同時に抽出する。
両coreはgzipで保存し、rawのhash・サイズ・行数をreceiptへ記録する。
原証明は前実験のローカル107MB gzipを保持し、過去の未完了receiptも書き換えない。

`replay_core.py` は保存されたcoreを元CNFへ結び付けて、別々の2実装で検査する。
DRAT coreは前実験のRAT禁止・削除無視のRUP検査器で、LRAT coreは
明示的hintを使う局所修正版lrat-checkで検査する。これにより、coreを採用できた場合は
元の大きな証明なしで、抽出されたcoreだけを再生できる。
幾何の符号化は別experimentの全節schema検査と整数幾何検査を前提とする。

```sh
uv run --locked python research/experiments/parabola-drat-trim-20261109/controls.py --output FRESH-controls.json
uv run --locked --with python-sat==1.9.dev21 python research/experiments/parabola-drat-trim-20261109/audit.py --shape 112 --timeout 600 --output FRESH-directory
uv run --locked python research/experiments/parabola-drat-trim-20261109/replay_core.py --shape 112 --output FRESH-core-replay.json
```

auditの再実行には原証明が必要だが、core再生には保存されたcoreと元CNFだけを使う。
既存出力の上書きは拒否する。今回のcoreも大きいためローカルに保持し、Gitからは除外する。
別checkoutではmanifest通りのcoreを復元する必要がある。Gitだけで再生できるとは主張しない。

## LRAT検査器の偽受理

原版lrat-check.cは、SATである `input/sat-unit.cnf` に対する
`input/false-empty.lrat` の偽空節を受理した。原因と現在の知識は
[K0714](../../knowledge/items/K0714-lrat-empty-clause-vacuous-rat-unsoundness.md) を参照する。
原文を保持し、局所コピーの `lrat-check-empty-fixed.c` で、RUP矛盾のない空節が
vacuous RATとして成功する経路を拒否した。原版の受理を証拠として採用しない。

```sh
uv run --locked python research/experiments/parabola-drat-trim-20261109/lrat_controls.py --output FRESH-lrat-controls.json
```

5制御例で原版・局所修正を比較し、原版の偽受理と局所修正での拒否を再現した。
コンパイラ・parser・残る経路を含む実装全体の形式証明を主張しない。
