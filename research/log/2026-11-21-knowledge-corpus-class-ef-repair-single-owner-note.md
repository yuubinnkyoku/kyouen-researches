# 単一オーナー宣言: knowledge corpus class E/F/D 修復（validate 509 → 1）2026-11-21

- 宣言: 2026-11-21T10:10Z（本宣言の出版が宣言時点）
- 宣言時 HEAD: `d173632fc19a3d9f9abf8e66d0595f4629748bf0`
- レーン: `research/experiments/knowledge-corpus-class-ef-repair-20261121/`
- 対象: `research/knowledge/items/*.md` 103 ファイル、
  `research/knowledge/VOCABULARY.yaml`、`research/knowledge/SCHEMA.md`、
  `tools/knowledge/common.py`、knowledge README への bullet 1 件追記

## 作業範囲

直前の class A/B 修復（`83f3eb6b`〜`1e268c33`・load errors 41→0）と
class C renumber（`7f6eafb0`・K1198-K1201）の続きとして、
item 1179 件の validate errors 509 件（class E/F/D）を修復する:

1. **front matter 構造 class E**（count 115 artifact mapping / 100 unknown role /
   71 unknown relation type / 50 unknown fields / 36 invalid relation mapping /
   21 missing fields / 21 topics 非list ほか）: REMO 系 18 item（K0926..K0951）と
   K0980-K0982 の front matter を正規形に全面再構築、`date`/`created`/`tags`
   を `common.py` の許容 field に追加、`VOCABULARY.yaml` に
   topic `frontier-bookkeeping`・`verification_methods` `machine-audit` を追加、
   `SCHEMA.md` に `extends`/`related` 行とメタ資料fieldの明記。
2. **語彙 class F**（unknown relation type / invalid kind / status-by-kind）:
   `related` を relation 語彙に追加、`theorem`→`proposition`（3件）、
   `experiment`→`verification`（28件）、`closed`→`proved`（K0568）、
   `mixed`→`proved`（K0931/K0933）、unknown topics を既存語に写像。
3. **artifact 実在 class D**（4件）: K1033 `scripts/` と K1160 `fresh-runs/` の
   directory artifact を実在 file 単位に展開、K1181 の census script path を
   experiment dir 直下の正しい位置に修正、K1088 の note 無し artifact 4 件に
   role+note を付与。**K1183 `wit_3x23_outer_4.witness.json` は本レーンの管轄外**
   （後述の委譲）。
4. **role 再写像**: corpus 全体の invalid artifact role 96 instance（48 file）を
   正規 role へ写像（record→log・audit→data・document→source ほか）。
5. 生成表（`generated/*.md`・README solution table）の再生成は build.py が
   validate 完全 green を要求するため、K1183 の残 1 error が close するまで
   **実施しない**（views は旧 front matter のまま残る一時状態を明示的に許容）。

## 受入条件（完了の宣言）

1. items 103 ファイル + config 3 ファイルの出版 push ごとに、
   fetch-back（raw pinned URL・SHA-256）で出版 byte と local 正本が一致。
2. 修正後 corpus の validate が load errors 0・validate errors 1
   （K1183 witness のみ・下記委譲）であることが
   独立検証器（census_v3 port・stdlibのみ・PyYAML非依存）で再現可能。
3. 修復 script が base commit `49ad0dbc0a13b77995913584d48986fc14163ae4`
   （items。ただし K1183 は宣言時 HEAD `d173632f` 版）から
   修正後 103 ファイル + config 3 ファイルを byte-exact に再生成すること。
4. fix table（全変換の機械可読記録）と before/after census を
   実験 dir に出版し、第三者が `git ls-tree` と checkout から再現できること。
5. 勝敗・証明状態の変更は一切行わない（11×11 空盤・二石 root {49,60}/{59,60}・
   S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま）。

## K1183 witness file の委譲

`research/experiments/three-row-q4-frontier-20261121/output/wit_3x23_outer_4.witness.json`
は repo 全体に存在せず、宣言時 HEAD の raw fetch でも 404。
K1183 の item と knowledge README bullet は m28 レーン（three-row q4 enumeration・
直近は `d173632f`）が 2026-11-21T09:47Z に更新済みで、witness file の
出版/撤回/参照書き換えのいずれを取るかは K1183 の正本所有者が決定する。
本レーンは K1183 の item byte にも knowledge README の K1183 bullet にも
触れない。K1183 が close した時点で build.py による views 再生成が可能になる。

## 先行宣言の不在確認

宣言時 HEAD `d173632f` の直近 30 commit を機械列挙し、
class E/F/D 修復・role 再写像・VOCABULARY/SCHEMA 拡張を対象とする
単一オーナー宣言・実験 dir・log は存在しないことを確認した
（class A/B・class C は `83f3eb6b`〜`1e268c33`・`7f6eafb0` で既に完結・
post-push verify `49ad0dbc` まで出版済み）。
