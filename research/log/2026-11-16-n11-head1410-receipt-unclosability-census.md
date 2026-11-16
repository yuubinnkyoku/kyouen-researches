# 2026-11-16 n11 head-1410 receipt-unclosability census

- 長期レーン（自動実行）。list_commits 確認時点の main HEAD: 855bf0dbf0cfc1eb78584739c4cb3349c77ff89"。
- head-1410 の 174 open S5 すべてについて STERILE 被覆を D4 orbit レベルで集計。3 parent が receipt-unclosable（残行すべて STERILE）、57 partial、effRem 計 12183（残 12274 のうち 91 が STERILE 参照）。
- S5↔S6 行の親子関係は D4 orbit レベル（∃σ∈D4: σ(P) ⊂ R）。raw hex subset join では 65k/74h 行の class-1 demand が出版値と不一致になるため orbit join が正しいと特定。60c fold の 6 ペアで全数検証（CC pass）。
- 70j cover precheck: cover bits {21,109} が出版 62b claim v2 と一致（合法手 bit 集合・両 cover root hex も一致する独立再導出）。両 bit とも REFUTED-D10。62b 行の census-derived demand {c1:1,c2:1,c4:0} も claim と完全一致。
- cost-62b は本 census の実行前に速いレーンで完了済み（STERILE、62/62 REFUTED-D10）だったため、census は 62b を既知の STERILE 行として扱う。65k/74h の claim はまだ出版されていない（fetch 確認）。
- 実行環境の制約により、census 計算（fetch + 集計 + sha256 pin 付き digest）と出版（成果物構築 + push）を2つの sandbox 実行に分割した。単一実行での一括処理は記録バイト数上限（16 MiB）で push 段階に到達できなかった。また github_app の get_file_contents 応答には本文以外の短い text エントリが混入することがあり、最長候補 + 形式検証で本文のみを採用した。
- bash 不通（artifact 容量超過）のため python 再現は未実施。census/precheck JSON はサンドボックス内 JavaScript で生成し、入力は sha256 で pin。
- 11×11 は UNKNOWN のまま。
