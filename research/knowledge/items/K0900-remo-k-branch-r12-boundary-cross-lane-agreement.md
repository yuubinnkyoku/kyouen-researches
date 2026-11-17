---
id: K0900
title: K0898 r=12境界のcross-lane独立再実行一致検証 — 別レーンの独立スイープがK0898出版packed記録とbyte一致（sha256 0835a06f…）・センサス98/583/34・34キー境界・分割表・max_states 666,030・STASIS4 0/0/0をcommit状態から独立再導出・STASIS系列committed監査の再現性欠陥を固定（K0895/K0897/K0898の監査はformat:"full"だがrepoはpackedのみcommitでfresh checkoutからbyte再現不能・差分は常に2箇所のformatラベルのみ・all_okは全てtrue・K0893 r=9は対照としてbyte再現可能・workflow audit step K0895/K0897/K0898は現状fresh checkoutで必須失敗・修正recipe提示）
kind: verification
status: verified
topics: [variants, maximal-safe, strategy-length, multiplayer]
aliases: [cross-lane agreement check r=12 boundary, STASIS series audit reproducibility scan]
relations:
- type: supports
  target: K0898
  note: 並走レーンが同出版を見る前に開始した独立r=12 cap≤10スイープ（committed JS engine・別プロセスツリー・15,863プロファイル・予算スキップ0）のpacked記録がK0898出版packed記録とbyte一致（出版ピン0835a06f…と同一sha256）。独立記録を本項の実験dirにcommitし検証器がbyte一致・センサス・分割表・max_states・STASIS4（K0897 r=11 packedとのdet/生存者/第1敗者0/0/0）をcommit状態から機械検証。full記録はサイズ制限でcommitせず、ローカルではK0898検証器の.gz経路でcommitted監査（249ec902…）のbyte再生成も確認
- type: supports
  target: K0897
  note: committed監査再現性スキャンの対象。r=11監査はformat:"full"を記録するがrepoにはpackedのみcommitされており、fresh checkoutでの再生成監査はformat:"packed"となってbyte比較がFATAL（run()はlive check前に終了）。差分は2箇所のformatラベルのみで再生成監査のall_ok=true（機械チェック全合格）。修正は所管レーンが実施
- type: supports
  target: K0895
  note: 同じ再現性欠陥を確定（r=10）。差分はformatラベルのみ・all_ok=true
- type: supports
  target: K0893
  note: 対照（control）。r=9監査は最初からformat:"packed"を記録しており、fresh checkoutからcommitted監査（f407faee…）をbyte同一に再現できる。K0895/K0897/K0898の出版手順との違いは、K0893はpack後に監査を再生成してcommitした点
artifacts:
- path: research/experiments/remo-k-branch-cap10-r12-boundary-independent-check-20261117/check_k0898_cross_lane_agreement.py
  role: verifier
  note: 自己完結・決定的・stdlibのみ・ネットワークなし・JS実行なし。7機械チェック（C1独立packed完全性・C2出版packedとのbyte一致・C3センサス/34キー/分割表/max_states再導出・C4 STASIS4 0/0/0・C5 4実験のcommitted監査再現性スキャン・C6 format欠陥の深比較固定・C7 K0893対照ピン）全合格・2回実行で監査JSON byte同一。K0898/K0897/K0895/K0893検証器をimportlibで読み定義とassemble_auditのみ使用
- path: research/experiments/remo-k-branch-cap10-r12-boundary-independent-check-20261117/report.md
  role: proof
  note: 独立再実行の経緯と手順・byte一致の意味論・監査再現性欠陥の原因分析（full形式が出版元ローカルに残った状態で監査生成）・workflow audit stepへの影響・修正recipe（.gz commitまたは監査再生成とピン更新）・限界
- path: research/experiments/remo-k-branch-cap10-r12-boundary-independent-check-20261117/output/js_cap10_r12.independent.packed.jsonl
  role: data
  note: 独立実行のr=12 cap≤10完全スイープpacked記録15,863レコード・326,021 bytes。K0898出版packed記録とbyte同一（sha256 0835a06fe3a2cc812b5434ef0d56146f72b2b019b144ed62544d437472c05274）
- path: research/experiments/remo-k-branch-cap10-r12-boundary-independent-check-20261117/output/check_k0898_cross_lane_agreement_audit.json
  role: data
  note: 検証器監査JSON（2回実行byte同一・committed fileとのbyte照合をrun()が実施）
