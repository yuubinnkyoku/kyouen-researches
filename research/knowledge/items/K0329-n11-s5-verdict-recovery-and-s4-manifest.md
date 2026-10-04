---
id: K0329
title: 11×11のs5 verdict cacheの回収とcoordinator永続化でLOSS class 2個・WIN 1個・verified certificate 2件を確定した
kind: computation
status: computed
topics: [search-methods, verification]
aliases: []
relations:
- type: depends_on
  target: K0105
  note: 11×11空盤勝敗は未確定であり、本項目も thereof閉じない
- type: supports
  target: K0092
  note: DFPNの局所完了と回帰が空盤勝敗を閉じていないことの裏付けを1件増やす
- type: verifies
  target: K0023
  note: reply r2=0 の s4 class 2個について有限の厳密判定を与える
artifacts:
- path: research/experiments/n11-search-methods/reports/N11-DFPN-S5-RECOVERY.md
  role: source
  note: 回収・cold replay検証・manifest実装・回帰の実測記録
- path: research/experiments/n11-search-methods/scripts/dfpn_s5_recover.py
  role: verifier
  note: ログから決定済みs5 verdictのみを回収しconflict時は停止
- path: research/experiments/n11-search-methods/scripts/dfpn_s5_replay_check.py
  role: verifier
  note: cold replayで261件すべてを独立再証明
- path: research/experiments/n11-search-methods/scripts/dfpn_s4_manifest_verify.py
  role: verifier
  note: s4 certificate manifestを盤面から再計算して独立検査
- path: research/experiments/n11-search-methods/scripts/dfpn_canonical_xcheck.py
  role: verifier
  note: C++とPythonのcanonical key規約が3396 classで一致することを照合
- path: research/experiments/n11-search-methods/scripts/dfpn_s5_merge.sh
  role: verifier
  note: canonical key単位のdeterministic merge。conflict 1件で即停止し何も書かない
- path: cpp/solvers/kyouen_dfpn_root.cpp
  role: solver
  note: coordinatorのs5永続化とs4 certificate manifest出力
---

# 11×11のs5 verdict cacheから失われた158証明を回収しLOSS class 2個・secured 10/119を独立検証で確定した

## 対象範囲

first=60, r2=0 の二石rootに対する、third move 119頂点・canonical s4 class 3396個
という**有限の被覆問題**に限定する。11×11空盤全体の勝敗は対象外。

## 発見: 証明が永続化されていなかった

直前のcoordinator実行（`1da3db9`記録）はclass 481をLOSSと証明し
secured 4→10と報告したが、当時の`run_coord`にverdictを保存する経路が無く、
その実行で確定した158個のs5 verdictはプロセス終了と共に消失した。
`s4_cache_save()`は呼び出し元が無く、`s4_cache`には要素が一度も入っていない
dead codeだった。

## 回収

ログの`[q-done]`行にはcanonical keyと決定済みverdictが残っており、
再探索419M nodesなしで証明を回収できた。

- 回収158件、**すべてLOSS**。UNKNOWN(result=0)は0件
- verdict行を持たない中断query 1件は破棄（budget切れを保存しない）
- 既存103件とのkey overlap 0、同一keyの異verdict 0

回収直後の cache は 261 件。coordinator を1 class 実行して
58件が新たに確定し、canonical cache は 319 件になった。

## 独立検証

**cold replay**: 空のtransposition tableから**319件すべて**を再証明。
4 shard並列。

- 回収158件: **158/158一致**
- coordinator 新規58件: **58/58一致**
- disagree 0、undecided 0

**conflict監査**: 重複0、異verdict 0、overlap 0。canonical cache は
WIN 1 / LOSS 318。

**canonical key規約照合**: `build_maps()`の8変換表をPython側に再現し、
3396 classすべてのkey・coverage・raw edgeがC++と一致（`CANONICAL_AGREE`）。

**s4 certificate manifest**: class 481（LOSS, cov 6, children 106）と
class 482（WIN, cov 6, children 111）を盤面から再計算した子集合と
cacheで検査し、`MANIFEST_VERIFIED`。
cache から各 edge の verdict を復元し
`class LOSS ⇔ 全 edge がLOSS`、`class WIN ⇔ 1 edge でもWIN` を確認した
（481 は4 edge 全てLOSS、482 は4 edge 全てWIN）。

**回帰**: 修正前後の binary を n=4..7 で並走比較し
verdict も expansion 数も一致（239 / 847 / 55561 / 2123417）。

**worker merge 手順**（`N11-DFPN-COVER-OPTIMUM.md` が要求していた手順）：
conflict 1件で即停止・UNKNOWN 除去・3ケーステスト `MERGE_GUARD_OK`。
実装直後に `mv` がフィルタ済み出力を未フィルタ staging で上書きし
UNKNOWN を復活させる欠陥を発見し修正した。

## 結果

| 指標 | before | after |
|---|---:|---:|
| s5 verdict cache | 103 | **319**（WIN 1 / LOSS 318）|
| 独立再証明済み verdict | — | **319 / 319** |
| 判定済み s4 class | 1 LOSS | **2 LOSS / 1 WIN** |
| 検証済み s4 certificate | 無し（dead code） | **2 件 / 217 children** |
| secured coverage | 4/119 | **10/119** |
| min_additional | 34 | **33** |
| 新規 exact nodes | — | **313,904,753**（class 482）|
| cache hit 率 | — | **386/444 = 87%** |
| 未解決 class | 3395 | **3393** |

class 481は`unknown_s5=4 → 0, UNKNOWN → LOSS`と変化した
（**新規exact nodes 0**、回収のみ）。
回収によりcoordinator選択則（unknown s5 が少ないclass優先）が
実際に機能したことが確認できる。

coordinator 1 class 実行で class 482 が **WIN** と判定された。
WIN class は cover の除外対象なので secured は増えないが、
**58件の新規 verdict が永続化され**（`cache_saved=58`）、
cache hit 87% を達成した。

## 限界

- **二石rootは1個も閉じていない。** secured 10/119 は
  reply r2=0 の cover 31 class のうち LOSS 2 件であり、
  空盤のrefutationではない。
- OPT=31に対しLOSS class は残り29個。
- **WIN class を先に確定するとcover の候補が狭まる。**
  coordinator は cover 最適化で避けるが、判定順序によっては
  refutation 不能な class に時間を払う。
- 回収は**既知のverdictの再利用**であって新しい証明ではなく、
  計算量の削減であって計算結果の拡大ではない。
- 1 classの新規証明は約40分。

**11×11の空盤勝敗はUNKNOWNのまま。**