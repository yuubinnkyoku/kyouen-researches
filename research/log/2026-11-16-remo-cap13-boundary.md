# 2026-11-16 remo cap13 boundary (K0882)

## 経緯

- 並走する同じレーンの実行がK0876修復3/3（c50f31f1・監査sha256
  19b4d833…）とr278（r=7,8×cap≤12）の出版を進めていたため、
  本実行は重複を避けてK0876 logの次の候補(ii)「枝サイズ≥13の
  剰余レンジ順序付け探索」に着手した。
- K0875の定理H12（cap≤12・r=3・非坍縮22キー）をcap 13へ伸ばす。
  列挙・Burnside・エンジン・mask twin・K0862 witness定数は出版済み
  K0876検証器（packed読み取り修復版）からverbatim抽出して再利用。

## 判定・結果

- cap 13のBurnside: fix(id),fix(trans),fix(cyc)=(432,906, 11,186, 252)
  → 軌道77,828。direct_constrained(13)が直接列挙でも77,828で一致
  （5.5秒）。キー数1,820。
- **順序保存部分列性の発見**: 正準列挙はcapを広げても既存プロファイル
  の相対順序を保つ（D_12⊂D_13・D_13⊂D_14）。このため cap≤13 の
  r=3 スイープは、D_12対応位置で K0876 出版 r=3 packed レコード
  47,595件を**全件再現**する。検証器はこれをsha256ピン付きの
  交差アーティファクト照合として組み込んだ（0不一致）。
- スイープ（mask_engine_fast.js・r=3・77,828プロファイル）は130秒で
  完了。packed出版形式のレコードは1,293,779バイト
  （sha256 47a5eb34f738dc60a74d4ef0c66e54032d7c79f2e3413b47c40dbc56c07df5fd）。
- **定理H13**: 非坍縮（mixed）キーは定理Hの22個のまま。サイズ13枝を
  含む455キーは全て坍縮。1,820キーの内訳は一様決定313・一様非決定
  1,485・mixed 22。
- 22キーの構造は不変: 決定側生存者一様P_1・非決定側可能生存者集合
  ⊆{{1,2},{0,1,2}}・per-key分割はK0876監査sweeps.r3.failing_partitions
  と完全一致。
- FL補題はcap≤13全77,828プロファイルで違反0（cap≤12観察の拡張）。
- 剰余レンズ: 1剰余330キー・3剰余300キーはすべて坍縮。2剰余1,190キー
  の非坍縮は22個のみ（すべて剰余対{0,2}）。「非坍縮⇒2剰余」の必要条件
  観察はサイズ13まで無反例。
- 最大状態数48,256（状態総数294,553,171）。
- cap 14の列挙（123,272軌道・Burnside一致）と部分列性（D_12,D_13⊂D_14）
  は確認済みだが、スイープは次回実行に回す（本実行はcap 13で出版を
  完結させる）。

## 検証

- verify_remo_k_branch_cap13_boundary.py（stdlibのみ・決定的）:
  19機械チェックall_ok + assemble二重実行byte同一。
  live: cap≤7全域2,048 verdicts（verbatim==mask twin==committed）、
  stride 32層化サンプル2,433 verdicts（mask twin==committed）、
  K0862出版44 witness再検証+committed突合、全てOK。
- K0876交差照合: 出版r=3 packed（sha256 ea7c6628…）47,595件全件再現、
  K0876監査JSON（sha256 19b4d833…）のr=3分割表と完全一致。
- 監査JSON: output/remo_k_branch_cap13_boundary_audit.json。

## 番号

- K0877-K0880はtwo-tokenレーンが使用済み、さらに並走する同じレーンの
  r278出版（元はK0878ラベル→K0878衝突回避でK0881に再採番）がK0881を
  使用したため、本項はK0882を採番（AGENTS.mdの再採番規約に従う）。
  検証器meta.itemはK0882。
- 並走レーンのr278出版（data 1/3が「K0878」ラベルでpush済み）は
  K0878-two-token-z6-y2と番号衝突の可能性があるまま残っている
  （item未出版なので実害はまだ無い。次回実行で注意）。

## 解釈規約

- 定理H13はr=3・cap≤13の有限完全列挙の範囲で主張。r≥4のサイズ11以上
  は未走査、サイズ≥14は未走査。「サイズ8が失敗に必要」はサイズ≤13で
  のみ確定。
- 「非坍縮⇒2剰余」は必要条件の有限観察であり一般証明ではない
  （K0872と同様の位置づけ）。
- 11×11空盤はUNKNOWNのまま。

## Artifacts

- research/experiments/remo-k-branch-cap13-boundary-20261116/{verify_remo_k_branch_cap13_boundary.py, mask_engine_fast.js, pack_records.py, report.md, output/js_cap13_r3.packed.jsonl, output/remo_k_branch_cap13_boundary_audit.json}
- research/knowledge/items/K0882-remo-k-branch-cap13-boundary.md
- research/knowledge/README.md（K0882行を追加）
- .github/workflows/refresh-knowledge-generated.yml（K0882監査step・trigger commentを追加）
