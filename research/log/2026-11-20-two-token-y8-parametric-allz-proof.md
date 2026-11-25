# 2026-11-20 2トークン残余ゲーム y=8族パラメトリック全称証明（K1135・旧仮番号K1133から再採番）

## 経緯と選定

- 実行開始時に最新 main を再取得し、AGENTS.md・research/knowledge/README.md・
  未解決事項を再照会した。K1131（y=7 パラメトリック全称証明）の「未解決」が
  明示していた「y=8 族の同型機械化（着手前に単一オーナー宣言を先行出版）」が
  次の一手で、単一オーナー宣言ノート
  research/log/2026-11-20-two-token-y8-parametric-allz-single-owner-note.md
  （宣言 2026-11-20T07:44:44Z・K1131 完成後に先行出版）が main にあることを
  確認し、宣言ノートの方針（cand8 テンプレート導出 → K1131 同型の監査機械 →
  3 実行 byte-identical → 出版）の直接実行として選定した。
- 並走レーン（n11 fold22/23・K1058 AG(2,16)・fold23 機械生成・K0863 系
  修正コミット）と y=8 族の経路不競合を list_commits と README・items で
  確認した（着手時点で README 最大は K1132・y=8 all-z 出版なし・宣言ノート
  のみ・search_code の K1133 表記 0 件だったが、これは検索インデックスの
  stale で、実際には並走 n11 レーンが fold23 に K1133 を使用済みだった
  〔push 後に判明・下記「K番号の再採番」参照〕）。
- y=8 固定 z 切片は z=6,8,9,10 の境界切片（K0888・K0996・K0998・K1010 の
  y=8 行）と z=15,16,17 の y>=6 一様族（K1065/K1077/K1087）が出版済み。
  この主張はそれらをすべて含意し、z=18,y=8（未着手）を含む z>=18 の
  y=8 行を一挙に閉じる。

## 導出

- cand7 対応の K1131 機材を取得し、SHA-256 照合
  （verify_y7_universal.py = 9200b591...・census_rows (y=7) =
  cbaa11fb...）。y=7 検証器は本環境で再実行し 12 チェック PASS を確認した
  後、cand7 を逐語転写した。
- cand8 のテンプレートは、生エンジン probe（z=0..40・x=8..z+30・
  R<=x+z+40 の 167,280 点）から T/P 表を構造抽出し、**初回適合で
  mismatch 0・T/P overlap 0**（y=6・y=7 で見られた「fit の唯一の修正行」
  が y=8 では存在しない。y=6 の偶z d=2 行・y=7 の偶z d=3 行の破れは
  値1無限帯の偶奇規則（y 偶なら x 奇行）で消える位置に y=8 の行クラスが
  なるため）。
  - マージ行 x<=z-9（S=x+8<z-1）は単一トークン閉形式そのもの。
    probe 全域で merge 命題の不一致も 0（167,280 点・mgBad 0）。
  - 基底点 8 点 {z+1,...,z+15}（y 点仮説の y=8 版）。
  - 対角行 x=z-8 の上端は O[1,z+8]（奇z）/O[1,z+7]（偶z）（格子規則
    r=z+y-[2(z-y)≡0 mod 4] の y=8 値。2(z-y)=2z-16≡0 mod 4 ⟺ z 偶）。
  - 掃引行 x=z+9・帯 O[z+16, x+z+8]（奇z）/O[z+17, x+z+8]（偶z）・
    定常 pin {z+16}/{z+17}（2y+z／2y+z+1）。
  - 前倒し pin：奇z は d∈{-4,0,4,8}→pin z+10,z+12,z+14,z+16・偶z は
    d∈{-6,-2,2,6}→pin z+9,z+11,z+13,z+15。格子公式
    pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4〕が y=5,6,7 に続き y=8 でも成立
    （4 族連続）。pin 行の d は d≡y (mod 4)（奇z）・d≡y+2 (mod 4)（偶z）。
  - pin 行（y=8 奇z d=8 行）の値1点 z+17（2y+z+1）は y=6 の d=7 行に
    対応する y 偶型の追加点。
  - tail R>=x+z+9 で (x+8) mod 2（偶数 y で値1無限帯が奇数 x 行。
    y=2,4,6 と同型）。
- 出版 z>=15 切片アンカーの転写は「tail 最優先・場合分けは出版優先順位
  厳守」で行い、K1065（z=15）・K1077（z=16）・K1087（z=17）の y>=6 一様
  分類を Y=2y=16・S=x+8 引数変換で y=8 特殊化した。z=16 の (8,0) 縮退セル
  （T=O[1,23]・P 空）と z=17 の merge セル（S=16<17 は O[1,S-1]・P 空）・
  S=17 行（d=1 は O[1,25] に到達）を出版どおり特殊化して手計算で全 d 跨って
  照合後、検証器 C1d で機械照合した（アンカー 65,826 点相当・bad 0）。
  加えて各切片の低R単一トークン縮約 R<=z+6 の y=8 行照合を追加
  （z=15,16,17 で R<=21,22,23・bad 0）。

## 証明と検証

