# 残余23行 代替9根掃引再実行第二検証（K1149）pristine 再実行による第三検証（2026-11-20）

## 概要

[K1149](../../knowledge/items/K1149-n11-residual72-replace9-sweep-reexec-second-verification.md)（K1146代替9根depth-10掃引の全18 probe再実行による独立第二検証・出版 commit `7ab77aa1`・検証機 SHA-256 `77cdd9e3…` 41,175 bytes・監査正本 `27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072` 11,242 bytes・24/24 gate・item側の二重採番〔six-row K1149〕には関与しない）の出版byte一式を再取得し、**18 probeの両パス（pass A・pass B）を第三者環境で新規に再実行する**第三検証を行った。K1153/K1155/K1157が「出版記録機の再実行」だったのに対し、本検証は出版されたDFPN probe事実そのもの（pinned runner v17によるdepth-10探索）を36 probe分（9根×両AND順序×2パス）最初から再計算する、この系譜で最も重い第三検証である。

単一オーナー宣言ノート: [`宣言ノート`](../../log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification-single-owner-note.md)（先着出版 commit `c3c4dd28b48ccf4f5782ddb9f1a81e46d24e4787`・2026-11-20T16:01:30Z 宣言時刻）。

## 対象（出版pin・fetch commit 87f56932 で取得し一致確認）

| ファイル | SHA-256 / pin | bytes |
| --- | --- | --- |
| 検証機 `verify_replace9_reexec_20261120.py` | `77cdd9e3450aed9d2c900475f15d9e09367985b909027c50e485995737252db4` | 41,175 |
| runner v17固定コピー `runner_v17.ts`（git blob） | `c132cc6425eee3feaeef1d697dd74f968cfedb59` | 12,481 |
| 出版掃引機 `replace9_d10_sweep_20261120.py` | `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41` | 33,969 |
| 出版掃引正本 `replace9-d10-sweep-20261120.json`（K1146 volume） | `e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e` | 15,403 |
| 出版probe-records `probe-records-replace9.jsonl` | `bdacf0e7056093145bef917ad384220b70c06be68bdd892b56dd23b3a7d4cb06` | 10,567 |
| 上流6正本 K1085/K1086/K1089/K1091/K1095/K1097 | `5fdd342d…`/`3045e152…`/`808fbda1…`/`edd7ac84…`/`335eca5e…`/`2896deb0…` | 39,221/21,835/17,511/17,963/16,605/43,540 |
| 出版監査正本 `replace9-sweep-reexec-second-verification-20261120.json` | `27fc420c…` | 11,242 |

出版側の入力配置（K1149実験dir・`n11-residual72-replace9-d10-sweep-20261120/`・上流各掃引dir・`n11-residual72-safe8-refuted50-refsolve-20261120/`・`n11-residual72-unsafe-classification-add2stones-20261120/`）からraw CDN（pinned commit）で取得した。本実験dir自体がstaging rootを兼ねる（下記レイアウト検証後、そのまま `--root .` で再実行可能）。

## 検証機（harness）

- `scripts/verify_k1149_reexec_third_20261120.py`（SHA-256 `ec55f78a2a109a60d295569aa856a9c01764859c64655ed6aae405d678234979`・18,525 bytes）
- `scripts/audit_k1149_machine_pin_gap_20261121.py`（SHA-256 `947e989bfb49af8b3ae8ecd280a7fa52e5b75343544048e4732abb3cc23a9ecd`・stdlibのみ・8/8 gate）
- `output/k1149-machine-pin-gap-audit-20261121.json`（SHA-256 `b491e45092befcd490633cfa0e822c7063ef04eea14e078307221be84b9c38a6`・3,524 bytes）
- Python stdlib＋Node.js runner。乱数・時刻・wall時間を監査JSONに含まない（出版記録の決定性字段 nodes/loss/capped/terminalStoneRange のみ）。fail-closed。
- 手順: pin gate 13点 → pass A新規再実行（本tree・4 workers・budget 240s）→ pass B新規再実行（隔離tree/cwd/HOME・入力複写）→ 出版掃引機を隔離treeでpristine再assemble → 検証機assemble（fresh両パス＋pristine volume入力）→ assembleを `PYTHONHASHSEED=random` で再実行 → tamper gate。出力はsorted keys・時刻なし。

## 手順と結果（全gate PASS・harness 3実行byte一致）

