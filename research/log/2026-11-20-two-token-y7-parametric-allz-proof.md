# 2026-11-20 2トークン残余ゲーム y=7族パラメトリック全称証明（K1131）

## 経緯と選定

- 実行開始時に最新 main を再取得し、AGENTS.md・research/knowledge/README.md・
  未解決事項を再照会した。K1127（y=6 パラメトリック全称証明）の
  「未解決」が明示していた「y=7 族の同型機械化（着手前に単一オーナー宣言を
  先行出版）」が次の一手で、単一オーナー宣言ノート
  research/log/2026-11-20-two-token-y7-parametric-allz-single-owner-note.md
  （宣言 2026-11-20T07:02Z・K1127 完成直後に先行出版）が main にあることを
  確認し、宣言ノートの「方針」（cand7 テンプレート導出 → K1127 同型の
  監査機械 → 3 実行 byte-identical → 出版）の直接実行として選定した。
  並走レーン（n11 fold/extract・K0893 r=9 境界など）と y=7 族の経路不競合を
  list_commits と README・items で確認した（着手時点で README 最大は K1130・
  y=7 all-z 出版なし・宣言ノートのみ）。
- y=7 固定 z 切片は z=6..17 まで出版済み
  （K0887・K0976・K0995/K0997/K1009・K1055/K1056/K1061/K1062・K1065/K1077/
  K1087 の y=7 行）。この主張はそれらをすべて含意し、z=18,y=7（未着手の
  次候補）を含む z>=18 の y=7 行を一挙に閉じる。

## 導出

- cand6・cand5 対応の K1126/K1127 機材を取得し、SHA-256 照合
  （verify_y6_universal.py = 2d75a817...・census_rows (y=6) = c41143fb...）。
  y=6 検証器は本環境で 12 チェック PASS（総 5,531,469 点・約49秒）。
- cand7 のテンプレートは K1023/K1126/K1127 と同じ手順で、生 census 行
  ダンプからの構造判読で導出した（derive7 → fit7：z=0..89・d∈[-22,15)・
  R<=x+z+16 の 329,655 点 wide fit・bad 0。z>=90 の raw 展開はメモリ上限で
  断念したが、出版 y=6 機械の raw 範囲〔z<=79+境界〕と同等の fit 被覆で
  十分）。
  - マージ行 x<=z-8（S=x+7<z）は単一トークン閉形式そのもの。
  - 基底点 7 点 {z+1,...,z+13}（y 点仮説の y=7 版）。
  - 対角行 x=z-7 の上端は O[1,z+6]（奇z）/O[1,z+7]（偶z）（格子規則
    r=z+y-[2(z-y)≡0 mod 4] の y=7 値）。
  - 掃引行 x=z+8・帯 O[z+14, x+z+7]（奇z）/O[z+15, x+z+7]（偶z）・
    定常 pin {z+14}/{z+15}（2y+z／2y+z+1）。
  - 前倒し pin：奇z は d∈{-5,-1,3,7}→pin z+8,z+10,z+12,z+14・偶z は
    d∈{-3,1,5}→pin z+9,z+11,z+13。格子公式 pin=2y+((x-y)+z)/2
    〔(x-y)+z≡2 mod 4〕が y=5,6 に続き y=7 でも成立（3 族連続）。
  - tail R>=x+z+8 で (x+7) mod 2（奇数 y で値1無限帯が偶数 x 行に戻る）。
  - **fit の唯一の修正行**: 偶z d=3 行（x=z+3）は b6 のみで無限帯 I[z+13]
    を持たない（対称な素朴外挿が最初に破れた行。値1無限帯の「y 奇なら
    x 偶行」規則で自然に説明される）。
