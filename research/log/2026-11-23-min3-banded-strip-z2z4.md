# run log: min>=3 banded window extension の z∈{2,3,4} クリティカルストリップ拡張・K1272（2026-11-23）

Vibe 高速レーン（定時自律実行・1セッション+出版継続）。前セッション（圧縮前）で
K1272 単一オーナー宣言・機体監査・Commit A まで完了し、本継続セッションで
fetch-back 検証と K item / run log 出版（Commit B）を行った。

## 選定（着手前の最新 main 確認）

- 宣言時 observed HEAD `952897e5`（K1252 non-Miquelian scope note・非接触）。
  認証付き list_commits で直近 12 コミットを点検し、min>=3 strip / 予想C1
  クリティカルストリップ系の対抗着手はなし。K1272〜K1274 items は 404・
  README 最高番号 K1271 を確認して仮採番 K1272 で着手。
- AGENTS.md・SCHEMA.md・K1264/K1268/K1270/K1271 の出版物（report・機体の
  SHA-256 記述）を事前照合。K1268 report が予想 C1 を open problem として登録済みで、
  K1270 item が「残る z>=2 帯は open」を明記・K1271 item が
  「min>=2 側の banded window 拡張との統合」を次課題に挙げていたため、
  クリティカルストリップ z∈{2,3,4} が情報価値最高と判断。

## セッションの流れ

1. **宣言前探査（手転写 engine・宣言ノート §6 に全開示）**: census_strip で
   R2(z) z=0..8 の崩壊掃引（z<=3 崩壊・z=4 で deviant (2,4) を 1 件・z>=5 で複数
   deviant・1回 OOM kill を含む）、census2 で 2トークン cell 表 (m=2..6)×
   (z=0..8) と C(3,4) 201形状、census3 で C(m∈{3..7},z∈{2,3,4}) 371形状ずつ
   （m=8 の乱数塊で 280s timeout 打ち切り）、census4 で次帯 z=5/6 の grid（観測
   として open で保持）と F の分解非依存掃引・D セル 5,517 点の D 式一致。
2. **紙面証明（宣言前・宣言ノート §2）**: F/R2/D を K0832 閉形式からの場合計算で
   閉じる有限 z 梯子を構成し、T-B を選択肢集合一致+m帰納で証明。m=3 では
   この梯子で C1 バンド全域 z<z*(3)=5 が落ちることを確認。
3. **単一オーナー宣言**（publish-then-execute・commit `4be51cb6`）:
   research/log/2026-11-23-min3-banded-strip-z2z4-single-owner-note.md
   ・Lemma U/F/R2/D + T-B・鋭さ・宣言 protocol D1-D7+census・変異電池 B1-B12・
   点数・比較数の宣言総計 21,565 / 64,730 を出版に先立ち全文開示。
4. **機体組立**: build_engine_from_published.py（sha-gate）が出版 K1264 検証器
   `108fdd65…`・出版統合窓機 `0ab66665…`・出版 K1271 機 `1ce7df23…` の3源から
   engine block（2,508B・pin `bd5f22e4…`）を cut・3方 byte 照合で機械挿入
   （PROVENANCE PASS・手転写ゼロ）。機体 SHA-256
   `009184eff1accbaa82cdea9eea5e81253252e6d3681e893b1fd30506d6acad9c`。
5. **監査実行（宣言出版後）**: 宣言 protocol D1-D7 を実行し宣言総計と実測が
   **完全一致**（21,565点 / 64,730比較 / bad 0・D3 deviant 集合 == {(4,)}）。
   D6c census（判定外）: m∈{4..7}×z=5×96形状 = 384点・engine bad 0・崩壊
   96/96×4 m（観測のみ・open 維持）。変異電池 B1-B12 は **12/12 捕捉**
   （B1:494, B2:218, B3:217, B4:216, B5:1, B6:1, B7:1, B8:1, B9:53, B10:570,
   B11:11640, B12:198）。決定性: 同一cwd×2・隔離 tree・`env -i` 別 HOME +
   `PYTHONHASHSEED=random` の4実行で audit.json byte-identical（SHA-256
   `c199946ad562fb7b20f20272a261a58d31cbebc61b7b6caba4c4335c83094af9`）。
6. **Commit A push**（commit `891c70e2a4deb1f92f00976289c161a8d73b8ce6`）:
   実験dir 4ファイル（機体・provenance gate・report・output/audit.json）を出版。
   push前に observed HEAD `701064f1`（inversive handoff log・非接触）を記録して
   競合なしを確認。
7. **fetch-back 検証（本継続セッションで完了）**: main 上の実験dir 4ファイルを
   push チャネルと独立な経路（raw.githubusercontent.com の一括取得）から取得して
   sha256sum 照合 → 4/4 ともローカル pin と byte 一致（機体 009184ef…・
   build b31a3837…・report 6c4d310f…・audit.json c199946a…）。
   Commit A は検証済み。
8. **Commit B（本コミット）**: K item
   research/knowledge/items/K1272-min3-banded-strip-z2z4.md（status proved）と
   本 run log を出版。push前に最新 main を取り直し、log/knowledge 系の
   並走コミット有無を確認（結果は下記）。

## 並走の記録（Commit B 着手時点）

- `701064f1`（inversive handoff log・20:07Z・非接触）。
- `0ba87be4`（batch-28 class 5343 7-LOSS行 adoption Part CO・単一オーナー宣言
  20:10Z・仮採番・本 K1272 と番号衝突なし・宣言中で本レーン Experiment outputs
  を「非接触」と明示的に確認済み）。
- いずれも log/knowledge 系で K1272 命題と重複しない。対抗宣言なし。

## 誠実記録

- 宣言前探査4種（うち OOM kill 1回・timeout 打ち切り1回）は宣言ノート §6 に
  全開示。宣言点数・比較数・deviant期待は protocol 定義からの算術計算であり
  探査実行の数値を参照していない。監査は宣言出版（`4be51cb6`）後に実行
  （publish-then-execute・監査各実行約19秒）。
- 機体組立は placeholder への機械挿入で転写事故なし（挿入後の再 cut ==
  engine block で確認済み）。
- 有限機械監査は証明ではない。全称主張は宣言ノート §2 の紙面証明による。
- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4・
  class 5343 はどの時点でも UNKNOWN のまま。nodes 数・wall 秒数を勝敗として
  読まない。

## 残務（次の候補）

- knowledge README（research/knowledge/README.md）末尾への bullet 追記
  （出版計画ステップ4・別コミット）。
- m>=4 の上位帯 z>=5（E3(z) 梯子の z=5 延長・D6c は grid 上反例不在を観測）。
  F/R2/D 梯子の m=2 行以遠・D セル z>=5 の deviant 構造。
