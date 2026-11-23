# 高速レーン実行log: y=18 two-token 全称検証器 part1（2026-11-23）

- 単一オーナー宣言: `2026-11-23-y18-universal-verifier-single-owner-note.md`
  （commit 1d46f883・push 2026-11-23T03:20:06Z・宣言時点観測 HEAD c15b1c3f・
  検証器実行前に事前出版・y=19 fitレーン（コード c15b1c3f・03:11:39Z・「Universal
  stage requires a separate declaration」明記）とは非接触合意〔対向宣言は
  y=19 fitのみで、y=18全称は本レーンが単一オーナー〕）。宣言ノートの事前横断
  予想（clip 38 tight・census幾何・型総数・全チェック点数の機械事前算出）は
  census merge予測1点を除きすべて宣言通り（下記誠実記録）。前回y=18 fit
  出版（K1242・commit 9e898f45/e9bf7991/fa789e27）が指名した次段階
  「y=18 全称（part1 12チェック+part2 C1d/C11r・K1242 昇格）」を実行。

- 選定理由: y<=17 は全称確定済み・y=18 fit は observed（K1242）で、
  y=17レーンと同一の機械翻訳・5世代連続の定型手続きで確実に出版可能かつ
  昇格レーン（part2込み）として情報価値最大と判断。y=19 fitは並走レーンが
  単一オーナー宣言済みのため完全非接触。

- 機械: verify_y18_universal.py（part1・12チェック・38,212 bytes・SHA-256
  14373419…・961行）を y=17 出版正本（verify_y17_universal.py part2正本・
  SHA-256 4253cf29…・commit ab23d120）から族定数適合で構造転写
  （A子 x==18 合流子 cand17(z,18,R-1)〔{17,18}≡{18,17}〕・x>=19 は
  cand18(z,x-1,R-1)・B子 出版 cand17 逐語〔Y→Y17 改名のみ〕・
  C子 1 xor cand18(z-1,x,R-1)・CLIP/SENT=38/39・census z=0..79・x=18..70・
  R<=x+z+19〔80*53=4,240行〕・merge x<=z-19・tail (x+18)%2・
  C7 seed 20261182・C8 の x=17 行は拡張整合行としてのみ・C8深部tail窓は
  出版cand17〔K1240 proved〕tail主張 R>=x+z+18→(x+17)%2 を照合）。
  転写は二重正本方式: scripts/check_transcriptions_y18.py（SHA-256 80fc9c31…）が
  @@TRANSCRIPTION marker 3ブロックを出版bytesと照合。y17機以降は出版機自体が
  markerを保持するため、機ソース抽出はEND marker行で打ち切る
  （engine 1,957 bytes がy17機同一ブロックとbyte一致・cand17 3,465 bytes が
  出版y17機cand17ブロックと出版cand17.py〔commit 6ca80e0e〕の2ソースとも
  Y→Y17改名差分のみで一致〔sources_agree〕・cand18 3,211 bytes が出版
  cand18.py〔commit 9e898f45・fit driver省き〕とbyte一致）→
  output/transcriptions-check-y18.json overall PASS・隔離側再実行もPASS。
  part2は C1d/C11r を in-place 拡張（y=13..y=17 と同一手続き・part1の
  12チェック本体byte不変）。組み立てscriptは出版しない。

- **誠実記録（組み立て段階のregion-splice欠陥・出版前にC1が捕捉）**:
  最初の組み立てbuildは、B子（cand17）ブロックを挿入した後の旧候補region
  切出し位置の探索がファイル先頭から走り、新B子ブロックの持つ
  CAND17-END markerに当たってしまい、テンプレートの旧cand17候補regionが
  新cand18ブロックの後に残存した。残存regionのmodule-level `Y = 17` が
  global Yを再代入し、転写したばかりのcand18テーブルが Y=17 で評価された
  （全特徴が1族分ずれる）。機のC1が即座に捕捉: 23,940点中 1,229 bad、
  不一致署名は1族シフトそのもの（pinが z+2*17+1=35 に現れる等）。builderは
  切出し位置を旧候補ヘッダ以降の最初のEND markerに固定し、構造的一意性
  assert（各転写marker 1回ずつ・module-level Y代入は `Y = 18` の1回のみ・
  閉形式定義1回ずつ・helper再定義数 3/2/2）を追加して修正。転写checkerは
  修正前後ともPASSだった（first-marker抽出のため）ため、builderがmarker
  一意性も検査するよう強化した。出版bytesは修正後のみ。この時に得た
  教訓「y17機以降の出版機はmarkerを保持するため、機ソース抽出・region
  切出しはmarker位置基準」は part2 (preflight/census_rows) でも適用する。

