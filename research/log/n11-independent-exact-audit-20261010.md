# 11×11 exact体系の独立監査

開始/fetch main: `ed75f33d9ccc1557df6143a59ec0994f46f28594`。branch/PRは作らずmainで作業。既存の大量のuntracked `.local` と旧実験outputを保存し、今回の新規outputだけを新ディレクトリに置いた。

K0371の主要極性修正を確認した後、C++ loader、追加Python loader、workflow inline mergeが隔離registryを通らないことを発見。旧誤WINを支持する独立exactをtracked/local rawの双方で見つけられなかった。中間S6の6誤WINから2 S5、6 S4へ辿り、2 S4だけにstatus依存が残ると確認した。歴史cache48ファイルは改変せず、現在のconsumerから隔離した。

新規監査器は円中心の整数分子・共線判定と8座標変換を使う。初版でraw-rooted復元が2,988件に留まり、既存の全5,734 cache値を全てpositive-budget replay支持として扱えないことを発見した。2,746件のcache-only葉を個別出所/hash付きで残し、信頼境界を狭めた。local補助監査でも新しい対応rawはなかった。旧集計を読み直す代わりにgeometryから全frontier、119第三手、integer cover/dualを再生成した。

代表4件の独立minimaxは各2,000-state limitでUNKNOWN。軽いS6 WINだけ、以下で30,000-state limitを試した。

```powershell
uv run --locked python -c "import sys,time; sys.path.insert(0,'research/experiments/n11-independent-exact-audit-20261010/scripts'); from independent import Board,solve_certificate; from audit import dump; start=time.perf_counter(); r=solve_certificate(Board(11),10448351135500075008+(1040<<64),30000); dump('s6-win-escalation.json',dict(verdict=r['verdict'],visited=r['visited'],seconds=time.perf_counter()-start,limit=30000)); print(r['verdict'],r['visited']); r['certificate'] and dump('minimax-s6-win-escalated.json.gz',r['certificate'])"
```

26,577 visited / 23.90秒でWIN、10,407-node terminal-leaf DAGを取得した。UNKNOWNをexactへ昇格させず、S5全件の再計算は行わなかった。C++テスト初版の「有効」fixtureが実際には非canonicalで拒否されたため、独立正規化済みcacheのキーへ修正した。checkerが入力不正を捕捉した例であり、solver結論の不一致ではない。

既存102 Python tests（knowledge33、boundary58、frontier6、polarity5）と追加12 tests、C++実cache/replay境界、既知盤n4..n7を含む12 solver回帰を実行。ソース修正後のhashは旧manifestに残る当時のソースhashとは異なる。旧raw/cache hashは新監査manifestから検査し、過去のコードのbyte同一性と修正後コードの意味検証を分ける。

最終知識はK0372、frontier正本はK0355。独立証明済みとsolver-trustedを混ぜないことが引き継ぎ上の最重要点。

最終C++ cover照合では31 LOSS / 268 WINは一致したがcoverageが116となった。原因は119要素のcoverage配列を0..120のcell IDで参照する範囲外アクセス、およびuncovered表示のcompact slot混同。元出力を `cpp-cache-cover-before-fix.csv` に保存し、修正後117/119・remaining100/108の実行回帰を追加した。新規探索を追加する前に原因を解消した。

最後に、汎用mergeへbudget=0のcache projectionをreplayとして渡すとcache経路の隔離を迂回できることも確認した。positive-budgetのraw条件と、active quarantineの明示解除を必須にした。UNKNOWN観測は証明として昇格させない。両迂回入力を拒否する12番目の回帰を追加し、frontierの既存6 testsと合わせて再確認した。

最終fetchで別作業の `e78c0b9d`（Grundy-five generator一ファイル追加）を検出し、差分を確認してfast-forwardで取り込んだ。今回の監査対象・K番号との衝突はなく、統合後にknowledge check/build/testsとhash検査を再確認した。
