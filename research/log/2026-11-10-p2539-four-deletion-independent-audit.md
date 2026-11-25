# 2026-11-10 p2539の四点削除近傍を独立監査

## 開始とmain統合

開始時のlocal mainはedd353947b0ffbab94c66309373b0f96c454aec9。
AGENTS.md、knowledge README、現行K0723と関連K0712・監査線、最新log・experimentを読んだ。
git fetch origin mainでd7ad79b6が追加されていた。
差分はn11のanalyze_proof_gap.pyの5行で、今回の幾何証拠や未コミットscreenとは重ならなかった。
origin/mainを競合なしでmergeし、cdf343cffb70b1e5ebfd10ced17338aea8ee60efとなった。
未コミットequality_screen_200k.jsonはmerge前後のbyte hash一致を確認して保持した。
実行中の研究計算はなく、SAT探索を重複起動しなかった。

## 作業の選択と結果

前回の下界1258点は既に独立安全・包含極大と確認済み。
同じ種の削除上限4・1259点要求はソルバUNSATのみだったので、保存228249行DRATの独立監査を選んだ。
新しいexperiment `parabola-p2539-exchange-audit-20261110` に監査と再生コードを追加した。
探索器・SATライブラリ・CardEncをimportしないschemaで、全86583節を独立に分類した。
38868幾何節には固定Fと要求点から真の禁止四点を対応させ、整数行列式を全実検査。
5072 one-hot節を照合し、31388空対counter節と11255削除counter節をprefix個数の四型へ解釈した。
各安全候補が全節のモデルへ拡張できることを証明した。補助変数領域は非衝突。

元DRATを固定DRAT-trim -Uで受理（17.1秒）、抽出64571行LRATを空節修正版で受理（5.1秒）。
圧縮CNF/LRAT・schema・幾何・固定種を別処理でも再生し成功した。
raw core.lratはローカル保持・Git除外、採用圧縮証明はGit管理して元DRATなしでも再生できるようにした。

これにより、原点・完全対{6,2533}を保ち、保存1258点集合から4点以下を除いて1259点以上へ改善することはできない。
固定点を変更する交換、5点以上除く交換、全体の最大値は未解決のまま。
別の量化範囲なのでK0724へ独立した局所排除を記録し、K0723から参照する。
前回のソルバreceiptや当時のREADME/logは書き換えない。

## 回帰と引継ぎ

2064個の小規模prefix割当て、六つの破損schemaを検査した。
和0 mod2539だが禁止四点でない(1,2,4,2532)は整数幾何で拒否した。
RUP六制御・空節修正版LRAT五制御も通過。原版LRATの偽受理は意図した対照であり採用しない。
通常のuv sync、knowledge check（706項目、error/warningとも0）、33 unittest、buildが成功した。
source・採用圧縮証明・保持raw証明・CNF・seed・schemaのhash bindingも照合した。
生成物の再生成byte一致とstage後のgit diff --exit-code -- README.md research/knowledge/generatedも成功した。

次回は元DRATを同じ条件で再監査する必要はない。
探索なら削除上限5以上または固定点変更を検討する。現在の全体範囲1258..1271は変わらない。
独立schemaのprefix解釈は他の有界交換監査へ再利用できるが、新入力の全節照合と幾何検査を省略しない。
