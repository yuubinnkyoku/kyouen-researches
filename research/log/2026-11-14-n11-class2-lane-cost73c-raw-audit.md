# 2026-11-14 n11 class2-lane cost-73c: raw sweep 独立監査

対象はS5 parent `00000000000000809082000000000000` のS6 child `00000000000000809082000000000080`。worklist part 2上のedge costは73、demand classはc1=2,c2=2,c4=0。

## raw data audit

raw batch 1..11を全件読み、各JSONL行を再集計した。

- batch構成: 1..10が各7候補、11が3候補。合計73候補。
- 各batchにpilot controlが1件、計11件。すべて `loss=false`、5,949 nodesで一致。
- 候補bitは73件すべて相異なり、保存されたin-flight claimのcandidate_bitsと完全一致。
- S6局面から全121点を独立列挙し、整数演算で4点共線・共円を検査した合法七石目集合とも完全一致（73件、欠落・余分0）。
- 73候補すべて `loss=false`、`capped=false`、`andclose=true`、terminal stone range [13,17]。
- 節点合計 **388,889,991** はsweep JSONと一致。
- heaviest 3候補 bit 120 / 32 / 67 は別プロセス再実行の節点数も完全一致。

## 結果と解釈

**73 REFUTED-D10、0 WIN7-D10、0 capped**。16番目のsterile child、cost-73帯では2番目。新しいWIN7証明書はなく、S6 worklist/frontierに変化はない。

ここでのREFUTED-D10は、各7石子局面から深さ10以内のWIN7が見つからなかったという意味だけであり、S6 childのLOSS証明でも、S5 parentの勝敗でもない。cost-73aは並行レーンの担当として触れていない。

この実験は探索記録の再現性を確認したもので、S2 `{59,60}`、二石root `{49,60}`、標準11×11空盤の勝敗は決めない。すべて引き続き **UNKNOWN**。
