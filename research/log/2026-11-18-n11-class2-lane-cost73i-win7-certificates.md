# 2026-11-18 n11 class2-lane cost73i: 12 WIN7-D10証明書の抽出・独立検証・出版 (2026-11-18)

## 背景

cost73i行（child `00000000000000403800400008000000`・S5 parent
`00000000000000403800000008000000`・石bits [27,46,59,60,61,70]・edge cost 73・
法候補73）は2026-11-17にfresh v17 depth-10 sweepが完走し、raw sweep audit
（git blob `33c8c6bb2b81301354e8b796f5a4751fb52aba3b`）で
**12 WIN7-D10 + 61 REFUTED-D10 / 0 capped**に確定していた。しかしWIN bits
[1, 9, 11, 18, 29, 38, 54, 82, 97, 100, 110, 111]の証明書は
main上に1つも出版されておらず（census v6以降のcensus JSONでも
「the 12 WIN certificates were NOT yet published on main ... the 73i map is
carried at audit strength」と記録されたまま）、73i行は証明書なしの
audit-strength-only行として残っていた。本出版はこの欠落を埋め、73i行を
78c/79cと同じ「証明書出版済み・fold待ち」の状態にする。

## 抽出: blind extraction（engine v15 inlined・MS=1<<23）

- driver `cert_driver73i.ts`（`cert_driver78c.ts`からのduplication・argv駆動・
  kill table空・防衛列はstdin）+ wrapper `extract73i_all_20261118.sh`
  （root=child|1<<bitを `legal_candidates.py` に与える）。
  extractorはrepo-verbatim `class4_child1_cert_extractor_exact_ms23.ts`
  （MS=1<<18→1<<23の1行置換のみ）。
- 12/12 bitがper-bit fresh processで抽出完了。**fbt_drops=0・fatalなし・
  capped per-move 0**。防衛数（root loser mobility）は
  bit1:59, 9:61, 11:61, 18:60, 29:56, 38:54, 54:63, 82:47, 97:57, 100:53,
  110:58, 111:60（合計689）。
- 抽出rows合計 **649,340**・抽出nodes合計 **102,080,312**・出版bytes合計
  **23,451,347**（`stats.json`にper-bit集計）。

## 独立検証1: engine-free Bareiss（verify_bit7_win7_cert.ts）

`verify_cost73i_one.sh`（78c orchestratorのduplication）で全12 root:
root-check stones=7・loser mobilityがRAW root上の `legal_candidates.py`
独立列挙と全bit一致・**全sub-root PASS**・terminal石数範囲[13,17]全域で
遵守・**consumed-winner-state union vs 証明書行集合 0 missing / 0 extra
（双方向・全root）**。12/12 PASS。

## 決定性

bit 82（最小 941,950 bytes）とbit 54（最大 2,549,054 bytes）をfresh
processで再抽出し**byte-identical**（md5 `03f3578c…` / `029e2bb1…`）。
`det-reextraction.json`に記録。

## 独立検証2: BigInt一般化円・第三実装（general-circle audit）

`audit_cost73i_certificates_general_circle_bigint_20261118.mjs`
（79c監査の第三実装を73iに適合・3x3 Cramer係数の整数円/退化直線評価で
探索器・verdict cache・4x4 Bareiss検査器を一切使わず、各rootの全合法な
敗者初手からAND/OR木を独立再走査）:
**12/12 PASS**・union 0 missing / 0 extra・terminal range [13,17]・
root canonはcensus側python実装と**12/12一致**（12 rootのD4 canon衝突なし）・
bit1のsubroots metadata（rootcheck + 59 move分のper-move stats）が
出版済みmetadataと**59/59完全一致**。totals: subroot_seen 1,395,567・
winner_states 901,604・terminals 225,230（監査JSON
`class2-lane-cost73i-certificates-third-independent-audit-20261118.json`）。

## 出版

- 証明書本体25ファイル（bit82は 941,950 bytesで単一ファイル、他11 bitは
  1,200,000 bytes閾値の行境界分割: 2-way × 9 bit + 3-way × 2 bit）。
  各partのgit blob SHAをmanifestにpin。`cat`で再結合するとmd5一致
  （README-split-bitN.md参照）。
- manifest `class2-lane-cost73i-win7-certificates-20261118.json`
  （git blob `8a766a4225c418cb5eae297404de71d7f402c103`）: 12証明書の
  root・rows・nodes・md5/sha256・d4_canon_root・raw_is_canon・
  parts pin（78c/79cと同一形式）。
- 12 rootcheck JSON + 12 subroots JSONL + stats.json + det-reextraction.json +
  driver/wrapper/verifier/auditスクリプト4件。
- 出版コミット（main）: metadata bundle 40ファイル = `6de3c330`、
  証明書part 25コミット = `af738fbb`..`062ee43c`（1 part = 1 commit）、
  manifest = `feef6bf3`、本監査JSON + auditスクリプト + 本log =
  このコミット（BASE_MAIN pin = `feef6bf3`）。
- 着地検証: SHA固定raw CDN取得 + `cmp` で**証明書25ファイル + manifest +
  metadata bundle 40ファイル = 66/66 byte-exact一致**（負荷キャッシュ404は
  SHA固定URLで回避）。

## 制限

- 本出版が証明するのは「このchildの12個の7石rootのそれぞれについて
  depth 10以内に先手勝ちが存在する（WIN7-D10）」のみ。**61 REFUTED-D10は
  LOSS証明ではない**。
- 73i receipt foldは並走laneのfold queue（66i/66j/69j/71e/72d後）のまま
  変更しない。manifest行のクローズも行っていない。
- 73i claim file（`class2-lane-cost73i-inflight-20261117.json`・claim v1
  in-flight）は並走lane管轄のため本出版では更新しない（raw sweep audit
  git blob `33c8c6bb`が完了根拠）。
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- census v17以降で73i行のfold欄を「12 certificates published（manifest
  git blob `8a766a42`・第三実装監査blobは監査JSON本文参照）」に更新
  できる（census更新はsweep lane管轄）。
- 78c・79c・73i以外のWIN-bearing行で証明書が未出版の行があれば同じ
  pipelineで埋める（66i/66j/69j/71e/72d/73j/73k/73lは冪等に
  「certificates/」dirの有無で判定できる）。
