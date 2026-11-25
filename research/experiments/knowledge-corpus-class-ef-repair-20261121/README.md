# knowledge corpus class E/F/D 修復（validate 509 → 1）2026-11-21

- 単一オーナー宣言: `research/log/2026-11-21-knowledge-corpus-class-ef-repair-single-owner-note.md`
  （2026-11-21T10:10Z・宣言時 HEAD `d173632fc19a3d9f9abf8e66d0595f4629748bf0`・受入条件5項目）
- 前段: class A/B load 修復（commit `83f3eb6b`..`1e268c33`・load errors 41→0）と
  class C renumber（`7f6eafb0`・K1198-K1201）は並走レーン完了済み。
  item 1179 件の残 validate errors 509 件（class E/F/D）を本レーンで修復する。

## 目的

knowledge corpus の validate を、K1183 の witness file 1 件を除く全 error について
green にする。これにより build.py による views 再生成と、以後の corpus 追加が
validate green 前提で進められる状態を作る。内容的な新知見は出さない
（item の数値・命題・関係の意味は不変。front matter の表記と語彙のみ修正）。

## 手法

- corpus 全体（item 1,179 件 + VOCABULARY/SCHEMA/common.py）を base commit
  `49ad0dbc0a13b77995913584d48986fc14163ae4` から raw 直取得で再構成
  （K1183 だけは宣言時 HEAD `d173632f` 版に差し替え。`d173632f` が触れたのは
  K1183・knowledge README・session log の 3 file のみで corpus 他部分は同一）。
- 検証器 `census_v3_classE.py` は公式 `tools/knowledge/check.py`（load_items + validate）
  の PyYAML 非依存 port。file 実在は `tree_manifest.txt`（宣言時 HEAD `d173632f`
  の repo tree・7,316 path）を oracle に代用する（公式器は実際の checkout を参照。
  両者は artifact 参照 22 probe の raw 存在確認で一致を確認済み: 21 exist・1 404
  = K1183 witness）。
- 修復は `repair_items.py` が base tree に対して決定的に適用する。
  byte 再現性を実測で確認してから出版した（下記「検証」）。

## 修正分類（509 error の内訳と fix）

before census（`output/census-before-classEF.json`）の 509 error は:

| class | count | 内容 | fix |
|---|---:|---|---|
| E-front | 115 | artifact must be a mapping（文字列path直書き） | front 再構築・path+role+note 三点組化 |
| E-role | 100 | unknown artifact role（record/audit/document 等） | 正規 role へ写像（96 instance・48 file） |
| E-reltype | 71 | unknown relation type（connects/see_also/relates_to/uses） | `related` 語彙追加 + `depends_on`/`related` へ写像 |
| E-fields | 50 | unknown fields（date/created/tags） | common.py 許容 field 追加 + SCHEMA.md 明記 |
| E-relstruct | 36 | invalid relation mapping（単key複数target形式） | 正規エントリ形式へ展開 |
| E-kind | 31 | invalid kind（theorem/experiment） | theorem→proposition 3・experiment→verification 28 |
| E-topics | 63 | missing/topics非list/空/unknown topic（21×3） | REMO 群 topics 再設定・語彙追加・写像 |
| F-status | 9 | invalid status・status-by-kind 不一致 | closed→proved 1・mixed→proved 2 |
| F-sol | 1 | invalid solution.verification | `machine-audit` 語彙追加 |
| F-alias | 1 | aliases must be a list | K0937 alias list 再設定 |
| D-path | 4 | artifact missing（実在しない path・directory 指し） | K1033/K1160 directory 展開・K1181 path 修正（3 fix）+ K1183 deferred |

警告（19→16）: K0980-K0982 の thin evidence 3 件が
role+note 付き artifact 追加により解消（新規警告なし）。

修正の機械可読な全記録が `output/fix-table.json`
（21 front 再構築・45 raw/block edit・96 role instance・6 config edit・注記: 修正を
受ける item は合わせて 103 file）。

## K1183 の委譲（deferred）

`research/experiments/three-row-q4-frontier-20261121/output/wit_3x23_outer_4.witness.json`
は repo 全体に存在しない（raw 404）。K1183 item と README bullet は直前
09:47Z に m28 レーンが更新済み（`d173632f`・witness-free 幅 {24..31}）で、
witness 参照の処方は K1183 正本所有者が決める。本レーンは 1 error を
「残 1・所有者 m28」として明示的に残し、build.py views 再生成を
K1183 close まで延期する。

## 再現手順

full checkout 保持者は公式器で同一結果が得られる:

```
python3 tools/knowledge/check.py   # 修正後: errors = K1183 witness の 1 件のみ
```

PyYAML 非依存側の再現:

1. base item 1179 file（`49ad0dbc`、K1183 は `d173632f` 版）+
   base VOCABULARY.yaml/SCHEMA.md/common.py 3 file（`49ad0dbc`）を
   raw pinned URL から取得して mirror を組み、`tree_manifest.txt` に
   checkout の実 file 一覧を置く。
2. `python3 scripts/census_v3_classE.py <mirror>` → before census
   （`output/census-before-classEF.json` と byte 一致）。
3. `python3 scripts/repair_items.py <mirror> <fix-table.json>`。
4. `python3 scripts/census_v3_classE.py <mirror>` → after census
   （`output/census-after-classE.json` と byte 一致: load 0 / errors 1 / warnings 16）。

## 検証（出版前実測）

- 修復 script を clean mirror に再適用し、修正後 103 item file と
  config 3 file が出版正本（root mirror）と全 file byte-exact で一致。
- after census の再生成 2 回が出版 byte と一致（`sort_keys` 決定的出力）。
- fix-table の raw_edits/rewrites/role_rewrites は修復適用時 log と同一内容。
- 公式 `build.py` は validate errors 非空で abort する設計のため、views 再生成は
  K1183 close 後に別レーン/次回が実施する（本レーンでは実行しない）。

## 解釈規約

本修復は corpus の構造整合のみを扱う。数値・命題・証明構造は不変。
修正対象 item のどの結果も勝敗や証明状態を変えない。
**標準11×11空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま。**
