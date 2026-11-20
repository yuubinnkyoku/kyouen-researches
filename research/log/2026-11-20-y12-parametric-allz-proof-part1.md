# y=12族パラメトリック全称証明 part1（正本検証器12チェック）（2026-11-20 長期レーン）

単一オーナー宣言（[宣言ノート](2026-11-20-y12-universal-verifier-single-owner-note.md)・
2026-11-20T17:12:00Z・commit d345c645）に基づく y=12 族着手の第二段階（正本監査 part1）の記録。
正本は[実験dir](../experiments/vertical-fiber-two-token-y12-parametric-allz-proof-20261120/README.md)。
対象は [K1152](../knowledge/items/K1152-two-token-y12-parametric-closed-form-fit.md)
（fit・status observed・2026-11-20 出版・commit da7f032cf8）。
知識itemは [K1162](../knowledge/items/K1162-two-token-y12-universal-verifier-part1.md)。

## 前提確認（着手時）

- 最新 main 再取得: HEAD f4af3e1b6d（17:18:42Z）まで。直前の 5 コミットは他レーンの宣言ノート・
  typo 修正（remo survivor 2件・n11 fold25 第二検証宣言）のみで、y=12 全称段階への着手・宣言はなし。
- K1152 fit レーンの宣言ノート（fe93c969・14:25:00Z）は「全称証明段階は本宣言の保持範囲外」と明示。
- 自レーン宣言 d345c645（17:03:31Z）が main 上に生存・保持範囲は part1（本段階）と part2（昇格判定）。

## 機械構成（17:20-17:45Z頃）

1. y11 正本検証器（K1143 part1・SHA-256 c57baf5c…）から生 2エンジン（H_ordered/H_canonical）・
   K0832 単一トークン表 single_token・mex を 77 行 verbatim 転写。
2. cand11 ブロック 102 行をブロック内 Y→Y11 改名のみで転写（改名以外の差 0 行・Y11 = 11 併置）。
   出版 verify_y11_universal.py 内の cand11.py（K1143 fit）逐語ブロックが直接の転写元で、
   B子 = cand11(z,x,R-1) 全域（x>=11・全z・全R）が出版fit域内。
3. cand12 ブロック 92 行を出版 cand12.py（K1152・SHA-256 79e588b3…）から fit driver と docstring
   を除き verbatim 転写（差 0 行）。ブロック内 q_odd/single_token_val/_bk 重複定義は y10/y11 慣行通り併置。
4. opts12（A子 = x==12 なら cand11(z,12,R-1)〔合流子 (11,12)≡(12,11)〕・それ以外
   cand12(z,x-1,R-1)・B子 = cand11(z,x,R-1)・C子 = 1 xor cand12(z-1,x,R-1)）・
   型機械（clip 2y+2=26・番兵 ±27・tail x+z+13・merge x<=z-13）・12チェック・census runner・main を
   y=12 機械本体として構成。機械組み立てスクリプトでの行単位照合に加え、生成物の
   `ast.parse` を確認。
5. SHA 表記の自己検証: 組み立て時 docstring の cand12 SHA-256 の転写崩れ（1文字分）を
   実 byte 再計算値 79e588b3…149131 に訂正。

## C11 census の設計経緯（本実験ホストの環境制約と設計判断）

- census box（446,040 点/エンジン）の無制限 memo 生エンジン 1 プロセス実行は前身試行で
  OOM kill（exit 137・maxrss 996MB・cgroup 約1.0 GiB）。行ごと cache-clear 版は
  300 秒の単一コマンド上限を超過し実行環境リセットを招いた（2回。この間の局所作業 dir 消失も記録）。
- 対策として bounded-memoization twin を設計: 出版エンジンの code object を
  module globals の浅い複写に再束縛（types.FunctionType）し、再帰参照名（H_ordered/H_canonical）を
  LRU 上限 1,600,000 のキャップ付きラッパへ差し替える。再帰定義の byte は正本と同一で、
  決定的純関数の memo 化は透過・LRU 追い出しは固定訪問順の下で決定的、したがって
  値は出版エンジンと厳密一致し cap は residency のみを制限する。単純な
  `lru_cache(cap)(engine.__wrapped__)` では再帰が無制限キャッシュへ抜ける（level-1 のみ cap が効く）
  ためglobals 差し替えが必須である点を実装前に特定した。
