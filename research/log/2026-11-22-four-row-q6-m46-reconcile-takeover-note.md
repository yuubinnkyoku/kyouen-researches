# 単一オーナー宣言（takeover）: 4行盤 q=6・M_{4,6} リコンサイル lane の引き継ぎ — 決定幅 m=35..38 の実行・出版（2026-11-22）

- 宣言時刻: 2026-11-22T10:28:15Z（直前の最新 main HEAD: 9854970e6b5ce7d2906bb4cdd413a81d193fe3ff・push 直前に再取得して記録する）。
- オーナー: 高速レーン（本セッション）・単一オーナー。同名の毎時タスクが並走する可能性があるため、本宣言以降は下記スコープへの同内容の並行着手を避けること。

## 引き継ぎの経緯

先行宣言 `research/log/2026-11-21-four-row-q6-m46-reconcile-single-owner-note.md`（commit df64d850・2026-11-21T19:56Z）のスコープを、
同一セッション群で 2026-11-21T20:21Z（part 1・commit e0684625）まで実行した後、実行環境失効で中断した。
part 1 の出版済み成果（(a) PASS・(c) PASS・(d) 較正 PASS・(d) CNF 生成 meta・(b) m=16..19 部分）はそのまま正本とし、
未出版だった (d) の kissat 実行（README 記録の (4,35,6) run1 観測値 UNSAT・conflicts 5,055,908 を含む）・run2・m=36..38・
(b) の高速移植掃引の続行を本セッションが最初からやり直して実行する。

## 本セッションのスコープ（受入条件は先行宣言のまま・fail-closed）

1. **(d) 決定幅 m=35..38（全実行を本環境でやり直す）**: genfast3.js（md5 12c2bd9c…・core sat2.js md5 282ae832…）で
   (4,34,6) 較正 CNF を再生成して出版 md5 1f58cdfc895ef4de493528ebf40d33f2 と byte 一致を確認した後、
   (4,35,6)..(4,38,6) の CNF を再生成し、pinned kissat 4.0.4 linux-amd64（md5 3a5eba830aa6008a604fcc9bbe99a325）で
   各幅 2 回実行・conflicts bit-exact を要求する。(4,35,6) run1 は先行 README の観測値と bit-exact なら相互検証として記録する。
   UNSAT 幅は four-row-q6-q7-frontier-20261121 への第5次帯延伸（output/q6ext5/ + scripts/append_records_q6d.js +
   records.jsonl append）として出版する。
2. **(b) 高速移植掃引の続行**: published port_fast_17_35.jsonl（m=17..19 一致済み）の後続 m=20..35 を
   同一 driver design（m ごとに node 起動・jsonl 既存 (m,target) 検査で resume）で続き、7計数フィールド照合を行う。
   予算で全幅に届かない場合は「m≤N まで第三実装一致・残り未検証」と明記して区別する。
3. **リコンサイル判断の出版**: (a)-(d) すべて受入条件を満たした場合のみ、新規 K 項目で M_{4,6}=16（K0302 先行証明・
   複数系統検証）のリコンサイルを記録し、K1177 側区間表記との接続・mwq_stabilization.csv・results/fixed-width README・
   knowledge README 末尾 bullet を更新する。（b) が部分完了の場合は現状維持・誠実記録のみ。

## 非目標（先行宣言と同一）

- 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2・class 1/2/4 は本レーンの無関係・UNKNOWN のまま。
- 未掃引幅（39+）への不存在主張はしない。conflicts 数・実行秒数を勝敗として読まない。
- branch/PR は作らず main に直接出版する。fetch-back は byte/sha 照合で行う。
- K0414/K0374 系譜・n11 S5 frontier・five-row/six-row/eight-row の各帯掃引レーンには一切触れない。
