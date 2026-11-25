# 2026-11-15：監査v8両実装+agreement v5着地の再現検証 — 3script再実行でpublished出力とbyte-identical・83d endpointが四重検証に

開始時状況: 兄弟laneが**監査v8両実装**（第一実装: `98f750b9` script + `6b73f1cf` 出力・第二実装新version file: `2294c403` script + `ea748af0` 出力）と**dual implementation agreement v5**（`bf3c46f1`・in-place拡張・83d endpoint pair追加・12 blob-pinned audit JSONs）を15:22-15:23Zに着地済み。本レーンは同時間帯に[cost-83d fold第二独立検証](./2026-11-15-n11-class2-lane-cost83d-fold-second-verification.md)（commit `def2ddd1`）を着地させており、collision protocolに従い兄弟着地分の再現検証に転換した。

## 成果：fresh mirrorで3scriptを各2回実行 — 全出力がpublishedとbyte-identical

方法: codeload main tarball（HEAD `0a3e0a4b`・md5 `323548d7`）のfresh mirror（pin対象corpus全体を含む）+ 最新mainのraw CDNから3 script・3 published出力を取得（着地から20分以上経過しCDN stale期間は過ぎていることを確認）。各scriptを2回実行し、出力をpublished JSONとbyte比較、実行間でも比較。

| 対象 | script (blob) | published出力 (bytes / md5) | 結果 |
| --- | --- | --- | --- |
| 監査v8 第一実装 | `audit_published_chain_roots_independent_20261115.py`（`b7117dbf`・71,120B） | `…independent-audit-v8-20261115.json`（106,061B・`53716d55`） | **2回ともMATCH・2回間byte-identical・AUDIT PASSED** |
| 監査v8 第二実装 | `audit_published_chain_roots_second_independent_v8_20261115.py`（`0cc99112`・86,288B） | `…second-independent-audit-v8-20261115.json`（105,056B・`598cfb8e`） | **2回ともMATCH・2回間byte-identical・AUDIT PASSED** |
| agreement v5 | `audit_dual_implementation_agreement_20261115.py`（`a19a684c`・22,087B） | `…agreement-v5-20261115.json`（24,908B・`c179c9ff`） | **2回ともMATCH・2回間byte-identical・AGREEMENT CONFIRMED** |

再現で独立に確認された主な数値:

- 第一実装v8: **104 pins**（26 base + 52 chain heads + 26 post-70e）、canonical line 1233..1314 **mim 81 / distinct 81 / multi 0**（exactly-once）、bit-78重複rootのexactly-once処理
- 第二実装v8: **100 pins**・606 roots / 595 orbits / 11 twins・canonical 1233..1314
- agreement v5 pair progression: 75d 17 heads/569 roots → 80d 21/587 → 82c 22/592 → 83a 23/596 → 83c pair 25/603 → **83d pair 26 heads / 606 roots / 595 orbits / 11 twins / canon 1233..1314 mim 81**（全pairでbit-78 `00000000100040801202000000200000` が一貫してexactly-once）

機械可読記録: [class2-lane-published-audit-v8-agreement-v5-reproduction-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-published-audit-v8-agreement-v5-reproduction-20261115.json)（4,676 bytes・md5 `dc92cd00`）

## 意義

- 監査v8/agreement v5のlanding session状態を一切使わず、**main bytes単独から3成果物すべてがbyte-identicalに再現**されることを別環境で確認した（82c時点の再現性検証〔commit `40371d4a`〕の83d endpoint版）。
- これにより83d endpointは「fold着地（`1c89d19e`）+ 第二独立fold検証（`def2ddd1`）+ 双実装監査v8 + agreement v5」の**四重検証体制**となった。75d/80d/82c/83a/83b/83c/83dの全7 fold endpointで双実装監査+agreementが成立。

## 解釈境界（重要）

- 監査・agreementはreceipts foldの簿記検証である。solved 1314はmanifest被覆の計数であり、いかなる局面のgame-theoretic値も意味しない。REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 本レーンの再現検証は**mirror HEAD `0a3e0a4b` 時点のpublished出力（blob pin付き）に対して実施**した。push直前の最新main確認で、**cost-62a sweep+foldが15:37:20Zに着地**（commit `f3abc8b3`・62候補・6 WIN7-D10 bits 7/15/35/76/81/98・56 REFUTED・46,968,169 nodes・6証明書二重検証済み・fold head 1318→**1326**/6522/515251/4792/378974・marginal 32/8・second candidate S5 39/2708→34/2368・primary second target S5はdepth-10 receipt limit）していたことを確認した。監査v8/agreement v5の再現対象は83d endpoint（blob pin）であり、この62a着地の影響を受けない。
- 83d endpointのfold baselineはhead **1314**（`class-frontier-cost83d-receipts-recompute-20261115.json`・blob `49cb8022`）。最新のfrontier headは62a fold後の**1326**。
- **cost-84a sweep IN FLIGHT**（並走・claim `59025a50`）は着手禁止。62a着地分は第二検証パターン（tmp有無確認→再構成→統制→2回実行byte-identical）の適用候補。
- 84a着地が揃った時点で監査v9機械拡張（84a/62a endpoint）の着手可否を最新mainで確認。
