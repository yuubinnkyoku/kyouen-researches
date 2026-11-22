# 2トークン残余ゲーム y=14族パラメトリック閉形式候補 cand14 の fitting（2026-11-22 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-22-y14-two-token-skeleton-single-owner-note.md)・2026-11-22T18:42:55Z・commit e3a856ad）に基づく
y=14 族着手の第一段階（fitting）の記録。正本は
[実験dir](../experiments/vertical-fiber-two-token-y14-parametric-allz-fit-20261122/report.md)・
知識項目は [K1233](../knowledge/items/K1233-two-token-y14-parametric-closed-form-fit.md)。

## 採番

push 直前に最新 main を再取得し、README 末尾 bullet が K1232（y13 universal part2）まで
であること・items に K1233 が存在しないこと（該当K1233 ファイル直接不在・README grep 空・
generated index の最終更新が K0894 前後と古いことの確認）を確認して K1233 に採番した。

## 選定

K1231（y=13 全称昇格・同レーン前回成果）のレジュームは「y=14 fit 着手判断」を
次の有力課題として指名し、y 偶族（y=10/y=12 と対置）の pin 行数・th 型・偶z pin 行数
増加則の y 偶族での挙動を判定材料としていた。価値比較の相手は「横断法則の y>=14
一般補題化レーン」だったが、y=14 fit は (a) 偶数 y 族で初めて「出版最終構造 seed による
外挿」をテストする、(b) pin mod 4 クラス回転・th 連続整数掃引・k 定数族式といった
一般補題化の対象法則に 14 番目の独立データ点を与える、(c) 単独で完結して出版できる、
の 3 点で最も情報価値が高いと判断して着手した（一般補題化レーンは本成果を食料とする）。

## 経緯

1. K1231/K1152/K1141 の横断観察・cand12/cand13 出版正本から y=14 の構造則を事前導出し、
   宣言ノート（commit e3a856ad・probe 実行前に出版）に「事前の横断予想」として全記録:
   pin格子統一式の y=14 適用（奇z d≡2 mod 4 の 7 行・偶z d≡0 mod 4 の 7 行・
   mod 4 クラス回転）、奇z I帯 k=floor((d+44)/4)・th=2k+[d≡y mod4]（連続整数掃引 15..29）、
   base z=floor((d+3y+1)/4)（5族目候補）・偶z I=floor((d+3y-1)/4)（4族目候補）・
   対角 cap・基底点 14・tail/marge 族式・band 下端 30・定常 pin z+28/z+29。
2. probe（`probe_y14.py`・y=11/y=12/y=13 版 probe の正当写し・Y=14・x range(14, z+30)・
   merge marker x<=z-15・R<=x+z+30〔2y+2=30 への cap 拡張は宣言済み〕）を実行し、
   961 行・74,834 点・約 5.5 秒で probe_rows.txt を生成（別 cwd 再生成で byte-identical・
   SHA-256 633f17cc… を確認）。
3. **初稿から一発で probe points: 74834 mismatch: 0 overlap: 0**
   （値頻度 0:36,711 / 1:28,593 / 2:9,530・値3なし）。y=12 fit が 240 点修正を要したのと
   対照的で、y=11/y=13 に続き偶数 y 族でも一発一致（実質 3 例目・偶数 y では初例）。
   宣言ノートの事前予想は全項目 fit level で一致（判定表は report 末尾）。
4. spot（`spot_y14.py`）初回実行で OOM kill（本 host のメモリ予算 3GB に対し
   y=11/12/13 版の無制限 LRU が積み上がる）。**LRU cap 1.5M・block 間 cache_clear の
   決定的退避版**に改修し再実行: 32,017 点 bad 0（深 R<=130 代表 15 行・大 z=31..40・
   23 d・x=y=14 エッジ・大 d∈{30,41,52}）・約 92 秒。merge 回帰 15,336 比較 0・
   tail raw 回帰 84 点 0。
5. 誠実記録: 上記 cap 改修版の初回実行（未出版）で bad=1 が残り、原因を調査したところ
   深行選択の (19,13) が y=14 族の定義域 x>=14 を下回る行選択ミスだった
   （{13,14} は正準降順で (14,13)＝y=13 族 x=14 行・生値1は正しく、cand14 は x<14 に
   何も主張しない）。該当行を (21,15) に修正して以後の全実行は bad 0。この incident は
   全称段階への重要な注意も与えた: **A子の x=14 行は {13,14}≡(14,13) で y=13 族 x=14 行
   と同一状態**（合流子は cand13(z,14,R-1)）。
