# K0900: K0898 r=12境界のcross-lane独立再実行一致検証とSTASIS系列監査再現性スキャン

2026-11-17。本項は2つの独立した成果からなる。

## 1. K0898出版のcross-lane独立再実行一致（agreement check）

K0898（3枝REMO決定性のr=12境界）は別レーンが出版した（commits
746b17d9 → 41544af1、2026-11-17 03:59-04:01Z）。本レーンは同出版を
見る前に同じr=12 cap≤10スイープを独立に開始しており、出版の重複を
避けてこの実行を**独立検証**に転用した。

- **独立実行**: committed JS engine（mask_engine_fast_r12.js・K0893
  修正版のbyte同一コピー・CLI引数r=12）を別プロセスツリー・別作業
  ディレクトリで実行し、15,863正規形プロファイル全域を予算スキップ
  なしで完全スイープした。プロファイルは検証器内蔵の正準列挙
  （direct_constrained(10)・15,863件）から再生成し、先頭・末尾・
  件数が元実行の入力と一致することを確認した。
- **packed記録のbyte一致**: 独立実行のfull記録を決定的packerで
  packed形式に変換した結果は、K0898出版のcommitted packed記録
  （15,863レコード・326,021 bytes・sha256 0835a06fe3a2cc812b5434ef
  0d56146f72b2b019b144ed62544d437472c05274）と**byte単位で完全一致**
  した。独立した2つの実行環境・プロセス起点が同一bytesを生成した
  ことは、このデータのcross-lane決定性の最も強い形の確認である。
  独立実行側のpacked記録を本ディレクトリに
  output/js_cap10_r12.independent.packed.jsonl としてcommitし、
  検証器（check_k0898_cross_lane_agreement.py）が両者のbyte一致を
  機械検証する。
- **full記録経由の監査再生成確認（ローカル実行・非commit）**:
  独立実行のfull記録を.gzとしてK0898検証器のload経路に与えると、
  検証器はcommitted監査JSON（sha256 249ec902…）を**byte同一に再生成**
  した。すなわち独立実行のfull記録は出版監査のsha256_uncompressed
  ピン（full形式のdigest）も含めて全ての監査値を再現する。full記録
  自体はGitHub pushトランスポートのサイズ制限（K0893がpacked形式を
  導入した理由と同一）によりcommitしない。
- **センサス・STASIS4の独立再導出**: 独立実行のpacked記録から
  (sizes,gamma)キーごとの決定性分類・per-key分割・max_statesを再導出
  すると、出版値（715キー・一様決定98・一様非決定583・mixed 34・
  境界7族34キー・max_states 666,030・分割表）と完全一致した。
  さらにK0897出版のr=11 packed記録とのdeterminedフラグ・生存者mask・
  第1敗者maskの差分は0/0/0で、STASIS4（全ラベル不動点）を独立実行
  側からも確認した（検証器C3/C4がcommit状態から再検証）。

## 2. STASIS系列4実験のcommitted監査再現性スキャン（欠陥の発見と固定）

K0898検証器を新規checkout状態（packed記録のみ）で実行したところ、
**committed監査JSONとのbyte比較がFATALで失敗する**ことを発見した。
調査の結果、K0895（r=10）・K0897（r=11）・K0898（r=12）の3項目に
同じ出版衛生上の欠陥があることを確定した:

- **原因**: 3実験ともoutput/にはpacked記録のみがcommitされている
  が、committed監査JSONの"sweep_inputs"とmachine check詳細は
  `"format": "full"`を記録している。監査は出版元レーンの作業環境で
  full形式記録がまだ残っている状態で生成された。新規checkoutでは
  load_jsonlはpacked経路のみを選べるため、再生成監査は
  `"format": "packed"`となり、2箇所のformatフィールド以外は完全に
  同一の監査でもbyte比較が失敗する。検証器run()はこの比較の後に
  live checksを実行するため、live checksは一度も走らない。
- **影響**: 各itemのevidenceが主張する「2回実行で監査JSON byte同一」
  は出版元の環境では真だが、commitされたrepo状態からは再現できない。
  workflow（refresh-knowledge-generated.yml）のK0895/K0897/K0898
  audit stepはfresh checkoutでは必ず失敗する。
- **K0893（r=9）は対照として健全**: r=9のcommitted監査は
  `"format": "packed"`を記録しており、新規checkout状態からbyte同一に
  再現できる（検証器C5/C7で機械確認）。
- **数学的な内容への影響はない**: 再生成監査は3実験とも
  all_ok=true・機械チェック全合格であり、差分は常に2箇所の
  formatラベルのみ（深比較で固定・検証器C6）。記録・証明・境界値は
  全く変わらない。これは出版再現性の欠陥であり、計算の誤りではない。
- **推奨される修正**（所管レーンが実施）: (a) full形式記録を
  output/js_cap10_rN.jsonl.gz としてcommitする（load_jsonlは.gzを
  優先するためformat:"full"監査が再現可能になり、workflow stepも
  通過する。本項の独立実行full記録がr=12についてはこれを満たす）、
  または (b) packed状態で監査を再生成してcommitし直し、各itemの
  pinned sha256を更新する。本項の検証器は(a)(b)どちらの修正後の状態
  でも通り、観測した状態（byte_identical / format_only_difference）を
  監査JSONに記録する。

## 3. 機械検証

`check_k0898_cross_lane_agreement.py`（自己完結・決定的・Python 3.11+
stdlibのみ・ネットワークなし・JS実行なし）。7機械チェック（C1〜C7）
全合格。2回実行で監査JSON byte同一（output/
check_k0898_cross_lane_agreement_audit.json）。検証器は4つのcommitted
検証器モジュール（K0893/K0895/K0897/K0898）をimportlibで読み、
定義とassemble_auditのみを使用する（live checksはworkflow audit step
が所管）。

## 4. 限界

- 独立再実行はr=12・cap≤10領域に限る。r=9/10/11のpacked記録自体は
  各出版の検証器が検証済みであり、本項はそれらの再スイープを行わない。
- full形式記録のsha256_uncompressed再現（§1の3点目）はローカル実行の
  観察であり、commit状態からは再検証できない（full記録がcommitされ
  ていないため）。§2の(a)修正が取られれば恒常的に再検証可能になる。
- 監査再現性欠陥の修正自体は本項では行わない（所管レーンのitemと
  ピンを変更するため、本項は欠陥の固定と修正recipeの提供に留める）。
- 枝サイズ11,12×r=9..12・r≥13・順位決定性などK0898の未解決事項は
  本項でも未解決のまま。
