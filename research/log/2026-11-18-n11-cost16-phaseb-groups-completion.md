# 2026-11-18 N11 cost-16 parent phase B groups 完了（425/425 pair-type membership・cross-lane恒等式成立・設計log 13値表の(4,29)転記誤り解決）

## 成果

31行 cost-16 parent `00000000000000003800000008001000`（425 pair type・全multiplicity 1）の phase B groups runnerを**完了**した。前回中断時点の394レコード（393 unique + 重複1）から、残り32 type（(4,29)再計算 + 帯(22,*)〜(28,30)）を計算し、**全425 pair-type membership（A/B splitつき）を確定**、canonical aggregate mode 9 checks + 完了検証script 25 checks 全PASS・二重実行byte-identicalで出版する。

- JSONL: `output/cost16-b-groups-20261118.jsonl`（425 records + 26 summary lines）
- aggregate output: `output/cost16-b-phase-groups-20261118.json`
- direct spot check: `output/cost16-b-direct-20261118.jsonl`（d=18, d=2）
- 完了検証: `verify_cost16_phaseb_groups_completion_20261118.py` → `output/cost16-phaseb-groups-completion-verification-20261118.json`（25 checks・二重実行byte-identical・sha256 `cc0b2bdd…`）
- 実行variants: `cost16_phase_b_groups_cap16m_20261118.py`（STATE_CAP 12M→16M単一変更）・`cost16_phase_b_groups_cap16m_pickled_20261118.py`（さらにparent構造をpickleから読む高速化・構造はcheck_structureで検証）

## 主要数値

1. **cross-lane恒等式 sum(b_part)/16 == B16 成立（exact）**: sum(a_part) = 34,586,809,369,409,015,820 = 15 × A16（2,305,787,291,293,934,388）・sum(b_part) = 10,570,608,806,176,751,488 = 16 × B16（660,663,050,386,546,968）・sum(all memberships) == 16 × total（2,966,450,341,680,481,356）。**per-pair-type分解（本run）とper-doubled-row d-slice分解（`9b2747f0`）・Node.js第三実装（`0ce32ace`）の3独立計算経路がB16/A16/totalで完全一致**した。B型総数の二経路一致検証（前回log記載の役割変更）がこれで完結した。
2. **設計log 13値表の照合: 12/13 完全一致、(4,29) b_partは転記誤りと確定**。設計log（`2026-11-18-n11-cost16-phaseb-groups-design.md`）表の (4,29) b_part = 25,742,803,159,389,724 に対し、(i) 前セッションのrollback後再計算record・(ii) 本セッションのfresh-memo独立再計算（G=127・memo 3,524,063状態・35.9秒・第3計算epoch）がともに 25,742,823,159,389,724 を与え、差はちょうど2×10^10。a_part（83,754,150,371,345,030）は全source一致。**恒等式 sum(b_part)==16·B16 が表側の値では成立しない（2×10^10過小）ことも裁定根拠**。設計logの「13値が権威ある出力」のうち(4,29) b_partセルのみ転記誤り。なおgroups進捗log記載の d=2 B_d「23,477,541,507,703,040」も本照合で phaseb-total log の 23,475,415,507,703,040 が正しいことが確定（direct mode再計算でも一致）。
3. **重複(0,8)レコードの決定性確認**: scratch退避JSONLに含まれていた pair (0,8) の同一root 2レコード（rollback前後の別invocation・memo 6,236,224 / 3,524,068）はa_part・b_part完全一致（84,443,033,500,707,374 / 25,797,556,390,267,152）。publication JSONLからは1通りのみ残し、両コピーの同一性は検証script check `dup.removed_08_copy_identical` で記録した。canonical aggregateのduplicate SystemExit対策。
4. **direct mode B_d spot check**: d=18（bottleneck行・276 terms）→ 18,319,351,945,126,110、d=2（hub行・435 terms）→ 23,475,415,507,703,040 がpublished b_slices と完全一致（B_d第三の独立経路）。
5. **全425 pair root membership > 0**（1,483 singleton含む全1,908 root positive）。membership上位は全てpair rootで、**pair最小 87,624,228,102,165,001 / singleton最大 1,798,095,446,108,235 = 48.7倍**（29行runner-upの約49倍と同一のpair独占構造）。
6. **membership分布（構造観察）**: 最大はpair (15,19) root `00000000000000801202020000081000` = 136,382,599,145,473,665 = 全最小coverの**4.5975%**（A成分のみでもA16の4.541%）。上位k本の単純和: top-4 = 17.86% / top-8 = 35.46% / **top-10 = 44.23%** / top-12 = 52.83%。top-50の行出現は**行18（17本）・行19（16本）が2大ハブ**（行18はcover options 64のbottleneck行と整合）。

## 検証

- canonical aggregate mode（`cost16_phase_b_groups_20261118.py`・published）9 checks全PASS・二重実行byte-identical（aggregate JSON sha256 `5a9474d5…` 両回一致・timing欄なし）。
- 完了検証script 25 checks全PASS・二重実行byte-identical（sha256 `cc0b2bdd…`）。入力pin: phase A output blob `fe4b4b55…`・B16 slice output blob `883275fb…` をgit blob SHA-1で照合してから使用。
- 本セッションの33 type新規計算((4,29)+32)は全て**1 type/invocation・fresh memo**（STATE_CAP 16M・実測memo ≈3,524,000状態・RSS ~450MB・30〜40秒/type）で実行し、**invocationごとにJSONLをknowledge scratchへsnapshot**した（環境リセットで作業dir消失が1回発生したが0レコード喪失）。
- pm値のmemo履歴非依存性は3計算epoch横断で実証済み（(0,8)・(4,29)の完全一致・12設計値の完全一致・恒等式）。

## 実験的事実（環境・運用）

- **本環境のcgroupメモリ上限は1,090,519,040 bytes（約1.04GB）**であって3.2GBではない。帯(22,*)の7-type shared-memo実行（GS=425 G=0・budget 170s）は7レコード書き込み完了後、(23,25)の木探索中にRSS ~913MB（memo 8.9M状態）で**cgroup OOM-kill**（exit 137）。以降は1 type/invocationで回避（全レコード無事）。
- bash 1コマンド300秒超で実行環境ごとリセットされ作業dirが消える（12-invocation連結loopで発生・loop後のcp未実行で12レコード喪失・値は決定的なので再計算で完全復旧）。**snapshotはloopの中で各invocation後に置く**のが正解（本logの通り最終的に実施）。
- uv check/build・unittestは本環境にrepo cloneとuvがなく未実施（歴代n11項目と同じ扱い・本runはknowledge item構造への変更なし・log/experiment/output追加のみ）。

## 次課題

1. **top-10 joint membership**（上位pair root 45組み合わせ・fresh-memo pm(V∖4行)各~40秒・計~30分）: 上位10本の単純和44.23%に対する真のkill（包含排除）の確定。
2. **ban生存曲線**（31行版・k点ごとにA位相40秒+31 d-slice ~19分/k点）: 29行版（`95b11316`）と同じ手法。
3. direct mode残29行（d≠18,2）のB_d独立再計算（各~40秒・published b_slices全行照合）。
4. membership上位rootの実際のverdict評価は並走sweep-lane管轄のまま。

## 解釈上の注意

membershipは代替最小cover計画の組合せ数であり探索コストでもverdictでもない。REFUTED-D10・STERILEはLOSS証明ではない。

## 11×11 状態

標準11×11空盤は **UNKNOWN**。二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4 もすべて **UNKNOWN**。
