# `{60,27}` solver-trusted LOSSをterminal-only DAGへ置き換える依存調査（2026-10-12）

## 計算した依存関係

K0414の119第三手表が使う32個のS4 LOSS classについて、各S4の全canonical S5子を独立Boardで再生成した。依存edgeは3,297本、必要な異なるS5 LOSS rootは2,995件。全件が現行exact S5 cacheでLOSS、うちcacheの `nodes>0` は65件（合計388,074,801 nodes）、`nodes=0` は2,930件だった。`nodes=0` はその行が探索されなかったという証明ではなく、direct solver探索nodeがcache行に記録されていない意味である（派生・保存cacheの両方が含まれる）。

K0375とK0377の現S4配下三根はこの依存集合内にあり、K0378の6根終局閉包DAGから再利用できるのは該当する3根。残る2,992 rootはこのroot-set analysisでは終局閉包されていない。K0372の10,407-node S6 WIN terminal-only証明は検証器・方式の再利用資産だが、上記S5 LOSS rootそのものではない。

## 優先順位

巨大DAGを一括生成せず、次の低・中・高direct-node標本でproof captureの節点数、辺数、終局数、最大RSS、出力bytesを測る。これは未実施のpilot候補であり、node数からcertificate費用を線形外挿しない。

| role | S5 root (lo, hi) | legal moves | cache nodes |
|---|---:|---:|---:|
| low | `(1297036693220623360, 0)` | 98 | 2,225,177 |
| middle | `(1297036692687946752, 0)` | 104 | 5,645,288 |
| high | `(1152921504607896576, 553648128)` | 100 | 11,267,484 |

pilot後、`nodes=0`のcache LOSSから合法手数70・94・110の三層を一つずつ選び、captureと独立閉包の実測容量を比較する。cache verdictの由来が異なる可能性を保持し、全てを同一種類の再探索対象とはみなさない。共通terminal closureは各rootを単独検証してから統合する。

## 再現と限界

```powershell
uv run --locked python research/experiments/n11-reply27-terminal-proof-priority-20261012/scripts/analyze_proof_gap.py
```

`output/terminal-proof-priority.json` はroot key単位のK0375/K0378重複、cache値、node記録、優先標本、入力SHA-256を含む。solver探索やproof captureは起動しない。2,995のsolver-trusted exact/cache依存を終局only proofへ置き換える作業は未完了であり、今回の119/119 proofはterminal-only独立minimax証明ではない。
