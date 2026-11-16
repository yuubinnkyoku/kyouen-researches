# 2026-11-16：head-1441 証明基盤の被覆冗長性監査 — cover multiplicity 1441 orbit全体で測定・単一receipt被覆571 orbit・複数receipt被覆437 orbit・sweep由来433 orbit・最大exclusive依存4 orbit/root・単点依存の集中なし

開始時main: `6719f0c6`（本レーン直前のfold agreement出版）。対象はcanonical head **1441/174/6407/506945/4680/370859**（cost-64g bit-89 fold着地後・`f14f8bdb`）。本監査は**証明基盤の冗長性・独立性の構造を定量化する新規メトリクス**であり、いかなるverdictも変更しない。

## 検証内容（出力 `output/class2-lane-head1441-cover-multiplicity-audit-20261116.json`・schema `n11-class2-lane-head1441-cover-multiplicity-audit-20261116-v1`・git blob `1307b4cc`・決定性2回byte-identical確認済み）

### 方法
- solved集合は本レーンの独立再構成（`independent_cost64g_bit89_fold_agreement_20261116.py` と同一入力・同一verbatim移植frontier semantics）: winners 498（win7-reuse-hits.csv.gz）∪ covers(761 published receipt roots)、bit-89 fold receipt root `00000000020100003800000008080000` を加えた**1441基盤762 receipt roots**。
- head control assert: covered1438 = 1438・covered1441 = 1441 完全一致（match True）。
- 各manifest s6 orbit（solved 1441内）について、それをcoverするreceipt root数（cover multiplicity）とwinners由来の有無を測定。各receipt rootのexclusive contribution（そのrootだけがcoverするmanifest orbit数）も測定。

### 測定結果（1441 solved orbitの内訳）
- **winners由来のみ（sweep WIN7被覆・7石receiptのcoversには非被覆）: 433 orbit（30.0%）**
- **単一receiptのみに被覆（single-cover）: 571 orbit（39.8%）**・cost合計 42,344
- **複数被覆源（冗長）: 437 orbit（30.3%）**・合計multiplicity分布: mult 2が206・mult 3が78・mult 4が51…mult 33までロングテール（合計multiplicity 2は「receipt 2枚」または「receipt 1枚+sweep WIN7 1件」の混合を含む）
- **exclusive contributionを持つreceipt root: 460/762**。最大は root `00000000020000003802002080000000` の4 orbit、次いで3 orbitのrootが4本（`00000000000000809082020000040000`・`00000000000000809082020400000000`・`000000000000008090a2400000000000`・`00000000000000809202000000800008`）。**単一rootへの依存は最大4 orbitで、大きな単点依存の集中は存在しない**。
- 残り302 rootは失効してもsolved不変（完全冗長被覆）。

## 意義

1. **head-1441のsolved 1441 orbitが「何枚の証明書で支えられているか」を初めて全数測定**。multiplicity 1の571 orbitはそれぞれ1枚の独立検証可能なWIN7-D10証明書（またはsweep WIN7 verdict）のみで支えられるが、依存の集中（単root最大4 orbit）はなく、証明基盤に構造的な単点障害がないことを確認。
2. 460 rootがexclusive contributionを持つことは、**以後のreceipt失効監査・conflict検出の重点集合**を与える: この460 rootの証明書照合がsolved 1441の安定性の実効的な最小検証集合。
3. sweep由来433 orbitは7石receiptの被覆構造からは独立な支え（5石parent行のWIN7 swept verdict）であり、receipt系とsweep系の二系統の証明源が1441を支える二重構造を定量的に確認。
4. 本監査は並走のcensus v4（`d5db5e3b`）・cost-65n sweep（in-flight `7dcd9767`）と完全に独立で、被覆測定のみを行いclaimを作らない。

## 解釈境界（重要）

- multiplicity・exclusive contributionは**manifest被覆の簿記の冗長性指標**であり、いかなる位置のgame-theoretic valueも示さない。multiplicity 1は証明書の不足を意味しない（各rootの証明書は独立検証可能・本レーンの過去logで盲抽出・byte-identical照合済み）。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。
- solved 1441はmanifest被覆の簿記。WIN7証明書は個別7石rootのfirst-player win（depth 10以内）のみを証明。REFUTED-D10はLOSS証明ではない。

## 今後

- 次fold（cost-65n行のsweep完走後に並走が実施）着地時は、本監査を再実行してmultiplicity構造の変化（新receiptのexclusive contribution・single-cover orbitの解消）を追跡する。
- 460 exclusive-contribution rootsの証明書blob pin一覧は次回監査の基礎データとして本JSON（blob `1307b4cc`）に保存済み。
