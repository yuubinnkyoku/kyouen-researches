# 2026-11-20 2トークン残余ゲーム y=9族パラメトリック全称証明（K1138 observed→proved 昇格）

## 経緯と選定

- 実行開始時に最新 main（HEAD 1196ec8ed・2026-11-20T09:34:42Z）を再取得し、
  AGENTS.md・research/knowledge/README.md・未解決事項を再照会した。
  単一オーナー宣言ノート
  research/log/2026-11-20-two-token-y9-parametric-allz-single-owner-note.md
  （宣言 2026-11-20T08:41:00Z）が main にあり、同宣言が保持する残工程
  （正本監査・census・出版）が未完であることを確認した。
- 同じ高速レーンの前回実行は JS サンドボックスで実行制約があり、
  y=9 fit（K1138・cand9.py 出版）と JS 12チェック予備検査（仕様確定・
  全 bad=0）までで終了していた。本実行は Python 3.12 実行環境で動くため、
  宣言ノートが残した正本 verify_y9_universal.py の構築・実行・出版を
  直接実行する形で選定した（宣言ノートと前回実行の same-owner 継続。
  並走レーン〔n11 residual29 / inversive K1058 / AG(2,16) / y10 skeleton
  survey〕と経路不競合を README・items・log で確認）。
- 前回 JS 予備検査が確定した仕様（12チェックの点数・構成・seed 20261123・
  CLIP=20/SENT=21 予想・C1d 6切片アンカー・低R縮約 R<=z+6）は本 Python 正本
  にそのまま引き継ぎ、結果も全一致した
  （research/log/2026-11-20-y9-universal-machine-js-preflight.md）。

## 導出と前検証（cand9 は fit 出版の逐語転写）

- 出版 cand9.py（main・SHA-256 6c3e9242...）を逐語転写し、z=0..14・x=9..40・
  R<=x+z+46 の 17,034 点を raw 順序保持エンジンと照合（bad 0）。
- C1d アンカー 6 切片の y=9 特殊化を raw エンジンで事前照合:
  A8y9（K0999/K1000・z=8 逐語・34,038 点）・A9y9（K1001・z=9）・
  A10y9（K1002/K1011・z=10・y>=6 の y=9 行）・A15y9/A16y9/A17y9
  （K1065/K1077/K1087・z=15/16/17・Y=2y=18・S=x+9 の引数変換・tail 評価
  最優先・過渡セルは y=9 では 2y+d>17 で全て消滅）。各 34,038 点 bad 0。
- x=9 では A≡B=cand8(z,9,R-1)（(8,9)≡(9,8) 多重集合合流・K1135）。

## 証明と検証

- K1135 の verify_y8_universal.py を y=9 に適応し verify_y9_universal.py
  を作成（12 チェック構成・CLIP=20/SENT=21）。子の評価は出版 cand8
  （逐語転写）と cand9 自身の z 外帰納。
- C1 生エンジン錨（22,995 点）・C1b 子アンカー（43,692 点）・C1d 出版
  z=8/9/10/15/16/17 の y=9 特殊化＋低R縮約 R<=z+6（yz アンカー 131,370＋
  lowR 9,966 = 141,336 点）・C2/C2b/C12 恒等式グリッド（226,968/9,330/
  1,904,056 点）＋マージ・tail 系・C3 選択肢分解アンカー（1,035 点）・
  C4 型機械ボックス±60（630,822 点・実現型 95,844・全走型 96,500・
  **clip ±20/番兵 ±21＝K1135 出版時予想 2y+2=20 の的中**）・C7 seeded
  遠方 probe 20万点（seed 20261123・tail 境界 x+z+10 を跨ぐ窓込み）・
  C8 境界多様体（727,077 点・dx∈[-21,13]・tail 窓 [x+z+10, x+z+12]）・
  C9 v 空間シェル掃引 [61,64]∪[89,92]∪[117,120]（922,890 点）・C11 生
  census アンカー z=0..79・x=9..70・R<=x+z+12（912,640 点・両エンジン・
  cache clear エンジン間）の計 **5,742,841 照合点**（うちマージ系
  1,526,072 点・tail 系 302,657 点）で**全チェック不一致 0**。
