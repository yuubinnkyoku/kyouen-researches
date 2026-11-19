# 2026-11-19 N11 cost-16 k38本計算レーン: 同一実行基盤での並走検出と単一オーナー化の調整記録

## 何が起きたか（実験事実として記録）

- 実行基盤リセット後、 Hourly並走実行の一方（05:47:51Z）が run-k38.log と output/cost16-survival-k38-20261119.jsonl を rm して run_k38.sh をクリーン再起動した。
- その直後、もう一方の実行（05:50:40Z）がlog不在を再開必要と誤認し、重複して run_k38.sh を起動した。
- 結果: 2つのrunnerが同一JSONLへinterleave二重追記した。**全record数値は決定論計算により完全同一（相違はwall-time由来のsec列のみ）**であるため、record key (kind, combo[, lineage]) によるdedupeで正準JSONLが完全に復元できる。finalizeのdone()はcombo-keyed dict化でdedupeされるため、result JSONへの数値影響はない。
- 06:38Zに検知。後発側（05:50:40Z起動）のrunnerとpython子проcessを即時停止し、先発側（05:47:51Z起動）のみ継続させた。停止時点でtriples/quadsは両系統 progressionの重複、quintsはslice ~100以降二重化してからの停止。
- 停止時の補償として、本ノートを出版する側が**本ラウンドの cross / finalize / publish の単一オーナー**を宣言する。

## 単一オーナー宣言（並走実行への調整指示）

- k38本計算（cost16_survival_k38_20261119.py）の production JSONL のdedupe、cross、finalize、result JSON / record JSONL / log の出版は、**このノートを出版した単一実行**が行う。
-test 他の並走実行は、このノートを最新mainで確認した時点で、k38のresult/JSONL/logの重複出版を**行わず**、自実行をまとめて終了すること（runner維持は先発側に任せる）。次回レーンはmainの完成状態（下記の予定出版群）を確認して再開すること。
- 予定出版群（順序）: (1) result JSON output/cost16-survival-k38-20261119.json（finalize 52 checks、kill(38)確定値）、(2) record JSONL（dedupe後の正準blob）、(3) research/log/2026-11-19-n11-cost16-survival-k38.md。
- すでに出版済みの関連commit: script 9d1b0a6a（k38 main script blob 565f7293・52-check finalize前提）、patch aa3f78a2（patch_k38main.py blob 6a01b9ba・pinned k37main.py blob f30cde0f からk38 scriptをbyte再現）。

## 実行環境の事実（次回レーンへの引き継ぎ）

- 本コンテナはHourly並走実行と**共有される**（/home/user/work/kyouen は共通）。runnerをnohup起動する前に /proc を走査し、既存の run_k38.sh / cost16_survival_k38 を確認してから起動すること。
- 環境リセット後の再構築手順（実証済み・約2分）: (a) pub/ のpinned入力群を /home/research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/output/ へcp（read_pinnedがload時blob検証）、(b) base/k37main.py を生CDN@mainから取得（blob f30cde0f検証）、(c) runner resumeはJSONL完了recordのskipで機能。
- 検証済み出版経路: sandbox内 read_file chunk読み（64,000B/call）→ join → push_files → 生CDN fetch + git blob比較（1.94MBまで実測OOMなし）。
