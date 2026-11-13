# 2026-11-14 class2-lane cost-60 WIN7証明書19件（第20セッション続き2）

- **成果**: cost-60 orbit（`00000000000000801a02000020000000`・c2=2）sweepで得た
  **19 WIN7-D10候補全て**の完全戦略木を抽出し、独立検証した。
  計 **605,587行・抽出総93,009,263 nodes**。全19件 PASS。
  記録: `output/class2-lane-cost60-win7-certificates-20261114.json`（コミット c37852d6）。
  証明書本体: `output/class2-lane-cost60-certificates/n11_s7_<root>.cert` ×19
 （各コミット: bit50=77002bb8, 117=a10e0b35, 113=7147e323, 20=b35df0a2,
  72=844768bd, 92=4c2ef53d, 111=a91d2c5e, 110=aca580af, 98=dade5a9e,
  96=f3d9eb52, 0=672c5d16, 26=5269867c, 1=eb19b336, 53=7e28dd4b, 10=27a03125,
  112=10eece6a, 25=79cef5f2, 76=9f66ee8c, 52=4a81f1e3）。
- **抽出**: `scripts/class4_child1_cert_extractor.ts`（v15規則・per-root fresh
  engine・loser初手ごとにdepth 9）。kill tableなし（blind）で全bit完了・fatal 0。
  行数: bit50=15,018（最小）〜bit52=49,003（最大）。
- **独立検証**: `scripts/verify_bit7_win7_cert.ts`（engine不使用・Bareiss 4x4整数
  行列式）で各証明書の**全loser初手sub-root**（43〜55手）を検証 —
  (a) 全winner手番局面に合法なstrategy手、 (b) terminalはloser手番のみ・
  terminal range [13,17]、 (c) opponent手番にstrategy行なし、 (d) 行列は
  sorted-unique、 (e) **consumed union == 行集合（完全一致）**、 (f) root-check
 （7石・4共円なし）。全19件 PASS・root-check PASS。
- **frontier効果（測定済み・正式反映は次回）**: 19 rootのcovers union 111軌道、
  うちafter-batch3 solved集合に対するmarginal manifest S6が**+34個**
 （690 → 724予想）。正式なfrontier再計算（recompute_frontier_full.pyへの
  本証明書群の組み込み）は次回の最初の作業。
- **実装上の重要修正（2件・push済み）**:
  (a) `class4_child1_cert_extractor.ts` — モジュールがESM（top-level export）のため
  strip-types下でCLIブロックの require('fs') が未定義となり、**rowsファイルが
  静かに1行も書かれない**バグ（本セッションで発見・再現）。top-levelの
  `import fs from 'fs'` に置換（コミット 9f86edc0・bit7 smoke 591行で検証）。
  (b) `verify_bit7_win7_cert.ts` — 同種のESM/requireバグを同修正
 （コミット 1aa0d4aa・本19証明書の検証で実使用しPASS）。
  いずれも改行リテラルは `String.fromCharCode(10)` 化（pushトランスポート耐性）。
- 運用: 16MiB sandbox制限のため、1回のrun_typescriptで読めるのは~28 ops
 （~1.7MB）。大容量pushは1ファイルずつ・read_file pagingでアキュムュレート
 （コンテキストには1文字も流さずにpush可能）。push後の raw 検証は
  commit sha指定URLかcontents APIで行う（main指定はCDN遅延で旧版を返すことがある）。
- 解釈ガード: 各証明書は「対応する7石rootから7石側が10手以内で全防御に勝つ」
  ことのみを証明する。REFUTED-D10は深さ10以内のWIN7の否定のみ。
  **class 2・class 4・S2 {59,60}・二石root {49,60}・11×11空盤はいずれも UNKNOWN**。
- レジューム: (1) 19証明書を組み込んだfrontier完全再計算（+34確定の正式化）、
  (2) 次のclass-2 lane最安未sweep orbitの選定（再計算後のrankingから）、
  (3) cost-74 class-4 `00000000020000003801000080000000`。
  並走レーンの最新mainを取り直してから。
