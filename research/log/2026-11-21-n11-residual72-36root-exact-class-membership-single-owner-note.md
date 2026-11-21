# 単一オーナー宣言: n11 residual72 36-root 10石D4クラス→root所属の正確な再生成と分割候補のクラスレベル評価（2026-11-21）

- 宣言: 2026-11-21T10:20Z（本ノートの出版が宣言時点）
- 宣言時 HEAD: `4940df5b9433c2bc2928fc09b4f9b01935a14188`（class E/F/D修復レーン part 2/5 出版直後）
- レーン: `research/experiments/n11-residual72-36root-exact-class-membership-20261121/`
- 並走上の位置づけ: 36-root depth-10掃引（宣言 `2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）は
  掃引オーナーレーンが実行中であり、本レーンはそのdriver・runner・roots・residual72・outputに一切触れず、
  判定probeも起動しない。36-root partition candidateレーン（f7466198出版済み）が
  「10-stone class-to-root membershipの正確な再生成はtime out」「per-worker class-copy計数は主張しない」
  と明示的に残した測定ギャップを埋める。

## 本レーンが実行するもの

1. **入力pin**: K1075正本
   `research/experiments/n11-residual72-full-cache-join-candidate-supply-20261120/output/residual72-full-cache-join-candidate-supply-20261120.json`
   （SHA-256 `49b6f85f…`・git blob `45744d82…`・取得済み照合一致）。
   方法pinは出版census検証器 `audit_36_root_three_ply_frontier_20261120.mjs`
   （SHA-256 `7177a25a…`）の列挙規約（11×11・8変換D4正準形・BigInt `[x²+y²,x,y,1]` 行列式・
   余因子/Leibniz両展開照合・合法手はbase・pairMask・occのBitMask全数）を正則に再現する。
2. **正確な所属マップ再構築**: 36 rootの三手先（10石）733,855 raw局面 → D4正準形クラス→root所属を
   全数再構築し、publish済み集計（全728,370類・root別733,800 membership・root内併合55・
   多重所属5,430 = 2-root共有5,420類 + 3-root共有5類・pairwise総重複5,435）を値単位で再現。
   同一列挙の副産物として8石（1手先）・9石（2手先）のクラス→root所属も収集する
   （現行censusは10石層のみで9石・8石のroot間多重所属は未測定）。
3. **出版正本との照合gate（fail-closed）**: 生成した全数値が出版census正本
   `36-root-three-ply-frontier-20261120.json`（SHA-256 `94fdb0c6…`）の
   summary・worker_stats・per_root・pairwise_overlap（221組・shared数全件）・multiplicity histogram と
   完全一致すること。一致しない項目が1つでもあれば原因解明まで結果出版を行わない。
4. **クラスレベル統計の新規出版**: 3-root共有5類の特定（クラスhex + 所属3 root）を初めて出版。
   strided baseline（roots[W::4]）と partition candidate（`worker-partition-candidate-20261121.json` の
   root_groups・SHA-256 `09b394b8…`）の両配分について、pairwise proxyではなく
   クラス単位の正確なworker統計（worker内冗長コピー数・worker横断スパン類数・per-workerユニーク類数・
   多重所属類のworker分布）を計算・出版。candidate JSONのbaseline/candidate統計
   （baseline loads 181,882/190,739/178,529/182,650・cross 4,193・candidate cross 2,000 等）との
   値一致も照合する。
5. **9石・8石層の同様の統計**: 2手先・1手先のクラス→root所属からworker横断/worker内統計を
   同形式で出版（root間共有の観察としてのみ。10石層の大小関係の外挿はしない）。

## 実行・出版手順

- 計算は本sandbox（2コア）内で逐次・1プロセス・root単位checkpoint方式（1 bash callの壁時計制限に対応）。
- 出版は: part1 = 実験dir（README・scripts・output/正確所属表と統計JSON）→
  part2 = セッションlog → part3 = `n11-search-methods/README.md` への参照行1行追加。
  K itemは作成しない（探索的測定は既存K1072/K1084/K1075族の正域に含まれ、partition candidateレーンと
  同様にitemを立てない先例に従う）。pushごとに最新main再取得・fetch-back byte照合。
- repoへ出版するのは多重所属類（10石層は5,425類程度と予想）と集計JSONのみ。
  全728,370類の正規一覧は巨大ため出版しない（再現scriptで誰でも再生成可能）。

## 非目標

- 掃引オーナーレーンのファイル・assignment・実行への関与は一切ない。
- 分割変更の提案・適用はしない（実測TT hit率との比較は掃引完了後の後続レーン）。
- candidate自体の改善探索（annealing再実行・新候補探索）は行わない。
- pairwise proxyかクラス計数かのどちらが「共表実装」を正当化するかの判断は行わない
  （幾何重複はDFPN表命中率ではない）。
- 勝敗・行閉鎖・root資格・S6行の簿記は一切変更しない。WIN証明書ではなく候補root。

## 受入条件（完了の宣言）

1. 照合gate: 12 gate相当 + pairwise 221組全件 + multiplicity + summary/worker_stats/per_root の
   値完全一致。1つでも不一致なら出版しない。
2. 決定性: クラス→root所属の再構築を2回（うち1回は別cwd）実行し、多重所属表がbyte-identical。
3. 正確統計はbaseline・candidate両方について機械可読JSONで出版し、candidate JSON既出版値と
   矛盾しないこと（矛盾時はfail-closed）。
4. 各pushはfetch-back raw固定URL（commit sha指定）でSHA-256照合。競合・timeout時は無理に
   押し進げず状況をlogに記録して次回実行へ回す。
5. 解釈規約: 幾何重複は実探索費用・表命中率ではない。REFUTED-D10はLOSS証明ではない。
   **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 先行宣言の不在確認

宣言時HEADまでの直近commit列挙と実験dir一覧で、exact membership再生成・クラスレベル
worker統計を標榜する単一オーナー宣言・実験dirは存在しないことを確認した
（partition candidate logは再生成time outと未主張を明記・census READMEも同旨）。
