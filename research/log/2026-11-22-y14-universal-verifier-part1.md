# y=14族パラメトリック全称証明 part1（正本検証器12チェック）（2026-11-22 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-22-y14-universal-verifier-single-owner-note.md)・
commit 24e418a9・2026-11-22T19:08:21Z・観測HEAD cd2c1095・push直前に対抗宣言なし確認済み）に基づく
y=14 族全称段階 part1 の記録。正本は
[実験dir](../experiments/vertical-fiber-two-token-y14-parametric-allz-proof-20261122/README.md)。
対象は [K1233](../knowledge/items/K1233-two-token-y14-parametric-closed-form-fit.md)
（fit・status observed・独立第二検証で同一閉形式の独立二導出が確定済み・「次段階の正本監査」を明記）。
知識itemは [K1234](../knowledge/items/K1234-two-token-y14-universal-verifier-part1.md)。

## 前提確認（着手時）

- 最新 main 再取得: 本レーン出版フェーズ着手時点で HEAD 340abef3（main 並走レーンは n11 系
  Part AU/AV batch-17 class 10661 の出版系列と K1058 v4/u4/z4 相互排他定理レーン）。
  直前コミットに y=14 全称段階への着手・対抗宣言はなし（自レーン宣言 24e418a9 が唯一）。
- K1233 fit レーンの宣言ノート（e3a856ad・18:42:55Z）は fit まで・K1233 の独立第二検証レーン
  （dc0a7cfc/04f1b30e）は検証までを範囲とし、全称段階は自宣言 24e418a9 が最初で排他モノなし。
- part1 push 直前の採番 3 点確認: knowledge README grep `K1234` 0 件（822,311 bytes・main）・
  item path `K1234-*` なし（items 一覧）・list_commits 30 件に K1233 言及 0 件（前回了: K1233）。

## 機械構成

1. 母体は出版 y13 part1 正本機械（K1232・commit ee3b6f73・SHA-256 b73d9aaa…）。
   imports + mex + 生2エンジン + K0832 単一トークン表を verbatim（同 byte は y11 正本の
   77 行 verbatim と y12/y13 出版時に確定済み）。
2. cand13 ブロック（B子）: y13 part1 機械の cand13 セクションをブロック内 Y→Y13 改名のみで転写
   （word-boundary Y 39 トークンの count-assert・改名以外の差 0 行。Y13 = 13 併置で cand14 ブロックの
   Y = 14 と共存。本ブロックは出版 cand13.py〔K1231・SHA-256 cb903c56…〕の fit driver 除外
   逐語転写で全称証明は K1231。隣接前族をB子に逐語転写するのは y11/y12/y13 機械
   （B子=cand10/cand11/cand12）に続き 4 連）。
3. cand14 ブロック: 出版 cand14.py（K1233・commit b6f74dfc・実 byte 再計算一致 61782b6e…）から
   docstring と fit driver を除き verbatim（差 0 行・ブロック内 Y 47 トークン count-assert）。
   ブロック内 q_odd/single_token_val/_bk 重複定義は y10-y13 慣行通りブロック毎に併置。
4. y=14 機械本体: opts14 の A子 = x==14 なら cand13(z,14,R-1)〔合流子 (13,14)≡(14,13)・
   x>=15 は cand14(z,x-1,R-1)〕・B子 = cand13(z,x,R-1)・C子 = 1 xor cand14(z-1,x,R-1)。
   型機械 CLIP,SENT = 30,31（clip 2y+2=30・番兵 31・10族連続 tight 候補の追試）・
   tail x+z+15・merge x<=z-15・census box 'z=0..79, x=14..70, R=0..x+z+15'・C12 深格子
   z=0..120・x=14..120・R<=x+z+17。y13 part1 版のyw依存数値（census box cap・merge/tail
   定数・B子 tail 窓アンカー (x+13)%2・seed を 20261142 に更新）を y=14 族定数へ差し替え。
   機械組み立てスクリプト（全置換に count assert）による再生成物は実行物と byte 一致
   （出版前に再確認）。
5. 組み立て時健全性 spot 4 種はすべて不一致 0: cand14 vs 独立第二検証レーン cand14 55,692 点・
   cand14 vs 生エンジン 2,268 点・cand13 vs 生エンジン 1,533 点・x=14 merger 行 970 点。

## C11 census の設計（y12/y13 part1 と同一設計の再適用）

- 実行ホストの cgroup RAM 上限（1,090,519,040 bytes ≒ 1.0 GiB）で census box
  （444,600 点/エンジン）を無制限 memo 生エンジンで 1 プロセス実行すると OOM kill する
  （y12 前身試行の実測記録〔y12 part1 published_run.txt〕と同一ホスト・同一上限）。
- 対策は同一設計の bounded-memoization twin（出版 code object を module globals 浅複写に再束縛し
  再帰参照を LRU 上限 1,600,000 のキャップ付きキャッシュへ差し替え）+ engine 別コマンド分割
  （C11ordered/C11canonical → census-<engine>.json）+ C11 モードでの fail-closed merge
  （engine名・box 表記・cache 上限・幾何からの再計算期待値 444,600/144,534/4,560・bad==0 を
  検証してから merge）。
