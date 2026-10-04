# 知識と物理構造の移行履歴

## 第1段階：論理上の正本と出典（当時の移行）

現在の知識は `knowledge/items/` を正本とする。時系列や失敗を含む旧記録は出典として保持し、この第1段階では大量の削除・renameを行わなかった。
移行の起点は最新mainの `9a574ca80380e35ef46fbbc99324218a38c7551e`。
依頼で指定されたknowledgeのschema・語彙・template・運用文書、researchの入口と本書、tools/knowledge、rootのuv環境はこのcommitには存在しなかったため、要求された構造を最小限新設した。

最初の27項目で盤面・証明書・幾何・一般定理の粒度とsolution metadataを検査した後、代表例だけで止めず、当時296項目へ展開した。
同一命題の後続実験は同じ項目の根拠へ統合し、誤った別命題はrefuted、根拠を撤回した主張はwithdrawnとして保持する。
全件のkind/status/topic、旧alias、artifact、未解決項目は[自動集計](knowledge/generated/summary.md)と[逆引き](knowledge/generated/aliases.md)を参照。

## 照合した領域

- root READMEの1〜10の勝敗、1〜9のAND/OR証明書、9の全81初手、10の15 D4代表による100初手分類、10の空盤全体の単一KYOENC4証明書の欠如、11の層0〜5と未確定勝敗。
- research/experiments/original-claims/outputの原文スコープ監査、全局面Grundy・T*/WFT・残余ゲーム、証明書の独立検査、探索順位・memo・staged実験の監査。
- research/experiments/fact-discovery/output、research/experiments/structural-discovery/output、docsの固定幅定理、ルール変種、幾何、最大・極大安全配置、7の結晶・骨格・再配置、整数放物線、passゲーム。
- resultsのCSV/JSON、certificatesの公開証明書、cpp/rustのsolverとverifier、KyouenのLean定理。重要な根拠は役割・用途・出典commitを付けて参照し、ローカルの巨大生成物や未追跡ファイルには依存させない。

最新の原文スコープ索引で採用済みの165原文IDはすべてaliasから辿れる。SUPPORTED/REFUTEDという古いラベルだけで決めず、有限計算・一般証明・部分成立・量化範囲を本文で区別した。
F系列、H系列、旧Cycle内の重要識別子も保持した。Cycleで再使用される短いIDは `Cycle1:H1` のように修飾し、異なる命題を同じaliasで結合しない。
関係の逆リンクは生成物に集約する。証明の一部分だけを全命題へのprovesにせず、依存または限定範囲のverifiesとして扱う。

## 訂正・留保

- 7×7は最新資料の全安全局面Grundy計算を採用。8×8もRound5の全6,700,711,937安全局面streaming Grundy DP完走を既存資産監査で採用した。8×8全状態の独立再計算・強解決証明書は未整備であり、「計算済み」と「独立検査済み」を区別する。
- 固定証明書の終局一覧と全最適戦略のT*を分離。既存JSONの5×5根のT*には5,7,9が入り、旧F-Yの全戦略についての排除主張はrefuted。固定証明書の一覧そのものは有効。
- 旧blind median評価の9/10盤面混同・累積memo混同を反映し、旧結論をwithdrawn。新しい分類器の精度、単発順位、実solver速度、容量を増やした再現は別の知識として範囲を記載。
- 共線の旧Θ(n^6)、最大と極大の混同、unsafe witness、未確定11勝敗、パリティの過大な一般化を現行結論に訂正。反証と証拠撤回を混同しない。
- F-Kは走査実装が半整数中心に限定されることを確認し、その範囲の結果として採用する。H6は既存R内二石データの平方距離10にLOSS {90,61} とWIN {73,66} が共存するため決着した。

## 残る範囲

第1段階の移行時点では、原文600件のうち435件がNOT_AUDITEDだった。これは当時まだ内容監査していない候補の件数であり、435件の数学的未解決問題を意味しなかった。
その後2026-10-04に全600件の内容監査を完了し、現在はNOT_AUDITED=0である。各原文はSUPPORTED / REFUTED / PARTIAL / INCONCLUSIVE / SCOPE_UNCLEARのいずれかに監査済みで、生きた集計と個別根拠は[監査範囲の項目](knowledge/items/K0079-600-original-claims-audit-boundary.md)および生成索引を参照する。旧仮説を機械的にK項目へ変換したわけではない。

