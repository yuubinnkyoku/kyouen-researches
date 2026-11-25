# 2026-11-10 保存1104点候補を整数幾何で独立監査

開始時は別作業によるrebase中でHEADが1d61afdeへ移っており、知識項目と生成物が未解決だった。履歴の読み取り中にrebaseが中止され、eece6d3cへ戻った。こちらではrebaseやindexを操作していない。mainとorigin/mainがeece6d3cで一致し、作業ツリーがクリーンで前回までの研究成果が戻り、対象計算プロセスがないことを確認して続行した。

AGENTS・knowledge README・K0693/K0702/K0706・前回log・experimentを読んだ。eece6d3cは、それまで他者の未追跡だったshape bのp2531出力とshape cのp2207出力をコミットしていた。保存出力を評価すると後者に1104点のSAT候補があったため、今回はp2531の次batchではなく候補の独立幾何監査を優先した。

## 再現と結果

```sh
uv run --locked python research/experiments/parabola-p2207-1104-witness-20261110/audit.py --output research/experiments/parabola-p2207-1104-witness-20261110/output
```

元JSONの自己申告を根拠にせず、1104パラメータの重複・範囲・原点・完全対307・空対1078を点集合から確認した。元receipt、入力、driver、generic検査器のhashを保存した。既存sourceを変更せず、専用の一時ディレクトリでgeneric整数4x4検査器をコンパイルした。

全61560516876四点をK0334の必要合同式で被覆し、残る27941252行列式を正確な整数で計算した。全て非零、終了コード0、経過時間10.659秒だった。安全三点の受理、二完全対の既知禁止四点・重複・入力打切り・合成数の拒否という5制御も期待通りだった。

## 正本と信頼境界

新しい下界の主張はK0722（仮番号）へ保存する。独立監査済み範囲は一般定理の上界と合わせて1104〜1105。K0693の等号1105不達成は全1103 d中21 dの修正版監査に留まるためneeds-reviewを維持し、正確値1104を採用しない。K0693に残っていた「1104かそれ未満か」という未確定値の記述を新しい下界の正本参照へ更新した。

新しいSAT探索は起動していない。p2531の独立被覆351/1265、残り914 dとp2647の範囲1303〜1322は変更しない。既存の計算出力・raw evidence・他者の変更は取り込んでいない。
同時に保存されたp2531 shape bのUNSATはソルバ主張のままであり、今回の幾何検査からその独立検証や上界強化を導かない。

既存outputを再指定する負例も実行し、FileExistsErrorで拒否され元4ファイルのhashが全て不変であることを確認した。制御結果は新しいoverwrite-control.jsonへ別保存し、元の証拠は上書きしなかった。

## 次回

p2207の等号1105排除にはK0693の残り1082 dの独立監査が必要。安全1104点の証人は再探索せず、この固定candidateとgeometry receiptを再利用する。p2531はbatch182-300/coverage.jsonをpriorとしてd=302以降の台帳集合差から継続できる。

## 統合検証

uv sync --locked成功、checkは704項目・error 0・warning 0、共通unittest33件は223.954秒で成功。build.pyで生成6viewとREADMEを再生成した。新しいdriverの回帰は実候補の幾何受理・5制御・既存output上書き拒否を実行した。既存のC++検査器、探索source、原receiptは変更していない。

新experiment8ファイルのraw bytesとindexの一致を確認した。作業途中に他者のcertify2207.pyとshape_class_2207_1105.jsonが未追跡で現れたため保持し、取り込まない。K0722の番号重複がないことを確認し、自分のK0722・K0693参照更新・experiment・独立log・生成物だけを指定してmainへ直接commitする。生成物の指定diff検査とstageの空白検査も実行する。