1. **pin gate（13/13 PASS）**: 検証機・runner git blob・出版掃引機・出版監査・出版volume・出版records・上流6正本を第三検証harness自身が独立SHA pinで照合。K1149検証機内部のfail-closed pinは上流6正本・runner・records・volumeを検査するが、K1146掃引機本体のSHAは検査していない（追加監査参照）。
2. **pass A（本tree・18 probes・12.8s）**: 18/18 probe完走・nodes総計 **3,574,172 == 出版値**・`00000000010000809002000040002001` が両AND順序で loss=true（nodes 608,293/691,784）・他8根16 probe は loss=false・capped/timeout/error 0。
3. **pass B（隔離tree/cwd/HOME・入力複写・18 probes・約12.9s）**: pass Aと同一の決定性字段が18/18で成立・nodes総計一致。
4. **pristine再assemble**: 出版掃引機を隔離treeで出版probe-recordsに入力して再実行し、出力SHA-256 `e8f5d674…` が出版掃引正本とbyte-identical。
5. **assemble**: fresh passA/passB/pristine volumeから検証機assembleを実行し、出力が出版監査 `27fc420c…` と**byte-identical（24/24 gate PASS）**。さらに `PYTHONHASHSEED=random` でのassemble再実行もbyte-identical。
6. **tamper gate（PASS）**: 複写treeで `input/k1097.json` のoffset 500 の1 byte をXOR 0x01で改変（改変後 SHA-256 `7cc71c5f…`）→ run modeは returncode 1・probe records未書込でfail-closed終了。
7. **harness自身の決定性**: 監査正本 `output/reexec-third-verification-audit-20261120.json`（SHA-256 `7e0824cc11c997882d6b01f528b0ac53205de3ce95891c901bf9da6eb29b7e43`・7,700 bytes）は同一cwd 2回＋隔離cwd/隔離HOME 1回の3実行でbyte-identical。harness全体の実行は1回あたり約25.4秒。

## 追加監査: K1149検証機の掃引機source pin

K1149第二検証機 `verify_replace9_reexec_20261120.py` の `SWEEP_MACHINE_SHA256` 定数をASTで調べると、値は **63文字**（`d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e595b7d2512bcd41`）であり、SHA-256の64桁ではない。さらに、この定数の読み出しは監査JSONの入力metadata（line 886）のみで、`gate(...)` への参照は0件だった。出版監査の `inputs.k1146_sweep_machine_sha256` にも同じ63文字が記録されている。

K1149の `pristine-reassemble-volume-byte-identical` gate は、再assemble後の出力SHAと出版volume SHAを比較するだけで、掃引機ソース自体のSHAを検査しない。したがってK1149の24/24 gateはprobe記録・再assemble結果の整合を示すが、掃引機ソースの出所までは単独で保証しない。なお、`SWEEP_RECORDS_SHA256` は検証機内で実際に照合されており、今回の欠落は掃引機本体のpinに限られる。

K1159第三検証harnessは、K1146公開commit `e9ea153bc469aa551689a5d275773553852f3342` の掃引機本体を独立に **64文字の正しいSHA-256 `d163b2a120ac46abee40d0b9a32269bce14a73901a85a80e5925b7d2512bcd41`** でpinし、さらにその機械をpristine treeで実行して出版volumeとbyte一致させた。これにより、第二検証機に残っていたソースpinの穴は第三検証層で補われている。K1149のprobe結果そのものを無効にする発見ではない。

追加監査機 `scripts/audit_k1149_machine_pin_gap_20261121.py`（8/8 gate）と正本 `output/k1149-machine-pin-gap-audit-20261121.json`（SHA-256 `b491e45092befcd490633cfa0e822c7063ef04eea14e078307221be84b9c38a6`・3,524 bytes）は、同一tree 2回＋隔離tree 1回でbyte-identical。

## 再現

```bash
# 本dirがstaging rootを兼ねる（scripts/に検証機とharness・input/に8入力・sweep/に掃引機tree・published-audit.json）。
cd <このdir>
python3 scripts/verify_k1149_reexec_third_20261120.py --root . --output output/reexec-third-verification-audit-20261120.json
# 上記監査正本とbyte一致するはず。要 Node.js (v22.x, --experimental-strip-types)。
python3 scripts/audit_k1149_machine_pin_gap_20261121.py --root . --output output/k1149-machine-pin-gap-audit-20261121.json
# pin表とSHA-256照合後の初回はraw CDN (pinned commit 87f56932…) からの再取得でも同じ。
```

## 解釈規約

loss=true（uncapped）はdepth-10内必敗のprobe事実の再現であり、証明書抽出の資格を本検証は与えない（抽出は宣言 `63877ffd2e` の別レーン）。loss=false（uncapped）はREFUTED-D10 probe事実の再現でありLOSS証明ではない。nodes数・solved数を勝敗として読まない。本検証は行を1行も閉じない。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。** 残余20行（pool P⁗ 120,416根・refsolve第5ラウンド宣言 `ace38772d9` 待ち）は本検証の後も全行open。

## 関連

- item: [`K1159`](../../knowledge/items/K1159-n11-residual72-replace9-sweep-reexec-third-verification.md)
- 研究ログ: [`研究ログ`](../../log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification.md)
- 単一オーナー宣言: [`宣言ノート`](../../log/2026-11-20-n11-residual72-replace9-sweep-reexec-third-verification-single-owner-note.md)
- 検証対象: [K1149 再実行第二検証実験](../n11-residual72-replace9-sweep-reexec-second-verification-20261120/README.md)
- 同系譜第三検証: [K1153](../n11-residual23-zero-triple-provider-reexec-third-verification-20261120/README.md)・[K1155](../n11-residual72-replace9-whole-record-reexec-third-verification-20261120/README.md)・[K1157](../n11-residual23-direct-fourth-geometry-reexec-third-verification-20261120/README.md)
