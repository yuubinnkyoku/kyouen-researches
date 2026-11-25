# 2026-11-17 n11 class2-lane: hybrid seed union preflight blocked

## 開始時点

最新 main は `03655b567a7ab76da080b2831c07efdd36bfeeed`（2026-11-17 13:22:32 UTC）。
`AGENTS.md` と `research/knowledge/README.md`、K0023・K0725・K0757・K0783・K0868・K0909、cost73k の境界4-way測定・seed容量設計・hybrid seed設計、および既存の measurement claim を確認した。

既存claimは `CLAIMED_IN_PROGRESS` だが `batches_run=0`。このmainにはhybrid seedの実測結果はなく、262件の実key/valueもまだ公開されていない。

## 実行環境の事前確認

Proxmox上で既存の計算環境を確認したが、今回の実測を安全に開始できる専用環境は見つからなかった。

- `pve-hp-aio`: 6 CPU core、ホストの利用可能メモリ1.39 GB、swap使用2.07/8.00 GB。CPU負荷は低いが、ホスト側メモリ余裕が小さい。
- 同ノードのVM 124: 4 core・12 GB設定。ゲスト内のMemAvailableは7,149,752 kB、ルート領域の空きは約3.6 GB。ただし、ゲスト内に `git`・`node`・`python3`・`uv`・`curl`・`nix` がなく、`/root/.nix-profile/bin` にも存在しない。
- `/tmp/kyouen-researches` は部分checkoutで、AGENTS・knowledge README・過去logのみ。今回必要なcost73kの実験スクリプトはない。`/tmp/kyouen-research-work/repo` は2026-11-16時点の別checkoutで、今回のpin付き実験一式ではない。
- `/tmp` と `/root` を対象に73k・memo・seed・dump名および50 MB超の一時ファイルを探したが、worker dumpや262件のkey/valueは見つからなかった。
- `pve`（Intel N100）は4 core・利用可能メモリ6.34 GBだが、稼働中のコンテナは既存サービス用であり、研究用の隔離環境ではないため使用しなかった。

## 判断

**実測ジョブは起動していない。** これは探索のtimeoutや失敗ではなく、実行前の環境確認で停止したもの。

したがって、以下はすべて未実施のまま。

- W0..W3および2-way A/Bのpin付き再構築
- 262件のonly-in-2way key/valueの抽出
- hybrid KYOENWM2 seedの生成
- MS=1<<25でのseed挿入・record identity・矛盾検査
- 22 rootの再実行と証明書22/22 byte一致確認

測定claimは `BLOCKED_PREFLIGHT` に変更し、`batches_run=0` を維持する。設計値やnode数を実測値として扱わない。

## 再開条件

- Git・Node.js 22・Python 3を使える専用の隔離guestを用意する（または既存guestへ導入する）。
- 4 workerのraw dump再構築とMS=1<<25 seedrunに必要なメモリ・ディスク余裕を確保する。
- pinned blobの照合後に262件を実データとして抽出し、FINAL4の順序を保ったhybrid seedを作る。
- seedrunのrecord identity・矛盾0・証明書22/22 byte一致を満たすまで、性能改善やcache完全性を成果扱いしない。

## 解釈ガード

新規WIN/LOSS verdictなし、証明書bytes不変、manifest行の閉鎖なし。WIN7-D10は個別7石rootの深さ10以内の先手勝ちのみを示し、REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWN。
