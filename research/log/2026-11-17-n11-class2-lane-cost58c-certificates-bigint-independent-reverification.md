# 2026-11-17：cost-58c証明書34ファイルのBigInt独立再検証 — 33/33 folded bits PASS（rows 1,156,691・md5全一致・sub-roots 1607）・bit76は文書済み13..17ガード拒絶を独立再現

開始時の最新mainは `0c486e53bb84c4418c9a6c89073cdc067a4172e8`（前エントリhead-1452 census v3出版済み）。cost64h fold receiptは本エントリ時点でも未着地（並走claim済み・着手禁止）。

## 出発点

前エントリのhead-1452証明書被覆census（775/775 certified・tier V 250 / tier R 525）の含意3で「tier R 525 rootの証明書bytes自体の再検証は今後の強化候補」と残した。tier R最大ブロックはreceiptcert単独181であり、その中心がcost-58c receipts recomputeの折り込み33件（証明書bytesは `class2-lane-cost58c-certificates/` に34ファイル42.9MBとしてmain出版済み）。そこで**58c laneの証明書bytes全件にBigInt独立検証verifierを再実行し、receipts recomputeのper-bit記録と機械照合**した。

## 実施内容

1. **bytes取得とpin照合**: `class2-lane-cost58c-certificates/` の34ファイルをmain commit `0c486e53` のsha-pin URLで取得し、各ファイルのgit blob SHA-1（`sha1("blob <size>\0"+bytes)`）をGitHub API listingのblob SHAと照合（**34/34 byte-exact**）。ファイル名1件（bit88）は手書き転写ミスで初回404になったが、API listing由来の正確名で再取得し解消（root hex 32桁を1桁落としていた）。転写ではなくAPI由来の名前を使うべき教訓。
2. **BigInt独立検証の再実行**: 出版済み `verify_win7_certificate_bigint_independent.mjs`（BigInt 3x3余因子展開・engine不使用・浮動小数点なし）を34ファイルへ実行（4並列、全体で数十秒）。
3. **per-bit機械照合**: 33 folded bitsについて、verifier出力の `strategy_rows` / `subroots_passed` とファイル全体のmd5を、`class-frontier-cost58c-receipts-recompute-20261116.json` の `cost58c_addition` per-entry記録（rows / md5 / `sub_roots_pass`）と全照合。
4. **bit76の診断**: guard無効化診断ビルド（1行差し替え・出版verifierには影響なし）でbit76の実terminal rangeを測定。

## 結果

- **33/33 folded bits PASS**: verdict「WIN7 certificate independently verified」、root 7石・`root_safe`・rows sorted-unique・union_missing 0 / union_extra 0 が全件成立。
- **per-bit記録との完全一致**: rows・md5（ファイル全体bytes）・sub_roots_passが**33件全て**でreceipts recompute記録と一致。総rows **1,156,691**（recompute totals `certificate_rows` と一致）、総sub-roots **1,607**（totals `certificate_sub_roots` と一致）。**mismatch 0**。
- **bit76は文書通りの拒絶を独立再現**: verifierは「terminal range outside 13..17」guardでexit 1。診断ビルドで実測したterminal rangeは**11..17**であり、`class2-lane-cost58c-inflight-20261116.json` のfold記録（「bit76 excluded: its certificate has terminal range 11..17, rejected by the BigInt verifier 13..17 guard」）と文言含め一致。bit76はfoldの33 receiptに最初から含まれておらず、簿記上の影響はない（bit76 rootはhead-1452 censusの775件母集団にも不在）。
- 34ファイルの全bytes md5をreverification JSONに記録し、blob SHA pinと二重で固定した。

## 含意

1. **tier R最大ブロック（58c折り込み33 root）が「記録の記述」から「bytes独立再検証済み」に格上げ**された。head-1452 censusのtier V/R構成（250/525）は今回の対象外だが、58c分33 rootは独立検証がこの環境で再実行・再現可能であることが裏付けられた。残るreceiptcert-onlyブロック（warm-multiband 33・multiband2 31・70c warm 6+warm3 3+hygiene 5等の証明書bytes）が次の再検証候補。
2. bit76のような「フォルダに出版されているがguardでfoldから除外された証明書」は、除外理由の文言まで含めて第三者環境で再現可能である。証明書フォルダの内容とfold簿記の整合（33 counted / 34 published）が独立裏付けされた。
3. 63c/63d sweepの証明書bytesはmain上に存在せず（sweepのpush_noteどおり）、per-entry記録（rows/md5/sub_roots_pass）のみ。bytes再生成は次回以降の候補として残る。
4. 本再検証はfrontier数字を一切変更しない。

## 保存物

- 再検証script: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reverify_cost58c_certificates_bigint_20261117.py`（repo rootから実行・34 blob SHA pin・全assert込み・2回実行byte-identical確認）
- 再検証JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost58c-certificates-bigint-independent-reverification-20261117.json`（schema `-v1`・34 entries・bit76 documented_exclusion付き）
- いずれも初版のため新規pathで出版。

## 信頼境界

本エントリの「PASS」は個別7石rootのWIN7-D10証明書の数学的検証の再実行であり、solved数やfrontierの変更を意味しない。md5照合の対象はrecompute記録に記載された「証明書ファイル全体bytes」である。bit76のFAILは証明書の誤りではなく、depth window 13..17外のterminal（ply 11）を含むことによる fold 時点の文書済み除外の再現である（同rootの価値は本エントリでは判定しない）。**標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 はすべてUNKNOWN。**
