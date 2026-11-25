# 2026-11-24 NCW class-enum closure 証明書: 単一オーナー宣言ノート

作業種別: **K1310 への evidence addition**（AGENTS.md「同じ命題のstatusや証拠の
更新は、原則として同じK項目を更新する」に従い、新規K番号は採らない）。
高速レーンの一本として、上記キットを単一オーナーで出版する。対抗宣言が
あれば本ノート以降の出版を中止する。

- 着手時観測 HEAD: `878e6946`（K1310 出版完了直後）。
- ノート push 時観測 HEAD: `46e02d0e`（Part DX batch-36 inc3。11×11 raw
  output の giant レーンで本作業と直交）。
- 対象パス（全て main 上で空きを確認済み）:
  - `research/experiments/ncw-class-enum-20261124/`（新規キット）
  - `research/log/2026-11-24-ncw-class-enum-closure.md`（実行 log）
  - `research/knowledge/items/K1310-noncongruent-window-collapse.md`
    （artifacts への1項目追加のみ。定理本文・status・relations は変更しない）

## 1. 主張の位置づけ（新規定理なし・過大主張の防止）

本キットが証明書を与えるのは、公刊 K1310 手証明（単一オーナーノート
`2026-11-24-ncw-window-single-owner-note.md`）の **SS2.4/SS2.5 mex 閉包
アルジェブラの層**である。すなわち:

- **分割（Partition）**: 非合同窓領域の各 cell（pair: z≥2, k∈[1,z−1],
  k≢z (mod 2), m≥1, g≥1 / bed: a≥1）を、比較ラベルのみの組合せ
  （pair: pz,pg,gs(3類),ggs(5類),gzs(6類),tau(7類),m1,g1,k1 /
  bed: pz,gs(5類),tb(5類),a1,k1）で分類すると、実現可能なラベル組合せは
  **pair 280 クラス + bed 39 クラス**であり、各クラスに具象 witness が
  存在する（Box lemma: 整合する差分有界オフセットは小座標で実現する）。
- **決定と閉包（Determination + Closure）**: 各クラスの申立値
  （T-NCW-P / T-NCW-B）と3つの typed 子値（A-fall / A-compress・g=1 corner
  bed・m=1 B-exit 単一トークン・C 子 (k−1,z−1) の concession flip 1^・
  k=1 C 子の K1303 帯域行）が**クラスラベルのみから記号的に決定**され、
  `mex(children) == claim` が**クラス毎に**機械検証される。ラベルは
  cell の関数・子はラベルの関数だから、クラス毎閉包 + 分割により閉包は
  **全 cell に対して有限場合分け（280+39 cases）で閉じる**（手証明の
  区域代数 SS2.4/2.5 に対応する機械証明書）。
- **接地（有限・census）**: coverage census が各 cell のラベル導出・
  申立・typed 子・mex 閉包・クラス表中の対応（分割完全性）を照合する。
  census は証明ではなく実機照合である。デフォルト z≤30, m≤12, g≤40, a≤14
  で pair 108,000 + bed 3,150 cells、深部 `34 16 44 20` で pair 203,456 +
  bed 5,780 cells。
- **転写ゲート（eqcheck）**: 同梱 `eqcheck.py` は shipped
  `enum_classes.py` を import し、その法則実装を公刊 K1310 kit
  （verify_k1310.py）の P / Bm / single_token(q_odd 版) / cpsfG の
  verbatim 転写と 1,031,085 点で照合する。
- 法則値そのものの engine 接地は公刊 K1310 公式監査（51,439 点・engine
  pin bd5f22e4…/582c93c1…・公式4走 byte-identical・変異電池 13/13）が
  既に確立しており、本キットは engine を import しない。

## 2. 事前宣言する機械的事実と pin

- `enum_classes.py` sha256
  `716b2976306a437d16f8e8ad088ffbe8f37f9131430a1a318c63b79f8becbad7`
- `eqcheck.py` sha256
  `6c005154bae91546edfb990ae749834a6acdb0fa86b446e4b2393334f633ffa1`
