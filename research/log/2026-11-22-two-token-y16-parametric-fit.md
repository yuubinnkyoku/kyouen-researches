# y=16 two-token パラメトリック閉形式 fit 実行記録（2026-11-22・高速レーン）

## 選定

前回実行のレジューム（y=15 全称 part2 出版完了・K1235 observed→proved 昇格・commit 126dcd13 21:14Z）が指名した
2候補「横断法則の y>=15 一般補題化レーン」と「y=16 族の fit」の価値比較を行い、**y=16 fit** を先に着手した。
理由: (a) 一般補題化レーンにとって偶数 y 系列の第4データ点（y=10/12/14/16）が最も価値のある追加材料である
（特に pin 行数 y/2 則 5→6→7→8・pin mod-4 回転の 3 周期目・I 帯掃引行数 15→15→17の +2 ジャンプ）、
(b) 単独で完結して出版可能（宣言→fit→spot→監査→item→README、K1233/K1235 と同型）、
(c) 「出版最終構造 seed 法則」の偶数 y 第3テスト（cand14→cand16）・「両偶奇 8 行 pin 格子の初例」
「初の全面 box 外マージ回帰」という3つの横断判定材料を同時に取れる、
(d) K1235/K1236 は 3トークン以上・y>=16 族を範囲外と明記しており着手障害なし、
(e) 直近100コミットに y=16 族着手なし（grep hit は n11 Part AX scaffold のファイル名誤検出のみ）を確認済み。

## 宣言（probe実行前に先行出版）

- 宣言ノート: [2026-11-22-y16-two-token-skeleton-single-owner-note.md](2026-11-22-y16-two-token-skeleton-single-owner-note.md)
  （commit `e0fbd99d`・2026-11-22T21:21:34Z・宣言時点観測 HEAD `607c876a`）
- 事前横断予想16項目（tail x 奇行 R>=x+z+17 値 (x+16) mod 2・基底点16点・マージ行 x<=z-17〔**y=16では
  box内マージ行0行・z>=33が必要、事前明記**〕・pin 格子 o_pin=(d+48)/2∈[17,32]・奇z 8行 d≡0 (mod 4)
  {-12,...,16}〔両偶奇8行の初例〕・偶z 8行 d≡2 (mod 4) {-14,...,14}・「pinスロット=th-1」6族目候補・
  base k=floor((d+49)/4) 7族目・偶z I k=floor((d+47)/4) 6族目・偶z対角値1全欠如 9族目候補・
  掃引/定常 pin z+32/z+33・band下端34・偶y族単一band則・17行掃引の初例・最終pin行 d=16=y の I[33) 型・
  初稿修正0予想・外挿点数74,741/行899）を全部 probe 実行前に登録し、**全項目 fit level で一致**した。
- probe box: z=0..30・x=16..z+29・R<=x+z+34（=2y+2・y=14/y=15 出版の宣言済み convention を継承）。
  K番号は K1237（push直前に確認: 直近100コミット最大K番号はK1236〔y15全称〕・items に y=16 族項目なし・
  対抗 y=16 宣言なし。K1058レーン〔円の数え上げ〕と n11 batchレーン〔Part AY/AZ/BA〕は非接触）。

## 実行と結果（すべて確定論的・正本は実験dir）

- cand16 初稿（出版最終構造 cand14〔K1233 全称昇格済み〕の Y+2 機械翻訳・コード本体は Y 定数・関数名・
  y 固有コメント以外は正本 cand14 と同一構造〔Y 正規化差分比較で確認〕）:
  **probe 899行 74,741点に一発完全一致**（修正0・mismatch 0・T/P重複0・値頻度 0:36,738/1:29,032/2:8,971・
  値3なし・約7秒）。**出版最終構造 seed 法則 4 連続**（cand11→13・cand12→14・cand13→15・cand14→16）。
- box 内 tail assertion（R>=x+z+17→(x+16) mod 2）: **16,182点 bad 0**（x 偶行は値0・band 上端 x+z+16 確認）。
- box 内マージ行: **0行**（宣言の事前明記どおり・x<=z-17 は z>=33 を要求）。
- box 内 pin census（audit fail-closed gate）: 奇z 8行・偶z 8行すべて値2で in-box 観測。
  偶z対角行値1 census: 計数0。
- box 外 spot（`spot_y16.py`・LRU cap 1.5M・148秒）: **35,825点 bad 0**。
  特に deep 24行で**全8奇z pin行・全8偶z pin行・両偶奇対角・偶z I 境界行 d=-15/+15・飽和行
  z-even base d=16・マージ境界行 x=z-17 両偶奇**を個別の行として生値検証し、
  **全選択行に x>=16 の機械 assert を実装**（y=14 fit の (19,13) 事故の構造的再発防止・今回が初適用で事故ゼロ）。
- tail raw 回帰 6行×14点=84点 bad 0・merge 回帰 cand16 vs K0832（z∈{33,40,47,54,64,77}・x=16..z-17・R<=x+z+33）
  **14,910比較 bad 0**（y=16 は初の全面 box 外マージ回帰）。
- 決定性: probe_rows.txt は同一cwd 再生・隔離 tree/cwd/HOME + PYTHONHASHSEED=random 再生の3回すべて
  byte-identical（SHA-256 5af7582d…）。make_audit_y16.py は fail-closed（mismatch/overlap/tail_bad/
  box内マージ行数≠0/偶z対角値1/pin census 16行不完全のいずれかで書かない）で audit.json 生成。
- fail-closed 改ざん試験: 有効7変種（probe値反転・行欠落・Y=17・pin mod4クラス交換・band下端2Y+2→2Y+3・
  band上端→x+15・tail開始→x+z+Y）すべて検出。試行した band 下端 2Y+2→2Y+1 は偶offset上で box 内同値
  （検出不可能）と判明し有効版に置換（誠実記録・audit.json に記載）。

## 出版

- Commit A: 実験dir `research/experiments/vertical-fiber-two-token-y16-parametric-allz-fit-20261122/`
  （report.md・cand16.py・probe_y16.py・spot_y16.py・make_audit_y16.py・output/audit.json）
- Commit B: 本item K1237 + 本fit log
- Commit C: knowledge README 末尾bullet追記
- 各 push 直前に最新 main HEAD を再取得し commit message に観測 HEAD を記録。

## 次段階（本実行の範囲外・別宣言）

- y=16 全称（verify_y16_universal.py・A子 H(R-1;(x-1,16);z)・B子 出版 cand15 逐語転写〔x=16 合流子
  (15,16)≡(16,15)〕・C子 1xor cand16(z-1,x,R-1)・型機械 clip 窓 2y+2=34 tight 判定〔12族目候補〕・census）
- y>=15 横断法則の一般補題化レーン（偶数 y 系列 4 データ点を揃えた本 fit が材料を供給）
- fast lane の他候補: REMO 3枝 cap≤15 r=3 sweep 等
