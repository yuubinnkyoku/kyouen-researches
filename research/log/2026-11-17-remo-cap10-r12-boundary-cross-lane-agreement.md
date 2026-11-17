# 2026-11-17 REMO cap≤10 r=12境界のcross-lane独立再実行一致検証とSTASIS系列監査再現性スキャン（K0900）

本レーンはK0897の次列として定理I r=12境界（cap≤10・15,863
プロファイル・r=12）のスイープを自律開始したが、実行中に並走
レーンが同成果をK0898として出版した（746b17d9/24f1f873/0f4639c9/
d7bfeee9/41544af1・2026-11-17 03:59-04:01Z）。数学的内容の重複
出版を避け、進行中の独立実行をK0898出版のcross-lane独立検証に
転用した。この判断はrepoの並行作業規約（AGENTS.md・同一成果の
重複回避・独立した実験として追加）に沿う。

## 成果

- **独立再実行のbyte一致**: committed JS engine（K0893修正版の
  byte同一コピー・CLI引数r=12）を別プロセスツリーで15,863
  プロファイル全域に実行（予算スキップ0）。独立実行のfull記録を
  決定的packerでpacked化した結果はK0898出版packed記録とbyte
  単位で完全一致（326,021 bytes・sha256 0835a06f…・出版ピン
  と同一）。独立記録を実験dirにcommitし、検証器がbyte一致を
  commit状態から機械検証する。プロファイル入力は検証器内蔵の
  正準列挙から再生成（先頭・末尾・件数一致を確認）。
- **出版値の独立再導出**: 独立記録から決定性センサス
  （715キー・98/583/34）・34キー境界（7族）・per-key分割表・
  max_states 666,030がK0898出版値と完全一致。K0897出版r=11
  packed記録とのdetフラグ/生存者mask/第1敗者mask差分は0/0/0
  （STASIS4全ラベル不動点を独立側から確認）。
- **full記録経由の監査再現（ローカル観察）**: 独立実行のfull記録を
  .gzとしてK0898検証器のload経路に与えると、committed監査JSON
  （sha256 249ec902…）がbyte再生成された。独立full記録は出版元の
  元記録と全監査値レベルで等価。full記録はpushトランスポートの
  サイズ制限でcommitしない。
- **STASIS系列監査再現性欠陥の発見と固定（新発見）**: K0895/K0897/
  K0898のcommitted監査JSONは`"format": "full"`を記録するが、
  3実験のoutput/にはpacked記録のみがcommitされている。fresh
  checkoutではload_jsonlがpacked経路しか選べないため再生成監査は
  `"format": "packed"`となり、検証器run()のcommitted監査byte比較
  がFATALで失敗してlive checksは一度も走らない。差分は常に監査JSON
  2箇所のformatラベルのみで、再生成監査の機械チェックは3実験と
  も全合格（all_ok=true）。K0893（r=9）はpack後に監査を再生成して
  commitしたため`"format": "packed"`を記録しておりbyte再現可能
  （対照）。影響: workflow（refresh-knowledge-generated.yml）の
  K0895/K0897/K0898 audit stepはfresh checkoutで必ず失敗する。
  修正recipe: (a) full形式記録を`output/js_cap10_rN.jsonl.gz`として
  commit（load_jsonlは.gzを優先・format:"full"監査が再現可能になり
  workflow stepも通過）または (b) packed状態で監査を再生成して
  commitし直しitemのpinned sha256を更新。修正は所管レーンのitemと
  ピンを変更するため本項では実施せずrecipe提示に留める。

## 検証

check_k0898_cross_lane_agreement.py（自己完結・決定的・stdlibのみ・
ネットワークなし・JS実行なし）。7機械チェック（C1独立packed完全性・
C2出版packedとのbyte一致・C3センサス/34キー/分割表/max_statesの
再導出・C4 STASIS4 0/0/0・C5 4実験監査再現性スキャン・C6 format
欠陥の深比較固定・C7 K0893対照ピン）全合格・2回実行で監査JSON byte
同一。K0898/K0897/K0895/K0893の4検証器をimportlibで読む（定義と
assemble_auditのみ・live checksはworkflow audit stepが所管）。
作業メモ: 実行環境の2度のリセットでスイープを失ったため、engineの
start引数による再開ラッパーで完走させた（記録はプロファイルの純
関数でbyte連結可能・K0898検証器docstringと同じ性質）。

## 限界・次の課題

- 独立再実行はr=12・cap≤10に限る。r=9/10/11のpacked記録は各出版の
  検証器が検証済みで再スイープしない。
- 監査再現性欠陥の修正実施は所管レーンに委ねる（recipe提示済み）。
  r=10/r=11のfull記録を持つのは出版元レーンのみである点も理由。
- 枝サイズ11,12×r=9..12（K0881のcap≤12拡張はr=7,8まで）が
  capレーンの次の自然な未走査セル。r≥13列はmax_states増大で要判断
  （剰余計数はr≥13で自明化済み）。