6. box 内 assertion: tail 領域 R>=x+z+15 の 15,376 点が値 (x+14) mod 2 に全一致
   （R cap 拡張の成果で y=12/y=13 fit では box 外に出ていた深帯を box 内で直接確認）・
   マージ領域 x<=z-15 の 222 点が single_token(x+14,z,R) に全一致。
7. audit 生成器 `make_audit_y14.py`（fail-closed: mismatch/overlap/tail_bad/mg_bad/
   偶z対角値1/pin 観測のいずれかで非ゼロなら書かない）を 2 回実行し byte-identical
   の audit.json を生成。合計 122,829 点比較・不一致 0・決定論的（純 Python 標準
   ライブラリのみ・秒数欄は host 固定ピン）。
8. 出版: 単一オーナー宣言ノート（commit e3a856ad・着手前）→ 実験 dir 6 ファイル
   （report.md・cand14.py・probe_y14.py・spot_y14.py・make_audit_y14.py・
   output/audit.json・commit b6f74dfc7d41676ca934c88a135660e666db2425）→ K1233 item＋本 log（本コミット）→
   knowledge README 末尾 bullet（後続コミット）。各 push は
   commit-pinned fetch-back + byte 一致検証。

## 主要な観察（全て fitting レベル・全称ではない）

- **pin 格子統一式の mod 4 回転テスト合格**: o_pin=(d+3y)/2∈[y+1,2y]・o_pin≡z+1 (mod 2)
  の単一式は y=5..13 で 9 族全称確定済みだが、y 偶族で pin 行の d≡y (mod 4) クラスが
  y=12 の d≡0 から y=14 の d≡2 に**回転する**初例テストで、格子・行数則（y/2=7 両偶奇）
  が回転後もそのまま成立した。y=10（d≡2）→y=12（d≡0）→y=14（d≡2）の周期 4 回転の
  実測 3 点が揃い、一般補題化の直接的証拠になった。
- **「pin スロット = th-1」型が 4 族連続（y=11/12/13/14）**: 偶数 y 族では pin mod 4
  クラスの回転に伴い th 規則（th=2k+[d≡y mod4]）も回転し、pin 行が常に th-1=2k を占有。
  skew 行（d≡0 mod 4）では slot=2k-1 が b_k 上端点と一致し th=2k。K1152 が指名した
  横断型の問いがさらに強い形（回転不変性）で回答された。
- **z-odd I 帯 th の偶奇分離が明白に**: 偶数 y（y=12/y=14）は連続整数掃引 th、
  奇数 y（y=9/y=11/y=13）は th=2k+1 ペア反復型。y=14 で掃引型 2 族目。
- base 行 k(d)=floor((d+3y+1)/4) が **5 族連続**（y=10..14）、偶z I 帯 k(d)=floor((d+3y-1)/4)
  が **4 族連続**（y=11..14）、偶z pin slot=2k+1 が **4 族連続**（fit level 各）。
- **初稿一発一致の seed 法則**: 出版最終構造 seed（cand12→cand14）は修正 0、
  暫定構造 seed（y=10→y=12）は 240 点修正。偶奇両系列で「最終構造 seed 一発一致」が
  揃い、y>=15 fit の予測難度見積りに使える。
- 偶z 対角行の値1全欠如が **7 族連続**（y=8..14・fit level。y<=13 は全称 6 族）。
  最終 pin 行 d=y の I[2y+z+1)=I[29) 型が 9 族的確定（pin off 28 は定常 pin 同値）。

## trust 境界

本成果は有限 fitting と spot 検証であり全称定理ではない。cand14 が全 z>=0・全 x>=14・
全 R>=0 で成り立つという主張は次段階の 12 チェック監査（A子=H(R-1;(x-1,14);z)・
B子=K1231 の出版 cand13 逐語転写〔x=14 合流子 (13,14)≡(14,13)・incident 5 の実証どおり〕・
C子=1 xor cand14(z-1,x,R-1)・型機械 clip 窓 2y+2=30〔10 族連続 tight 候補〕・
census z=0..79・x=14..70）で判定する。3 トークン以上・y>=15 族・固定幅・q 点版安定化長・
標準 11×11 は範囲外。
