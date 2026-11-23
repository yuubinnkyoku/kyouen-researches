# 単一オーナー宣言（takeover #2）: (4,23,5) 残存 x2 サブバケット 60 個の完走と (4,23,5) の決着（2026-11-23）

- 宣言時刻: 2026-11-23T15:12Z（直前の最新 main HEAD: `a012ca4a`・K1058 AG(2,11) commit。push 直前に再取得して記録する）。
- オーナー: 高速レーン（本セッション）・単一オーナー。同名の毎時タスクが並走する可能性があるため、本宣言以降は下記スコープへの同内容の並行着手を避けること。

## 引き継ぎの経緯

- 前回 takeover（2026-11-22T10:28Z 宣言 `2026-11-22-four-row-q5-m23-class-split-takeover-note.md`）は
  part1（commit `03ae14d5`・50 UNSAT pieces + c01 multi 220s INDET）以降の出版を行っていない
  （実験 dir `research/experiments/four-row-q5-m23-class-split-20261121/` への最終 commit は
  2026-11-21T19:49Z のまま）。よって本セッションが lane を引き継ぐ。
- 現HEAD で coverage_check.py を records.jsonl（30 行: k3 直接 + multi 7 クラス + 対照）と
  records23.jsonl（51 行: k0/k1/k2 + c01 multi INDET）の併合に対して実行した機械監査の結果:
  **未決着バケットはちょうど c0k3p0/p1/p2 の x2 サブバケット 60 個**
  （p0: B=1..21 の 21 個・p1: B=2..21 の 20 個・p2: B=3..21 の 19 個）。
  その他 79 keys はすべて UNSAT 決着・SAT なし。x2 は coverage_check.py が設計上
  「直接試行スキップ・x2 で完結」とする c0k3p0/p1/p2 に限る。

## 本環境での較正（2026-11-23T15:10Z・全項 bit-exact）

- 陽性対照 (4,20,5) c0k3p1: CNF md5 `362034b2` byte-exact 再生・pinned kissat (md5 `3a5eba830aa6008a604fcc9bbe99a325`) SAT・**conflicts 375,415 bit-exact**・20.1s。
- (4,22,5) c0k3p0 CNF md5 `bf26eee9` byte-exact・c0k3p0x2b1 CNF md5 `7db59b4b` byte-exact。
- スクリプト pins: sat.js `0cc6021a`・sat2.js・sat3.js・sat4.js・verify_witness.py・x2gen23.sh・coverage_check.py は main から取得し md5 照此済み。

## 本セッションのスコープ

1. **60 x2 サブインスタンスの決着**: `x2gen23.sh`（sweep runner・chunk 再開可能・records append-only・
   cap 220s・INDET は honest negative・不在主張ではない）で c0k3p0, c0k3p1, c0k3p2 を走らせる。
   sat4.js + pinned kissat・CNF 生成は決定的。
2. **全 UNSAT なら**: coverage_check.py の claim_complete が真であることを機械的に確認し、
   「witness-free 幅集合 {21,22,23}・K0821 監査規約により **M_{4,5} = 21 または ≥ 25**」を
   実験 README 結果節・K 項目・knowledge README bullet・mwq_stabilization.csv に反映する。
   x2 の場合分けの完全性（B ∈ p+1..21・k-aware 上限・disjoint case analysis）は sat4.js の
   コメントと coverage_check.py の expected_x2 が担保する。
3. **いずれかで SAT が出たら**: 掃引を停止・witness を復号・二系統検証（sat.js 整数 verifyConfig +
   Python verify_witness.py）して **M_{4,5} ∈ [24,140]** とする。
4. **出版**: records23.jsonl 増分 push（append-only）・chunk driver の生ログ・決着後に README・K 項目・CSV。

## 非目標

- 4×24 以降への主張はしない。上界 U_{4,5}=140（K0318）は不変。
- 標準 11×11 空盤・二石 root は本レーンの無関係・UNKNOWN のまま。conflicts 数・実行秒数を勝敗として読まない。
- branch/PR は作らず main に直接出版する。fetch-back は byte/sha 照合で行う。
