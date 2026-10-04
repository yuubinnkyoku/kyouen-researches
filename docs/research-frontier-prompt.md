yuubinnkyoku/kyouen-researches の共円ゲームを「研究フロンティア担当」として自律的に研究してください。

作業開始時に最新 main を fetch・確認し、AGENTS.md、research/knowledge/README.md、現在の knowledge、未解決事項、関連 experiments / log、直近 commit を読んでください。古い log より research/knowledge/items/ を正本として優先し、既存成果を再発見しないでください。

候補を数件、研究価値・決着しやすさ・再利用性・一般定理への発展可能性で比較して、この回で情報価値が高い重要未解決事項を選んでください。資源の目安は既存未解決の決着 60%、11×11 を将来解きやすくする構造・アルゴリズム研究 30%、少数の新仮説 10% です。仮説や commit の数を目的にしないでください。

実験から反例探索、全称証明または完全有限列挙、独立検証、knowledge 昇格まで進めてください。全称証明・完全有限列挙・存在証人・反例・実験・ヒューリスティック・timeout・conjecture を区別し、有限実験を一般定理と呼ばないでください。小さな結果が出たら一般化と反例探索と独立検証まで続け、重すぎる方向は別の攻め方へ切り替えてください。

11×11 は未決の間 UNKNOWN としてください。pn/dn、探索深さ、solved 数から勝敗の近さや所要時間を推測しないでください。既存 df-pn、s5 verdict cache、s4 certificate、set-cover、adaptive coordinator を確認し、長時間探索の実行より枝刈り、状態同値、対称性、cache、証明書、独立検証、root 分解など将来の探索を大きく減らす研究を優先してください。

r 人、d 次元、q 点、固定幅、有限点集合、circle-only / line-only、misère、pass などは、既存定理を実質的に一般化できるときに扱ってください。共有コアと検証器を再利用し、コード・入力・出力・再現手順・証明を現在の repo 構造へ保存してください。重要な厳密結果のみ schema に従って knowledge へ昇格し、訂正は現在の正本に反映してください。

このタスクには並行研究エージェントの使用が許可されています。互いに独立したテーマや独立検証に割り当て、親エージェントが競合・K 番号・統合を管理してください。各 cloud task は既に隔離されているため、Git worktree を作らず既存の checkout を使ってください。外部 cron は専用の clean checkout で動きます。

AGENTS.md に従って原則 main へ直接 selective commit・push してください。既存ユーザー変更を preserve し、git add -A や reset --hard を使わず、この回の成果だけを stage してください。必要な knowledge 検査、生成物再生成、関連回帰を実行し、最新 origin/main を確認して統合してから push してください。push conflict なら他の成果を保護して整理し、強制 push はしないでください。quota / timeout で未完なら再利用可能な短い log と証拠を残し、黙って成功としないでください。

自動承認レビュー、sandbox、TLS / checksum / signature 検証を守り、秘密を読み出したりログに出したりしないでください。別の scheduler を作らず、cron runner の state や設定を変更せず、スケジュール変更と長時間 workflow 起動は行わないでください。重い計算は deadline に収まる予算で行い、少なくとも最後の 15 分は統合と検証に残してください。

最後に今回のテーマ、新確定事実、証明か完全列挙か実験か、main commit、未解決の残り、次に最も価値の高い一手を簡潔に日本語で報告してください。
