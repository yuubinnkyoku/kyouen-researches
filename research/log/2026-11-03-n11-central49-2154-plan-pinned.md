# 2026-11-03：中央49フォーカス2,154計画のworklistを証明書として固定

併用運用メモ。2026-11-03-n11-central49-2154-terminal-gated-focus-dispatch.md の後続。

`focus_s7_worker_2154.py --plan-out` を実行し、フォーカス局面
`00000000000000203808000000000040` の64個の子のうち2個がK0637由来の終局証明LOSS7（`...2040a000000000040`、`...02043800800000000010`）と確定済み、残り62個が未検証で、ワーカー分担が 16/16/15/15 であることを再確認した。成果物 `research/experiments/n11-central-19-cover-20261031/output/focus2154_plan.json`（9KB、決定的生成・日付フィールドなし、source certificate sha256 `39a3b3f1…`）を repo に固定した。

- WSL Ubuntu（g++・python3）で `--self-test` PASS（negative_tests=11）、`--plan-out` 成功。
- `--audit-plan … --worklist 0/1/2/3` を順に監査し、いずれも5つのSHA-pinned終局戦略（replay: 26169/20039/6010/7376/9993状態、自前4×4整数Bareiss検証器で再照合）の再生と、各worklist 16/16/15/15件の所有権を確認。異常終了なし。
- 報告は schema 通り `unverified` を維持。証人・2,154七石の勝敗は本作業では一件も証明していない。空盤・二石root・s6局面の勝敗はすべて UNKNOWN のまま。

実際の捜索はワーカー側の仕事であり、本作業はその前段の「割当の再生成と監査」の固定にとどまる。機能的な成果は2,154義務から後続の証明作業で消費されることでのみ現れる。
