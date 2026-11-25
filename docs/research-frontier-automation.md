# 研究フロンティアの cron 実行

`scripts/research_frontier_cron.py` は永続 Linux ホスト上の cron から、最新 main を読み、最大 4 時間 50 分の Codex 研究を開始する補助です。使用量の上限で失敗した回は、次の cron で 1・2・4・6 時間の間隔をおいて再試行します。上限を回避する処理はありません。quota 回復後に再び成功するには、同じホストと認証が有効なまま必要です。

クラウド task の VM や snapshot は常駐プロセスを維持しません。この補助を保存したことは、Codex cloud の将来 task、quota リセット、VM 再起動をスケジュールしたことを意味しません。

## 永続ホストへの設定

Python 3.11+、Git、Codex CLI、起動中の cron service、Codex の通常のログイン、対象 repo の read / push 権限を準備してください。認証ファイルを cloud VM からコピーせず、ホストの正規の `codex login` で認証してください。Codex CLI の `--approve-for-me` を利用するため、同オプションを提供するバージョンを使ってください。sandbox と承認レビューを無効にしません。

専用 checkout を使い、別の人や task と同時に変更しないでください。Git worktree は不要です。以下は永続ホストで実行する例です。`/srv` の例は、そのユーザーが読み書きできるディレクトリに置き換えられます。

```sh
git clone https://github.com/yuubinnkyoku/kyouen-researches.git /srv/kyouen-researches
codex login
python3 /srv/kyouen-researches/scripts/research_frontier_cron.py \
  --repo /srv/kyouen-researches --state-dir /srv/kyouen-frontier-state --preflight
python3 /srv/kyouen-researches/scripts/research_frontier_cron.py \
  --repo /srv/kyouen-researches --state-dir /srv/kyouen-frontier-state --install-cron
crontab -l
```

preflight は最長 60 秒の read-only inference を確認します。インストーラも、実際の inference が成功した場合だけ現在の crontab を読み、無関係な entry を保持して、この repo 用の管理 block を更新し、read-back します。毎時 17 分に起動し、ファイル lock により重複実行を skip します。cron の時刻はホスト設定に従い、研究 deadline と state log の timestamp は UTC です。

専用 checkout の開発依存は repo の setup 手順で事前に用意してください。通常の実行は main の clean 状態を要求し、`git fetch origin main` と fast-forward のみ行います。branch / PR を作らず、研究エージェントが検証した成果を選択して main に commit・push します。未公開 commit、変更済み・未追跡ファイル、未完の出力は自動削除や自動 stage をしません。

quota / timeout / CLI error で中断した回の変更や未公開 commit は、開始時 clean だった専用 checkout の HEAD と全 Git-visible 変更の SHA-256 fingerprint を終了時に記録します。次回はその HEAD と内容が完全一致する場合だけ、自分の前回成果として保存しながら続きを実行します。最新 origin/main を改めて fetch し、研究エージェントへ安全な上流統合を指示します。fingerprint が一致しない変更は引き取りません。

`state.json` が `needs_review`、または前回 runner 自体が突然止まり `running` のままの場合は、次回研究を止めます。まだ agent が走っていないことと、残った変更・未公開 commit を確認し、統合・push してから、その state ファイルを削除して再開してください。失敗した Git 更新、認証、推論は `cron.log`、個々の stderr / events log に残ります。state と log は checkout の外、umask 077 で保存します。

停止するには `crontab -e` で `# BEGIN kyouen-research-frontier` から `# END kyouen-research-frontier` までを削除してください。既に走っている回は自然に deadline まで続きます。

## 2026-10-05 JST の cloud 実機確認

- Codex CLI 0.159.0-alpha.3 は存在し、`codex login status` は ChatGPT 認証ありと報告した。秘密の値は確認していない。
- `crontab` / `cron` / `crond` / `at` がなく、`systemctl is-system-running` は `offline`。インストール済み scheduler と常駐 service がない。
- 60 秒以内の read-only / ephemeral CLI probe は推論開始前に `failed to initialize in-process app-server client: Read-only file system` で終了した。
- log と sqlite 保存先を `/tmp` に移す公式 config override でも同じ初期化エラー。ファイル metadata syscall のみの診断で、保護された Codex home 配下の chmod が EROFS と確認できた。credential の複製や保護の回避は行っていない。
- したがってこの cloud VM に動作する永続 cron を設定したとは報告できない。永続ホストと通常認証、起動中 cron が残る前提条件。

補助の回帰検査は `python3 scripts/test_research_frontier_cron.py`。最新 main の更新、汚れた checkout の保護、lock、quota event、timeout、crontab 保持を、実サービスへの副作用なしで検査します。外部ホストでの実 Codex 研究や quota 回復は、この VM では未検証です。
