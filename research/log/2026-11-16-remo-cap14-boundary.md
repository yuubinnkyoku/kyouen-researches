# 2026-11-16 remo cap14 boundary (K0883)

## 経緯

- 前回実行（K0882・定理H13・cap≤13）のレジューム項目「cap14スイープ」を
  同一セッション内で実施。cap14の列挙・Burnside・部分列性（D_12,D_13⊂D_14）
  は前回確認済みだったため、正準列挙生成（10.5秒）→r=3スイープ（324.6秒）
  →pack→解析→検証器→出版まで一気通貫で完了した。
- K0882の検証器を機械変換（stage1-4・各置換は単独性assert付き）して
  cap14版を作成。定数は解析実行（analyze14.py）から機械抽出。

## 判定・結果（定理H14）

- cap 14のBurnside: fix(id),fix(trans),fix(cyc)=(692,102, 15,638, 308)
  → 軌道123,272。キー数2,380。
- **H13の外挿予想（境界は22キーのまま）は反証**: 非坍縮（mixed）キーは
  **52個** = 定理Hの22 + **30個の新キー**。30個すべてサイズ14枝を含む。
- 新キーは9つの多重集合: (2,3,14),(2,9,14),(3,3,14),(3,8,14),(3,9,14),
  (3,14,14)×γ=0..1（12キー）と (8,9,14),(9,9,14),(9,14,14)×γ=0..5
  （18キー）。有限観察: 定理H多重集合の{8,9}要素の置き換え形
  （候補11のうち(2,8,14),(8,8,14)は坍縮）。14 ≡ 8 ≡ 2 (mod 3)。
- 52キーすべて剰余対{0,2}・決定側生存者一様P_1・非決定側可能生存者集合
  ⊆{{1,2},{0,1,2}}。定理Hの22キーのper-key分割は不変（K0876監査と一致）。
- FL補題はcap≤14全123,272プロファイルで違反0。1剰余420・3剰余400キーは
  すべて坍縮、2剰余1,560キーの非坍縮は52個のみ。
- 最大状態数74,695（状態総数686,151,143）。
- 順序保存部分列性（D_13⊂D_14）でK0882出版r=3 packedレコード77,828件を
  D_13対応位置で全件再現（0不一致）。
- **「サイズ8が失敗に必要」はサイズ14で反例**（(2,3,14)等は8を含まない）。
  K0882 reportのguard（サイズ≤13でのみ確定）どおりの結果。

## 検証

- verify_remo_k_branch_cap14_boundary.py（stdlibのみ・決定的）:
  21機械チェックall_ok + assemble二重実行byte同一。
  live: cap≤7全域2,048 verdicts（verbatim==mask twin==committed）、
  stride 32層化サンプル3,853 verdicts（mask twin==committed）、
  K0862出版44 witness再検証+committed突合、全てOK。
- K0882交差照合: 出版r=3 packed（sha256 47a5eb34…）77,828件全件再現、
  K0876監査JSON（sha256 19b4d833…）の定理H 22キー分割表と完全一致。
- 監査JSON: output/remo_k_branch_cap14_boundary_audit.json
  （sha256 fae365285964deed238a4995479346cc354b316e6661ffe95e03fab08530f501）。

## 出版運用

- packed出版blob（2,097,654B・123,272件）はrun_typescriptのメモリ上限
  （16MiB・read_fileの記録コール当たりoverhead込みで~1.3MBが実用上限）
  を超えるため、**行境界2分割のpart1of2（1,033,246B）+part2of2
  （1,064,408B）**として2コミットで出版（n11証明書のpart1of2/part2of2
  慣例と同じ方式）。検証器はper-part sha256ピン+joined shaピンで照合。
  pushはMemoryLimitErrorでもpush_files自体は実行済みの場合があるため
  必ず着地確認（今回はgit blob sha照合でOK）。
- コミット構成: part1of2 data 1/2 → part2of2 data 2/2 → verifier+audit
  +report+engine+packer → item/log/README bullet/workflow audit step。

## 番号

- K0883は本項が最初の使用（push前にitems/の空きを確認済み）。
  並走r278レーン（K0881）のitemはまだ出版されていない。

## 解釈規約

- 定理H14はr=3・cap≤14の有限完全列挙の範囲で主張。r≥4のサイズ13以上は
  未走査、サイズ≥15は未走査。
- 置換対応・「非坍縮⇒2剰余」は有限観察であり一般証明ではない。
- 11×11空盤はUNKNOWNのまま。

## Artifacts

- research/experiments/remo-k-branch-cap14-boundary-20261116/{verify_remo_k_branch_cap14_boundary.py, mask_engine_fast.js, pack_records.py, report.md, output/js_cap14_r3.packed.jsonl.part1of2, output/js_cap14_r3.packed.jsonl.part2of2, output/remo_k_branch_cap14_boundary_audit.json}
- research/knowledge/items/K0883-remo-k-branch-cap14-boundary.md
- research/knowledge/README.md（K0883行をK0882行の直後に追加）
- .github/workflows/refresh-knowledge-generated.yml（K0883監査step・trigger commentを追加）