- K1131 の verify_y7_universal.py を y=8 に適応し verify_y8_universal.py を
  作成（12 チェック構成・CLIP=18/SENT=19）。子の評価は出版 cand7（逐語転写）
  と cand8 自身の z 外帰納。x=8 では A≡B=cand7(z,8,R-1)（(7,8)≡(8,7) 合流）。
- C1 生エンジン錨（22,680 点）・C1b 子アンカー（44,886 点）・C1d 出版
  z=15/16/17 y>=6 族の y=8 特殊化＋低R縮約（75,924 点）・C2/C2b/C12 恒等式
  グリッド（230,496/9,282/1,914,220 点）＋マージ・tail系・C3 選択肢分解
  アンカー（1,224 点）・C4 型機械ボックス±60（635,394 点・ボックス実現型
  73,529・全走型 73,685・**clip ±18/番兵 ±19＝K1127/K1131 予想 2y+2 の的中**
  ・±17/±18 では中間帯下端 R-z=18 が番兵と衝突して confluence 違反）・
  C7 seeded 遠方 probe 20万点（seed 20261123・tail 境界 x+z+9 を跨ぐ窓込み）・
  C8 境界多様体（643,475 点・dx∈[-19,11]・tail 窓 [x+z+9, x+z+11]）・
  C9 v 空間シェル掃引（925,254 点）・C11 生 census アンカー z=0..79
  （922,320 点・両エンジン・cache clear エンジン間）の計 5,625,155 照合点
  （うちマージ系 1,558,050 点・tail 系 330,477 点）で全チェック不一致 0。
- 純 Python・標準ライブラリのみ・検証器約58秒・census 約14秒。
- 再現性: 同一 cwd 2 回＋別 cwd 別ディレクトリ・別 HOME 1 回の計 3 回実行で
  audit.json（SHA-256 06694603...）が byte-identical。census.txt
  （a91cd438...）は raw 生成そのもので、T/P 全リスト（461,160 点）が
  cand8 表と独立照合スクリプトで完全一致。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y8-parametric-allz-proof-20261120/
  （report.md・verify_y8_universal.py・census_rows.py・output/audit.json・
  output/census.txt）。ローカル正本の SHA-256（verify = bcad4148...・
  census_rows = 2213070b...・audit.json = 06694603...・
  census.txt = a91cd438...）を出版後に GitHub 取り直し分と照合する。
- item: research/knowledge/items/K1135-two-token-y8-parametric-allz-universal-proof.md
  （kind: proposition, status: proved。relations: depends_on K0832/K1131、
  generalizes K0888/K0996/K0998/K1010/K1065/K1077/K1087（いずれも y=8 行の
  特殊例化）。K番号は push 直前に再取得で確認したが search_code のインデックス
  遅延で fold23 の K1133 を見逃した。push 後に ID 重複を検出し、AGENTS.md の
  再採番規約（main の既存 K1133 〔fold23〕・K1134 〔6×m q=8 band〕は変更せず、
  後発の本項を再採番）により K1133 から K1135 に再採番した）。

## K番号の再採番（統合時対応）

- コミット1（実験dir・item・log・audit、29fbe13e）の push 時点では、
  並走 n11 レーンの fold23 item（research/knowledge/items/
  K1133-n11-residual29-win8-receipt-fold-root208090020004.md・26168d3d で
  先行出版済み）が main に存在していたが、push 直前確認に使った
  search_code（K1133 query）が 0 件を返した（インデックス stale）。
  コミット2（census.txt、5b7c0b48）後に README を再取得して重複
  （K1133 が2 item・K1134 も n6q8 band が使用済み）を検出した。
- 対応: AGENTS.md「統合時に main 上の番号と衝突する新規項目を再採番し、
  その項目を参照する新規 relation や Markdown 参照も更新する。main に
  既に存在する K番号は変更しない」に従い、本項を K1135 に再採番
  （item id・log・README bullet・CI step 名を更新。report.md・
  verify_y8_universal.py・census_rows.py・audit.json・census.txt は
  そもそも K1133 表記を含まないため byte 不変）。
- index: research/knowledge/README.md に bullet 追加、
  .github/workflows/knowledge.yml に CI audit step 2 件
  （verify_y8_universal.py・census_rows.py・git diff --exit-code）を
  K1131 census step の直後に追加。

## 次に開くもの

- y=9 族の同型機械化（着手前に単一オーナー宣言。y=9 は奇数 y で tail・
  マージ行 P の偶奇が y=7 型（x 偶行）に戻る。clip 窓 ±20/±21〔2y+2=20〕が
  予想される。B 子は本項の cand8・C 子は 1⊕cand9 の z 外帰納で自己完結）。
- 横断法則（基底点 y 点・tail 開始 x+z+y+1・掃引帯・中間帯・定常pin・
  前倒しpin格子公式 pin=2y+((x-y)+z)/2〔(x-y)+z≡2 mod 4〕・対角行上端
  格子規則 r=z+y-[2(z-y)≡0 mod 4]）の一般証明レーンの開設
  （y<=8 で全称確定・y=5..8 で pin 格子公式 4 族連続）。
- 型機械 clip 窓の一般式（必要半径 2y+2 候補の補題化。y=5..8 で 4 族連続
  tight・3 予想連続的中）とボックス外新規型ゼロの補題化。
