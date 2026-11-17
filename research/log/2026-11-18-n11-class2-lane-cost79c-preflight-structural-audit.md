# 2026-11-18 n11 class2-lane: cost79c 構造事前監査

## 開始時点と参照した正本

最新の commit search で確認した main の先頭は `06e7bb70f392084a3ccbabb02cae621587184c3b`。branch / PR は作成しない。

作業前に `AGENTS.md` と `research/knowledge/README.md` を読み、関連する正本として K0023、K0863、K0865、K0868、K0907、K0909 を確認した。直近の実験記録は cost78c の census v12 cross-lane agreement（7/7 PASS）と cost79c claim v1。cost79c claim はまだ `batches_run=0` であり、探索結果は存在しない。

## 独立に再導出した幾何

対象S6は `00000000000000c09002000200000000`、石位置bitは `[33,49,60,63,70,71]`。

K0868の生残手規約に従い、座標を `(x=i mod 11, y=floor(i/11))` として、浮動小数を使わないBigIntの4×4持ち上げ行列式で再計算した。

- 6石親の15個の四点部分集合に禁止配置なし。
- 全115空セルを走査し、既存6石の全20三点組との行列式を検査。
- 生残候補は79個。claimの `legal_candidates` と完全一致し、差分は0。
- 79候補はopen 68個と確認11個に、重複・欠落なく分割される。
- driverのbatch 1〜8はサイズ `9,9,9,9,9,9,9,5` でopen 68個を完全分割。batch 9は確認11個と完全一致。
- 深さ10、1 bit当たりcap 1e9、andclose 1、対象childの指定を確認。
- v17/v15 runnerのGit blob SHAはclaimのpinと一致。driverは `--nocontrol` を渡さず、v17のpilot_d6（loss=false・3402 nodes）を各batchで必須実行する。各候補でfreshEngineを作り、v17のfbt probe飽和時fallbackもソース上で確認した。

## D4対称性と確認候補

確認11 bitすべてについて、対象7石rootをD4の8変換で正準化し、claimの `root_canon` と11/11一致した。bit110はcost73k bit87の出版manifest（blob `0892aed0...`）にあるWIN7 rootと正準形が一致することも確認した。

さらに、親S6のD4安定化群は恒等変換のみで、79個の合法な7石rootのD4正準形も79/79個すべて異なる。したがって、この行の79候補には盤面対称性による追加の重複削減余地はない。open 68件は、別の既知verdict転送がない限りそれぞれ探索対象のままである。

なお、確認bitの対象側11正準形とbit110の既知WIN sourceは今回再検査したが、残り10件のsource raw rootはこの監査では再取得していない。そこはcensus v12 overlayとcost79c claimの既存転送記録を引き継ぐ。

## 結果

17/17 checks PASS。再現用Node.jsスクリプトと機械可読JSONを同じexperiment directoryに追加した。実行時の入力pinはclaim・driver・v17・v15・cost73k manifestのGit blob SHAで固定した。

## 探索を開始しなかった理由

Proxmoxの観測値は、pve-hp-aioが空き1.64 GiB・メモリ使用率89.3%、pve N100が空き6.35 GiBだがCPU iowait 21.3%。稼働中VM124は4 vCPU・root空き3.6 GiBで、git/node/python3/uvが見つからなかった。専用checkoutと実行環境を安全に用意できないため、9 batchの深さ10探索は起動していない。共有ホストへ新規の重い負荷は載せていない。

## 解釈境界と次の作業

この監査は探索前の構造確認であり、新しいverdict・証明書・receipt・manifest閉鎖はない。cost79c claimの `batches_run=0` は変更していない。実行環境が整った後、既存driverでbatch 1〜9を実行し、raw JSONLをpin付きで保存する。WIN7-D10が出た候補だけ盲検抽出・独立検証へ進める。

`REFUTED-D10` は深さ10以内の先手勝ちが見つからなかったという結果であり、LOSS証明ではない。標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はすべて **UNKNOWN** のまま。