- 出版 z>=6 切片アンカーの転写は K1127 と同じ「tail 最優先・場合分けは
  出版優先順位厳守」で行い、K1065（z=15）・K1077（z=16）・K1087（z=17）の
  y>=6 一様分類を Y=2y=14・S=x+7 引数変換で y=7 特殊化して hand-check で
  数十行照合後、検証器 C1d で機械照合した（66,096 点 bad 0）。加えて各切片
  の低R単一トークン縮約 R<=z+6 の y=7 行照合を追加した（10,098 点 bad 0）。

## 証明と検証

- K1127 の verify_y6_universal.py を y=7 に適応し verify_y7_universal.py を
  作成（12 チェック構成）。子の評価は出版 cand6（逐語転写・byte 照合）と
  cand7 自身の z 外帰納。
- C1 生エンジン錨（22,365 点）・C1b 子アンカー（46,086 点）・C1d 出版
  z=15/16/17 y>=6 族の y=7 特殊化＋低R縮約（76,194 点）・C2/C2b/C12 恒等式
  グリッド（233,975/9,242/1,924,263 点）＋マージ・tail系・C3 選択肢分解
  アンカー（1,188 点）・C4 型機械ボックス±60（639,859 点・実現型 54,762・
  **clip ±16/番兵 ±17＝K1127 予想 2y+2 の的中**）・C7 seeded 遠方 probe
  20万点（seed 20261123・tail 境界 x+z+8 を跨ぐ窓込み）・C8 境界多様体
  （581,526 点・dx∈[-17,10]・tail 窓 [x+z+8, x+z+10]）・C9 v 空間シェル
  掃引（927,594 点）・C11 生 census アンカー z=0..79（931,840 点）の
  計 5,594,132 照合点（うちマージ系 1,589,081 点・tail 系 359,738 点）で
  全チェック不一致 0。
- 型機械 clip 窓の確認: ±15/±16 では中間帯下端 R-z=2y+2=16 が番兵 16 と
  衝突して confluence 違反が発生し、±16/±17 で解消（窓広げ直し要否の
  予想〔y=7 では clip 16〕が K1127 通り的中。族式候補 2y+2 は
  y=5:12,y=6:14,y=7:16 で 3 族連続 tight）。
- 純 Python・標準ライブラリのみ・検証器約49秒・census 約11秒。
- 再現性: 同一 cwd 2 回＋別 cwd 別プロセス（/tmp）1 回の計 3 回実行で
  audit.json（SHA-256 a9893a15...）・census.txt（b161142e...）とも
  byte-identical。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y7-parametric-allz-proof-20261120/
  （report.md・verify_y7_universal.py・census_rows.py・output/audit.json・
  output/census.txt）
- item: research/knowledge/items/K1131-two-token-y7-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1127、
  generalizes K0887/K0976/K0995/K0997/K1009/K1055/K1056/K1061/K1062/K1065/
  K1077/K1087（いずれも y=7 行の特殊例化）。K番号は push 直前に再取得で
  確認（README 最大 K1130・K1131 未使用））
- index: research/knowledge/README.md に bullet 追加、
  .github/workflows/knowledge.yml に CI audit step 2 件
  （verify_y7_universal.py・census_rows.py・git diff --exit-code）追加。

## 次に開くもの

- y=8 族の同型機械化（着手前に単一オーナー宣言。y=8 は偶数 y で tail・
  マージ行 P の偶奇が y=6 型に戻る。clip 窓 ±18/±19〔2y+2=18〕が予想される。
  B 子は K1131 の cand7・C 子は 1⊕cand8 の z 外帰納で自己完結）。
- 基底点 y 点仮説・tail 開始 x+z+y+1・掃引帯・中間帯・定常pin・前倒しpin
  格子公式 pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4・pin行 d≡y(奇z)/y+2(偶z)
  mod 4〕・対角行上端格子規則 r=z+y-[2(z-y)≡0 mod 4] の一般証明
  （y<=7 で全称確定済み・y=5..7 で pin 格子公式 3 族連続）。
- 型機械 clip 窓の一般式（必要半径 2y+2 候補の補題化）とボックス外新規型
  ゼロの補題化。
