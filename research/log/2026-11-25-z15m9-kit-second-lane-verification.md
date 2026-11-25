# 検証 log: z15-min9 事前探査 kit (`5ec6c35d`) の第二レーン独立検証 — 高速レーン 2026-11-25

並走 hourly 実行が出版した **z=15 floor-9 (min>=9) 事前探査 kit**
(`research/experiments/strip-z15-min9-20261125`・commit `5ec6c35d`・
log `research/log/2026-11-25-z15m9-predecl-exploration.md`) に対する本
レーン (第二実行環境) での独立検証の記録。K1320 完了 log 次課題 1 を巡って
**両レーンが同窓口で同時進行**したため、push 直前の最新 main 再取得で先行
出版を検出した本レーンは重複出版を取りやめ、定型どおり検証モードに転換した。
本 log は一意の filename で出版する追加検証資料であり・kit・main 成果の
再出版ではない。すべて観測・検証事実の記録であって、定理・全称命題の主張を
含まない。

## 競合の状況 (honest)

- 本レーンは着手時 HEAD `a481d85b` (K1320 item 出版) を確認後、同じく
  K1320 完了 log 次課題 1「floor-9 z=15 セル梯子の宣言前 census kit」を
  **独立に (並走実行の存在を知らずに)** 構築・実行・凍結まで完了させていた
  (`explore_z15f9pre.py` sha256
  `b09f88bc6ba0d02e5ba6fd91debc2491e812f4f6d48369d838f74ba8856fdc5e`・
  凍結 .out sha256
  `22f0d14f754a16dae1d8ffd3ded83b7ddc0094bd7ab451fae285a8da6fae1c60`・
  3 走 byte-identical rc 0 各 ~16 秒)。
- **push 直前の最新 main 再取得で並走出版 `5ec6c35d` を検出**し、本レーンの
  z=15 kit 出版を取りやめた (重複 dir 名 `strip-z15-min9-20261125` の
  二重出版を回避)。検出から転換まで本レーンの成果は一切出版していない。
- 以降の処理: ①出版 bytes の検証 (下記 §1)・②独立実装同士の値レベル
  照合 (§2)・③本レーンにのみ存在した観測の保存出版 (§3)。

## §1 出版 kit の byte 検証 (publish-then-execute 第二実行環境)

- `research/experiments/strip-z15-min9-20261125/` 4 ファイル +
  log 1 ファイルを raw fetch し sha256 採番: `explore_z15m9.py`
  `00d15acb489c63fb7177d6dc5d5ba265c46fb79b462a9bfad75bc60d48679075`・
  `explore_z15m9.out`
  `52a9808e7d0f43db69e13f083c1c0b7626d003f011d340319583e9d6f67821f9`・
  `engine_block.py` `582c93c1…` (出版 chain と byte 一致・埋込 pin
  `bd5f22e4…`assert は機体実行時に PASS を確認)。
- **出版 bytes からの再実行 3 走** (既定 + PYTHONHASHSEED=random 同一 cwd +
  env -i PYTHONHASHSEED=5150 隔離 dir) がすべて rc 0・stdout byte-identical
  (各 ~21 秒)・**出版 .out と完全 byte 一致** = 決定性・再生性を第二環境で
  確認。

## §2 独立実装間の値レベル照合 (第二実装検証に相当)

`explore_z15m9.py` (並走・9 段構成) と本レーンの `explore_z15f9pre.py`
(8 段構成 + 行記録系セクション) は同一の凍結原典 `explore_z15pre.py`
(`3e2a8ab8…`) から別々に書かれた機体であり・共有測定域は完全に独立な
実装で二回測定されたことになる。照合結果:

- **共有 8 セル F15f9..A215f9**: 形状数 312 = 312・multivalue 0 = 0・
  **deviant 表 (s 位置・方向・値・崩壊値・個数) が全セルで完全一致**
  (F {14 下向き・15 穴・s>=16 上向き恒常・領域内 26}・G {14}・E {12 下,14 上}・
  D {12 下}・C {10 下,12 上}・B {10 下}・A {10 上}・A2 なし)。
  **床 10→9 下げで deviant 構造が出版 floor-10 表と同一**という並走結論を
  本レーンの実装も独立に再生。
- **tail spots s∈{41..48}**: 共有 8 セル分 64 行が完全一致
  (F15f9 の 8 行のみ 2 vs 0)・並走キットの追加 A315f9 8 行も含めて
  不一致行の構成は同一。
- **帯域下子 floor-9 (`H(16;Y;16)` vs `v(s,16,16)`)**: 両実装とも
  312 形状・deviant 0・multivalue 0。
- 相補的 (定義域が異なる) 測定: 並走キットの A315f9 セル (312 形状・
  deviant 0)・strip m=9 掃引 (265 形状・違反 0)・in-band 152 形状記録
  (分離 0) と、本レーンの m=9 行 X 域掃引 (**アリティ <= 4・min(X)=9 厳密・
  S∈{9..47}: 235 形状・分離 0**〔出版 152 形状を包含し 4 トークン 83 形状を
  追加〕)・行 tail spots (**S∈{48..60}: 13/13 一致**)・m=9 base spot
  (**H(25;(9,9);15)=0=v(18,15,25)**) はすべて矛盾なく・合計すると
  z=15 m=9 行は複数の相補的定義域で分離 0 が揃った。

**不一致 0 件**。二実装は共有測定域ですべて一致した。

## §3 本レーンにのみ存在した観測の保存

本レーンの z=15 ビルドにのみ存在し・並走キットに含まれない測定:

- **m=8 beyond-frontier z=15 記録** (m=8 の z=15 は z*(8)=14 の 1 つ外側・
  R=24・S∈{8..47}・出版 z14pre section (d) と同パラメータ):
  **362 形状中分離ちょうど 1 点 X=(8,8)・値 0 vs 崩壊 1 (下向き)** —
  出版 z=14 frontier 記録の唯一の分離 (8,8)〔2 vs 1 上向き〕が
  **frontier の 1 つ外で存続し上向き→下向きに反転** — ストリップ系列初の
  beyond-frontier データ点。**本観測は第二レーン出版の
  `research/experiments/strip-z16-min9-20261125/` kit section (g) として
  (frozen .out に埋込の形で) 保存出版した** (同一 kit 内で zone z=16 系の
  frontier 記録と同格の front-family 観測として整理・詳細は同 kit の
  README/log)。

## 取りやめた成果物の取り扱い

本レーンの `explore_z15f9pre.py` / .out / README / log (z=15 8 段版) は
**出版しない**。その情報内容は上記のとおり (a) 並走出版 kit が共有域を
完全にカバー (b) 相補測定値と sha256 は本 log に記録 (c) beyond-frontier
記録は z16-min9 kit section (g) に移植、の 3 点で失われていない。
repo 側に二重出版を残さない。

## 主張の区別 (定型)

本 log の記録はすべて検証事実・機械観測 (判定外) であり、定理・全称命題・
予想の主張を含まない。11×11 空盤・二石 root・S2・class 1/2/4 は全時点
UNKNOWN・verdict 不消費。
