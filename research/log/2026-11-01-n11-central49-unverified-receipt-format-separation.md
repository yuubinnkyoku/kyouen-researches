# 2026-11-01：中央49の作業者報告を厳密S5 cacheと形式上分離

開始時の最新 `main` は `21a99ca8dbaba71e1691dcf21a00ce81a6d04809`。AGENTS.md、knowledge README、K0023・K0329・K0417、中央49の2,208類計画と直近の二証人置換監査、作業者結果の読込・統合処理を確認した。

## 問題

`--audit-focus-plan --merged-out` が出力するCSVは、独立再検証されていない作業者の報告であるにもかかわらず、行頭が厳密判定cacheと同じ `s5verdict` だった。付随するJSONの注意書きはCSVに残らず、別の処理へ誤投入すると「検証済みの厳密S5判定」に見える危険があった。特に結合時のnode数は元の探索記録ではなく0に書き換えていた。

## 修正

- 結合CSVは `s5workerreport,lo,hi,5,verdict,0` とし、先頭に `# evidence_level=WORKER_REPORTED_NOT_INDEPENDENTLY_REPLAYED; NOT A CERTIFICATE` を付す。元の `s5verdict` 読込器はこの行種別を拒否する。
- `--existing` 専用の読込器はこの未検証行種別だけを許可する。担当外・重複・UNKNOWN・不正数値・node数の偽装を拒否する。実際の作業者CSVは従来どおり `s5verdict` を受け取るが、凍結計画の担当とWIN/LOSS矛盾を監査し、証明には昇格させない。
- `--focus-plan` / `--worklist` の再開、凍結計画の検証、4作業者の割当て、原子的な新規ファイル作成は維持。自己試験とCIに、形式分離および生の`s5verdict`を既存結合報告として拒否する回帰を追加。

以前の形式で生成した未検証の結合CSVは、意図的に `--existing` で拒否する。移行する場合は出所を照合し、独立検証済みcacheと混同しないことを確認してから新形式へ変換する必要がある。形式の分離は**独立した勝敗証明ではない**。作業者報告の内容が正しいことも保証しない。

未判定S5は2,208類、優先S4の未判定子は94類、未証明S4は28類。新規S5判定、S4 LOSS証明、二石root閉鎖は0件。標準11×11空盤は **UNKNOWN**。
