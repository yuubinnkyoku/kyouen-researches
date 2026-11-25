# 2026-11-22：(8,12) 帯閉包の完了と記録公開 — M_{8,12}=17 EXACT・w=8 で2例目の完全決着

前回セッション（2026-11-15）は3回の実行環境リセットと VibeFS 障害で中断し、q12 掃引 231..882 の
完走分を含むローカル成果物の格納を次回に回した（実験 README の「環境障害の記録」参照）。
本セッションは knowledge マウント（_q12band-takeover-kit: 正本 records/sweep-q12.jsonl・3シャード・
checksums・較正記録・scripts・src oracles・kissat）で成果物一式を復旧した「接管セッション」であり、
掃引を完走して全記録を公開し、claims を完了形に更新した。

## 成果1：q12 掃引 231..882 の完走と全866幅 UNSAT の確認

- genfam12.js + sweep-q12.sh（kissat 4.0.4 def-mode・resume-safe）で m=231..882 を完走。
- 正本 records/sweep-q12.jsonl（866行・md5 9c628f8e25ca541d82491e322743789a）を再集計:
  **m=17..882 の全866幅 UNSAT（INDET 0・SAT 0・欠落 0・連続・q=12・rc 全て 20）**。
- conflicts は min 679（m=51）・max 6,653（m=17）・median 1,655.5（下側中央値 1,655）・
  p90 2,868（nearest-rank）・総計 1,598,748。
- 既完走の 17..230 と合わせ witness-free 帯 17..882 が確定し、U_{8,12}=883（K0318 proved）
  との合わせで **M_{8,12}=17 EXACT（w=8 では (8,11) M=21 に続き2例目の完全決着）**。

## 成果2：接管較正 29/29 PASS（commit baf00946）

- (A) 11/11 — sat2.js 全三つ組census vs genfam12 CNF byte-identity（8×11..16 q11/q12）
- (B) 10/10 — genfast.js 弦対census vs genfam12 CNF byte-identity（8×17/20/26/40/60 q11/q12）
- (C) 8/8 — 公開済み records/sweep-q11.jsonl の CNF md5・vars・clauses が
  m=21,26,40,100,300,500,700,907 で再現
- 記録: records/calibration-takeover-20261122.jsonl。scripts（genfam12.js・sweep-q12.sh）は
  832ae3cc・85dd161d で byte-exact 体裁整えまで完了。

## 成果3：記録の3シャード公開と byte 検証

正本を300行単位の3シャードに分割して push_files で公開（push 時の転記エラーは fetch-back
検証で検出・修正し、最終的にシャード md5 まで一致を確認）:

- shard1 m=17..316（300行・md5 2ffc285045d40230cb72e5e86db2c0f4）:
  3de95445 → byte-fix 1a9e6e43 → byte-fix 2 e6d7652d
- shard2 m=317..616（300行・md5 898b981feafbadaef4bcdbb5695c1a48）: 5d03e08b（一発一致）
- shard3 m=617..882（266行・md5 6e86b860cd39603da89a64bbdb0436a2）:
  559de93a（"clausees"→"clauses"・"cnf_MD5"→"cnf_md5" の2箇所転記ミス）→ 修正 33f4d041
- 3シャードの連結は正本と cmp で byte-exact。md5 対照表は records/sweep-q12.checksums。

## 成果4：claims の完結（本 commit）

- experiment README: 状態を (8,12) COMPLETE に更新、(8,12) 節に掃引統計とシャード検証を記載、
  接管較正節を追加、ファイル欄と環境障害記録を解決済みに更新。
- claim-20261115.json: status COMPLETE、q12_in_flight を q12_complete（M=17 exact・統計・
  接管記録・session_log）に置換、environment_note を解決済みに更新。
- K0843: 主張4を M_{8,12}=17 exact に更新、シャード・checksums・接管較正・scripts の
  7 artifacts を追加、title/scope/evidence/限界を両帯完了の体裁に更新。
- results/fixed-width/mwq_stabilization.csv 行31: (8,12) を
  exact-threshold,8,12,12,17,proved に置換（CSV 内 w=8 では (8,11) に続き2行目）。

## 成果5：公開成果物からのサンプル再実行 — 8/8 bit-exact

main に公開済みの scripts/genfam12.js と sat2.js/sat.js
（seven-row-inband-families-20261114; md5 はキットと同一）だけを用いて CNF を再生成し、
公式 release から新規ダウンロードした kissat 4.0.4（binary md5 3a5eba830aa6008a604fcc9bbe99a325・
掃引時の binary と bit-exact 同一）で再解決した:

- 対象8幅: m=17（conflicts max）・51（min）・231（接管掃引の起点）・316/317・616/617
  （シャード境界）・882（最終幅）
- **8/8 すべて CNF md5・vars・clauses が公開記録と bit-exact 一致し、kissat 再実行も
  UNSAT・conflicts が公開記録と bit-exact 一致**（6,653 / 679 / 2,097 / 1,835 / 1,668 /
  1,869 / 1,731 / 1,996）
- 記録: records/rerun-sample-20261122.jsonl（tag rerun-1）
- 位置づけ: 同一実行環境という限界はあるが、CNF 生成から解決まで公開成果物のみで
  再構成される点で掃引実行とは独立の確認経路。別環境での全幅独立再実行は今後の課題。

## 残務（後続レーン）

- decode_model.js・verify_all.js・SAT フロンティア生ログ・UNSAT 生ログ batch tar は未格納
  （binary は push 経路なし・records の conflicts/CNF md5 が当面の整合担保）。
- (8,12) の完全な独立第二検証（別実装・別環境での掃引全幅再実行）は今後の候補
  （第1段階のサンプル再実行 8/8 bit-exact は成果5で完了）。
- 11×11 等の長期レーンは本レーンの管轄外。
