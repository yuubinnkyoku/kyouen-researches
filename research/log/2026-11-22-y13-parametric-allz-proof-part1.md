# y=13族パラメトリック全称証明 part1（正本検証器12チェック）（2026-11-22 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-22-y13-universal-verifier-single-owner-note.md)・
2026-11-22T17:59:40Z・commit 7196cbd570c638ffbdcf8edfb17ccd8b6df8ead3）に基づく y=13 族
全称段階 part1 の記録。正本は
[実験dir](../experiments/vertical-fiber-two-token-y13-parametric-allz-proof-20261122/README.md)。
対象は [K1231](../knowledge/items/K1231-two-token-y13-parametric-closed-form-fit.md)
（fit・status observed・2026-11-22 出版・「次段階の12チェック全称監査」を明記）。
知識itemは [K1232](../knowledge/items/K1232-two-token-y13-universal-verifier-part1.md)。

## 前提確認（着手時）

- 最新 main 再取得: 着手時点で HEAD 5b6af2ed（17:55:39Z・K1231 fit 出版系列の直後）まで。
  直前コミットに y=13 全称段階への着手・宣言はなし（自レーン宣言 7196cbd5 が最初）。
- K1231 fit レーンの宣言ノート（d3404db8・17:01:05Z）は「fitから全称証明段階まで保持」を明示して
  おり、自宣言は part1+part2 保持として K1231 の正本監査実施者を明確化・矛盾なし。
- 並走レーンは n11 系（Part AS batch-14 class 23101 reaudit・Part AT q042 if-adopted 分解。
  18:13Z 時点で出版系列進行中）・k=8/k=9 arc counts レーンなどの非接触領域。
  y=13 全称段階のオーナーは自宣言のみで対抗宣言なし。

## 機械構成

1. 母体は出版 y=12 part2 正本機械（K1152/K1162・verify_y12_universal.py SHA-256 e2092976…）。
   imports + mex + 生2エンジン + K0832 単一トークン表を verbatim（同 byte は y11 正本の
   77 行 verbatim と y12 part1 出版時に確定済み）。
2. cand12 ブロック（B子）: y12 機械の cand12 セクションをブロック内 Y→Y12 改名のみで転写
   （word-boundary Y を含む行数 == 改名差分行数の count-assert・改名以外の差 0 行。
   Y12 = 12 併置で cand13 ブロックの Y = 13 と共存。B子 = 出版 K1152 全称族の逐語ブロック。
   全称証明済み族をB子に逐語転写するのは y11 機械の cand10・y12 機械の cand11 に続き 3 例目）。
3. cand13 ブロック: 出版 cand13.py（K1231・SHA-256 cb903c56…6e2e09・実 byte 再計算一致）から
   docstring と fit driver を除き verbatim（差 0 行）。ブロック内 q_odd/single_token_val/_bk
   重複定義は y10-y12 慣行通りブロック毎に併置。
4. y=13 機械本体: opts13 の A子 = x==13 なら cand12(z,13,R-1)〔合流子 (12,13)≡(13,12)・
   x>=14 は cand13(z,x-1,R-1)〕・B子 = cand12(z,x,R-1)・C子 = 1 xor cand13(z-1,x,R-1)。
   型機械 CLIP,SENT = 28,29（clip 2y+2=28・番兵 2y+3=29・9族連続 tight 候補の追試）・
   tail x+z+14・merge x<=z-14・census box 'z=0..79, x=13..70, R=0..x+z+14'・C12 深格子
   z=0..120・x=13..120・R<=x+z+16。y12 part2 版から C1d/C11r 系は除去（part1 は12チェック構成）。
   y12 由来キー名 violations_at_clip25 → violations_at_clip27（print 文言含む）を修正。
   機械組み立てスクリプト（全置換に count assert）による再生成物は実行物と byte 一致
   （SHA-256 b73d9aaa…・ast.parse OK）。

## C11 census の設計（y12 part1 と同一設計の再適用）

- 実行ホストの cgroup RAM 上限（1,090,519,040 bytes ≒ 1.0 GiB）で census box
  （445,440 点/エンジン）を無制限 memo 生エンジンで 1 プロセス実行すると OOM kill する
  （y12 前身試行で exit 137・maxrss 996,376KB・行ごと cache-clear 版が 300 秒コマンド上限超過、
  は y12 part1 published_run.txt の実測記録。y=13 は同一ホスト・同一上限）。
- 対策は y12 part1 と同一の bounded-memoization twin（出版 code object を module globals
  浅複写に再束縛し再帰参照を LRU 上限 1,600,000 のキャップ付きキャッシュへ差し替え。
  再帰定義の byte は正本と同一・決定的純関数の memo 化は透過・LRU 追い出しは固定訪問順で
  決定的）+ engine 別コマンド分割（C11ordered/C11canonical → census-<engine>.json）+ 
  C11 モードでの fail-closed merge（引擎名・box 表記・cache 上限・幾何からの再計算期待値
  445,440/153,117/4,640・bad==0 を検証してから merge）。
