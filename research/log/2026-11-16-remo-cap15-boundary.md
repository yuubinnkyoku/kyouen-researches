# 2026-11-16 remo cap15 boundary (K0886)

## 経緯

- 前回実行（K0883・定理H14・cap≤14）のレジューム項目「cap15スイープ」を
  実施。正準cap≤15列挙→r=3スイープ（189,864プロファイル）→pack→
  解析→検証器→出版まで一気通貫。
- **番号**: 実験中の仮番号はK0884だったが、push前の最新main確認で
  並走two-tokenレーン（z=6,y=5）がK0884を取得済みだったため
  AGENTS.mdの再採番規約に従いK0885へ再採番し、その後の再確認で
  同レーン（z=6,y=6）がK0885も取得していたことが判明したため
  **K0886へ再度再採番**した。
- **環境喪失と完全再生成**: 第一実行（packed 4 shaピン・監査JSON
  sha `d5d21c28…`・2回実行byte同一まで完了・未push）の後、実行環境の
  リセットでワークスペース（検証器・生成物・草稿すべて）を喪失した。
  main上のK0883/K0876出版成果物（maskエンジンはmain出版blobとsha同一・
  K0883検証器）を取得し直し、列挙・スイープ・packを**独立環境から
  再生成**したところ、joined+3部のsha256ピン4点すべてが第一実行の
  記録値とbyte一致（cross-environment byte-identical）。検証器は
  K0883出版検証器から単独性assert付き機械変換で再構築し、定数は
  再生成レコードから機械抽出、監査・live checkを再実行した。
- K0883の検証器を機械変換（単独性assert付きの置換群）でcap15版を
  作成。定数は解析実行（analyze15.py）から機械抽出。

## 判定・結果（定理H15）

- cap 15のBurnside: fix(id),fix(trans),fix(cyc)=(1,074,198, 21,414, 372)
  → 軌道189,864。キー数3,060（一様決定399・一様非決定2,551・mixed 110）。
- **H14の外挿は15でも反証**: 非坍縮（mixed）キーは**110個** = H14の52 +
  **58個の新キー**。58個すべてサイズ15枝を含む（680キー中58個）。
- 新キーは11の多重集合: (14,14,15),(14,15,15)×γ=0..9（20）・
  (2,8,15),(2,14,15),(3,8,15),(3,14,15)×γ=0..1（8）・
  (8,8,15),(8,9,15),(8,14,15),(8,15,15),(9,14,15)×γ=0..5（30）。
- **γ窓0..9の初出現**（従来の失敗族はγ≤5）: (14,14,15)/(14,15,15)。
- **ndet可能生存者集合{0,1}の初出現**: 8と15を併せる6多重集合28キー
  （cap≤14では{{1,2},{0,1,2}}内）。
- 置換レンズ（有限観察）: H14の52キーの{8,9,14}要素1〜2個を15へ置換した
  候補74キー中50個がmixed・24個坍縮。残り8新キーはγ窓外側（γ=6..9）。
  新mixedはすべて8枝または14枝を併せ持つ。
- 110キーすべて剰余対{0,2}・決定側生存者一様P_1・H14の52キーの
  per-key分割は完全不変（K0883・K0876監査と完全一致）。
- FL補題はcap≤15全189,864プロファイルで違反0。1剰余525・3剰余525キー
  はすべて坍縮、2剰余2,010キーの非坍縮は110個のみ。
- 最大状態数120,202（状態総数1,545,731,088）。
- 順序保存部分列性（D_14⊂D_15）でK0883出版r=3 packedレコード123,272件
  をD_14対応位置で全件再現（0不一致・per-part shaピン照合）。

## 検証

- verify_remo_k_branch_cap15_boundary.py（stdlibのみ・決定的）:
  24機械チェックall_ok + assemble二重実行byte同一 + **別プロセス2回
  実行で監査JSON byte同一**。live: cap≤7全域2,048 verdicts
  （verbatim==mask twin==committed）、stride 32層化サンプル5,934
  verdicts、K0862出版44 witness再検証+committed突合、全てOK。
- K0883交差照合: 出版r=3 packed（part1of2/part2of2の2分割・joined
  sha256 710f3289…）123,272件全件再現、K0876監査JSON（sha256 19b4d833…）
  のH22分割表とK0883監査JSON（sha256 fae36528…）の52キー分割表と完全一致。
- スイープレコードは第一実行（別環境）の記録shaピン4点とbyte一致
  （joined `7c44da46…`・part1 `ddda26c9…`・part2 `2c30fe0b…`・
  part3 `efa6b55d…`）。

## 出版運用

- packed出版blob（3,318,169B・189,864件）は1コミットでpush可能なサイズを
  超えるため、**行境界3分割のpart1of3（1,069,591B）+part2of3
  （1,109,169B）+part3of3（1,139,409B）**として3コミットで出版
  （n11証明書のpart分割慣例と同じ方式）。検証器はper-part sha256ピン
  +joined shaピンで照合。
- コミット構成: part1of3 data 1/3 → part2of3 data 2/3 → part3of3
  data 3/3 → verifier+audit+report+engine+packer → item/log/README
  bullet/workflow audit step。
- pushはtools.github_app.push_files（1コミット1ファイル・着地は
  git blob sha照合で確認）。

## 番号

- 仮番号K0884は並走two-tokenレーン（z=6,y=5・2026-11-16 20:42出版）が、
  再採番後のK0885は同レーン（z=6,y=6）が取得済みだったため、
  **本項はK0886へ再採番**（AGENTS.mdの規約どおり・2段階）。

## 解釈規約

- 定理H15はr=3・cap≤15の有限完全列挙の範囲で主張。r≥4のサイズ13以上は
  未走査、サイズ≥16は未走査（16≡1 (mod 3)で未観察剰余）。
- 置換対応・「8/14併有」・γ窓拡張・ndet生存者{0,1}・「非坍縮⇒2剰余」は
  有限観察であり一般証明ではない。
- 11×11空盤はUNKNOWNのまま。

## Artifacts

- research/experiments/remo-k-branch-cap15-boundary-20261116/{verify_remo_k_branch_cap15_boundary.py, mask_engine_fast.js, pack_records.py, report.md, output/js_cap15_r3.packed.jsonl.part1of3, output/js_cap15_r3.packed.jsonl.part2of3, output/js_cap15_r3.packed.jsonl.part3of3, output/remo_k_branch_cap15_boundary_audit.json}
- research/knowledge/items/K0886-remo-k-branch-cap15-boundary.md
- research/knowledge/README.md（K0886行をK0883行の直後に追加）
- .github/workflows/refresh-knowledge-generated.yml（K0886監査step・trigger commentを追加）
