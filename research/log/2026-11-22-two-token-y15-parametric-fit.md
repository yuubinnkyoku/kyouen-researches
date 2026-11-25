# y=15 two-token パラメトリック閉形式 fit 実行記録（2026-11-22・高速レーン）

## 選定

前回レーンのレジューム（y=14 全称 part2 出版完了・K1233 observed→proved 昇格）が指名した
2候補「横断法則の y>=15 一般補題化レーン」と「y=15 族の fit・全称」の価値比較を行い、
**y=15 fit** を先に着手した。理由: (a) 一般補題化レーンにとって y=15 の実データ点が
最も価値のある追加材料である（各横断法則の次の族での成否が補題の形を決める）、
(b) 単独で完結して出版可能（宣言→fit→spot→監査→item→README、K1233/K1234 と同型）、
(c) y 奇族の pin 行数増加則（6→7→8）と「出版最終構造 seed 法則」の奇数 y 第2テスト
（cand13→cand15）という2つの横断判定材料を同時に取れる、(d) y>=15 両候補は
K1233/K1234 の範囲外宣言済みで着手障害なし。対抗宣言チェック（過去24時間の全コミット・
search_code "y15"/"y=15"・既存13/29件はすべて z 固定 boundary 系の別軸）を
実施して不存在を確認した。

## 宣言（probe実行前に先行出版）

- 宣言ノート: [2026-11-22-y15-two-token-skeleton-single-owner-note.md](2026-11-22-y15-two-token-skeleton-single-owner-note.md)
  （commit `26a1ad28`・2026-11-22T20:04:00Z・宣言時点観測 HEAD `7038952a`）
- 事前横断予想12項目（tail x 偶行 R>=x+z+16 値 (x+15) mod 2・基底点15点・マージ行
  x<=z-16〔**y=15ではbox内マージ行0行・z>=31が必要、事前明記**〕・pin 格子
  o_pin=(d+45)/2∈[16,30]・奇z 8行 d≡3 (mod 4) {-13,...,15}〔初の8行族〕・
  偶z 7行 d≡1 (mod 4) {-11,...,13}・「pinスロット=th-1」5族目候補・
  base k=floor((d+46)/4) 6族目・偶z I k=floor((d+44)/4) 5族目・偶z対角値1全欠如
  8族目候補・掃引/定常 pin z+30/z+31・band下端32・初稿修正0予想）を全部
  probe 実行前に登録した。
- probe box: z=0..30・x=15..z+29・R<=x+z+32（=2y+2・y=14 出版の宣言済み
  convention を継承）。K番号は K1235（push 直前に3点確認: README grep 0・
  search_code 全repo 0件・items に y=15 族項目なし〔K0903 は z=6 固定 boundary の別軸〕）。

## 実行と結果（すべて確定論的・正本は実験dir）

- cand15 初稿（出版最終構造 cand13〔K1231 全称昇格済み〕の Y+2 機械翻訳）:
  **probe 930行 74,865点に一発完全一致**（修正0・mismatch 0・T/P重複0・
  値頻度 0:36,770/1:28,846/2:9,249・値3なし・約6秒）。
- box 内 tail assertion（R>=x+z+16→(x+15) mod 2）: **15,810点 bad 0**
  （R cap 2y+2=32 により1行あたり17点の深さまで直接確認）。
- box 外 spot（`spot_y15.py`・LRU cap 1.5M・121秒）: **39,215点 bad 0**。
  特に deep 15行で**全8奇z pin行・全7偶z pin行を個別の行として生値検証**
  （行数則 (y+1)/2=8・(y-1)/2=7 の直接確認）し、**全選択行に x>=15 の機械
  assert を組み込んだ**（y=14 fit の (19,13) 事故の再発防止を構造化）。
  bigz z=31..40×27d・x=y=15 エッジ・大d{32,43,54}・掃引/定常行も含む。