- run1 実測: ordered 14.8秒・canonical 16.6秒・cgroup 内で OOM なし。

## 実行結果（overall PASS・total_points 6,377,860・total_bad 0）

- フル12チェック（チェック名明示）: C1 22,230/0（両生エンジン）・C1b 42,447/0（K0832・
  出版cand13〔B子〕・x=14合流子の3要素）・C2 222,705/0・C2b 19,140/0（深tail行 z∈{60..400}）・
  C3 1,185/0（選択肢集合の生列挙完全一致）・C4 606,427/0（clip 30/番兵31・C4時点 248,232 型・
  identity/confluence とも 0）・C4t clip 29 で 2,480 収束違反・最初 (60,92,92)
  （bad 総計外の tightness probe・**clip 2y+2=30 が tight・10族連続
  y=5..14: 12/14/16/18/20/22/24/26/28/30**）・C7 200,000/0（seed 20261142・z,x<=3000）・
  C8 993,021/0（境界多様体・dx∈[-30,17]・tail 窓 [x+z+15, x+z+17]）・C9 910,710/0（vシェル）・
  C11 889,200/0（両 part merge）・C12 1,864,368/0（深格子 z=0..120）。
- merge corollary（x<=z-15 → single_token(x+14,z,R)）1,370,848 点・tail corollary
  （R>=x+z+15 → (x+14) mod 2）212,713 点・不一致 0。型総数 281,912。
- 監査 SHA: verify_y14_universal.py 4ecdec11…・audit.json
  f8f7180f958ebda39cc0e2efdb64b00416d8e01ea901ef2970201e870d6b7d76（3,105 bytes）・
  census-ordered 6bb64b3c…・census-canonical f31a990e…。

## 決定性と fail-closed

- audit.json・両 census part ファイルとも、同一cwd 2 回＋隔離 tree/cwd/HOME＋PYTHONHASHSEED=random
  1 回（census parts は隔離側で再生成）の 3 実行で byte-identical（sha256sum 3 組一致）。
  監査は時刻・実行時間・パスを含まない。
- fail-closed 検査 3 件（census points 改ざん 444,600→444,601・merge corollary 点数改ざん・
  ordered part 欠落）はすべて FAIL-CLOSED メッセージで捕捉・PASS 出力なし。
  改ざん後は正本復元（sha 再確認）でフル12チェック再実行・byte-identical を確認。
- audit.json は最後に実行したモードの監査を同じパスに書くため、出版正本はチェック名明示の
  フル12チェック実行で確定（単体 C11 モード・default モードは部分監査で上書きする点に注意）。
- builder（scripts/build_verify_y14.py）の再生成物は実行物と byte 一致（出版前に再確認）。

## 出版系列（本実行・scripts/ 誤配置修正の誠実記録つき）

1. commit A 677ced40（実験dir 7 ファイル…ただし組み立てscriptの path を scripts/ ではなく
   実験dir直下に書いてしまった: push_files に渡した path 定数の手違い。byte 内容自体は正本）。
   push 直前 HEAD チェック（340abef3 不変・実験dir/対抗宣言なし）→ push。
2. fix commit 94069d48: scripts/build_verify_y14.py を正位置に配備（byte 内容は
   677ced40 の誤配置コピーと同一・SHA-256 24246a5d…）。fix commit 9050d4f6: 実験dir直下の
   誤配置コピーを削除。以後の fetch-back byte 検証（commit-pinned raw CDN + cmp）は
   9050d4f6 で 7/7 ファイル一致で完了。
3. commit B（本コミット）: item K1234 + 本 log。push 直前に採番 3 点確認を実施
   （knowledge README grep `K1234` 0 件・items 一覧に K1234-* なし・list_commits 30 件に
   K1234 言及 0 件。前回了: K1233）。
4. commit C: knowledge README 末尾 bullet（K1234 part1 の要点・commit B push の HEAD 取り直し→
   末尾追記→pinned SHA cmp）。

## 次段（part2・本宣言の継続）

- preflight_c1d_y14.py: C1d アンカー組み込み前 fail-closed 事前検証（出版アンカー×H_ordered×
  H_canonical×cand14 の 4 方照合 + 低 R 単一トークン縮約の y=14 行照合）。anchor block は
  y13 part2 正本検証器（079b49ad…）から verbatim 抽出。
- census_rows.py 第三実装（y13 版の adapt・XMIN=14, XMAX=70, RBUF=16, tail (x+14)%2・
  rows 80*57=4,560）+ C11r。
- 検証器 in-place 拡張（C1d/C11r 追加）+ フル14チェック 3 回 byte-identical + fail-closed で
  **K1233 を同番号で observed→proved に昇格**（K1141/K1143/K1152/K1162/K1231 の前例と同一手続き）。
  3トークン以上・y>=15 族は範囲外のまま。

## 解釈規約

- K1233 は本 part1 出版後も **observed** のまま。昇格は part2 完了まで行わない。
- 行閉鎖・勝敗主張は一切なし。標準 11×11 空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 はすべて **UNKNOWN** のまま。
- 有限照合は有限観察の機械的証拠であり、trust 境界は y=5..13 系列と同一
  （選択肢分解の健全性・mex 恒等式・有限型空間の完全性）。
