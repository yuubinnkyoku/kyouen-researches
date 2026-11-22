# 単一オーナー宣言: six-row (6,6) m=25 追い込み — 6×25 行欠損極大安全配置の存在判定ラッパー（2026-11-22 高速レーン）

- 宣言時刻: 2026-11-22T00:26Z
- 宣言時 HEAD: `30c1d67cbd61a3896338c44e9f471376eaa33f39`
- 実験 dir: `research/experiments/six-row-q6-m25-frontier-crunch-20261122/`
- セッション log: `research/log/2026-11-22-six-row-q6-m25-frontier-crunch-session-log.md`
- 前線: K1215 は 6×24 witness を出版し M_{6,6}∈[25,495]、6×25 をfrontierとした。本レーンは 6×25 の追い込みのみを扱う。

## 位置づけ

K1215 で 6×24 class{1}/{2} の SAT witness を出版した直後のfrontier追い込み。6×25 は
{1}/{2} の plain 250s INDET（1,222,228/1,207,894 conflicts）・krow固定 k=4 の 260s INDET
（1,126,385/1,294,221）のみで、残り33正準クラスは未走査。本レーンは K1215 と同一の機材
（sat3.js 出版正本pin・kissat 4.0.4 sha256 `21da5d98…`）で以下を順次実行し、6×25 の
hardness map を広げる。

## スコープ（fail-closed）

1. 対象は 6×25 q=6 標準ルール盤のみ。正準行鏡映欠損クラス 35 個（63 非空部分集合の鏡映簡約代表）のうち
   未走査の 33 クラスを `sat3.js --class=D` で走査（cap は各 260s まで・INDET は誠実記録）。
2. {1}/{2} の難クラスは既存の krow 固定（k=4・INDET）に加え k∈{0..3} への分解、
   必要時 minpos split（p ≤ floor((25−1)/2)=12・H 鏡映 sound split）・`--lex=H` 交差符号化。
3. 主張の形式:
   - いずれかのクラス SAT ⇒ witness decode → sat.js verifyConfig + Python Fraction 2系統検証・
     tamper 対照・D4+並進での K1215 6×24 witness との非合同判定 → M_{6,6} 下界 25→26。
   - 全 35 クラス UNSAT（分解込み・INDET 残らず）⇒ 6×25 は行欠損 witness-free で M_{6,6}=25 確定
     （K0821-audit 規約・上界 U=495 は不変）。この判定は有限機械検証の範囲。
   - それ以外（一部 INDET 残存）⇒ hardness map の改訂のみで終了。不在主張はしない。
4. 機材再使用の較正: 実行開始時に census アンカー再現 + 陽性対照（6×24 class{1} SAT・出版 K1215 records
   と bit-exact）+ 陰性対照（2×9 q=4 class{0} UNSAT 517）を最初に回す。較正落ちの場合は本レーン中止。
5. conflicts 数・nodes 数を勝敗として読まない。標準 11×11 空盤・二石 root・S2・class 1/2/4 は
   非接触で UNKNOWN のまま。
