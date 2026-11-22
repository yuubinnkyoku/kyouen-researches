# y=14族 fit（K1233）の独立第二検証（2026-11-22 高速レーン・第二実行）

本 log は [K1233](../knowledge/items/K1233-two-token-y14-parametric-closed-form-fit.md)
（y=14 族パラメトリック閉形式候補 cand14 の fitting・単一オーナー宣言
2026-11-22T18:42:55Z・commit e3a856ad）に対する**独立第二検証**の実行記録。
正本は
[実験dir](../experiments/vertical-fiber-two-token-y14-parametric-fit-second-verification-20261122/README.md)。

## 経緯: 二重並走と fit 出版の譲渡

本レーン（同一の毎時高速レーンタスクの別実行）は、K1233 の著者レーンとは
独立に y=14 族の閉形式導出を進めていた。本レーンの導出は K1231/K1152/K1141 の
横断統一則（pin 格子統一式・pin スロット=th-1・k 定数族式・対角 cap・tail/merge
族式）から y=14 の生データを見る前に構築したもので、3Y mod 4 = 2 による pin 行
フリップ〔奇z d≡2 (mod 4) {-10,-6,-2,2,6,10,14}・偶z d≡0 (mod 4)
{-12,-8,-4,0,4,8,12}・両偶奇 7 行は族初〕および奇z I 帯行の混合 th 則
th=2k+[d≡2 (mod 4)] を事前に予想し、自前 probe（90,049 点）に**初稿一発一致**
（mismatch 0・overlap 0）していた。

出版のために K 番号を採番しようとした直前に最新 main を再取得したところ、
対抗宣言（2026-11-22T18:42:55Z・commit e3a856ad）が**本レーンの宣言予備時刻
18:43:14Z より 19 秒先行**していることを発見した。単一オーナー規則により
fit 出版は対抗レーンに譲り（本レーンの宣言・fit 出版は main に一切なし）、
完成済みの独立導出・probe・12 チェック監査バッテリを第二検証側に転用した。
対抗レーンは実験 dir（commit b6f74dfc7d）・K1233 item + fit log（5d6db5ce）・
knowledge README bullet（0f0d2fb71）を出版済み。

## 第二検証の設計（相補的 probe box）

両レーンの probe box は偶然にも相補的だった:

- K1233（勝者）: z=0..30・x=14..z+29・R<=x+z+30（2y+2=30 cap 拡張）・961 行 74,834 点
- 本レーン: z=0..33・x=14..z+30・R<=x+z+28・1,139 行 90,049 点・merge 行 15 行
  （K1233 box は merge 3 行。x<=z-15 の merge 境界 z>=29 までの被覆が z<=33 を要求）

共通 72,912 点・K1233 専有 1,922 点（R∈{x+z+29, x+z+30} 広め cap の帯）・
本レーン専有 17,137 点（z=31..33 の 14,409 点・x=z+30 エッジ行 2,728 点）。
生値照合は双方向で**計 164,883 点・mismatch 0**。

## V1-V4 結果

- V1: 本レーン生 probe 90,049 点（うち K1233 box 外 17,137 点は本検証で初めて
  K1233 cand14 の生値照合を受ける）→ **mismatch 0**
- V2: K1233 出版 probe_y14.py から probe 行を再生成（961 行・74,834 点・
  行表 SHA-256 633f17cc0472…・K1233 audit と同一指紋）し本レーン cand14 を照合
  （K1233 専有点 1,922 含む）→ **mismatch 0**
- V3: 両 cand14 実装の判定等価をエンジンなし純算術グリッド（z=0..120・
  x=14..z+60・R<=x+z+28）で照合 → **2,241,162 点 mismatch 0**
- V4 fail-closed: K1233 正本 cand14 の Y 定数改ざん（コード行アンカー・
  docstring 由来の mine はスキップ）が V1 型照合で捕捉（933 mismatch）。

合計 overall **PASS**（`second_verification.json`・SHA-256 04b7221432…）。
決定性: 本検証器 2 実行 + 出版レイアウト（兄弟 dir・K1233 出版 file の
fetch-back copy）での再実行がすべて byte-identical。

## 持込み資産

本レーンの独立導出・probe・監査は第二検証の正本として実験 dir に出版する:
probe_y14.py（生二重再帰生成器・約 6 秒・cache 2,125,289）・probe_rows.txt
（90,049 点の y=14 生行表としての初出版・SHA-256 8559dc59e4…・3 回再生成
byte-identical）・cand14.py（独立導出・provenance 記載・値頻度 0:44,161 /
1:33,563 / 2:12,325）・audit_fit.py（K1233 の spot/回帰と独立設計の 12 チェック
バッテリ・A 90,049 / B 15,946 / C 1,125〔15 行〕/ D 1,904 / E 2,080 / F 12,940 /
G 2,794 / H 3,787 / I 10,513〔122 行〕/ K 再生成 byte 一致 / fail-closed
L1-L3 捕捉・3 実行 byte-identical・audit.json SHA-256 8d99ec0e27…）・
y14_second_verification.py（本検証の正本検証器）。

## 併存の観察（maintainer判定事項・記録のみ）

検証中に、同一対象（2トークン残余ゲーム y=13 族パラメトリック閉形式）を
叙述する項目が [K1171](../knowledge/items/K1171-two-token-y13-parametric-closed-form-fit.md)
（2026-11-20 fit・「主要族式が揃って破れた族」分析・pin slope 1 記述）と
[K1231](../knowledge/items/K1231-two-token-y13-parametric-closed-form-fit.md)
（2026-11-22 再fit→全称 proved・pin 格子統一式成立）の **2 項目で併存**している
ことを観察した。y=12 族（K1152 が y=10 暫定構造 seed の 240 点修正を経て族式確定）
と同種の「初期 fit の構造誤読が再 fit で修正される」事案の可能性があるが、
K1171 を反証扱いにするか・エイリアス化するかは repo 規則（反証した命題は残す・
異なる修正版は別項目）上の maintainer 判断に属する。本レーンは K1171 item 本文に
一切触れず、本記録のみを残す。なお K1231 の正本 cand13 は本レーンの y14 導出
（横断統一則 seed）の直接の根拠であり、K1233 の主張も K1231 系の族式で
貫かれている。

## trust 境界

本成果は有限照合（生値 164,883 + 判定等価 2,241,162 点）による K1233 証拠の
強化であり、**cand14 の全称性には一切言及しない**（status observed 不変）。
全称段階（verify_y14_universal.py・12 チェック・B子=K1231 出版 cand13 逐語転写・
型機械 clip 窓 2y+2=30 の tight 判定〔9 族連続 tight 継続の 10 族目候補〕・
census z=0..79・x=14..70）は K1233 の次段階で、着手には新たな単一オーナー宣言
が必要（K1233 宣言は全称段階を範囲外と明記）。標準 11×11 空盤・二石 root
{49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。
3 トークン以上・y>=15 族・固定幅・q 点版安定化長は範囲外。