- merge 回帰（box 内 0 行の事前宣言に対し、box 外で全量): cand15 vs
  K0832 single_token、z∈{31,38,45,52,62,75}・x=15..z-16・R<=x+z+31 の
  **14,325比較 bad 0**＋マージ境界行 (31,15)/(32,16)（x=z-16）の生値全点一致。
- tail raw 回帰: 6行×14点=**84点 bad 0**（値 (x+15) mod 2）。
- 合計 **128,489点比較・不一致0**。
- 決定性: probe_rows.txt 3回再生成（同一cwd・別cwd・隔離tree/cwd/HOME+
  PYTHONHASHSEED=random）で byte-identical（SHA-256 `2c7b72ad…`）。
  make_audit_y15.py 3回実行で audit.json byte-identical（SHA-256 `5c329dd4…`）。
- fail-closed 5種捕捉（隔離dir）: (1) probe 1点値改ざん→mismatch 1・audit中断・
  (2) pin位置値改ざん→mismatch 1・audit中断・(3) Y定数 15→14→mismatch 3,547・
  overlap 56・(4) pin mod4クラス改ざん→mismatch 120・audit中断・
  (5) probe_rows.txt 欠落→照合不能・audit未書き出し。復元後 baseline byte-identical。

## 事前横断予想の判定（全12項目一致）

tail・基底点・マージ・pin格子〔8行/7行〕・pin行数増加則 6→7→8・5→6→7
〔y=11/13/15 の3点で確定〕・「pinスロット=th-1」5族連続〔全8 pin行で
th(d)-1=o_pin(d) が格子・算術両面で恰好〕・奇z I k=base同一式+th=2k+1
ペア反復継続・base 6族目・偶z I 5族目・偶z pin 2k+1〔7行すべて恰好〕・
対角 cap 奇y向き・偶z対角値1全欠如 8族目候補・掃引/定常pin・band下端32・
初稿修正0（seed法則 3連続一発一致: 11→13・12→14・13→15）。
判定表は [report.md](../experiments/vertical-fiber-two-token-y15-parametric-allz-fit-20261122/report.md) 参照。

## 誠実記録（出版成果物への影響なし）

1. (a) 隔離実行の初回で `env -i` による PATH 喪失で python3 未発見（y=14 運用知見の
   再発確認・絶対パス指定で解決）。(b) fail-closed 復元確認の初回試行で、同一秒内に
   **同サイズ**の tampered ソースを元に戻したため CPython の pyc mtime+size 検証が
   stale bytecode を再利用し、一時的に tampered 挙動の audit 結果が出た（`__pycache__`
   削除で真の復元を確認）。以後コード改ざん試験後は `__pycache__` を明示削除する。
2. その他の逸脱なし。spot の深行選択は x>=15 assert で機械ガード済み
   （y=14 の事故型を構造的に排除）。

## 出版

- commit A `8222f6f6`: 実験dir 6ファイル（report.md・cand15.py・probe_y15.py・
  spot_y15.py・make_audit_y15.py・output/audit.json）→ fetch-back 6/6 byte一致。
- commit B: K1235 item + 本 log。
- commit C: knowledge README 末尾 bullet。
- 実験dir: `vertical-fiber-two-token-y15-parametric-allz-fit-20261122`。

## 状態・次段階

- **K1235 は status observed のまま**（全称は未証明・本 item は有限fit の機械的証拠のみ）。
- 次の最有力: (a) **y=15 全称証明段階**（verify_y15_universal.py・新規単一オーナー宣言必須・
  B子=出版cand14逐語転写〔x=15 合流子 {14,15}≡{15,14}〕・A子合流の正準順序注意
  〔本fitのx>=15機関assertが実証済み〕・型機械 clip 窓 2y+2=32 の tight 判定
  〔11族連続候補〕・census z=0..79・x=15..70）、(b) 横断法則の一般補題化レーン
  （y=15 の実データ点〔pin行数増加則・th-1スロット算術恰好・8族連続〕を
  組み込んだ族表の一般補題化。fitデータは y=1..15 が揃った）。
- y>=16 族・3トークン以上・固定幅・q点版は非接触のまま。
- **標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。**
