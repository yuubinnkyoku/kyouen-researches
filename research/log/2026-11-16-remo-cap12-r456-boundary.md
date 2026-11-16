# 2026-11-16 — REMO 3枝: cap≤12のr=4,5,6サイズ境界（K0876）とworkflow step復元

## Context

K0875定理H12（r=3・cap≤12・非坍縮22キー不変）が「r≥4×枝サイズ11,12の
組合せセルは未走査」を限界として残した。このセルは実質的な悬案だった:
r=4はcap≤10で12キーmixedであり、サイズ11,12枝がr=4,5,6に新しいmixed
キーを加えるかは有限計算の外にあった。同時に、現行mainの
workflow ymlから「Audit K0875 three-branch REMO cap12 size boundary」
stepと「Audit K0874 independent verification」stepが
check.py red repairコミットで脱落している回帰を発見していた。

## What was done

- r=3..6×47,595プロファイルの判定を、決定的JavaScript maskエンジン
  （mask_engine_fast.js）で生成する構成にした。1コア・1GB cgroup・
  bash 1回最大300s・バックグラウンドプロセスがbash呼び出し境界で
  死ぬ制約のため、resume_sweep.shによる分割再開スイープで実行し、
  レコードをgzip -n圧縮してコミット対象とした。
- 検証器 verify_remo_k_branch_cap12_r456_boundary.py を作成
  （committed recordsのsha256照合・Python mask twinのlive checks・
  出版定数の機械再現・40 machine checks・assemble二重バイト同一）。
  live checksは検証器の実行が長すぎるため sliced_live.py で
  cap≤7全域・層化サンプル・全witnessに分割実行した。
- **JS maskエンジンの共有savedColバグを発見・修正**: 排除（elimination）
  のネストで退避配列をクロージャ間で共有し、内側elimが外側の退避値を
  上書きし得た。r=3は実行経路の偶然で無被害、r≥4は破壊され得た。
  per-call退避配列へ修正し全レコードを再生成、修正後に
  verbatim==twin==JS三重照合0不一致を確認。
- 実行環境リセットでスイープ作業ファイルが一度消滅し、検証器と
  Knowledgeチェックポイントから再構築して続行した。
- workflow yml回帰を修復: 34c1ece4版から脱落2 stepをverbatim復元し、
  K0876監査stepとtrigger commentを追加した。

## Results

- **定理I12（K0876・新規）**: cap≤12でもr=4,5の非坍縮キーは(8,8,9),
  (8,9,9)×γ=0..5の12個ちょうど、r=6は(4,4,8),(4,8,8)×γ=0..2の
  6個ちょうどで、出版cap≤10境界（K0864定理I）と完全同一。
  サイズ11/12枝を含むキーでmixedは0個。センサス
  r=4: 216/1137/12、r=5: 163/1190/12、r=6: 163/1196/6。
- 失敗キーの生存者・可能生存者集合・分割計数・ミラー交代はcap≤10
  出版と完全不変。小枝族10キーはr≥4で全域一様非決定。
- 剰余レンズ: 新2剰余キー576/592/605個は全て坍縮。r=4では出版失敗対
  {0,1}を持つ新キー60個（すべてサイズ12枝を含む・(9,12,12)/(9,9,12)/
  (1,1,12)等15多重集合）も全て一様非決定（アウトオブサンプル）。
  r=5,6ではそのような新キー0個。
- FL違反0×4r、Δ=0×1,512プロファイル（サイズ11/12枝含む784個）全定理D値、
  G′生存者0不一致、定理D表84エントリ一致、r=3 committed recordsは
  K0875出版auditを正確に再現。
- 40 machine checks全合格。audit sha256
  b13593f041957a5bf58c850ab1fd9adbb49f36332ab2a8079a695727f057eaad。
- yml: K0875・K0874独立検証step復元+K0876 step追加。

## Consequences

- **r=2..6×cap≤12の3枝REMO決定性境界が確定**（r=2はK0864定理Iで715キー
  完全坍縮・r=3はK0875・r=4,5,6は本項）。残る未走査:
  r=7,8×サイズ11,12（K0866/K0869のcap≤10境界の拡張）、r≥9、
  枝サイズ≥13。
- r=4のアウトオブサンプル剰余テスト（60キー全て坍縮）は
  K0872剰余署名の必要条件としての証拠を1段強めたが、一般必要条件の
  証明は未解決のまま。
- 次の候補: (i) r=7,8×cap≤12スイープ（本項のレコード生成・検証構成を
  そのまま再利用可能）、(ii) 枝サイズ≥13の剰余レンジ順序付け探索、
  (iii) K0872剰余署名の一般必要条件の証明の試み。

## Artifacts

- research/experiments/remo-k-branch-cap12-r456-boundary-20261116/{verify_remo_k_branch_cap12_r456_boundary.py, mask_engine_fast.js, resume_sweep.sh, resume_check.py, gen_profs.py, report.md, output/js_cap12_r{3,4,5,6}.jsonl.gz, output/remo_k_branch_cap12_r456_boundary_audit.json}
- research/knowledge/items/K0876-remo-k-branch-cap12-r456-boundary.md
- research/knowledge/README.md（K0876行を追加）
- .github/workflows/refresh-knowledge-generated.yml（脱落2 step復元・K0876監査step・trigger comment 2行を追加）

## Interpretation guard

定理I12はr=4,5,6・サイズ≤12の有限完全計算であり、r=7,8・サイズ≥13への
外挿でも特徴づけでもない。順位決定性は本項で再導出していない
（maskエンジンのレコードはorder列を再現しない）。「一様非決定」は
決定性レベルの話で、可能生存者集合はr・atom配分に依存してよい。
本項の有限観察を全称定理へ昇格させない。
