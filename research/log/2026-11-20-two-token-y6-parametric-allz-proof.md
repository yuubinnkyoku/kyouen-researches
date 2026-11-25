# 2026-11-20 2トークン残余ゲーム y=6族パラメトリック全称証明（K1127）

## 経緯と選定

- 実行開始時に最新 main を再取得し（着手時点で直近は K1058 円整数論レーンの
  連続コミットと six-row q=8 band-closure の単一オーナー宣言）、AGENTS.md・
  research/knowledge/README.md・未解決事項を再照会した。
- K1126（y=5 パラメトリック全称証明）の「未解決」が明記していた
  「y=6 族の同型機械化（着手前に単一オーナー宣言を先行出版）」が次の一手で、
  単一オーナー宣言ノート
  research/log/2026-11-20-two-token-y6-parametric-allz-single-owner-note.md
  （宣言 2026-11-20T06:02:16.073Z・先行出版）が既に main にあることを確認し、
  宣言ノートの「方針」（cand6 テンプレート導出 → K1126 同型の監査機械 →
  3 実行 byte-identical → 出版）の直接実行として選定した。
- 前段の実行で cand6 導出・検証器構築・全チェック PASS まで到達した状態で
  作業環境が消失したため、本実行では出版済み素材（K1126 検証器 byte 再現・
  K1065/K1077/K1087 出版レポートの anchor 平面）のみから全成果を再構築して
  から出版した（下記）。main へは y=6 関連の先行成果は宣言ノートのみで、
  並走レーン（n11 fold/extract・K1058・six-row q=8）との経路不競合を確認。
- y=6 固定 z 切片は z=8..17 まで出版済み
  （K0993/K0994/K1008・K1055/K1056/K1061/K1062・K1065/K1077/K1087）で、
  この主張はそれらの y=6 行をすべて含意し、z=18,y=6（未着手だった次候補）を
  含む z>=18 の y=6 行を一挙に閉じる。

## 導出（再構築を含む）

- cand6 のテンプレートは y=5 テンプレート（K1126 cand5 の 6 差分族・行クラス
  構造）を y=6 に昇格させる形で導出した。wide fit（生両エンジンとの
  155,595 点照合・bad 0）でまず確定、T-table は初回で完全一致した。
  - マージ行 x<=z-7（S=x+6<=z-1）は単一トークン閉形式そのもの。
  - 基底点 6 点 {z+1,...,z+11}。
  - 対角行 x=z-6 の上端は O[1,z+6]（奇z）/O[1,z+5]（偶z）（格子規則
    r=z+y-[2(z-y)≡0 mod 4] の y=6 値）。
  - 掃引行 x=z+7・帯 O[z+12, x+z+6]（奇z）/O[z+13, x+z+6]（偶z）・
    定常 pin {z+12}/{z+13}（2y+z／2y+z+1）。
  - 前倒し pin：奇z は d∈{-2,2,6}→pin z+8,z+10,z+12、偶z は
    d∈{-4,0,4}→pin z+7,z+9,z+11。y=5 の pin 行と合わせると
    pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4〕の格子公式で統一される
    （横断観察・y<=6）。
  - tail R>=x+z+7 で (x+6) mod 2（偶数 y で値1無限帯が奇数 x 行に戻る）。
- **anchor 転写の優先順位の発見**: 出版済み z=15/16/17（K1065/K1077/K1087）
  の y>=6 一様全 Grundy 分類の closed form を y=6 特殊化する際、
  (i) tail を先に評価する（tail 領域が他のどの場合分けよりも広い）、
  (ii) 場合分けは出版レポートの優先順位を厳守する（z=17〔K1087〕は
  d>=19（=2y+7）の定常帯を他の d 行よりも先に判定する）ことで初めて
  全点一致した。y 行の新規転写では「tail 最優先・d 大きい方から順に
  fallthrough を潰す」が安全な手順である。
