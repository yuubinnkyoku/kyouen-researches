# 2026-11-18 N11 cost-16 parent（00000000000000003800000008001000・31行）最小coverのB型総数厳密決定・全最小cover総数確定

## 成果

cover表4番目の31行 cost-16 parent `00000000000000003800000008001000`（31 open non-STERILE行・cost 16 exact・2,333候補・1,908 root = 425 pair type（すべてmultiplicity 1）+ 1,483 singleton）について、phase A（出版済み・commit `2adf7f94`）で未確定のまま残っていた **B型総数（16 pair・1行二重被覆型）を厳密に決定し、全最小cover総数を確定**した。check設計は並走checkpoint（commit `d2901d15`・script出版）を引き継ぎ、本セッションで完全実行・二重実行して出版する。

- script: `research/experiments/n11-head1410-partial-parent-nonsterile-children-20261118/cost16_parent_preanalysis_20261118.py`（commit `d2901d15` で出版済み・変更なし）
- output: 同dir `output/cost16-b-phase-total-20261118.json`
- 31 checks all PASS。

## 主要数値

1. **B型総数 B16 = 660,663,050,386,546,968（約6.6e17）**: 16 pair root で1行だけが二重被覆される型の最小cover計画数（31 = 2·16−1 の奇数r B型）。
2. **全最小cover総数 = 2,966,450,341,680,481,356（約2.97e18・A型 77.73% + B型 22.27%）**。29行runner-upの全最小cover総数（4.59e16）の約65倍。**これで31行parentは11・18・23・29行に続き5 parent目として総数・membership解析が完全完遂**（本プロジェクトで厳密計算した最大のparent）。
3. **per-d slice設計でphase Bを安全化**: B16 を31個の独立な per-d slice B_d = Σ_{a<b∈N(d)} w(d,a)w(d,b)·pm(V∖{d,a,b}) に分解し、各sliceに新規memo（観測最大 3,524,540 状態 ≤ singleton位相の 3,524,561）を持たせた。旧設計（単一共有memoで全425 pair membershipを計算）はpair位相でmemoが920万状態を超え3.2GB環境でOOM-killしていたが、**slice設計は全位相がsingleton位相以下のメモリプロファイルに収まる**。各slice 276〜435 anchors（計約11,000 anchors）・実行30〜40秒/slice。
4. **アンカー計測（29→31行スケーリングの実測）**: 新規memoでの singleton anchor pm(V∖s) は baseline29 で 514,212〜514,227状態（出版~514Kと一致）、target31 で 1,346,244〜1,346,258状態（最初のアンカー1,346,254は出版30行木1,346,254と同一）で成長比2.62x。**target31のB位相アンカー pm(V∖{d,a,b}) は 514,222〜514,229状態で、ちょうどbaseline29のsingleton anchorと同規模**（3行除去で29行スケールに到達）− anchored状態空間は行数でなく候補構造で決まることの追加実測。baseline29のB位相アンカーは196,342〜196,399状態、B位相アンカー成長比2.62x。

## 検証

- **A位相の出版値完全再現**: A16 = 2,305,787,291,293,934,388・全31 per-row pm・memo状態数 3,524,561 が出版phase A output（blob `fe4b4b55`）と完全一致。
- **実装検証**: 出版済み29行runner-up output（blob `05f54eb5`）の全1,505 singleton membershipを同一実装が完全再現（0不一致）。
- **二重実行（環境リセットを跨いで成立）**: 完全実行2回（1回目は300秒コマンド上限超過でホスト環境ごとリセットされ作業dirを喪失したが、全31 slice値・memo・anchor計数を含む全数値をリセット前に記録済み）。リセット後の再構築・再実行で **全31 sliceの B_d・memo_states・anchors が完全一致**、aggregate（A16・B16・total）も並走checkpointのfirst completed run（commit `d2901d15` のmessage記載値）と完全一致。**実質的に3独立実行で全数値一致**。最終JSONはtiming欄をstripしてあるので二重実行はbyte-comparable。
- **並走第三実装クロスチェックとの整合**: Node.js第三実装（commit `0ce32ace`・82 checks・二重実行byte-identical・full 11-row anchorで757 root membership再現 + 31 fresh-memo B slices + 31 fresh-memo A slices）が A16/B16/total を本出力と完全一致で再現。**本出力の B16 = 660,663,050,386,546,968 は、並走のpair membership進行（commit `c07af83d`・394/425再計算済み）が定義したcross-lane aggregate check「sum(b_part)/16 == B16」の錨**として機能する。
- 入力pin 6ファイル（worklist・census・ledger・cover表・phase A output・runner-up29 output）はgit blob SHAでbyte-exact検証してから使用。候補root JSONL（出版せず・20,532,577 bytes）は同梱 `enumerate_global_candidate_roots_20261118.py` で再生成（39.5秒・6,337行・row数はphase-1出版と一致）。
- 実行時間の実測: measure baseline29 約2.5分・measure target31 約8分（singleton anchor 11.3秒/個・B位相アンカー3.9秒/個）・A位相38秒・B slices 計約19分・assemble 11秒。

## 実験的事実（運用）

- 300秒コマンド上限を超える複数フェーズ連結コマンドは、超過時刻に環境ごとリセットされ作業dir（repo再構築・workdir両方）を失う。知識記録の「位相ごとにコマンドを分ける」運用の重要性を再確認。一方で**計算自体は完全に決定的**で、リセット後の再実行が全数値を再現した（scriptのper-anchor/per-slice checkpoint設計に加え、コマンド出力の全slice値を会話記録に残しておくことでリセット後も照合可能）。
- B_d の分布: 最小 18,319,351,945,126,110（d=18・bottleneck行）・最大 23,475,415,507,703,040（d=2,3,13・pair degree 30のハブ行3本が同値）。slice間のB_d比は1.28以内で、29行runner-upで見たpair rootへのmembership集中（約49倍）と異なり行方向にも平準化している。

## 次課題

1. **31行parentの生存曲線**（上位pair root banでA+B再計算: A位相40秒 + 31 slice約19分/k点。slice pm treeの再利用設計があれば削減可能）。pair membership上位の絞り込みには並走のb_part進行（`c07af83d`）と本出力のB16錨照合が前提。
2. **31行parentの全425 pair root membership**: 並走がgroups scriptで進行中（394/425・`c07af83d`）。完了後はcross-lane aggregate check sum(b_part)/16 == B16（本出力値）で検証。
3. cross-parent joint分析は並走が5 cheapest parentに拡張済み（commit `3a04ca5b`・5-way joint exact cost 56 vs 58）。残る検証側ワークロードは生存曲線と、並走出力の第三実装クロスチェック。

## 解釈上の注意

A型・B型総数は代替最小cover計画の組合せ数であって探索コストでもverdictでもない。本分析はcover計画の組合せ論のみを主張する。REFUTED-D10・STERILE は LOSS 証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて UNKNOWN。
