# 2026-10-12: reply27 root `{60,27}` LOSS を119手被覆から確定

## 発見順

- 最新 `origin/main` をfetchして `1bdd30b71adaf8f476a98922f1b454bdd369feb3` までfast-forward。solver実行前にactive agent/processがないこと、対象S4の106 S5子、raw history、cache隔離、保存S6証拠を再確認した。
- 初期UNKNOWN66件から共有/単独と合法手数帯を散らして8件を選び、冷たいS5 exactを15M node上限で実行。最初の8件は7 LOSS / 1 UNKNOWNだった。以後のバッチも同条件で探索し、全66件の新規結果は65 LOSS / 0 WIN / 1 UNKNOWN、403,074,801 nodes。15M UNKNOWN `(1152921504607899649,536870912)` は再実行しなかった。
- そのS5の独立S6境界は98子。保存済みexact S6 WIN 2件をrawで照合し、残る96を12個の8件batchで1M層別走査。77 WIN / 19 UNKNOWN / 0 LOSS、40,892,814 nodes。UNKNOWNは同予算で繰り返さず、K0374にならって15Mへ一度だけ上げる。
- 15M escalation第一組は8/8 WIN、20,979,393 nodes。第二組はlegal strataの先頭4件までで3 WIN / 1 LOSS、12,882,895 nodes。S6 LOSS `(1152921504675009536,536870912)` の1,000,000上限ではなく15,000,000上限rawは5,859,060 nodesで確定し、S5 odd AND LOSSの証人となった。runnerはこのexact LOSS直後に停止し、未 dispatch siblingを保存しなかった。
- S6全境界に残る分類は90 WIN / 1 LOSS / 7 UNKNOWN（保存済み2 WIN、fresh 1M 96件、15M escalation12件を合算）。親S5は一つのexact S6 LOSSからLOSS。UNKNOWN7はexactへ昇格せず、結論に不要。
- 安全化済みatomic mergeでS5 LOSSを統合。全3384 S4境界を再生成すると対象S4は106 LOSS、第三手被覆119/119。整数最小追加数0、有理LP双対0。全119 root moveに一つずつS4 LOSS応手を割当て、三石AND→二石ORを伝播し`{60,27}` root LOSSを監査した。第三手100・108は新しいS4 classで覆った。

## 探索・記録上の修正

- S6 runnerの選定スクリプトは、過去に同じ予算でexact済みの子を全境界preflightで拒否してしまった。候補抽出段階でのみ試行済み子を除外するよう修正し、同予算solver rerunは発生していない。
- 15M escalation後は、1M UNKNOWNと後続budget exactが同じrootに存在する。これは履歴矛盾ではなくexactが低予算UNKNOWNを上書きするので、選定スクリプトの過剰conflict guardを外した。反対exactは監査・safe mergeが拒否する。
- 完了した coverage 119/119に対し、従来frontier scriptが `[100,108]` を常時要求して失敗した。検査を「残余は既定2手または空」にし、残余が空なら対象S4の106子すべてLOSSであることも要求した。
- 15MでS6 LOSSを得た時点で残るS6は探索停止した。これはS5 ANDの完全なLOSS証明に十分。未実行7子はUNKNOWNのまま最終集計に記録した。

## 根拠と限界

各direct S5/S6 raw、1件ごとのrun manifest、幾何・raw SHA監査、exact-only cache、atomic merge receipt、frontier/cardinality/LP、root move witnessは [実験README](../experiments/n11-s4-boundary-direct-20261012/README.md) と同実験の`output/`に保存した。merge後cacheは5,851行（WIN159 / LOSS5,692）、SHA-256 `c469eff06559c57b7f4b679c80c1e576c7bddb6f69ea03da0b8b64d0ef4aa198`。

これはsolver-trusted exact葉に依存する有限root LOSSで、独立整数幾何は合法境界・被覆・AND/ORを照合した。cache-only prior leavesを含む全体のterminal-only独立minimax DAGは作っていない。`{60,27}` rootはLOSS、11×11空盤面は未分類のまま。

## 最新mainへの統合確認

後続の統合作業は最新 `origin/main` `2f023e6ee7a314c791f42010bb3111b736d93efe` を基点とし、他作業の未コミット変更を含めない隔離checkoutで行う。raw移動manifestを追加し、保存S6 raw 2件をGit管理下の同一SHAファイルから監査できるようにした。raw inventoryは23監査receipt中202参照、176 unique raw全てのSHA/replay rowを検証し、untracked local raw参照0件を確認する。

初手は21 D4軌道に分類し、初手60と `{27,57,63,93}` をLOSS、残る19軌道を未確定と記録する。中心60の合法後手応手120/120を独立確認した。terminal-only依存調査は2,995 S5根のうちK0378で閉じた3根を特定し、残り2,992根のproof pilot優先順位だけを計算した。空盤弱解決探索、追加solver探索、巨大proof captureは開始していない。

## 統合検証

`uv sync --locked` は成功。独立frontier監査、119手root監査、保存raw relocationを用いたS6 raw/幾何/極性/AND監査、176 raw inventory、初手D4/応手probe、proof-gap依存分析はいずれも成功し、S6再監査中のbaseline cache置換後はfinal cache SHA `c469eff06559c57b7f4b679c80c1e576c7bddb6f69ea03da0b8b64d0ef4aa198` を復元確認した。生成6 viewとroot READMEは `tools/knowledge/common.py` のcanonical rendererで作成し、stage後 `git diff --exit-code -- README.md research/knowledge/generated` と `git diff --cached --check` は成功した。

`tools/knowledge/check.py` はK0414〜K0416のsource項目エラーなしで58 errorsを返した。`build.py` は前段validatorが同じmissing artifact参照で停止し、33件unittestのうち32件成功・`test_canonical_items_validate`のみ同じ58件で失敗した。参照先は最新mainで未追跡の別作業artifact（元checkoutではuncommitted）なので、依頼どおりこのcommitへ含めない。既存SyntaxWarningも出るが本件変更箇所ではない。
