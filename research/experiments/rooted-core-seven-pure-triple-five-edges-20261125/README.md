# rooted-core-seven-pure-triple-five-edges-20261125

K0684（固定残余核＋長道の全称34周期予想）への same-K evidence update。
**7点・純三点辺・五本以下の完全族**（raw 384,168件・根付き924型・閉包2,948状態・
新規2,604状態）の Grundy 列を長さ0..1211までの全整数値で確定し、K0682有限窓定理により
**開始571以降の全長34周期を認証**（`jointly_certified=true`・族のprefix上Grundy最大33
［二点辺混在6点残留 `[6,[3,6,13,24,44]]` が唯一担う・7点初期型の最大は27］）。

主な成果:
- 7点の純三点辺核として初めて K0684 evidence-family を拡張（それまでの
  フロンティアは6点全型10,688状態）。
- **6点の二点辺混在clutter 1,379状態の初認証**（7点核の着手による三点辺の退化で
  出現。既出版の純三点辺6点監査には含まれない型）。この族では開始571の
  最悪破綻も二点辺混在状態 `[6,[3,13,22,28,49]]` が担う。
- 型数924をBurnside軌道数計算で独立導出、軌道安定化子総和=raw件数で照合。
- 6公式走（同一cwd 通常×2・`PYTHONHASHSEED=random/1`×2・隔離tree `env -i`×2）が
  すべて byte 一致。うち2走はサンドボックス障害後の別サンドボックスでの再現で、
  記録済み sha256 `5a1efeba...` を完全再現（環境をまたいだ再現性）。

## ファイル

- `solve_core.py` — 共同適応solver（engine.pyの再帰・K0682基底表の遅延拡張・
  チェックポイント再開・有限窓認証）。sha256
  `35a563254da03da66c2f12a512c489c82405d2ba2c396d1a0746f5e5a25272e5`。
- `drive_slice.py` — ドライバ（mode `smoke6`=6点×6本以下 smoke再現・他=7点公式）。
- `shard_records.py` / `combine_records.py` — recordsの6分割shard化と正規単一ファイル
  への再結合（再結合で sha256 `5a1efeba...` の byte 再現を検証済み）。
- `verify_enum.py` — E1..E7: 枚挙再現・Burnside軌道数924・軌道安定化子総和
  384,168・canonical固定点・閉包2,948={2604新規+344既知}・shard型集合一致。
- `verify_values.py` — V1..V7: 独立再実装の再帰で全値再計算・全レコード照合・
  窓認証・基底表整合・301純triple状態の出版6点監査（×6本・全型両方）全長一致・
  1,379混在状態の出版監査不在確認。
- `verify_direct.py` — 階層化400状態×長さ0..6の原始ゲーム照合（2,800検査・
  安全状態922,862）。
- `verify_tamper.py` — fail-closed改変電池（T4..T10全件検出）。
- `verify_smoke.py` — smoke6_records.json と出版6点×6本以下監査の全レコード一致。
- `output/shards/part00..05.json` — 公式認証レコード（2,604状態、連結で
  `output/official_records.json` 相当）。
- `output/smoke6_records.json` — 宣言前探査の smoke 成果物（出版監査と全一致・
  sha256 `dd416a011862303466dc5028e6665f6a37c13de2bf4916514becaf22d6f8eebf`）。

依存: `research/experiments/rooted-core-tail-periodicity-20261107/`
（engine.py・基底表 audit.json）、
`rooted-core-six-pure-triple-six-edges-20261107/output/audit.json`・
`rooted-core-six-pure-triple-full-20261108/output/audit.json`（照合用）。

実行規約・宣言は `research/log/2026-11-25-rooted-core-seven-pure-triple-five-edges-single-owner-note.md`
および run log を参照。数値は全て有限族に関するもので、K0684の全称予想の証明ではない。