- 期待 stdout（決定的・byte 一致）:
  - enum 既定: ```RESULT: PASS pair_classes=280 pair_bad=0 bed_classes=39 bed_bad=0 xpair=0 xbed=0 census_pair=108000 census_pair_bad=0 census_bed=3150 census_bed_bad=0 missing_class=0```
    （直前行 `pair classes: 280  bad=0`・`bed classes: 39  bad=0`・
    `cross-validation failures: pair=0 bed=0`・
    `coverage census: pair cells=108000 bad=0 bed cells=3150 bad=0 missing-class=0`）
  - enum 深部（argv `34 16 44 20`）: 同形式で
    `census_pair=203456 census_pair_bad=0 census_bed=5780 census_bed_bad=0`
  - eqcheck: ```EQCHECK: comparisons=1031085 bad=0``` +
    `RESULT: PASS eqcheck_comparisons=1031085 eqcheck_bad=0`
- 既定 census stdout 全体の sha256（predry 4走で byte 一致を確認済み）:
  `4284f248a319cf9e8ba02916b7eebaed3be97d9e41f717e0e53f6dc311160651`
- 深部 stdout sha256:
  `a4149b372defbcba2cdcf9f88f89047b93d8965e9e34c8178504bf5f394bc80e`
- eqcheck stdout sha256:
  `a7bfb3bb05dd7a7f6f627230fc78c31818f5a9832aad1fd859404cf32b917650`
- 失敗閉鎖: 両スクリプとも bad>0 で rc!=0。

## 3. 変異表（tamper・事前宣言・全て rc=1 の FAIL が期待値）

| id | 操作 | 期待 RESULT |
|----|------|--------------|
| t1 | `sym_claim_pair` の zone-A parent-NEG 申立 `[g odd]` を `[g even]` に反転 | FAIL pair_bad=110 xpair=110 census_pair_bad=57600 |
| t2 | `sym_cchild_kge2` から concession flip `1 ^ ` を除去（構築期の実際の draft バグの再現） | FAIL pair_bad=205 xpair=230 census_pair_bad=100800 |
| t3 | witness 棄却条件 `gs >= 0` を `gs >= -1` に戻す（gs=−1 の3クラスが欠落する歴史的 off-by-one の再現） | FAIL pair_classes=277 census_pair_bad=12 missing_class=12 |

いずれも刊行物の一部として `tamper/` に変異スクリプトと出力を凍結する。

## 4. 構築経緯（honest・宣言前に全て発見・修正済み）

draft（出版前・未公刊）で3つのバグを電池自身が検出し、出版前に修正した:

1. pair C 子評価器で tau 7類ラベルの wave 判定に label 2（tau==z）を誤って
   含めていた（子枠 z−1 では tau≤z−1 が条件。label 0/1 のみが有効）。
2. pair/bed 両 C 子評価器で concession flip `1 ^` を落としていた
   （typed children は budget R−1 の譲渡手で 1^ 反転を伴う。t2 が再現）。
3. `pair_witness` の gs ラベル 0（gs≤−1）の棄却条件が `gs >= -1` で
   gs=−1 を誤棄却し、z=3, k=2, g=1 近傍の3クラスが列挙から漏れていた
   （t3 が再現）。

いずれも本キット固定後の cross-validation + coverage census + missing-class
検査が bad=0 を出しており、上記3変異の FAIL は検査器がこの種のバグを
確実に検出することを示す。

## 5. スコープの限界

- L2（B-exit 一様則）の記号的評価器は tau ラベル列（g=z, g=z+1 の限界
  分岐を含む導出表）で実装しているが、これは (g+1)%2 一様則と
  全ラベルで一致する（機械的に eqcheck/E3 の single token 照合の内側で
  接地）。
- 本キットは mex 閉包アルジェブラの証明書であり、法則の全称性そのものは
  公刊 K1310 手証明が担う。census は有限である。11×11 への verdict 消費は
  一切行わない（UNKNOWN 維持）。

publish-then-execute: 本ノート刊行後、(a) キット出版、(b) fetch-back での
sha 検証、(c) fetch-back bytes からの公式走（enum 4走: 同一 cwd×2 +
隔離 tree/env -i×2・eqcheck 2走）、(d) 監査成果物 + 実行 log + K1310
artifacts 1項目追加、の順で実行する。