- 結果（part1・overall PASS・約75秒/回〔census両部込み〕）:
  総照合点 **6,354,790・全bad 0**・型 523,398
  （C1 23,940 / C1b 43,296 / C2 225,449 / C2b 19,492〔x∈{18,23,…,68}〕 /
  C3 1,305 / C4 585,189 / C4t 585,189〔probe〕 / C7 200,000 /
  C8 1,035,729 / C9 900,534 / C11 877,680 / C12 1,856,987）・
  型総数系列（y14 281,912 → y15 335,658 → y16 394,686 → y17 457,645 →
  **y18 523,398**）。
  **C4t: clip 37（2y+1）違反 1,012・最初 (60,100,100) → clip 2y+2=38 は
  tight・tight 14族連続確定（y=5..18: 12/14/…/34/36/38）**で
  「最初の違反がband下端 R-z=2y+2 と歩む」則は6観測目
  （(60,90,90)→…→(60,98,98)→(60,100,100)・宣言の事前予想どおり違反>0で
  tight確定）。merge帰結 x<=z-19 → single_token(x+18,z,R)
  1,121,822点 bad 0（宣言どおり z>=37 でcensus merge行が初めて非空・
  4族連続のprobe box外全域census anchor）・tail帰結 R>=x+z+19 → (x+18)%2
  192,210点 bad 0。

- census（C11）: 両エンジン各438,840点 bad 0（merge 110,682・tail 4,240・
  約19秒/engine）。本host（Vibe remote sandbox・~1.0GiB cgroup）は
  y=12..y=17 と同一設計の bounded-memoization twin（LRU cap 1,600,000）で
  C11ordered/C11canonical 別コマンド実行・C11モードで部品検証
  （box文字列改ざん・欠落とも FAIL-CLOSED）の上で期待値幾何再計算と merge。
  **誠実記録**: 宣言noteのcensus merge per-engine機械事前算出は 105,651 と
  していたが、これは宣言note側の算術スリップで、機の独立幾何再計算・
  両census部品の実測は **110,682**（check_C11のfail-closed期待値再計算が
  部品と一致）。他の全予測値（11チェック全点数・part1総計6,354,790・
  census 438,840・tail 4,240・preflight box）は宣言どおり完全一致。

- 決定性: audit.json SHA-256 c090be81…・census-ordered af284ab7…・
  census-canonical 9c817177… の3実行 byte-identical（同一cwd 2回 +
  隔離tree/cwd/HOME + env -i + PYTHONHASHSEED=random・転写検査と両census
  部品は隔離側で再生成しbyte一致）。出版treeで正典runを実行
  （output/published_run.txt: 転写検証→census両部→フル12チェック rc=0・
  audit byte一致）。

- fail-closed 9種（スクラッチtreeで実施・改ざん8種全捕捉+誠実記録1件）:
  T1 census box改ざん → FAIL-CLOSED・T2 census部品欠落 → FAIL-CLOSED・
  T3 cand18 band下端（2Y+2→2Y）→ C2で捕捉・T4 cand18 z-even steady pin
  （z+2Y+1→z+2Y-1）→ C2で捕捉・T5 merge境界（z-19→z-18）→ merge bad>0・
  T6 clip窓（38/39→36/37）→ C4 confluence conf_bad>0・T7 合流多重集合
  （(18,17)→(18,16)）→ C1bで捕捉・T8 A子（cand17→cand18 at x==18）→
  C3/C2で捕捉。**T9 深部tail窓 (19,20,21)→(18,20,21) は bad 0**: これは
  出版cand17（K1240 proved）のtail主張 R>=x+z+18 の内部点 z=x+z+18 での
  整合性で検出対象外（y17のT5拡張整合性観察と同型）。真の境界外
  （17,20,21）シフトは C8 bad 40 で捕捉。C4t passive: clip 37違反1,012>0。

- 解釈規約（宣言どおり）: part1 は K1242 全称の機械的証拠の構成であり
  status は observed のまま。昇格判定は part2（C1d 出版固定z切片アンカー
  〔preflight fail-closed〕+ census_rows.py 第三実装 y=18 版
  〔XMIN=18・RBUF=20〕+ C11r・同一単一オーナー宣言の継続）で行う。
  11×11標準盤・二石root・S2・class 1/2/4 は UNKNOWNのまま、
  照合点数を勝敗として読まない。3トークン以上・y>=19族・固定幅・
  q点版安定化長は非接触。

- 出版: part1 commit A（実験dir: 検証器・転写checker・output 5点
  〔audit/census両部/published_run/transcriptions-check〕・実験README）、
  commit B（K1244 item + 本log）、commit C（knowledge README bullet）。
  push直前にHEAD再取得・K1244の不在を確認（K1243はy=19 fitレーンが
  出版済みのため繰上げ）。

- 次のレジューム: part2着手（part1着地済み・同宣言継続）。preflight_c1d_y18.py
  （出版 verify_y17 正本から anchor block 逐語・y=18 行4方照合
  x=18..45・R<=x+z0+30〔z0∈{8,9,10,15,16,17}〕=12,432点 + 低R単一トークン
  縮約 R<=z+6〔z0∈{15,16,17}・x=18..159〕=9,372点・出力
  output/preflight-c1d-y18.json）→ census_rows.py y=18版（XMIN=18・XMAX=70・
  RBUF=20・ZHI=80・token (x,18)・tail assert R>=x+z+19・出力4,240行）→
  検証器14チェック化（check_C1d掃引 x=18..159・R<=x+61〔127,374点〕・
  check_C11r: values range(0,x+z+21)・tail=(x+18)%2・rows==80*53=4,240）→
  3回byte-identical + fail-closed電池6種 →
  **K1242 observed→proved 昇格**（同一K項目・K1240/K1237前例）・
  K1244 part2追記・part2 log・README bullet・実験README追記。
