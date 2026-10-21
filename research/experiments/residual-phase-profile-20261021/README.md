# 残余構築の費用分解と索引化 (2026-10-21)

## 固定プロトコル

前回の `../residual-gate-calibration-20261021/` の52局面と深い3局面をそのまま使う。
入力・期待値のSHA-256は各summaryに記録する。各行は新しいsolver、共有cacheなし、
外側予算5000 nodes。52局面は独立subset-mexの既知勝敗と一致を要求し、深い3局面は
前回同様UNKNOWNを要求する。新しい確定値が出た場合は停止して別途検証する。

`--residual-profile` は構築、構造処理、残りのGrundy評価を排他的に計測する。
構造処理には各Grundy呼出しの入口でのminimal化、閉形式の認識と適用、圧縮、成分分割、
共有時の正準化を含む。Grundy側はmemo、子生成（play/normalize内のminimal化も含む）、
再帰管理、mex等を含む。map破棄や勝敗変換は内訳に含めない。
子再帰の構造処理を親の構造時間に重ねない。profileは既定OFF。

profileの閾値は6/12、1回。時計呼出しの影響があるため、性能比較は別のprofile OFF実行で
閾値OFF/6/12を3回反復し、各局面の中央値を合計する。反復ごとに閾値の順序を回転する。
構築が支配的ならcompletion索引による同値な構築を実装し、同じ入力で比較する。
新たな未知盤探索やworkflowの自動起動は行わない。実行例:

```sh
python research/experiments/residual-phase-profile-20261021/run.py \
  --solver /tmp/solver --label scan-profile --profile
```

結論の範囲はこの固定コーパスに限る。外側node予算は残余kernel内部の仕事を数えない。
既定handoffを変更するには独立した性能上の根拠が必要。

## 索引方式と同値性

盤面が安全でlegal maskが正しい場合、残余辺の大きさは2/3/4のいずれか。
`completion[a,b,c]` はソート済み3点と禁止四点組を成す4点目の集合である。

- legalの各2点組について、occupiedの点xを足した3点のcompletionとoccupiedが交わればrank 2。
- legalの各3点組のcompletionとoccupiedが交わればrank 3。
- legalの各4点組の最後の点が先頭3点のcompletionにあればrank 4。

各場合で得た4点は相異なり、残りはすべてoccupiedなので従来scanが得る辺である。
逆にscanが得る四点組をlegalに残る点の数で場合分けすると上の列挙に必ず現れる。
rank 0は安全性、rank 1はlegalの定義から除かれる。小さいrankから処理し、既存辺を
含む候補を捨てることで、後から除去される辺はなく、同じ極小族になる。
最後に数値順へsortしてlabelled表現も一致させる。occupied/合法点は変更しない。

`--residual-builder=scan|indexed|auto` はexact replayでの比較用。既定autoは
`C(L,2)*O+C(L,3)+C(L,4) < 禁止四点組数` の場合だけ索引方式を選ぶ。
これは粗い仕事量の見積もりであり、全入力で最速であるとは主張しない。
従来scanは残している。残余handoff自体の既定値は引き続きOFF。

## 検査

`cpp/tests/test_kyouen_residual_builders.cpp` は同じGrundy値だけでなく、密なlabelでの
頂点maskと極小辺族そのものを比較する。4×4の全65,536占有maskのうち安全な5,811局面、
8×8の空盤と1点占有（64ビット境界）、保存済み11×11全826局面が対象。
安全な4×4全局面と8×8の1点占有と11×11全826局面では各合法手の遷移後も比較し、
残余playの頂点/辺族と盤面から直接作り直した子の一致も検査する。
通常buildとUBSanで同じ検査を行う。CIはこれらの有限比較、protocolの6テスト、
保存出力の再集計のみ。時間比較や深い探索はCIから起動しない。

```sh
c++ -std=c++20 -O2 -Icpp/solvers cpp/tests/test_kyouen_residual_builders.cpp -o /tmp/builders
python research/experiments/residual-phase-profile-20261021/audit.py --test /tmp/builders
python -m unittest discover -s research/experiments/residual-phase-profile-20261021 -p test_protocol.py
python research/experiments/residual-phase-profile-20261021/verify_outputs.py
python research/experiments/residual-phase-profile-20261021/run.py \
  --solver /tmp/solver --label indexed-timing --builder indexed --repeats 3
python research/experiments/residual-phase-profile-20261021/run.py \
  --solver /tmp/solver --label scan-timing --builder scan --repeats 3
```

## 完了記録

`comparison.md` は `report.py` で保存summaryから生成する。全1210根評価の再集計を
`verify_outputs.py` で検査済み。内訳profileは各builder 110行、時計OFFの比較は
各builder 495行（52+3局面 × 3閾値 × 3反復）。52局面は全勝敗一致、深い3局面は
全てUNKNOWN、探索ノード数も両builderで一致した。

閾値6/12で、時計OFFの探索時間は52局面で83.3%/62.9%、深い3局面で96.4%/61.9%削減。
それでも深い3局面の閾値6はOFFの約3.6倍、閾値12は約126倍かかった。
既定handoffはOFFを維持する。計算量の粗い比較によるbuilderのauto選択は採用する。

測定は単一hostでindexedの3反復の後にscanの3反復を行った。各反復内では閾値を回転。
OFFはbuilderを呼ばず、別時間帯でのばらつきの参考になる。
compiler、binary hash、実装commitとauditのみの差は `build-provenance.json` に記録した。
通常/UBSanの両builder比較とmicro-kernel検査（107427 oracle states / 2068 clutters）を完了。
最終solverの4×4空盤は通常探索と残余handoffの両方で既知の後手勝ちを再現し、
shadow設定では119局面の遷移監査と勝敗照合を完了した。
