# ローカルmainの研究変更の統合（2026-10-20）

同期先は `8b79eeff2ca1c6dba25720b034cd45ef83ef9f10`。元のローカルmainは `6a7567c774f18c67cad79f19ff49279831105acc` で、40コミット分をfast-forwardしてからローカルの研究変更を統合した。生成物の競合は手で統合せず、正本から再生成した。

未コミット変更の原形は `incoming-local-changes.patch`、再計算で変化していた過去の出力は `rerun-output/`、追加の実行出力は `raw-local-output/` に保持する。これらは今回の正しい完了計算として採用したものではない。特にn8の再計算出力には低層の辺数が0になった版があり、元の完了出力を置き換えない。個人用の出力先を持つpatched C++も `source/` に資料として保存し、共有solverへ適用しない。

ローカルの仮K0436・K0437はmain上の既存番号と衝突するためK0487・K0488へ再採番した。明示参照されていたscratchpadの報告・検査器・有限データ10ファイルを `source/` に移した。各KのartifactはGit管理される配置へ更新した。

12×12の12石証人、13×13の13石証人は、元の余因子展開検査器と、今回追加した差分3×3行列式検査器の両方で安全性・極大性を再計算した。どちらも禁止四点0・阻害されない空点0。範囲は各単一証人の存在に限り、最小極大サイズや最大安全サイズの更新ではない。再実行は `uv run --locked python research/experiments/local-main-integration-20261020/verify_witnesses.py`。

`verify_k0059.py` の奇数m≤500の250例も再計算し不一致0。それ以外の2026-10-17の追記は当時の研究報告であり、今回全探索や全測定を再実行していない。s_10=10という裏付けのない追記は既存の9≤s_10≤10へ訂正し、K0232の量化未指定のstatusもscope-unclearを維持した。

Lean追加5モジュールを検査し、`lake build`（28 jobs）と `lake build Kyouen.SquareCert2x2`（4 jobs）は成功した。SquareCert2x2はnative_decideに依存する小さい具体証明書であり、巨大9×9証明書のLean核検査を意味しない。

依存パッケージやrootの一時ビルドログは研究成果として追加しない。新しい長時間探索は起動していない。

最終規約検査: `uv sync --locked`、knowledge check（482項目、エラー0・警告0）、33単体テスト（298.519秒、OK）、build、生成物の再生成差分0を確認した。`incoming-local-changes.patch` は旧仮番号と旧生成物を含む履歴資料であり、自動適用用ではない。
