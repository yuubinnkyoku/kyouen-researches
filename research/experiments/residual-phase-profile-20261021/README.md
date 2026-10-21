# 残余構築の費用分解と索引化 (2026-10-21)

## 固定プロトコル

前回の `../residual-gate-calibration-20261021/` の52局面と深い3局面をそのまま使う。
入力・期待値のSHA-256は各summaryに記録する。各行は新しいsolver、共有cacheなし、
外側予算5000 nodes。52局面は独立subset-mexの既知勝敗と一致を要求し、深い3局面は
前回同様UNKNOWNを要求する。新しい確定値が出た場合は停止して別途検証する。

`--residual-profile` は構築、構造処理、残りのGrundy評価を排他的に計測する。
構造処理にはminimal化、閉形式の認識と適用、圧縮、成分分割、共有時の正準化を含む。
Grundy側はmemo、子生成、再帰管理、mex等を含む。map破棄や勝敗変換は内訳に含めない。
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
