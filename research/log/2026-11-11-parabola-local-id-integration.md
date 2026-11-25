# 2026-11-11 未push剰余放物線項目のK番号統合

remote mainの213a7898dacaf8e662ccb5c3940545e180565cc3には、公開済みの別研究K0723〜K0729が追加されていた。
未pushローカルの剰余放物線項目とK0723〜K0727が衝突したため、origin/mainの番号を保持し、ローカル側を次の通り再採番した。
番号だけの統合であり、数学的命題や証明の採否を変更していない。

| 未pushローカルの旧番号 | 統合後の正本 | 内容 |
|---|---|---|
| K0723 | [K0730](../knowledge/items/K0730-p2539-safe-bound-and-maximal-witness.md) | p2539の1258点安全証人と上界 |
| K0724 | [K0731](../knowledge/items/K0731-p2539-fixed-pair-four-deletion-local-exclusion.md) | 元の完全対を保持する四点削除排除 |
| K0725 | [K0732](../knowledge/items/K0732-p2539-origin-retaining-four-deletion-exclusion.md) | 原点を保持する四点削除排除 |
| K0726 | [K0733](../knowledge/items/K0733-p2539-four-deletion-local-optimum.md) | 全形状の四点削除局所最適性 |
| K0727 | [K0734](../knowledge/items/K0734-p2539-five-deletion-improvement-necessary-shape.md) | 五点削除改善の必要条件、116点除外と26点gate |

現在のknowledge itemのid・ファイル名・relation・本文参照を更新した。K0097とK0702の参照も更新した。
凍結済みexperiment・log中の旧番号は、その時点のローカルIDを表す歴史記録として保持する。
特にREADMEやsourceをhashで結んだ証明・receiptは書き換えていない。旧番号の現在の意味はこの表で解決する。
生成物は正本の統合・衝突解消後にbuild.pyで再生成する。

今回の116点・26点の実験は番号衝突判明前に作成・監査されており、保存済みREADMEの旧K0727は統合後K0734を指す。
他者の未コミットequality_screen_200k.jsonは保持し、取り込んでいない。

統合時にincoming K0724/K0727のtitleに未quoteのコロンがありYAML解析不能、K0728にartifact note欠落があった。
数学的内容は変えずtitleをquoteし、既存sourceの説明noteを補った。
通常の移動参照は現行正本で更新し、6個のhash固定実験README内の7本だけをfrozen_links.jsonで歴史的参照として認識する。
layout検査器は元ファイルSHA-256と現行正本の実在・path範囲を検査し、未登録・hash不一致・移動先不在・範囲外は拒否する。
これはhashに結び付く証拠READMEを書き換えると再現検査が壊れるという、実際に確認された統合上の不都合への限定対応である。
生成物や通常のリンク切れを免除せず、過去のMarkdown表示を書き換えるものでもない。対応表の現行リンクから正本へ移動できる。

統合後は716項目・error/warningとも0、通常36 unittest成功（458.110秒）、生成物再生成一致を確認した。
専用7 layout testでhash不一致、未登録source、移動先不在・範囲外、重複manifest keyを拒否した。
凍結READMEの元bytesは変更しておらず、既存のqualificationやsource hashを維持している。