- 実測: ordered 13-15 秒・canonical 15 秒・各 maxrss 約 550-563MB（cgroup 内で余裕）。
  1.6M cap で cache は上限に達しない見込みだが、上限値を明記して監査に残す。
- engine 別コマンド分割（C11ordered/C11canonical → census-<engine>.json）とし、C11 モードが
  両 part を幾何からの再計算期待値（446,040/161,700/4,720・公式再計算）・engine 名・box 表記・
  cache 上限・bad==0 で fail-closed 検証してから merge する構成。

## 実行結果（overall PASS・total_points 6,311,993・total_bad 0）

- C1 21,660/0（両生エンジン）・C1b 41,666/0（K0832・出版cand11・x=12合流子の3要素）・
  C2 224,273/0・C2b 18,964/0・C3 1,125/0・C4 616,484/0（clip 26/番兵27・C4時点 181,374 型）・
  C4t clip 25 で 3,540 収束違反・最初 (60,88,88)（bad 総計外の tightness probe・
  **clip 2y+2=26 が tight・8族連続**）・C7 200,000/0（seed 20261132）・C8 890,765/0・
  C9 915,654/0・C11 892,080/0（ordered 446,040 + canonical 446,040）・C12 1,872,838/0。
- merge corollary 1,417,623 点・tail corollary 232,510 点・不一致 0。型総数 191,789。
- 検証器 SHA-256 f73614f7…・監査 audit.json SHA-256 7dcc4505…（3,141 bytes）・
  census-ordered 195670f0…・census-canonical af4111f8…。

## 決定性と fail-closed

- audit.json・両 census part ファイルとも、同一cwd 2 回＋隔離 tree/cwd/HOME＋PYTHONHASHSEED=random
  1 回の 3 実行で byte-identical（cmp）。監査は時刻・実行時間・パスを含まない。
- fail-closed 検査 3 件（census points 改ざん・merge corollary 改ざん・part 欠落）はすべて
  FAIL-CLOSED メッセージで捕捉・PASS 出力なし。改ざん後は正本復元で PASS・byte-identical 再確認。

## 出版系列（本実行）

1. part1 commit 60622f35（実験dir 6 ファイル: README + verify_y12_universal.py +
   output/audit.json + census-ordered/canonical + published_run.txt）。
   push 直前 HEAD チェック（f4af3e1b6d 不変）→ push → pinned-SHA raw CDN fetch-back 6/6 cmp byte-identical。
2. part2（本コミット）: item K1162 + 本 log。push 直前 3 点確認を実施
   （knowledge README grep `items/K1162-` 0 件・item path 404・list_commits 15 件に K1162 言及 0 件）。
3. part3: knowledge README 末尾 bullet（part2 push の HEAD 取り直し→末尾追記→pinned SHA cmp）。

## 次段（part2・本宣言の継続）

- C1d（出版固定z切片アンカー z=8/9/10/15/16/17 の y=12 行特殊化）の構成。
- census_rows.py 第三実装（z=0..79・x=12..70・R<=x+z+13）による独立 census 照合。
- 上記と 3 回 byte-identical で K1152 の observed→proved 昇格判定を行う。
  K1152 fit レーンは昇格判断を全称段階のオーナー（本レーン）に委ねている。

## 解釈規約

- K1152 は本 part1 出版後も **observed** のまま。昇格は part2 完了まで行わない。
- 行閉鎖・勝敗主張は一切なし。標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて **UNKNOWN** のまま。
- 有限照合は有限観察の機械的証拠であり、trust 境界は y=1..11 系列と同一
  （選択肢分解の健全性・mex 恒等式・有限型空間の完全性）。