巨大具体証明書のLean内検査、10の全空盤単一証明書、11の真の勝敗、K10/s10の確定、禁止四点組の単独解除による勝者反転、全G11連結などは未完了としてK項目化済みである。
これらを解く新しい研究は今回実行していない。各verifierを全入力について再実行したという主張もしない。
細かな過去のmicrobenchmark・作業指示・進行報告・未採用候補は全てを独立K項目にせず、重要な現行結論の出典として旧文書を保持した。

第1段階では出典互換性のため旧資料を原位置に保持した。2026-10-04の第2段階でこの方針を更新し、参照修正・hash provenanceの区別を伴う物理移行を実施した。現在の正本は引き続き `research/knowledge/items/` だけである。

新規資料を追加するときの分類基準は次のとおり。

| 内容 | 所属 |
|---|---|
| 現在成立する命題・未解決・反証・検証境界 | knowledge/items |
| 再現手順・入力・実行条件・結果manifest | experiments |
| 発見順序・判断・失敗の経緯 | log |
| 旧結論・重複・当時の計画 | archive（出典を維持） |
| 仕様・利用方法・実装説明 | docs |

## 再生成と検査

PRの最終確認で当時の全296件を内容slug付きファイル名に変更し、K番号とaliasは保持した。
定義・方式はactive、検証結果はverifiedに整理し、語彙のstatus_by_kindで組み合わせを検査する。
当時、READMEの生成領域は「主結果」の説明直後に置いた。現在は短い現況導入の直後に置く。8×8の全局面DPは後続監査でcomputedへ更新し、独立全状態検査の未整備を検証境界として表示する。
入口となる50件（K0001〜K0035、K0041〜K0050、K0068〜K0072）の文章を再確認し、安全集合数・証明書ノード数・層別列挙・極大サイズ分布を対応の分かる表や数値列へ整形した。
これらは知識の再作成や新規研究ではなく、参照・状態制約・表示・文章品質の修正である。

```sh
uv sync
uv run --locked python tools/knowledge/check.py
uv run --locked python tools/knowledge/build.py
uv run --locked python -m unittest discover -s tools/knowledge/tests
git diff --exit-code -- README.md research/knowledge/generated
```

最後の差分検査は正本と生成物をcommitした状態で行う。CIはlocked環境で構造検査、自己参照・循環、alias衝突、artifact境界、README保護の回帰テスト、再生成差分を検査する。
第1段階ではREADMEの旧本文を保持して生成マーカー間だけを更新した。第2段階では手書き部分も現行入口へ更新した。孤立・薄い根拠はwarningであり、数学的結論の正しさを構造検査だけで保証するものではない。

## 最新mainでの未解決再監査（2026-10-04）

旧PR移植後のmainではK0071・K0077・K0078はすでに閉じている。全open/conjecturedの再照合と関連確定項目の証拠境界は[監査記録](experiments/original-claims/reports/knowledge-open-freshness-main-2026-10-04.md)を参照。旧研究Markdownは出典として保持し、K項目を現在の正本とする。

## 第1段階のmainへの集約

2026-10-04時点で、現行knowledge schema・generated view・CI・README導線はmainへ集約済み。旧構造向けopen PRは0件。旧 `refactor/research-knowledge-structure` と `codex/open-freshness-audit` の固有成果もmainへ回収済みで、両refはmainと同一commitへ揃えた。当時の論理移行では旧研究ファイルを原位置に残した。当時残っていた原文435件のNOT_AUDITEDは、物理構造と独立した内容監査バックログだった。2026-10-04の後続監査でこのバックログは全件処理され、現在はNOT_AUDITED=0である。

ランタイム一時物はcurrent treeから除外し、固定バイナリ・検証JSON・研究ログなど再現性に必要な資産だけを残す。

## 第2段階：物理SSOT移行の完了（2026-10-04）

開始mainは `48fa9f78f0933a9f20485f4f2be16d88a4bce232`。開始時に最新mainを取得し、branch・PRを作成せずmainへ段階的にcommitした。
**物理SSOT移行も完了**。現在知識の唯一の正本はknowledge/items、再現資料はexperiments、時系列はlog、旧資料はarchive、reader文書はdocs、公開横断machine outputはresultsに分類した。
旧 `night-research/` と `research/verification/` は空READMEも含めてcurrent filesystemから撤去した。
旧exploration・root experiments・artifacts・notes・tmp-kbも有用な役割へ移した。rootのround5_b520_n3.jsonとscratch_n45.jsonは実験出力へ移した。

