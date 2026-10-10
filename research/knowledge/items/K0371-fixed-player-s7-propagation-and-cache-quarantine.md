---
id: K0371
title: reply27のS7境界での先手固定伝播と旧2件のS5 WIN根拠撤回
kind: verification
status: verified
topics: [square-outcomes, verification, certificates, provenance]
aliases: []
relations:
- type: depends_on
  target: K0372
  note: 追加loaderと中間S6・上位S4依存の独立再監査範囲
- type: depends_on
  target: K0002
  note: 勝敗は手番側ではなく元の先手の固定命題
- type: verifies
  target: K0355
  note: S7由来のcache根拠を再監査し、有効な現行frontierを再計算
artifacts:
- path: results/n11-s5-evidence-quarantine.json
  role: data
  note: 旧cache ancestryから再流入させない2キー。局面自体の勝敗の反証ではない
- path: research/experiments/n11-boundary-recovery-20261006/scripts/fixed_player_outcome.py
  role: verifier
  note: 偶数OR・奇数ANDの固定プレイヤー集約
- path: research/experiments/n11-strategy-redesign-20261010/tests/test_polarity.py
  role: verifier
  note: S4..S10の全二子三値境界をBoolean completionで照合し、cache再流入も検査
- path: research/experiments/n11-strategy-redesign-20261010/output/audit.json
  role: data
  note: 有効なcacheと全3384 classの再分類
- path: research/experiments/n11-strategy-redesign-20261010/output/upper-boundary-certificate.json
  role: certificate
  note: 完全S5/S6境界。exact葉の再帰的minimaxはsolverを信頼する
- path: research/experiments/n11-boundary-recovery-20261006/output/post-5dfabf84-s7-witness-derived-s5.cache
  role: source
  note: 不正なS7反転を根拠にWINを追加した旧一次資料。内容を改変していない
- path: research/experiments/n11-boundary-recovery-20261006/output/post-2199bcc8-s5-10448351135499552768-128-s7-witness-derived-s5.cache
  role: source
  note: 同じ誤りによる旧一次資料。現在の証明に使わない
---

solverの `exact_replay` の1/2は、全層で「元の先手のWIN/LOSS」である。
手番が交替しても子のverdictを反転してはいけない。

| 層 | 元の先手WIN | 元の先手LOSS |
|---|---|---|
| S4 / S6 / S8 / S10 (OR) | 少なくとも一つの子がWIN | 全合法子がLOSS |
| S5 / S7 / S9 (AND) | 全合法子がWIN | 少なくとも一つの子がLOSS |

空の合法子集合では偶数層LOSS・奇数層WIN。UNKNOWNを含む場合、存在条件の確定証人がなく全子条件も揃わなければUNKNOWNとする。合法手は石数を一つ増やし、有限盤の探索は停止する。終局の手番側敗北を基底に、石数に関する逆向き帰納法でこの集約が得られる。D4商では各軌道の合法子集合が対応するため、全canonical childで十分である。

旧S7 runner / prepare / materializer / 二つのparent verifier / saved intersection auditには、S7 LOSSをS6 WINへ反転する処理があった。main `52239697a6a65b11889669725f8599604d53656f` 時点の次のS5 WINは、この不正な推論だけを根拠としており、根拠を撤回する。

- `(1152925911243358208,536870912)`
- `(10448351135499552768,128)`

保存された直接S5 replayは両方15M UNKNOWNで、別の直接exact支持は今回のraw交差監査では見つからなかった。したがって両局面をUNKNOWNへ戻す。これは両局面がLOSSであるという主張ではない。旧S7のexact LOSS raw自体はこの推論誤りによって無効にならない。

該当helperを訂正し、cache union / cover / local completion / saved S6の主要loaderに隔離規則を適用した。古いcacheとlogを上書きせず、今後のcache-only unionから両キーを除外する。再認定には新しい独立に支持されたexact replayまたは正しい完全境界と、registryの明示的更新を要する。

今回のexact再実行とgeometry監査の結果、別のS4 `(1333065489702715392,0)` は正しいS5 WIN証人を得てWINと判定された。これは旧2局面の再認定ではない。全reply27の現在値はK0355を参照する。

独立determinant/D4監査は安全性、合法親子、canonicality、完全上位境界とcache集約を確認する。exact葉の再帰的勝敗は変更していないC++ solverへの信頼に依存し、全探索木を独立に再検証した証明書とは区別する。

後続の[K0372](K0372-n11-independent-exact-evidence-trust-audit.md)は、旧反転の中間S6 WIN 6件と全上位依存を再構成した。追加のPython reader、C++永続cache reader、手動workflow内mergerには隔離漏れが残っていたため補強した。開始mainでの「主要loaderの訂正」を全経路での再流入防止完了と解釈しない。再認定にはregistryとC++コンパイル済み隔離表の両方を明示更新する。raw/cacheそのものは歴史資料として保存している。
