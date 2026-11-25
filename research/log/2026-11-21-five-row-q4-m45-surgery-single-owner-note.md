# 単一オーナー宣言: five-row (5,4) m=45 witness hunt — bounded surgery + translation cascade (2026-11-21 高速レーン)

- 宣言時刻: 2026-11-21T22:40Z 前後
- 宣言時 HEAD: `451e0fe8e45d3c699a9b191c0c00f2909a5d9d6f`
- 実験 dir（本宣言の成果物の置き場所）: `research/experiments/five-row-q4-band-45plus-20261121/`
- セッション log: `research/log/2026-11-21-five-row-q4-m45-surgery-session-log.md`

## 位置づけ

K1209 は (5,4) の width-40 witness 16 石集合を確定し、five-row-q4-band-41plus-20261121 は
その D4 像×並進 census で witness 帯を m=41..44 に広げて **M_{5,4} ∈ [45, 567]**（上界は
K1207 需要供給不等式 T_5=567・不変）とした。m=45 witness の存在は UNDETERMINED のまま。

本レーンはその次前線 **5×45 の構成的 witness 探索**（さらに見つかれば 46.. への連鎖）を
単独で行う。手法は six-row (6,4) m47..51 witness chain と同一の「既知種の並進 cascade +
bounded-edit surgery（classes: kR1A / kR2A, k ≤ 3, |R|+|A| ≤ 5, |A| ≥ 1; pair coverage が
単一生存石のみに依存する組は探索対象外）」である。

## スコープ（fail-closed）

1. Seeds は出版済み種のみ: K1209 の 16 m40 witness 石集合（`five-row-q4-witness-band-40plus-20261121/output/distinct-m40-witnesses.json`・sha256 `61cc7874…`）および
   41plus census の 4 R=44 placement を含む R ≥ 41 placement 34 個
   （`five-row-q4-band-41plus-20261121/output/census-5row-m40seeds.json`）。
2. 主張は **存在主張（下界更新）のみ**。witness が見つかった幅の分だけ
   M_{5,4} の下界を更新する（上界 567 は不変）。CSV（`results/fixed-width/mwq_stabilization.csv`）
   は本レーンでは更新しない（41plus/K1211 と同じ運用。値は K item と README に記録）。
3. bounded surgery が全種・全 placement で陰性の場合、その記録は
   「宣言した edit class 内の scoped negative」であり、m=45 の不在主張ではない。
4. 5×45 の SAT/UNSAT 判定・def-mode 掃引は行わない（別レーンの重装備領域）。

## 受入条件

1. **器材 pin**: engine（`engine_v2.py` sha256 `99bd45ae…`・`five-row-q4-band-41plus-20261121/scripts/`
   と byte-identical）、`append_criterion.py` sha256 `d08d8fb1…`、`verify_node.mjs` sha256 `fb2c8c9e…`、
   m39 seed `witnesses/s5x39q4.json` sha256 `fe4edef0…`、16 m40 witnesses sha256 `61cc7874…`。
   すべて main から取得し sha256 照合。本レーンは新規 engine を書かない（driver/config のみ追加）。
2. **陽性対照**: (a) census 較正: m40_1 id s15 → R=42 / firstUncovered [42,1]・
   m40_3 id s15 → R=40 / [40,1]（41plus の calib gate と同一値）。(b) surgery 較正: K1209 m39 seed
   （s5x39q4.json）の 5×40 への placement に対して engine v2 surgery（remBudget 2）を実行し、
   発見 witness の石集合レベルで K1209 の出版 16 witness（distinct-m40-witnesses.json）
   と照合（rem2add2 級の再現度を確認してから本番に使う。完全再現に届かない場合は
   差異を診断して本レーンの解釈に明記する）。
3. **witness 検証は 3 系統**: engine `verify`（4x4 行列式・第三 codepath 含む）+
   `append_criterion.py`（Fraction・criterion 幅評価）+ `verify_node.mjs`（BigInt Bareiss）。
   陰性対照（tamper）は全系統 fail すること。
4. **決定性**: census・surgery の主要出力は 2 回実行で byte 一致。
5. **reporting**: 有限 census・bounded surgery（scoped）・全称（無し）を明確に区別する。
   標準 11×11 空盤・二石 root・S2・class 1/2/4 は本レーンの非目標で UNKNOWN のまま。
   nodes 数/leaf 数を勝敗として読まない。

## 他レーンとの排他（2026-11-21T22:35Z 時点の宣言状況）

- five-row q6/q5 m23/m27 sd≤6 surgery（`5c4cfca9`・成果 `c20103072`）と sd≤(4,3)/(3,4)
  partial sweep（`0b2a6466f`）: いずれも (5,6)/(5,5) の m23/m27 前線で (5,4) とは
  対象 dir・主張ともに disjoint。
- five-row-q4-band-41plus（`bab006ad` 宣言・21:35Z 出版完了）: 同 (5,4) の m41..44 だが
  出版済み・claim 完了。本レーンはその seeds を参照するだけで同 dir には触れない。
- six-row (6,4)（K1211/K1213 レーン群）・four-row (4,4)/(4,5)/(4,6)・n11 全般・
  seven-row q4 m69+: すべて対象外。