一回限りのdocs prereg/result/auditとresults内のMarkdown・図・legacy certificate logは実験へ移し、旧仮説帳・統合サマリはarchive、discovery cycleはlogへ分類した。
共有solverを複製せず、共有研究libraryはscripts/researchへ分離した。空dump・debug/editor片・完全一致重複・obsoleteなreport編集generatorは削除した。
開始時ですでに構文エラーのあった2本は監査出典としてarchive/incomplete-scriptsに保存した。

現在のK0001〜K0320の**320件**を保持した。kind・status・topic・alias・relation・solution metadataは開始時点と一致し、数学的な新規研究やstatusの変更を行っていない。
当時296件という第1段階の数字は移行履歴であり、現行件数ではない。

knowledge artifacts、Markdownリンク、主要source/runner path、workflow参照を新pathへ更新し、generated viewを再生成した。
当時のpath + SHA256を保存した監査JSON/manifestはhistorical provenanceとして保持し、[path対応表と説明](archive/physical-ssot-2026-10-04/README.md)から現在の所在を辿れる。
旧path文字列の禁止ではなく、knowledge checkがcurrent filesystem上のlegacy pathの再登場を拒否する。
同じ検査でrepo-local Markdownリンク・Python構文・主要source/runner参照・workflow working-directoryも検査する。

root READMEは現行入口へ書き換え、古い12≤M_{3,5}≤56、m=22..55未決、次の対象4行q=8という説明を撤去し、M_{3,5}=12・M_{4,8}=11と正本への導線へ更新した。
1〜8の全安全局面解析、9/10の弱解決、11の未解決、8盤の独立全状態監査の留保を区別した。

検査はuvのlocked環境、knowledge integrity・unit test・generated差分、既存C++ build/小盤certificate、固定幅・幾何・game-structure・saturation regression、Lean、Rust独立verifierを対象にした。
物理移行そのものは、当時残っていた435原文の内容監査、11盤の勝敗、巨大具体証明書のLean核内検査等を解決したという意味ではない。その後、435原文を含む残件の内容監査は完了してNOT_AUDITED=0となったが、数学的に未解決の命題まで解決したわけではない。現在の境界はknowledgeを参照する。

### 長時間実験workflowの起動境界

移行後のpushで、旧設定のon: pushにより11盤のprobe/sweep jobが自動起動したため、実行中の4件を停止した。停止を要求したもう1件は要求前に完走済みだった。これを含め、完走済みのsmoke/threshold jobの結果も現在知識へ取り込んでいない。
未知盤のprobe/sweepはworkflow_dispatchだけで明示的に実行するようにし、通常pushでは既知盤のregressionとCI・knowledge・Rust検査を実行する。
これは構造変更による新たな探索の自動起動を防ぐ変更で、solverや数学的statusの変更ではない。

## 物理移行の検証記録

- 移動2,234、削除45、新規26ファイル。分類と歴史的path対応はarchive/physical-ssot-2026-10-04/paths.tsvを参照。
- K0001〜K0320の320件、alias 252、artifact参照1,184（固有ファイル393）。broken artifact/relation/link/source runner/workflow working-directoryは0。generated warningは0。
- kind/status/topics/aliases/relations/solution metadataを開始mainと機械比較し、一致を確認した。9個の凍結監査・hash receiptは開始mainのGit blobとbyte単位で一致する。
- uv sync --locked、knowledge check、全unit test、knowledge build、generated差分検査に成功。最終CIは追加のlayout回帰を含む33 testsを実行する。
- CMakeの通常build、1〜6証明書の生成と独立検査、10/11 rootとplain solverのmemo self-test、既存の三石root回帰に成功。
- fixed-width、geometry、game-structure、saturationの既存既定回帰に成功。全長の巨大排除や未解決盤の新たな探索は回帰の範囲に含めていない。
- Lean buildとdemo、Rustの9 unit tests・2 reference tests・self-test・266行/4ファイルのevidence auditに成功。Rust CI/reader commandsは使用binaryを明示した。
- [CI（C++・imported regression・Lean）](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/37184192703)、[Knowledge integrity](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/37184192722)、[Rust verifier](https://github.com/yuubinnkyoku/kyouen-researches/actions/runs/37184192782)で成功を確認した。同じpushの3/4/5/6石proof、witness log/mmap、既知盤hybrid regressionも成功。

旧path文字列は歴史資料と移行説明の12ファイルに4,657箇所残る。内訳はpath対応表1,852、当時の監査JSON等2,797、旧引き継ぎ・未完了コード・QA・実行log 7、移行説明2。
現在の実行path・Markdown link・knowledge artifactsにあるlegacy参照は0。historical文字列をcurrent参照と誤認しないように、各experiment/archive入口でprovenanceの扱いを説明した。
