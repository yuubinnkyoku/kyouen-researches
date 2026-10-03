# K項目への移行範囲

## 正本と出典

現在の知識は `knowledge/items/` を正本とする。時系列や失敗を含む旧記録は出典として保持し、今回大量の削除・renameは行っていない。
移行の起点は最新mainの `9a574ca80380e35ef46fbbc99324218a38c7551e`。
依頼で指定されたknowledgeのschema・語彙・template・運用文書、researchの入口と本書、tools/knowledge、rootのuv環境はこのcommitには存在しなかったため、要求された構造を最小限新設した。

最初の27項目で盤面・証明書・幾何・一般定理の粒度とsolution metadataを検査した後、代表例だけで止めず、296項目へ展開した。
同一命題の後続実験は同じ項目の根拠へ統合し、誤った別命題はrefuted、根拠を撤回した主張はwithdrawnとして保持する。
全件のkind/status/topic、旧alias、artifact、未解決項目は[自動集計](knowledge/generated/summary.md)と[逆引き](knowledge/generated/aliases.md)を参照。

## 照合した領域

- root READMEの1〜10の勝敗、1〜9のAND/OR証明書、9の全81初手、10の15 D4代表による100初手分類、10の空盤全体の単一KYOENC4証明書の欠如、11の層0〜5と未確定勝敗。
- research/verificationの原文スコープ監査、全局面Grundy・T*/WFT・残余ゲーム、証明書の独立検査、探索順位・memo・staged実験の監査。
- research/exploration、night-research、docsの固定幅定理、ルール変種、幾何、最大・極大安全配置、7の結晶・骨格・再配置、整数放物線、passゲーム。
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

原文600件のうち435件は最新監査索引でもNOT_AUDITEDである。これは未監査の候補であり、435件の数学的未解決問題でも成立済み知識でもない。
この領域をすべて機械変換すると古い未検証主張を正本に昇格させるため、[監査範囲の項目](knowledge/items/K0079-600-original-claims-audit-boundary.md)から出典と境界を辿れる状態にした。個々の候補の事実認定は残る重要な監査領域。

巨大具体証明書のLean内検査、10の全空盤単一証明書、11の真の勝敗、K10/s10の確定、禁止四点組の単独解除による勝者反転、全G11連結などは未完了としてK項目化済みである。
これらを解く新しい研究は今回実行していない。各verifierを全入力について再実行したという主張もしない。
細かな過去のmicrobenchmark・作業指示・進行報告・未採用候補は全てを独立K項目にせず、重要な現行結論の出典として旧文書を保持した。

物理移動は別作業とする。分類の基準は次のとおり。

| 内容 | 所属 |
|---|---|
| 現在成立する命題・未解決・反証・検証境界 | knowledge/items |
| 再現手順・入力・実行条件・結果manifest | experiments |
| 発見順序・判断・失敗の経緯 | log |
| 旧結論・重複・当時の計画 | archive（出典を維持） |
| 仕様・利用方法・実装説明 | docs |

## 再生成と検査

PRの最終確認で全296件を内容slug付きファイル名に変更し、K番号とaliasは保持した。
定義・方式はactive、検証結果はverifiedに整理し、語彙のstatus_by_kindで組み合わせを検査する。
READMEの生成領域は「主結果」の説明直後に置く。8×8の全局面DPは後続監査でcomputedへ更新し、独立全状態検査の未整備を検証境界として表示する。
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
READMEの旧本文を保持し、生成マーカー間だけを更新する。孤立・薄い根拠はwarningであり、数学的結論の正しさを構造検査だけで保証するものではない。

## 最新mainでの未解決再監査（2026-10-04）

旧PR移植後のmainではK0071・K0077・K0078はすでに閉じている。全open/conjecturedの再照合と関連確定項目の証拠境界は[監査記録](verification/knowledge-open-freshness-main-2026-10-04.md)を参照。旧研究Markdownは出典として保持し、K項目を現在の正本とする。
