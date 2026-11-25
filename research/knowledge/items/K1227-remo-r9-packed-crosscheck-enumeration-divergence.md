---
id: K1227
title: K0893 r=9 packed記録のK0864 verbatimエンジンによる独立部分交差検証（6457/15863件・survivors/first_losers/determined全一致・13件はstates数も一致）と、K0869系/K0862系正準列挙の相互非互換（先頭125件のみインデックス一致・i=125以降はatoms経由のreindexが必要）
kind: verification
status: verified
topics: [variants, multiplayer, verification]
aliases: [r9 packed records independent crosscheck, canonical enumeration order divergence]
relations:
- type: verifies
  target: K0893
  note: r=9 cap≤10完全スイープのpacked記録を、別実行のK0864 verbatim Pythonエンジンによる6457/15863プロファイルの新規計算とプロファイル単位で比較（survivors/first_losers/determined 0不一致・13件はreachable-state数も一致）。K0893のpacked bytesから34失敗キー・34行分割表・剰余センサス57/336/322・一様決定98/一様非決定583/mixed 34・max_states 363,630の独立再解析も全一致
- type: depends_on
  target: K0864
  note: 交差検証に使用したverbatim region-gameエンジンと補題FL（本検証では 冗長アンカー・スナップショット6457件で違反0）
- type: depends_on
  target: K0862
  note: 比較に使用した2つの正準列挙（direct_constrained系とenumerate_profiles系）とBurnside計数の系譜
- type: related
  target: K0869
  note: r=8 compactが使う列挙順序（K0862系direct_constrainedとは先頭125件のみ一致）の非互換を記録。K0869の値・statusは不変
- type: related
  target: K0881
  note: K0876/K0881のpacked r=2..8記録もK0862系列インデックスを使用しており、K0869系とのrawなper-index結合は不能（r≤8のreindex表は本項では出版しない）
artifacts:
- path: research/experiments/remo-k-branch-cap10-r9-independent-crosscheck-20261122/README.md
  role: proof
  note: 経緯（単一オーナー宣言049d7d1cの撤回を含む）・結果3点・等価性根拠・限界
- path: research/experiments/remo-k-branch-cap10-r9-independent-crosscheck-20261122/verify_crosscheck_r9_partial.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ。9機械チェック（Burnside/両列挙集合一致・phi全単射・スナップショットとpackedのsha256ピン・6457件3フィールド交差検査・13件states witness live・先頭12件live結合・FL/Δ=0アンカー・K0893 pinned定数のpacked再解析）全合格・二重実行でaudit byte同一
- path: research/experiments/remo-k-branch-cap10-r9-independent-crosscheck-20261122/output/r9_python_partial_verdicts.jsonl
  role: data
  note: 独立計算のr=9 verdictスナップショット6457レコード（K0869系列インデックス・atomsはiから純関数再導出・sha256 f8fffc4602e3efa62ccf7d726c53a87f6f6bc7614dc90a610db8da9f65640e06・422,048 bytes）。初回push 3de9e95eではパイプライン読み取り上限により981行に打ち切られていたが、9759774bで完全版を再pushしfetch-backでbyte同一を確認済み（実験READMEのerratum参照）
- path: research/experiments/remo-k-branch-cap10-r9-independent-crosscheck-20261122/output/crosscheck_r9_partial_audit.json
  role: data
  note: 監査JSON（sha256 2a6846b81b17641c7fa75797f71b2c030aca60522f97f21f79aec9332cdfc95c・二重実行byte同一）
