# Part DK interim note: execution-environment outage during P2 invocation (2026-11-24)

Part DK (宣言 `e411045b`・単一オーナー・publish-then-execute・observed HEAD at
declaration `41c9ede4`) 中の誠実な中途記録。A scaffold `890e6186` 出版後、
cross-invocation step design に従い invocation A (P1) を実行し完走した。続く
invocation B (P2) の発行時に実行環境 infra failure ("Filesystem rollback failed /
temporarily unavailable"・~08:2xZ) が発生し、以来本hostのローカルfilesystemが
復旧しない。本noteは evidence不消失担保のための観測記録であり、**PASS/勝敗の
主張ではない**。

## P1 観測 (this-host fresh-cold・budget 25,000,000)

```
replay,0,5,93,0,25000000,2,21954135,126,1155173304438358016,68719476736
# replay_done rows=1 wall_s=126
```

- interpretation (行spoleのみ・verdict不消費): **P1 単独では node-exact PASS
  ではなく、result=2 (LOSS) nodes 21,954,135 の単一pass観測** である。
  PASS要件 (p1==p2 node-exact 2-pass) は P2 未実施のため**未充足**。
  ac013 は batch-30 唯一の 20M EXHAUSTED 行であり、本観測は「25M budgetで
  解決した可能性」を示すが、確定はP2 + runner_dk.sh (両pass fileの
  replay_done guard + pinned比較 + status.log append) 完了後に限る。
- wall_s=126 (hostは ~230k nodes/s 級・25M EXH級でも300s内に収まる見込み)。
- scratch rate probe (3M budget・throwaway・非採点): result=0 nodes 3,000,000
  wall_s=13 (~231k nodes/s)・このprobeはevidence採点対象外の事前測定。

## 状態と次step (takeover規約は宣言 `e411045b` の3.5h停滞基準を適用)

- A scaffold 9/9 file fetch-back byte一致済み (commit-pin URL・sha一致)。
- P1 raw file はローカル置き場が失われた可能性があるため、P2が実行可能に
  なった時点で **P1も含めて fresh-cold 再実行** (published kit `890e6186` から)
  して両passを出版するのが最も安全な回収経路 (DJ precedent: pre-wipe観測と
  再実行の完全一致を以て回収・決定性はpublish-then-execute設計で担保済み)。
  ただしローカルP1 raw file が byte無傷で存続している場合はそれをそのまま
  出版してよい (replay_done guardが再実行を制止する)。
- verdict不消費・閉鎖・被覆・secured・root勝敗の主張をしない。nodes数・
  wall秒数を勝敗として読まない。**標準11×11は本Partのどの時点でもUNKNOWN
  のまま**。WIN/LOSS採用は scrutiny owner C++第二実装 gate `9193f5b6…` 通過後の
  別adoption Part (pinned merger `90711961…` 経由) のみ。

(observed HEAD at push: 00e17cda04ce29dc5ea4d7011c12baef5d9437b6)