- clip tightness の独立確認: 同ボックスで CLIP=19/番兵 20 に縮めると
  confluence 違反 5,355 件（identity は不変）。y=9 の特徴距離の最大
  R-z=2y+2=20（中間帯下端）が番兵と衝突するため。**必要 clip 半径の
  族式候補 2y+2 は y=5:12, y=6:14, y=7:16, y=8:18, y=9:20 と 5 族連続
  tight・予想 4 連続的中**（JS 予備検査の 2,425 件違反と定性一致）。
- census_rows.py: z=0..79・x=9..70・R=0..x+z+12 の全点 456,320（4,960 行）
  で生二重再帰の行ごと Thue-Morse 指数・T・P・tail を抽出。tail アサート
  （R>=x+z+10 で (x+9) mod 2）全行成立・値0点数 227,416・エンジン状態数
  4,682,179。output/census.txt（844,176 bytes）に全行表。
- 純 Python・標準ライブラリのみ・検証器約66〜70秒・census 約17.4秒。
- 再現性: 同一 cwd 2 回＋別 cwd・別 HOME・env -i の隔離 1 回の計 3 回実行で
  audit.json（SHA-256 f12c17b1...）が byte-identical。
  verify_y9_universal.py = 299acb6a...・census_rows.py = 14462d64...・
  census.txt = 1904c550...（出版後に GitHub 取り直し分と照合する）。

## K1138 の昇格（新規採番なし）

- AGENTS.md「同じ命題の status や証拠の更新は、原則として同じ K 項目を
  更新する」に従い、fit 出版済みの
  research/knowledge/items/K1138-two-token-y9-parametric-closed-form-fit.md
  を observed から proved に昇格する（title・scope・evidence 更新・証明
  artifacts 追加・relations に K1135 および C1d アンカー依存
  K0999/K1000/K1001/K1002/K1011/K1065/K1077/K1087 を追加）。
- 横断法則の昇格: マージ命題 y=1..9 全称確定・tail 開始 x+z+y+1 は
  y=2..9 の 8 族連続確定・値1基底点 y 点仮説は y=1..9 の連続 9 例・
  pin 格子公式 z+(d+3y)/2 は y=5..9 の 5 族統一・clip 窓 2y+2 は
  5 族連続 tight・pin 行追加値1点 2y+z+1 は y=6,8,9 で 3 族連続。

## 出版

- 実験 dir: research/experiments/vertical-fiber-two-token-y9-parametric-allz-proof-20261120/
  （report.md・verify_y9_universal.py・census_rows.py・output/audit.json・
  output/census.txt〔単独コミット〕）。
- item: K1138 を昇格（上記）。index: README の K1138 bullet 更存・
  .github/workflows/knowledge.yml に CI step 2 件（verify・census・
  git diff --exit-code）を追加。
  push ごとに最新 main を再取得して競合確認を行う。

## 次に開くもの

- y=10 族の cand10 fit（着手前に単一オーナー宣言を先行出版。
  y=10 raw skeleton survey〔同日出版 log〕で骨格要素観測済み・
  一般化候補式は y=7..10 の 4 族で一致観測。y=10 は偶数 y で tail・
  マージ行 P の偶奇が x 奇行。clip 窓 ±22/±23〔2y+2=22〕が予想される）。
- 横断法則（基底点 y 点・tail 開始 x+z+y+1・掃引帯・中間帯・定常pin・
  前倒しpin格子公式 pin=z+(d+3y)/2〔(x-y)+z≡2 mod 4〕・対角行上端格子規則
  r=z+y-[2(z-y)≡0 mod 4]）の一般証明レーンの開設
  （y<=9 で全称確定・pin 格子公式 5 族連続）。
- 型機械 clip 窓の一般式（必要半径 2y+2 の補題化。5 族連続 tight・
  4 予想連続的中）とボックス外新規型ゼロの補題化。
- 低R単一トークン縮約 R<=z+6 の全 z 一般化（y=9 では z=15,16,17 で観測）。
