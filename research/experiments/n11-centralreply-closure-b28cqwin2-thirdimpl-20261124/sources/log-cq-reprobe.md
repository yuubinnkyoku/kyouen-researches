# Part CQ 完成 log: batch-28 (class 5343) EXHAUSTED 11-row の高budget (20M) 再probe (2026-11-23)

宣言: `research/log/2026-11-23-part-cq-b28exhausted-reprobe20m-declaration.md` (commit `44bd22a7`)。
実験dir: `research/experiments/n11-centralreply-class5343-b28exhausted-reprobe-20261123/`
(kit 34 + outputs 32 + docs 2 = complete・MANIFEST-sha256.txt 66 entries machine-pinned)。

## 成果

batch-28 (closure class 5343) の published EXHAUSTED 11行を**新条件 budget 20,000,000**
で2-pass fresh-cold再probeし、**7行が解決 (全てWIN・nodes 15.4M〜17.2M)**:
aa004 15,616,012 / aa005 15,957,877 / aa030 16,765,560 / aa031 17,185,014 /
aa035 15,424,243 / aa047 16,230,465 / aa053 16,685,872 (全2-pass node-exact・
status.log PASS + WIN-HALT 二重記録)。**4行は20MでもEXHAUSTED (honest UNKNOWN)**:
aa021 / aa028 / aa032 / aa050 (全nodes=20,000,000 2-pass一致)。LOSS 0・mismatch 0・
window-exceeded 0・truncated-retry 0。

- **batch-28のEXHAUSTED残: 11行 → 4行**。4行は今後の別条件候補としてopen。
- anchors: aa036 (2, 955,659) / aa046 (1, 2,185,149) 20M派生runnerでpublished 15M値と
  node-exact (end-to-end妥当性確認)。
- val-gate fresh 4/4 node-exact (at2m 2M exhaustion ×2 / 15m 3,651,923 + 5,040,200)。
- audit: PASS・3回実行 stdout + audit.json byte-identical (json `6227eb2c…`)・
  tamper電池 4/4 fail-closed (p2-nodes / result反転 / replay_done削除 /
  registry reprobe_condition.budget)・各probe復元byte一致。
- derived runner: published runnerの EXACTLY 1行diff (BUDGET 15M→20M)・`c5e86d49…`。
  no-15M-re-search規約無傷 (同一15M条件は再実行せず・20Mは別宣言条件)。

## 誠実記録

- B commit (`962348f9`) message中の audit.json hash `a2452e59` は手転写ミス。
  正値は `6227eb2cfeb14c31799d94f19436c07233d55c8301d8640ee266b8cc3a366692`
  (MANIFEST + README実行記録で訂正・commit messageは不可逆)。
- tamper電池の(d)は当初registryに存在しないtop-level `budget` keyを改変しゲート不発火。
  正フィールド `reprobe_condition.budget` で再実行し捕捉確認 (auditor側は無傷・
  電池設定ミス)。失敗も実験事実として記録。
- 前回sessionの A scaffold pushは着地していなかった (16MiB制約で結果未確認終了)。
  list_commitsでrepo実状態を確認してから再pushし重複なし (observed HEAD `699a13bc`)。

## Interpretation guard (verdict不消費)

7 WIN行はprobe-level honest labelsのみ。canonical adoptionは別宣言adoption Part
(pinned fail-closed merger)経由のみ、WIN行はscrutiny owner C++第二実装 gate待ち。
本Partはadoption・closure・secured coverage・root勝敗に一切触及しない。
**標準11×11空盤・class 5343・全キーはこの時点で UNKNOWN**。

## commits

- A `dd68c4d6` (HEAD-before `699a13bc`)・fetch-back 34/34
- B `962348f9` (HEAD-before `001278ac` = Part CR B)・fetch-back 32/32
- C `19866654` (HEAD-before `962348f9`)・fetch-back 2/2
