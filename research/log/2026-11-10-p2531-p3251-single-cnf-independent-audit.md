# 2026-11-10 p2531・p3251単一CNFを独立監査

開始mainは7f084d16。AGENTS・knowledge README・K0693/K0702/K0706/K0708・最新log・experimentを確認した。fetchしたorigin/main 9a94e90aは既に取り込み済み。両対象の計算が走っていないことを確認し、別素数のscreenと他者の未追跡equality_screen_200k.jsonは保持して取り込まない。

既に保存された両CNFと元DRATを使い、前回のp2207独立schema・共通検査関数をsource hashと意味検査receiptに結び付けて再利用する。新しいSAT探索は起動しない。

## 再現

```sh
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/check_case.py --p 2531 --output research/experiments/parabola-single-cnf-audits-20261110/output/p2531 --timeout 180
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/check_case.py --p 3251 --output research/experiments/parabola-single-cnf-audits-20261110/output/p3251 --timeout 180
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/regression.py --output research/experiments/parabola-single-cnf-audits-20261110/output/regression.json
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/replay.py --saved research/experiments/parabola-single-cnf-audits-20261110/output/p2531 --output research/experiments/parabola-single-cnf-audits-20261110/output/replay-p2531.json
uv run --locked python research/experiments/parabola-single-cnf-audits-20261110/replay.py --saved research/experiments/parabola-single-cnf-audits-20261110/output/p3251 --output research/experiments/parabola-single-cnf-audits-20261110/output/replay-p3251.json
```

## 結果

p2531の8854変数・59662節は21502構造節と38160幾何節、p3251の11374変数・87888節は27622構造節と60266幾何節に独立分離できた。全提供幾何節を整数行列式で禁止四点と確認した。

元DRATのhashと行数を照合し、両方がRUP限定検査と空節処理修正版LRATで受理された。採用LRATはそれぞれ57444行・17916629 bytes、44623行・13975536 bytes。採用CNF・LRAT gzipの別処理実再生と全source・schema・幾何・証拠hash bindingも成功した。

両実入力の正例と10件のschema改変・素数取り違えの負例を確認した。凍結schemaの既存小素数意味検査のhashも照合した。既存source・原CNF・元DRAT・旧receiptは変更していない。

## 正本と引継ぎ

K0702/K0708の単一CNF上界1266/1626を、入力の忠実性から圧縮証明実再生まで独立監査済みとして記録する。旧d別の被覆539/1265と84/1625は履歴として維持し、新しい単一CNF経路の完了と混ぜない。正確な最大値や他素数の結論、Lean形式証明は主張しない。

K0097/K0101に残る監査未完了の古い参照と、p2647の旧範囲1296〜1323を現在の正本参照へ更新した。K0706の浅い候補の確定条件も、個別全数走査に限定せず対象集合を覆う証拠の独立監査へ表現を整えた。過去のlogやraw evidenceは書き換えない。

次回は新しいscreen結果をUNKNOWN・ソルバ主張・証明保存・独立監査に分けて評価する。単一CNF経路が閉じた両素数の未被覆dを理由に旧探索を機械的に再実行せず、必要な新命題か独立検証の目的を確認して選ぶ。

## 統合検証

uv sync --locked成功、checkは704項目・error 0・warning 0、共通unittest33件は200.753秒で成功。build.pyで生成6viewとREADMEを再生成した。新しいcontrollerの正例は両実入力・証明検査・圧縮証明実再生、負例は10件のschema改変・素数取り違えで確認した。凍結schema・既存検査器・元CNF・元DRATは変更していない。

raw core.lrat 2個（17916629/13975536 bytes）は採用gzipの展開bytesと一致し、ローカル保持・Git除外を確認した。変更対象は今回のexperiment・独立log・K0702/K0708と関連参照K0097/K0101/K0706・派生物に限定する。他者のscreen結果は取り込まない。出力を含むexperimentのraw bytesとindexを照合し、生成物の指定diff検査・stageの空白検査を通してmainへ直接commitする。