- 環境消失後の再構築手順の記録（本実行）:
  1. K1126 出版検証器 verify_y5_universal.py を raw.githubusercontent から
     取得し、SHA-256 3392a8f1...（K1126 出版版）と byte-identical である
     ことを確認（エンジン・single_token・cand5 の正本として再用）。
  2. cand6 を再導出 → wide fit 155,595 点 bad 0（消失前と同趣旨）。
  3. anchor 転写 → self-test 25,578 点 bad 0・C1d 66,297 点 bad 0。
  4. verify_y6_universal.py を再構築（961行・SHA-256 2d75a817...）し
     全 12 チェック PASS（総照合 5,531,469 点・bad 0・実現型 39,383）。
  5. census_rows.py は消失前コードと byte-identical に再現され
     （SHA-256 c41143fb...）、census.txt も byte-identical 再生
     （SHA-256 f69be2b4...・470,600 点・状態数 3,338,636）。
     監査 JSON は同一 cwd 2 回＋別 cwd 1 回＋再構築後の新規環境 1 回の計 4 回
     で byte-identical（SHA-256 ed051639...）。
     消失した「生成物」が出版済みコードとデータの byte レベルで完全復元
     したことは、決定論的監査パイプラインの強度の副次的な実証になった。

## 証明と検証

- K1126 の verify_y5_universal.py を y=6 に適応し verify_y6_universal.py を
  作成（12 チェック構成・C1c なし）。子の評価は出版 cand5（逐語転写）と
  cand6 自身の z 外帰納。
- C1 生エンジン錨（22,050 点）・C1b 子アンカー（47,261 点）・C1d 出版
  z=15/16/17 y>=6 族の y=6 特殊化（66,297 点）・C2/C2b/C12 恒等式グリッド
  （237,405/9,194/1,934,185 点）＋マージ・tail系・C3 選択肢分解アンカー
  （1,365 点）・C4 型機械ボックス±60（644,215 点・実現型 39,383・
  **clip ±14/番兵 ±15**）・C7 seeded 遠方 probe 20万点（seed 20261122）・
  C8 境界多様体（498,387 点）＋tail 値照合・C9 v 空間シェル掃引
  （929,910 点）・C11 生 census アンカー z=0..79（941,200 点）の
  計 5,531,469 照合点（うちマージ系 1,621,917 点・tail 系 360,923 点）で
  全チェック不一致 0。
- **clip 窓の広げ直し**: y=5 機械の ±12/±13 をそのまま使うと中間帯下端
  R-z=2y+2=14 が範囲外、+1 広げた ±13/±14 ではその 14 が番兵 14 と衝突して
  confluence 違反が発生する。±14/±15 で解消した（窓を広げ直す必要が生じた
  初の族。必要 clip 半径の族式候補 2y+2：y=2:6, y=3:8, y=5:12, y=6:14 が
  tight、y=4 の ±12 は余裕付き。y=7 では clip 16/番兵 17 が予想される）。
- 純 Python・標準ライブラリのみ・検証器約 45 秒・census 約 9 秒。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y6-parametric-allz-proof-20261120/
  （report.md・verify_y6_universal.py・census_rows.py・output/audit.json・
  output/census.txt）
- item: research/knowledge/items/K1127-two-token-y6-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1126、
  generalizes K0993/K0994/K1008/K1055/K1056/K1061/K1062/K1065/K1077/K1087。
  K番号は push 直前に 3 点確認（README grep "K1127" 0 件・items パス 404・
  list_commits）で K1127 を取得した）
- index: research/knowledge/README.md に bullet 追加、
  .github/workflows/knowledge.yml に CI audit step 2 件
  （verify_y6_universal.py・census_rows.py・git diff --exit-code）追加。

## 次に開くもの

- y=7 族の同型機械化（着手前に単一オーナー宣言。y=7 は奇数 y で tail・
  マージ行 P の偶奇が y=5 型に戻る。clip 窓 ±16/±17〔2y+2=16〕が予想される。
  B 子は K1127 の cand6・C 子は 1⊕cand7 の z 外帰納で自己完結）。
- 基底点 y 点仮説・tail 開始 x+z+y+1・掃引帯・中間帯・定常pin の族式・
  前倒しpin格子公式 pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4・pin行
  d≡y(奇z)/y+2(偶z) mod 4〕・対角行上端格子規則
  r=z+y-[2(z-y)≡0 mod 4] の一般証明（y<=6 で全称確定済み）。
- 型機械 clip 窓の一般式（必要半径 2y+2 候補の補題化）とボックス外新規型
  ゼロの補題化。
