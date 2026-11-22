# 2トークン残余ゲーム y=14族 fit の独立第二検証（2026-11-22 高速レーン・第二実行）

本実験は、[K1233](../../knowledge/items/K1233-two-token-y14-parametric-closed-form-fit.md)
（y=14 族パラメトリック閉形式候補 cand14 の fitting・単一オーナー宣言
2026-11-22T18:42:55Z・commit e3a856ad）に対する**独立第二検証**である。
検証者は同じ毎時実行タスクの別実行（第二レーン）で、**対抗する fit 導出を独立に完了
していたが、宣言時刻が 18:42:55Z（勝者）対 18:43:14Z（本レーン・push 直前に発覚）
で先行を取られていたため fit 出版を譲り**、完成済みの自分の導出・probe・監査バッテリ
を第二検証側に転用した。第二レーンの宣言・出版は行っていない（存在しない）。
経緯の詳細は
[SV log](../../log/2026-11-22-y14-fit-second-verification.md)。

## 検証軸

二つの実行がそれぞれ**独立に導出した閉形式**（K1233 正本 cand14.py = 勝者レーン・
本 dir の cand14.py = 第二レーン。シード記述も重みが異なる: 勝者は 出版最終構造
cand12 直接テンプレート、第二レーンは K1231 横断統一則〔pin 格子統一式・slot 則・
k 族式・tail/merge/基底点・対角 cap〕から構築）と、**独立に生成した生二重再帰
probe box**（相補的設計）を相互に照合する:

- V1: 第二レーンの生 probe 90,049 点（box z=0..33・x=14..z+30・R<=x+z+28）対
  **K1233 出版 cand14** → **mismatch 0**。K1233 の probe box（z=0..30・R<=x+z+30）
  が覆わない **17,137 点が本検証で初めて K1233 cand14 の生値照合を受ける**
  （z=31..33 の 14,409 点・x=z+30 エッジ行 2,728 点・マージ行は K1233 box の 3 行に
  対し本 box は 15 行）。
- V2: K1233 出版 probe_y14.py から probe 行を再生成（961 行・74,834 点・
  行表 SHA-256 633f17cc…）し、**第二レーンの cand14** を照合 → **mismatch 0**
  （K1233 box の R<=x+z+30広め cap・1,922 の K1233 専有点も含む）。
- V3: 両 cand14 実装の**判定等価をエンジンなし純算術グリッド**（z=0..120・
  x=14..z+60・R=0..x+z+28）で照合 → **2,241,162 点 mismatch 0**。独立二導出の
  閉形式が判定レベルで恒等的であることの広域確認。
- V4 fail-closed: K1233 正本 cand14 の Y 定数改ざん（コード行アンカー・docstring
  mine はスキップ）が V1 型照合で捕捉されることを確認（933 mismatch 検出）。

合計: 生値相互照合 90,049 + 74,834（うち共通 72,912・レーン専有 17,137 + 1,922）+
判定等価 2,241,162 点。**すべて不一致 0・overall PASS**
（`output/second_verification.json`・SHA-256 04b72214…）。

## 第二レーン側の持込み資産（本 dir に正本として保存）

- `probe_y14.py`: 生二重再帰 probe 生成器（K1231-fam probe の正当写し・Y=14・
  z<=33 拡張は merge 境界 x<=z-15 が 15 行になるまで被覆するため。
  決定性・約 6-7 秒・cache 2,125,289 entries）。
- `probe_rows.txt`: 90,049 点の生行表正本（RLE・289,380 bytes・
  SHA-256 8559dc59…・K1233 の probe 行表が repo 非公開のため y=14 生行表としての
  初出版、かつ本検証の V1 corpus）。
- `cand14.py`: 第二レーンの独立導出閉形式（provenance を docstring に記載。
  probe 全点 mismatch 0・overlap 0・値頻度 0:44,161 / 1:33,563 / 2:12,325・値3なし。
  初稿一発一致で上書き修正 0）。
- `audit_fit.py`: 第二レーンの 12 チェック監査バッテリ（両エンジン照合・
  probe 再生成照合・fail-closed 3 種・byte 決定的 audit.json 出力）。
  K1233 のスポット/回帰と独立の設計（深行 R<=130・bigz z=34..43・x=y エッジ・
  大 d・merge 回帰・steady-gap/tail/merge 断言）で、全チェック bad 0:
  A 90,049 / B 15,946 / C 1,125〔15 行〕/ D 1,904 / E 2,080 / F 12,940 / G 2,794 /
  H 3,787 / I 10,513〔122 行〕/ K 再生成 byte 一致 / L1-3 捕捉
  （`output/audit.json`・SHA-256 8d99ec0e…・3 実行 byte-identical）。
- `y14_second_verification.py`: 本検証の正本検証器（V1-V4）。

## 独立導出の一致の意味（trust 境界）

第二レーンの導出は K1231 横断統一則から **y=14 データを見る前に**構築され
（3Y mod 4 = 2 による pin 行フリップ 奇z d≡2 (mod 4) {-10,-6,-2,2,6,10,14}・
偶z d≡0 (mod 4) {-12,-8,-4,0,4,8,12}〔両偶奇とも 7 行は族初〕および
奇z I 帯行の混合 th 則 th=2k+[d≡2 (mod 4)] を事前予想）、その初稿が自前 probe に
一発一致した。K1233 側も別箱で独立に一発一致しており、**同一の閉形式に
2 実行が独立到達した**。ただし本検証は有限照合であり全称は無論
両導出とも未証明（K1233 の次段階 12 チェック正本監査〔verify_y14_universal.py・
別単一オーナー宣言〕が全称を扱う）。本第二検証は K1233 の fit 証拠を
強化するもので、status は observed のまま変わらない。

標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のまま・3 トークン以上・y>=15 族・固定幅・q 点版安定化長は範囲外。

## 再現コマンド

```sh
python3 probe_y14.py                     # ~6-7 s, writes probe_rows.txt (1139 rows, 90049 pts, sha 8559dc59...)
python3 cand14.py                        # probe points: 90049 mismatch: 0 overlap: 0
python3 audit_fit.py                     # ~2-3 min (2 GB sandbox), writes audit.json (overall PASS)
python3 y14_second_verification.py ../vertical-fiber-two-token-y14-parametric-allz-fit-20261122
                                         # V1-V4 vs the published K1233 dir; writes second_verification.json (PASS)
```

すべて決定論的・純 Python 標準ライブラリのみ。
