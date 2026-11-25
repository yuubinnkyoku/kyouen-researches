# Part CS 完成 log: batch-28 (class 5343) remaining-EXHAUSTED 4-row の高budget (25M) 再probe (2026-11-23)

宣言: `research/log/2026-11-23-part-cs-b28exhausted-reprobe25m-declaration.md` (commit `e31b6f8a`)。
実験dir: `research/experiments/n11-centralreply-class5343-b28exhausted-reprobe25m-20261123/`
(kit 35 + A-fix 1 + outputs 19 + docs 2 = complete・MANIFEST-sha256.txt 54 entries machine-pinned)。

## 成果

Part CQ (20M再probe) 後に残っていた batch-28 (closure class 5343) EXHAUSTED 4行を
**新条件 budget 25,000,000** で2-pass fresh-cold再probeし、**3行が解決 (全てWIN)**:
aa021 22,942,323 / aa028 21,563,925 / aa032 20,312,294 (全2-pass node-exact・
status.log PASS + WIN-HALT 二重記録)。**aa050 は25MでもEXHAUSTED (honest UNKNOWN)**:
nodes=25,000,000 2-pass一致。**→ batch-28のEXHAUSTED残: 4行 → 1行 (aa050のみ・
15M/20M/25Mの全条件で未解決)**。LOSS 0・determinism mismatch 0・window-exceeded 0。

- anchors: aa036 (2, 955,659) / aa004 (1, 15,616,012) は25M派生runnerでpublished値と
  node-exact (25M runner `9048c329…` = published runbatch.shのEXACTLY 1行diff)。
- val-gate fresh 4/4 node-exact (at2m 2M exhaustion ×2 / 15m 3,651,923 + 5,040,200)。
- audit (`9722ca42…`・schema `n11-centralreply-c5343-b28exh-reprobe25m-audit-v1`):
  PASS・3回実行 stdout + audit.json byte-identical (json `c6622d57…`)・tamper電池 4/4
  fail-closed (p2-nodes / result反転 / replay_done削除 / registry reprobe_condition.budget)
  ・各probe復元byte一致・clean control PASS。
- aa050のp2は1回inner-timeoutでtruncatedしたが、published runner guardがsidecar退避し
  次invocationでp2のみfresh-cold再実行して完走 (設計どおり・TRUNCATED-RETRY 1回で
  WINDOW-EXCEEDED不発火・sidecar `aa050.p2.truncated.234741.out` 出版)。

## 誠実記録

- **A-fix**: published A版session step `cs_local_step.sh` (`cbab0017…`) が旧runner名
  `runbatch_b28exh20m.sh` 参照のまま (派生時の1-token取りこぼし)。初回step invocationで
  rc=127 file-not-foundとして即検出・**targetは1キーもsolver実行されず**。修正版
  `bb744c2c…` を commit `614750b3` で出版してから実行。
- **環境リセット事故**: A-fix直後のfetch-back bash呼び出しでインフラ失敗
  (command-not-rerun) → 実行環境リセット・未出版のローカル成果 (当時のval-gate 4・
  anchors 2キー分・status.log) が消失。publish-then-execute設計により実害ゼロ:
  published scaffold (commit-pinned) からkit 36ファイルを再fetch・sha照合一致・
  val-gate/anchorsはfresh-cold再実行で同一結果を再現 (protocolどおり)。
  Published evidence (A/A-fix/B/C) はすべてrepo側にのみ存在し失われていない。

## Interpretation guard (verdict不消費)

3 WIN行はprobe-level honest labelsのみ。canonical adoptionは別宣言adoption Part
(pinned fail-closed merger `90711961…`) 経由のみ・WIN行はscrutiny owner C++第二実装
gate `9193f5b6…` 待ち。本Partはadoption・closure・secured・root勝敗に一切触及しない。
aa050は15M/20M/25Mのsame-condition再probe禁止のまま別条件候補としてopen。
**標準11×11空盤・class 5343・全キーはこの時点で UNKNOWN**。

## commits

- 宣言 `e31b6f8a` (HEAD-before `fb1c540d` Part CR completion log・fetch-back sha `6eeeebcd…`)
- A `38624142` (HEAD-before `e31b6f8a`)・fetch-back 35/35
- A-fix `614750b3` (HEAD-before `38624142`)・fetch-back 1/1 (再構築時にbyte検証 `bb744c2c…`)
- B `37c52cfb` (HEAD-before `4e8229fd`)・fetch-back 19/19
- C `01be24f9` (HEAD-before `37c52cfb`)・fetch-back 2/2