scope: '3枝REMO（cap≤10・15863正準プロファイル・r=9）について、(a) K0893出版packed記録とK0864 verbatimエンジンの別実行による新規計算6457/15863プロファイルがsurvivors/first_losers/determinedの3フィールドで完全一致し、うち13件はreachable-state数も一致すること、(b) スナップショット上で補題FL剰余が違反0、Δ=0プロファイル267件が定理D再帰のr=9列と一致すること、(c) K0893 pinned定数（34失敗キー・分割表・剰余センサス・センサス・max_states）がpacked bytesからK0862系列列挙の下で再導出されて全一致すること、(d) K0869系列挙とK0862系列挙が同一の15863プロファイル集合を異なる順序で列挙し、インデックスは先頭125件（0..124）でのみ一致すること（i=125以降は非一様なずれ・オフセット変化点1098個）を確認する。交差検証は部分（約41%）でありK0893全体の再証明ではない。順位決定性フィールドはJS側に存在せず交差検証しない。r・cap・盤面の値主張を一切変更しない'
evidence: '公開検証器verify_crosscheck_r9_partial.py（自己完結・決定的・stdlibのみ・外部入力なし）の9機械チェック全合格・assemble二重実行でaudit byte同一（sha256 2a6846b81b17641c7fa75797f71b2c030aca60522f97f21f79aec9332cdfc95c）。交差検査は6457レコードのスナップショット（sha256 f8fffc46…・K0869系列インデックス順・atomsはiから純関数）とK0893 committed packed記録（sha256 a2bb16bc…をbyte検証）をatoms一致の全単射phiで対応付けて実行し、survivors/first_losers/determinedの不一致0/0/0。states witness 13件（i=120..132・両系の到達状態数も一致）とスナップショット先頭12件はverbatimエンジンのlive再実行でコミットフィールド（order_determined・o0込み）と照合。列挙Aは枝刈り版を使用（filter合否はorbit repで不変・枝刈り候補のrepはkept候補のrepと一致し得ない・巡回順序不変の3点の等価性、およびverbatim構成との15863件全順序一致をオフライン検証）。当初のper-index比較は列挙非互換を約80%のverdict不一致と誤読した（atoms一致の下では0不一致）ことを記録し、両系iのraw結合禁止を運用規則として明記する。限界: 部分交差検証（6457/15863）・順位決定性はJS側に無く検証対象外・r≤8のreindex数値表は出版せず・K0893/K0869本文とstatusは不変'
---

# K0893 r=9 packed記録の独立部分交差検証と列挙順序非互換の記録

## 経緯

2026-11-22の高速レーンは「3枝REMO決定性のr=9境界」を単一オーナー宣言
（`049d7d1c`）の下で開始したが、**K0893〔2026-11-17〕が宣言スコープの
全内容をすでに出版済み**であることが掃引後に判明した（r=8境界のK0869
までしか遡らずcap10-r9実験dir/K0893項を検索しなかった起因）。
宣言は撤回（session log参照）し、掃引で得たK0864 verbatimエンジンの
新規r=9計算資産（6457プロファイル・予算スキップ0）を独立交差検証に転用
した。

## 結果

- **交差検証（部分）**: スナップショット6457/15863プロファイルと
  K0893 packed記録をatoms一致の全単射phiで比較し、
  survivors/first_losers/determinedの3フィールドすべてで不一致
  0/0/0。13件（i=120..132）はPython verbatimエンジンの
  reachable-state数とJS maskエンジンのstates数も一致
  （C6 witness・live再実行で検証器が固定定数と照合）。
- **アンカー**: FL剰余 6457/6457違反0（K0864の全称証明の冗長
  アンカー）。Δ=0プロファイル267件が定理Dのr=9列と全一致。
- **K0893 pinned定数の独立再解析**: packed bytesからK0862系列
  列挙のキー集計で34失敗キー（完全一致）・34行の分割表（全行一致）・
  剰余センサス57/336/322・一様決定98/一様非決定583・mixed 34・
  max_states 363,630を再導出し全一致。K0893検証器はlive
  engine再実行中心のため、この統計再導出は独立系統。
- **列挙順序の非互換（運用事実）**: K0869 r=8 compactと
  K0893（K0875/K0876/K0881/K0862系）packedは同一15863プロファイル
  集合を異なる順序で列挙。インデックスは0..124のみ一致し125以降
  ずれる（オフセット変化点1098個）。**両系のiをrawで結合しては
  ならない**（atomsまたは検証器が再導出するphiで対応付ける）。
  当初の比較がこの非互換を約80%の「verdict不一致」と誤読した
  （atoms一致では0）ことが、この規則の動機である。

## 限界

- 交差検証は部分（約41%）。K0893全体主張の再証明ではない。
- 順位決定性はJSエンジンに存在しないため交差検証しない
  （K0893自身と同じ制限。order欄はC7でsnapshot⇔verbatim再実行のみ）。
- r≤8のreindex数値表は出版しない（機材を示したので再導出可能）。
- K0893/K0869の本文・status・値は不変。標準11×11空盤・二石root・
  S2・class 1/2/4は本項と無関係でUNKNOWNのまま。
