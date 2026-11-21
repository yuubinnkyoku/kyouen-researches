# 2026-11-21 n11 residual72 36-root 正確クラス所属再生セッションlog

## 判断の経緯

- 本実行は長期レーン（標準11×11決着）として、まず最新main（開始時HEAD `22e3d176`）・
  AGENTS.md・knowledge README末尾bullet・直近log・実験dir一覧を確認した。
- 現在進行中の単一オーナー宣言: 36-root depth-10掃引（2026-11-20宣言・実験dirは準備ファイルのみで
  実行中）、knowledge corpus class E/F/D修復（10:10Z宣言 `c035d99a`・part 2/5出版中）、
  four-row q5 m23 class-split（09:36Z）、s11 min-maximal decision（07:22Z）。
  いずれも着手不可。
- worker partition candidate（`f7466198`出版済み・宣言不要の探索的測定）が
  「10-stone class-to-root membershipの正確な再生成はtime out」
  「per-worker class-copy計数は主張しない」を明示的に残しており、この測定ギャップは
  未着手かつ、掃引オーナーレーンと一次素材が完全に独立（K1075正本・出版census・candidate JSON
  すべて出版済み）であることから本レーンの対象とした。
- 単一オーナー宣言 `93efcb7f`（10:20Z・宣言時HEAD `4940df5b`）を出版してから着手した。

## 実施内容

1. K1075正本のpin取得とSHA-256（`49b6f85f…`）・git blob（`45744d82…`）両照合。
2. 実験script `scripts/exact_membership_regen_20261121.mjs` を作成。出版census検証器
   （`audit_36_root_three_ply_frontier_20261120.mjs`・sha `7177a25a…`）の
   BitMask全数・D4正準形・BigInt行列式・root四点組安全性を正則に再現し、
   10石クラスhexをroot単位でchunk出力（regen段階）し、assemble段階で
   20 gate・正確統計・出力書き込みを行う2段構成。
3. 全36 root再生: point checks 16,007,211・一意三点組 132,291・root四点組 1,260が
   出版censusの全数と同一。**逐次1プロセスで約3.5秒**（partition candidateレーンの
   「time out」は再現しなかった。同レーンの試行方法に固有の制約だった可能性が高いが、
   他環境の事情は本logからは確定できないため観察として記録する）。
4. assemble: 20/20 gate PASS。主要内容:
   - 多重所属hist {1: 722,945, 2: 5,420, 3: 5}・membership 5,430・全728,370類（出版値同一）。
   - **pairwise 221組がshared数・worker割当・並び順まで出版正本と全件同一**。
   - per-root計数36件全件が出版census per_rootと同一。
   - baseline/candidate両配分のcross/within pairwiseがcandidate JSON出版値と一致
     （4,193/1,242・2,000/3,435）・d4 per-worker負荷も一致。
   - 3-root共有5類を初めて特定（README表参照・0-based witness_full index）。
   - クラスレベル正確統計: baseline worker内冗長1,241/横断4,189に対し
     candidate worker内冗長3,432/横断1,998（横断−52.32%・保存則1,241+4,189=3,432+1,998=5,430）。
   - 9石層（新規）: 56,464一意類・133多重・baseline 29/104・candidate 84/49。
   - 8石層（新規）: 2,251類・root間共有は完全に0。
5. 決定性: 別cwd・別プロセス（/tmp配下copytree）でのregen+assemble 20/20 gate PASS・
   4出力物すべてbyte-identical。
6. part1 `432db238`（実験dir 6ファイル・読みは全てtool file_system paging連結による
   機械経由でpush・fetch-back 6/6 byte一致）。

## 実装上の透明な失敗記録（出版前に対処）

- (a) 所有ビットマスクをJS numberで実装した最初の版で、bitwise演算のint32打ち切りにより
  index 32..35のrootの所属ビットが失われ、多重所属hist {2:5,337,3:4}・membership 5,345と
  出版値{2:5,420,3:5}・5,430から乖離。BigIntビットマスクに置換して解消（乖離85は
  上位4 rootの消失分）。この乖離自体がfail-closed gate（hist照合）で捕捉され、
  出版には至っていない。
- (b) baseline配分を関数 `(i => % 4)` で渡した際、統計関数が配列添字参照を行っていたため
  `undefined` workerに集計が落ちた。配列渡しに統一。
- (c) per-root要約にworker欄の取りこぼしがありwstats照合が落ちた。欄を追加。
- (d) 出力JSONのスリム化（重複するmulti_root_classes列の分離）時に分離先書き込みを
  `result.stone10.multi_root_classes`参照のまま残し、一時的に当該出力が`null`になったのを
  再生成で修正。最終版は`multi10`から直接ソートして書き込む。

いずれも最終出版物には含まれず、最終版の20 gateと2環境byte一致が本証拠である。

## 出版物

- part0 宣言: `93efcb7f`（fetch-back byte一致）
- part1 実験dir: `432db238`（README・script・output 4 JSON・fetch-back 6/6 byte一致）
- part2 本log・part3 `n11-search-methods/README.md` 参照行1行追加。

## 解釈とレジューム

- クラスの幾何共有は表命中率ではない。candidateの横断コピー削減（−52.32%）と
  worker内冗長増大（×2.77）は同じ証拠の両面であり、worker内共表（local TT共有）の実測が
  ない段階ではどちらの面が支配的か判定できない。したがって分割変更の提案は行わない。
- 9石層・8石層の同種統計は本測定が初出版（8石層の共有完全ゼロは、fresh witness rootが
  1手先で全く重ならないことを含む観察）。
- 次回レジューム: (a) 36-root depth-10掃引の完了後、掃引オーナーが
  実測TT hit/表再利用計数を出版した時点で、本測定のクラスレベル統計とのすり合わせ
  （pairwise proxy・クラス計数・実測hitの3層対照）が高価値。(b) 本測定は決定的・3.5秒で
  再現可能なため、36 rootの増分（掃引結果で新鮮さが失われたrootの除外・追加）が生じた
  場合も同一scriptで即時に再計算できる。(c) multi-root-class表はworker割当subproblemの
  厳密化（2-root共有5,420類のworker並列割当など）に直接使える正確な枝刈り材料である。
- 行は1行も閉じない。nodes数・coverage数・クラス計数を勝敗として読まない。
  REFUTED-D10はLOSS証明ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**
