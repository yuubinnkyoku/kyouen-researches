---
id: K0714
title: 固定したupstream LRAT検査器はRUP矛盾のない空節を受理し偽UNSATを返す
kind: proposition
status: computed
topics: [verification, certificates, provenance]
aliases: []
relations: []
artifacts:
- path: research/experiments/parabola-drat-trim-20261109/vendor/provenance.json
  role: data
  note: upstream commit、Git blobとWindows checkout双方のhash、改行変換の照合、コンパイル指定
- path: research/experiments/parabola-drat-trim-20261109/vendor/lrat-check.c
  role: source
  note: 指定commitの本文を保持するWindows CRLF checkout。LF正規化はGit blobとbyte一致
- path: research/experiments/parabola-drat-trim-20261109/input/sat-unit.cnf
  role: data
  note: 単位節1だけの充足可能なCNF
- path: research/experiments/parabola-drat-trim-20261109/input/false-empty.lrat
  role: data
  note: 節1のhintだけで空節を導いたとする1行の偽LRAT反駁
- path: research/experiments/parabola-drat-trim-20261109/lrat-check-empty-fixed.c
  role: verifier
  note: RUPが矛盾しなかった空節をRAT分岐へ渡さず拒否する局所修正版
- path: research/experiments/parabola-drat-trim-20261109/lrat_controls.py
  role: verifier
  note: 原文と局所修正をソースからビルドし正例・hint破損・偽空節を比較
- path: research/experiments/parabola-drat-trim-20261109/output/lrat-controls.json
  role: data
  note: 5制御例の原版・修正版の実測結果とsource/binary hash
- path: research/experiments/parabola-drat-trim-20261109/README.md
  role: source
  note: 証拠形式・原版不具合・局所修正と監査での扱い
scope: 指定commitのlrat-check.cをWindows GCC、-std=c99 -O2 -DLONGTYPE -Dgetc_unlocked=getcでビルドした具体的な偽受理。別のdrat-trim.cの誤判定や全LRAT検査器の問題を主張しない。
evidence: p cnf 1 1と節1の充足可能入力に対し、2 0 1 0の偽空節を原版が終了コード0・c VERIFIEDで受理。局所修正は拒否し、正しいresolution反駁を受理する。
---

## 反例

元CNFは `p cnf 1 1` と `1 0`。割当1=trueがモデルであり、UNSATではない。
偽LRAT列は `2 0 1 0` の1行だけで、空節に対するhintは元の単位節1のみ。
unit propagationは1=trueを導くだけで、矛盾しない。
ところが指定原版はこの列を受理し、終了コード0と `c VERIFIED` を返した。

## 原因と局所修正

checkClauseは空節でもlist[0]=0から擬似的なpivotを計算し、RUPが矛盾しなかった場合に
RATのない分岐へ進む。intro[pivot^1]=0により、補集合側に出現しないpivotだとして成功する。
しかし空節にはpivot literalがなく、vacuous RATとして追加することはできない。
空節は必ずRUPの矛盾を必要とする。

原文はvendorに保持し、局所修正版ではcheckRedundancyがCONFLICTだった場合だけ空節を受理する。
それ以外の空節はRAT関連処理へ入る前に拒否する。
5制御例で、修正版は正しいresolution反駁を受理し、hint欠落・誤った節・偽空節・空節なしを拒否した。
これは当該経路の修正と有限回帰であり、任意入力についての検査器全体の健全性証明ではない。

## 監査への影響

この原版LRAT検査器の受理だけを幾何命題の根拠には採用しない。
同じrepoのdrat-trim.cは別実装であり、この反例をそのまま同ファイルへ適用したものではない。
抽出された証明が正しいかどうかは、局所修正版とRAT禁止の別RUP検査によって個別に確認する。
ソルバのUNSAT主張やp=2647の幾何命題を反証したものではない。
