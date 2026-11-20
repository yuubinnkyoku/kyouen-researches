# 研究ログ: 残余23行の零triple-providerを行+2点生成で第四の幾何再導出（2026-11-21）

## 経緯

1. **最新main確認**: 着手時のmainは `f8da922b1110b28fc812e06a5674d9940da6a2fe`。K1155（K1151 whole-record第三検証）までを確認し、K1156は未使用。AGENTS.md・knowledge README・SCHEMA・VOCABULARYを確認した。
2. **単一オーナー宣言**: `2026-11-21-n11-residual23-zero-triple-provider-direct-fourth-geometry-single-owner-note.md` をmainへ先行出版（commit `b0db8dfec12b163ec51292922fc5fab4fac3ff66`）。K1147/K1148の既存作業と重ならない「零行だけの行+2点直接生成」に範囲を限定した。
3. **入力固定**: K1148のfixture・第三幾何監査、K1147の外部第二検証監査をmainの `f8da922...` から取得。SHA-256はそれぞれ `51e7a465...`、`526eada2...`、`17dbd6ab...` と一致。
4. **独立計算**: 各零行に対して空き115点から2点を選ぶ全6,555生成を行い、D4正準化、全28子局面の再構成、4×4行列式24置換展開による安全性判定を実施。K1148の3行×8³向き和集合生成器・既存3×3判定述語は呼び出していない。
5. **初回実装の修正**: 最初の試行で、整数rootを辞書キーにした後に16進文字列キーとして参照する型不一致を検出した。公開前に整数キーから32桁16進表現へ明示変換して修正し、修正後の検証器だけを正本とした。
6. **結果**: 12 gate PASS。各零行の三行候補根数は4/5/5、和集合8根、内訳は共円四点あり5・安全だが除外済み3・P'''に残る根0。K1148の8根・被覆行・分類・共円四点座標と完全一致した。
7. **再現性・改ざん検査**: 通常実行・別作業場所・`PYTHONHASHSEED=random` の3実行で監査JSON SHA-256 `c4e55dbe...` が一致。入力fixture offset 100をXOR 0x01で改変するとSHA pin不一致で終了コード1、出力未作成。改変入力SHA-256は `b94877c9...`。

## 数値

- 生成事象: 19,665（3行×6,555）
- 各零行のD4根: 6,555
- 子局面検査: 550,620（19,665×28）
- 三行候補根: 4 / 5 / 5
- 三行候補根の和集合: 8
- 共円四点を含む: 5
- 安全だがREFUTED-D10除外済み: 3
- P'''に残る三行被覆根: 0
- 監査: 12/12 gate PASS、3実行byte-identical

## 解釈

K1147の数え上げ証明書が使う3零行の幾何前提を、K1148とは異なる生成方向で再導出した。P'''の全providerが最大3行を覆うというK1147側の全数集計を前提にすると、零行3つを覆うには少なくとも2根が必要で、残り20行に使える被覆枠は最大19となる。これによりP'''上の8根被覆不可能性の幾何前提を独立に補強する。

ただし、P'''の全provider census・REFUTED-D10除外の妥当性そのものを再計算したわけではない。被覆はゲーム証明書ではなく、行は1行も閉じていない。新規probe・証明書抽出・receipt foldは行っていない。

**標準11×11空盤・二石root `{49,60}` / `{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。**

## 検査上の制約

`uv sync --locked` は成功。スパース作業木でのrepo全体knowledge検査は、既存41項目のYAML/front matter読込エラーに加え、作業木へ展開していないartifact 3,739件があるため全体成功とは扱えない。これらは本変更の外にある既存項目・未展開ファイルであり、本レーンでは改変しない。K1156自身のfront matter・artifact存在・参照先は個別検査する。generated領域は規約どおり直接編集しない。

## リポジトリ検査

- `/usr/local/bin/uv sync --locked`: 成功。
- K1156単体のfront matter・語彙・relation target・8 artifact path検査: PASS。
- スパース作業木の `tools/knowledge/check.py`: 1,098 items / 9,581 errors / 14 warnings。既存41項目のYAML/front matter読込エラーに加え、artifact 3,739件とMarkdownリンク・source pathの未展開が混在するため、完全checkoutの全体検査結果とは扱えない。
- `tools/knowledge/build.py`: 同じ検査エラーで生成前に停止。`research/knowledge/generated/` とroot READMEの生成領域は規約どおり編集していない。
- `tools/knowledge/tests` の全体実行、および `test_knowledge.py` 単独実行は各60秒の実行上限に達し、完了要約を得られなかった。成功扱いにしない。
- K1156の検証器は `py_compile` と12 gateを通過し、3実行の監査byte一致・tamper fail-closedを確認済み。

出版直前のmain再確認では `887e594de70e41290d5db27590d4d971d91b4515` が最新で、K1147外部第二検証のpristine再実行第三検証に対する別スコープの単一オーナー宣言だけが追加されていた。K1156項目は未使用であり、本レーンのK1147/K1148幾何再導出とは重ならない。

## 公開・再取得

- 単一オーナー宣言: `b0db8dfec12b163ec51292922fc5fab4fac3ff66`。
- 実験入力・検証器・監査・README・K1156 item・本ログはmainへ順次直接出版。K1156 item commit: `1d1b185a7de36748d1653a48f1f0ca397a3b75da`、本ログ初版 commit: `ee150508e82fcab767983fa1521d8cfc6948e0b2`。
- knowledge READMEのK1156項目追記: commit `65980eac02a370db535785af0e5326afdd754d71`。
- 同commitのraw公開内容から、実験README・検証器・入力3件・監査・K1156 item・knowledge README・本ログ・単一オーナー宣言の計10ファイルを再取得し、ローカル出版正本と全件byte-identicalを確認。knowledge READMEのSHA-256は `749fa9f5e31d41b0454f62e0b5990bf9b1d083e9957a9670dd875a128d06feb7`。
- K1156を含む最新コミットのcombined statusはstatus/check runが返らず、CI成功とは扱わない。
