# 2026-11-19 長期レーン成果物（11×11 D10プール完全判定・第7/第8 WIN7-D10証明書）

本フォルダは 2026-11-19 の長期レーン実行で得られた未出版成果物一式。GitHub push トランスポートのない実行だったため、出版（K1044以降・最新main再確認必須）は次回以降の実行が行う。

## 含める成果（要約）

- **117-root候補プールのdepth-10完全判定**: resolve4 により 109 REFUTED-D10 + 8 WIN7-D10 + 0 未検証（17×11の5親target残余86行はこのプール内のD10候補では閉じない）
- **第7 WIN7-D10証明書**: G=`00000000040080801202000000100001`（51/51合法手・552,457 nodes・21,829行）
- **第8 WIN7-D10証明書**: H=`00000000040000801202000000100001`（58/58合法手・2,655,359 nodes・39,163行）
- **第7・第8レシートフォールド**: S6フロンティア 6,224/492,830 → 6,223/492,762 → 6,222/492,688、solved S6 1,624→1,625→1,626、5親target 26/112
- sweep35（29候補掃引: WIN 1/REFUTED 28/CAPPED 0、canon_hex(child)事故と修復記録を含む）
- sweep6（6 zero-cover候補掃引: WIN 1/REFUTED 5/CAPPED 0）
- sweep28 K1039再現（56 probe ノード単位EXACT一致）
- resolve2 / resolve3 / resolve4 記録（resolve3.pyの出力パス上書きバグ修正済み）

## 主要SHA-256

| ファイル | SHA-256 |
| --- | --- |
| cert-7th/win7-root-00000000040080801202000000100000-20261119.n11 | 7049f7cb54163ce49d640e86d079fb47ad0a3adf9aa3d2a8e40bbe4b7a85ecb3 |
| cert-8th/win7-root-00000000040000801202000000100001-20261119.n11 | 7e0599f7fa177a1667fc63b1c81ad1114aeca7a5bc2102c7caed81986aa04d03 |
| sweep35/eligible-29-candidate-root-depth10-sweep-20261119.json | 8b7ba7d6b6fbfef057267e95c66efc036779c7d90ec918ec8beaa6a6618b95a5 |
| foldv2/output/seventh-win7-receipt-fold-20261119.json | f1baf15942d3efeaa3ca75c4d803148239269715e297aaf9b00042611543b737 |
| foldv2/output/eighth-win7-receipt-fold-20261119.json | afcf7d0ad0d6ca1edf31e150a7ba840f802a6382506f4a662b4e13567fbd30a2 |
| foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json | 2ad70afba4236375925dfd13230bb599b2d38f93631d6ded266fd77d34432e09 |
| foldv2/output/post-seventh-receipt-cover-resolve3-20261119.json | c42c3434b0d866789be782dccb61c369bf8f7e216e3abe7306cd0a50068c2f3e |
| foldv2/output/post-sixth-receipt-cover-resolve2-with-sweep-20261119.json | 16673dc7b9f61c2b108832f4ff61da1ae6b69c47e907c02404b053df76a18c0e |

## 構成

- `sweep35/`: 29候補掃引（driver.sh・driver_fix5.sh・assemble_sweep35.py・roots.json・roots-reprobe5.json・抽出JSON・probe-records {w0,w1}有効24root分・probe-recordsfix 5root再probe・round1-quarantine/ 隔離記録・workerログ）
- `sweep6/`: 6 zero-cover候補掃引（driver.sh・roots.json・probe-records-w{0,1}・workerログ）。WIN = H、REFUTED 5
- `sweep28-repro/`: K1039の再現実行（probe-records-w{0,1}・residual-28-root JSON。全56 probeがノード単位で出版値と一致）
- `cert-7th/`, `cert-8th/`: 証明書（.n11テキスト）+ extraction-summary + independent-verification + bareiss-subroots + bareiss-union-audit + extraction-progress + extract-stdout.log + win_legal_gen.json（第7のみ）+ extract_root_rec_20261119.mjs + scripts/（extractor・BigInt verifier・Bareiss verifier）
- `foldv2/`: fold_fourth_fifth_sixth.py / fold_seventh.py / fold_eighth.py / resolve2.py / resolve3.py（出力パス修正済み）/ resolve4.py / dump_candidates.py（bug note: round-1のcanon_hex事故はdump_candidates.py由来の候補 Pillow ではなくdriver側のchild正準化が原因）+ output/ 8記録
- 注意: 巨大で冗長な rows-*.txt / consumed-*.txt は含めていない（.n11 と verification JSON から再導出可能）

## 出版時の注意（次回実行へ）

1. 最新mainを必ず取り直す（2026-11-19 12:57Z時点の最新確認値: `ddc36617` = K1043。高速レーンがK1041〜K1043を出版済みのため、本成果は **K1044以降**）
2. .n11 はテキストとして出版（.gz をGitHub text経路でpublishすると破損するという過去の実績に基づく）
3. フォールドチェーンの出版機械: K1038出版済みの C-fold に D+E を合流（6,226→6,224/492,830、target 25/112）→ 第7（6,223/492,762・26/112）→ 第8（6,222/492,688・solved 1,626）
4. sweep35/sweep28の引擎 (probeドライバ) は raw maxbit child を使うこと（canon_hex(child) 禁止）

## 未解決であること（interpretation guard）

11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/2/4 はすべて UNKNOWN。REFUTED-D10 は LOSS ではない。residual 86行の「stranded」は117-rootプールというスコープでの候補不足を意味するだけで、数学的な閉鎖不能証明ではない。