- 実測: ordered 13.3秒・canonical 16.4秒・各 maxrss 約 549-562MB（cgroup 内で余裕）。

## 実行結果（overall PASS・total_points 6,353,143・total_bad 0）

- default mode（C11 抜き 11 チェック + C4t）: PASS・5,462,263 点・corollary merge 1,085,513・
  tail 208,062（C11 加算前）。
- C11ordered / C11canonical: 445,440 点 bad 0・merge 153,117/0・tail 4,640/0（各エンジン）。
- フル12チェック: C1 21,945/0（両生エンジン）・C1b 42,041/0（K0832・出版cand12〔B子〕・
  x=13合流子の3要素）・C2 226,527/0・C2b 19,052/0（深tail行 z∈{60..400}）・C3 1,155/0
  （選択肢集合の生列挙完全一致）・C4 611,504/0（clip 28/番兵29・C4時点 214,984 型）・
  C4t clip 27 で 2,987 収束違反・最初 (60,90,90)（bad 総計外の tightness probe・
  **clip 2y+2=28 が tight・9族連続 y=5..13: 12/14/16/18/20/22/24/26/28**）・
  C7 200,000/0（seed 20261132・z,x<=3000）・C8 953,151/0（境界多様体・dx∈[-28,17]・
  B子 tail 窓アンカー付き）・C9 913,194/0（vシェル）・C11 890,880/0（両 part merge）・
  C12 1,862,190/0（深格子 z=0..120）。
- merge corollary（x<=z-14 → single_token(x+13,z,R)）1,391,747 点・tail corollary
  （R>=x+z+14 → (x+13) mod 2）217,342 点・不一致 0。型総数 234,180。
- 監査 SHA: verify_y13_universal.py b73d9aaa…・audit.json
  db7c5fa56f407f09ed6604d7677aaab681d78649dc85379d977c5bd58c8e42de（3,103 bytes）・
  census-ordered 264d7cd8…・census-canonical 82fb8803…。
- 12チェック満点監査 wall 約 32.8 秒。

## 決定性と fail-closed

- audit.json・両 census part ファイルとも、同一cwd 2 回＋隔離 tree/cwd/HOME＋PYTHONHASHSEED=random
  1 回の 3 実行で byte-identical（sha256sum 3 組一致を確認）。監査は時刻・実行時間・パスを含まない。
- fail-closed 検査 3 件（census points 改ざん 445,440→445,439・merge corollary 点数改ざん・
  canonical part 欠落）はすべて FAIL-CLOSED メッセージで捕捉・PASS 出力なし。
  改ざん後は正本復元（sha 再確認）で PASS・フル12チェック再実行で byte-identical を確認。
- audit.json は最後に実行したモードの監査を同じパスに書くため、単体 C11・default モードは
  部分監査で正本を上書きする点に注意（本実験では検査後にフル12チェックで正本を再確定）。

## 出版系列（本実行）

1. commit A ee3b6f7325d6d4ae697f93d1f4c520dfd06f59f3（実験dir 6 ファイル: README +
   verify_y13_universal.py + output/audit.json + census-ordered/canonical + published_run.txt）。
   push 直前 HEAD チェック（175864a5 不変）→ push → commit-pinned raw CDN fetch-back 6/6 cmp byte-identical。
2. commit B（本コミット）: item K1232 + 本 log。push 直前に採番 3 点確認を実施
   （knowledge README grep `K1232` 0 件・item path 404・list_commits 30 件に K1232 言及 0 件。
   前回了: K1231 が y=13 fit として最新採番）。
3. commit C: knowledge README 末尾 bullet（commit B push の HEAD 取り直し→末尾追記→pinned SHA cmp）。

## 次段（part2・本宣言の継続）

- preflight_c1d_y13.py: C1d アンカー組み込み前 fail-closed 事前検証（出版アンカー×H_ordered×
  H_canonical×cand13 の 4 方照合 + 低 R 単一トークン縮約の y=13 行照合）。
- census_rows.py 第三実装（y=12 版の adapt・XMIN=13, XMAX=70, RBUF=15, tail (x+13)%2）。
- 検証器 in-place 拡張（C1d/C11r 追加）+ フル14チェック 3 回 byte-identical + fail-closed で
  **K1231 を同番号で observed→proved に昇格**（K1141/K1143/K1152/K1162 の前例と同一手続き）。
  3トークン以上・y>=14 族は範囲外のまま。

## 解釈規約

- K1231 は本 part1 出版後も **observed** のまま。昇格は part2 完了まで行わない。
- 行閉鎖・勝敗主張は一切なし。標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて **UNKNOWN** のまま。
- 有限照合は有限観察の機械的証拠であり、trust 境界は y=1..12 系列と同一
  （選択肢分解の健全性・mex 恒等式・有限型空間の完全性）。
