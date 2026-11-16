# 2026-11-16：汎用独立fold投影ツール出版 — head 1438/1441基盤の再構成assert + 任意のWIN7-D10 receipt root集合の投影head・marginal・5親delta・hist deltasを即時計算（bit-89で`6719f0c6`のagreementと完全一致をテスト確認・D4衝突assert動作確認・65n仮root投影1442で動作実証）

開始時main: `9888e42c`（本レーン直前のcost-65n claim検証出版）。並走レーンのcost-65n sweep（59 bits・IN FLIGHT `7dcd9767`）の完走・fold receipt着地時に**独立投影・一致検証を即座に実行できる状態を事前に整える**のが目的。本ツールはbookkeeping投影のみを行い、engine searchを実行せず、いかなるverdictも作らない。

## ツール内容（`scripts/fold_projection_head1441_tool_20261116.py`・git blob `ac75cb70`・14,797B）

- 使用法: `python3 fold_projection_head1441_tool_20261116.py [--basis 1438|1441] ROOT_HEX [ROOT_HEX ...]`
- 基盤headの独立再構成（761 published receipt roots [+ bit-89 root @1441] + winners 498・verbatim移植frontier semantics）と**6数値assert**（1438/174/6410/507143/4683/371057 または 1441/174/6407/506945/4680/370859）。
- 各rootについて: 7石確認・D4 canon・**folded rootsとのorbit衝突assert**・covers/marginal/marginal_in_manifest・manifest内閉鎖行のhex特定。
- 全root fold後の投影head 6数値・demand histogram deltas・影響親のrows/edge cost before→after・失われた行のhexとedge cost。
- 出力はJSON 1ファイル（basis・root数をファイル名に含む）。

## 動作テスト（3点すべてPASS・テスト産物JSONは出版せず）

1. **bit-89再現テスト**（`--basis 1438 00000000020100003800000008080000`）: 投影head **1441/174/6407/506945/4680/370859**・mim 3（child + `00000000000000801202010000080000` + `00000000020000801002010000080000`）・hist deltas 3バケット各-1・**5 affected parents の rows/edge_cost before→after・lost rows・lost cost が本レーンのfold agreement record（`6719f0c6`・JSON blob `f74df27e`）と全フィールド完全一致**（receiptsフィールドもroot/canon/covers/marginal/mim/marginal_manifest_hexes全一致をassertで確認）。
2. **D4衝突検出テスト**（`--basis 1441` にbit-89 rootを再fold）: 「D4-collides with a folded root」assertで正しく停止 — 二重fold・軌道重複の誤使用を防ぐ。
3. **65n仮root投影テスト**（`--basis 1441 00000000000000801202010000800002`〔cost-65n child + bit 1・65n claimのlegal candidateの1つ・WINであることは全く主張しない**仮**入力〕）: 投影 **1442/174/6406/506880/4679/370794**・mim 1（child `00000000000000801202010000800000` のみ）・hist delta `c2=2,c4=0`: -1・2 affected parents（SH親 `00000000000000003800000008002000` 29→28・第2親 `00000000000000801202010000000000` 48→47）— **cost-65nのWIN receiptが着地したときの投影照合が引数1つで即座に実行できることを実証**。

## 意義

1. 並走のcost-65n sweep完了・fold receipt着地時、**独立投影・一致検証がこのツール1本・数秒で完了する状態**を確立。bit-89で`6719f0c6`の成果とbit-level完全一致しているため、ツール自体の正しさは既出版のagreement recordに対して検証済み。
2. 以後のclass2-lane fold（65n・66帯・…）ごとにagreement scriptを個別に書く必要がなくなり、独立検証の固定コストが大幅に低下。
3. 衝突assert（fold済み軌道への再fold禁止）により、誤ったroot指定を自動検出。

## 解釈境界（重要）

- 本ツールはmanifest被覆の簿記投影のみ。**どのrootの「WIN仮投影」も、そのrootのWIN7-D10証明書が出版・独立検証されて初めて意味を持つ**。テスト3の1442投影はツール動作確認であって、bit 1のWIN主張でもhead 1442の主張でもない。
- REFUTED-D10はLOSS証明ではない。NOT-STERILEは勝敗決着ではない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1/class2/class4は引き続きUNKNOWN**。

## 今後

- 並走のcost-65n claim v2・raw batches・証明書着地時: (1) raw batch独立再パース照合、(2) 本ツールでWIN rootの独立投影、(3) 並走fold receiptとの一致検証、をこの順で実施する。