scope: 'K0898が確定した有限パラメータ領域（3枝合成族・枝サイズ≤10・15,863正規形プロファイル・715キー・r=12）について、(1)並走レーンによる同領域の独立した完全スイープ実行がK0898出版packed記録とbyte単位で一致すること、ならびにその記録から決定性センサス（一様決定98・一様非決定583・mixed 34）・34キー境界集合・per-key分割表・max_states 666,030・K0897 r=11 packed記録とのdetermined/生存者mask/第1敗者mask 0/0/0差分（STASIS4）がcommit状態から再導出されて出版値と一致すること、(2)K0893/K0895/K0897/K0898の4実験ディレクトリについて、committed監査JSONがcommitされたrepo状態（packed記録のみ・full形式・.gzなし）からbyte再現可能か否かを機械判定した結果（K0893は再現可能・K0895/K0897/K0898はformatフィールド2箇所のみの差で再現不能・両バージョンとも機械チェックall_ok）と、その出版手順上の原因・workflow audit stepへの影響・修正recipeの提示。r=9/10/11の再スイープ、監査欠陥の修正実施自体、枝サイズ11,12×r=9..12、r≥13、順位決定性、一般則の全称昇格は含まない'
evidence: '検証器check_k0898_cross_lane_agreement.pyの7機械チェック全合格（2回実行で監査JSON byte同一）。C2: 独立実行packed記録（本項実験dirにcommit・15,863レコード）とK0898 committed packed記録の全文byte比較で一致・sha256は出版ピン0835a06f…と同一。C3: 独立記録+正準列挙から(sizes,gamma)キー分類を再導出し715/98/583/34・34キー境界集合・per-key分割表・max_states 666,030がK0898出版値と完全一致。C4: K0897 committed r=11 packed記録とのdeterminedフラグ・生存者mask・第1敗者mask差分が0/0/0。C5/C6: 4実験のcommitted監査を新規checkout状態（packedのみ）から再生成し、K0893はbyte一致（f407faee…対照ピン）・K0895/K0897/K0898は再生成監査がcommitted監査とformatフィールド2箇所（"full"→"packed"）を除き深比較で完全一致し両all_ok=true・検証器run()のbyte比較はFATALでlive check前に終了することを固定。独立実行のfull記録はGitHub pushトランスポートのサイズ制限のためcommitしないが、ローカルではK0898検証器の.gz経路でcommitted監査（249ec902…）がbyte再生成されることを確認済み（report.md）。本項は検証記録であり新たな数学的主張をしない'
---

# K0898 r=12境界のcross-lane独立再実行一致検証

## 命題・範囲

K0898出版（別レーン・2026-11-17 03:59-04:01Z着地）と、同出版を
見る前に本レーンが独立開始していた同一のr=12 cap≤10スイープの
**cross-lane一致検証**、およびSTASIS系列4実験のcommitted監査
再現性スキャン。

- **独立再実行のbyte一致**: 独立実行（committed JS engine・CLI r=12・
  別プロセスツリー・15,863プロファイル・予算スキップ0）のpacked
  記録は、K0898出版packed記録と**byte単位で完全一致**
  （sha256 0835a06f…・出版ピンと同一）。独立記録を本項の実験dirに
  commitし、検証器がcommit状態から両者のbyte一致を機械検証する。
  独立した2実行が同一bytesを生成したことは、このデータの決定性の
  最も強い形のcross-lane確認である。
- **出版値の独立再導出**: 独立記録から決定性センサス
  （715キー・一様決定98・一様非決定583・mixed 34）・34キー境界
  （7族）・per-key分割表・max_states 666,030がK0898出版値と完全
  一致。K0897 r=11 packed記録とのdetフラグ/生存者mask/第1敗者mask
  差分は0/0/0でSTASIS4（全ラベル不動点）を独立側から確認。
- **監査再現性欠陥の固定（本項の新発見）**: K0895/K0897/K0898の
  committed監査JSONは`"format": "full"`を記録するが、repoには
  packed記録のみがcommitされている。出版元環境ではfull形式記録が
  残った状態で監査生成・2回実行byte同一を確認したためitemの
  evidence主張は出版元では真だが、**fresh checkoutでは再生成監査が
  format:"packed"となりbyte比較がFATALで失敗し、live checksは一度も
  走らない**。差分は常に監査JSONの2箇所のformatラベルのみで、再生成
  監査の機械チェックは3実験とも全合格（all_ok=true）。K0893はpack後
  に監査を再生成してからcommitしたため`"format": "packed"`を記録し、
  fresh checkoutからbyte再現可能（対照）。影響:
  workflow（refresh-knowledge-generated.yml）のK0895/K0897/K0898
  audit stepは現状fresh checkoutで必ず失敗する。修正recipe:
  (a) full形式記録を`output/js_cap10_rN.jsonl.gz`としてcommit
  （load_jsonlは.gzを優先するためformat:"full"監査が再現可能に
  なる・workflow stepも通過）または (b) packed状態で監査を再生成
  してcommitし直しitemのpinned sha256を更新。本項の検証器は
  修正後の状態（byte_identical）でも欠陥状態
  （format_only_difference）でも通り、観測状態を監査JSONに記録する。
  修正自体は所管レーンのitemとピンを変更するため本項では実施しない。

## 限界

- 独立再実行はr=12・cap≤10に限る（r=9/10/11の再スイープは不要・
  各出版の検証器が既に検証済み）。
- 独立実行full記録のsha256_uncompressed再現確認はローカル観察
  （full記録がcommitされていないためcommit状態からは再検証不能。
  修正(a)が取られれば恒常的に再検証可能）。
- 監査再現性欠陥の修正実施、枝サイズ11,12×r=9..12、r≥13、順位
  決定性、「r≥9で境界が定常」という全称主張は本項でも未解決。

## 再現

`check_k0898_cross_lane_agreement.py`（自己完結・決定的・Python 3.11+
stdlibのみ・ネットワークなし・JS実行なし・7機械チェック全合格・
2回実行で監査JSON byte同一）。K0898/K0897/K0895/K0893の4検証器
モジュールをimportlibで読む（定義とassemble_auditのみ・live checks
はworkflow audit stepが所管）。監査JSONはoutput/
check_k0898_cross_lane_agreement_audit.json。
