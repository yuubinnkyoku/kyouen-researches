# 残余72行 replace9 whole-record第二検証（K1151）pristine 再実行による第三検証（2026-11-20）

## 概要

[K1151](../../knowledge/items/K1151-n11-residual72-replace9-whole-record-second-verification.md)（K1146代替9根depth-10掃引のwhole-record独立第二検証・出版 commit `f7aa541f342d67b33f34fee2df5e31c262cb0691`・2026-11-20T14:41:19Z・本レーン出版）の実験一式（検証機・10入力snapshot・監査正本）をbyte単位で再取得し、pristine再実行による第三検証を行った。出版社が本レーン自身であるため、本検証の意味は「出版byteをGitHubから再取得するだけで、監査正本がpin＋入力のみから新規に再生成できること」（輸送・転写・ローカル記憶を介さない独立検証可能性）の確定にある。

単一オーナー宣言ノート: [`宣言ノート`](../../log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md)（先着出版 commit `f3097440c0ca5021018c0f4fdbb55cb2fb2fee09`・2026-11-20T15:06:08Z 宣言時刻）。

## 対象（出版pin・commit f7aa541f で取得し一致確認）

出版実験dir: `research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120/`（13ファイル）

| ファイル | SHA-256 | bytes |
| --- | --- | --- |
| 検証機 `verify_replace9_whole_record_20261120.py` | `e92fb7556a6f12c6e3cee06477e5387ddb6214cb58875e4ee3385010f9043e8a` | — |
| 監査正本 `replace9-whole-record-second-verification-20261120.json` | `5888afb3e1c07f8555fbafc73fc0b9d1006b0a31c88bbdd55a0d8975c0cabcb4` | 115,002 |
| 10入力snapshot `output/.input-*.json(l)` | 検証機内部のfail-closed pin（K1085/K1086/K1089/K1091/K1095/K1097/cover-decision/probe-records/replace9/K1147外部監査） | — |

## 検証機（harness）

- `scripts/verify_k1151_reexec_third_20261120.py`（SHA-256 `cf1ae8ba390faf74fe149015777e46f8502a7fa23c9db35b17c7a3a1ff161f70`・11,144 bytes）
- Python stdlib のみ。乱数・時刻・環境依存出力なし（監査JSONはsorted keys・実行時間を含まない）。fail-closed。
- 引数: `--root`（machine.py と10入力snapshot・published-audit.json を含むstaging root）、`--output`（監査JSON出力先）。

## 手順と結果

1. **pin gate（2/2 PASS + 入力10件stage）**: 検証機・出版監査のSHA-256 pin一致。10入力snapshotは出版commitのraw CDNから取得（検証機内部pinが全入力をfail-closed照合）。
2. **pristine再実行（4/4 byte一致・新規生成）**: 各実行前に監査ファイルをtreeから削除した上で（正本の既存bytesに依存しない新規生成）、
   - 同一cwd 2回（ambient・PYTHONHASHSEED unset）
   - 隔離tree複写+隔離cwd+隔離HOME 1回
   - 隔離+PYTHONHASHSEED=random 1回
   全4実行で returncode 0・334 gate all_pass=True・出力 SHA-256 `5888afb3…`（115,002 bytes）で出版監査とbyte-identical。1実行あたり0.2秒未満。
3. **tamper gate（PASS）**: 複写treeで入力 `.input-replace9.json` のoffset 7701 の1 byte をXOR 0x01で改変（改変後 SHA-256 `74e25aa4…`）→ returncode 1・出力未書込でfail-closed終了。
4. **harness自身の決定性（3実行 byte一致）**: 同一cwd 2回＋隔離cwd 1回で監査JSON（本正本）byte一致。監査正本: `output/reexec-third-verification-audit-20261120.json`（SHA-256 `6e06f12ad311ef1bc568dc775a39b6edb72e43f7696fab874b2755d5c3f0986a`・5,024 bytes・pin gate 2/2・10入力sha記録・run gate 4/4・tamper gate PASS・interpretation_guard 5文言同梱）。

## 再現

```bash
S=f7aa541f342d67b33f34fee2df5e31c262cb0691
D="research/experiments/n11-residual72-replace9-whole-record-second-verification-20261120"
B="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/$S/$D"
mkdir -p root/scripts root/output
curl -sS "$B/scripts/verify_replace9_whole_record_20261120.py" -o root/scripts/verify_replace9_whole_record_20261120.py
curl -sS "$B/output/replace9-whole-record-second-verification-20261120.json" -o root/published-audit.json
for f in k1085 k1086 k1089 k1091 k1095 k1097 cover-decision k1147-external-audit probe-records-replace9; do
  curl -sS "$B/output/.input-$f.json" -o "root/output/.input-$f.json"
done
curl -sS "$B/output/.input-probe-records-replace9.jsonl" -o root/output/.input-probe-records-replace9.jsonl
# 上のpin表とSHA照合後:
python3 verify_k1155_reexec_third_20261120.py --root root --output audit.json
# 本正本と byte 一致するはず
```

注: harnessの再現snは本実験dirのscripts/から取得（ファイル名は `verify_k1151_reexec_third_20261120.py`・上記コマンド中のK1155表記はitem番号を指す）。

## 解釈規約

本検証は残余23行のどの行も閉じない。WIN8-D10 candidate は証明書ではない。REFUTED-D10 は LOSS 証明ではない。node数・solved数を勝敗として読まない。本検証は出版記録の第三者による再生（re-execution）検証であり、DFPNエンジン自体の再実行は含まない（18 probeの全再実行はK1149レーン管轄）。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 関連

- item: [`K1155`](../../knowledge/items/K1155-n11-residual72-replace9-whole-record-reexec-third-verification.md)
- 研究ログ: [`研究ログ`](../../log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification.md)
- 単一オーナー宣言: [`宣言ノート`](../../log/2026-11-20-n11-residual72-replace9-whole-record-reexec-third-verification-single-owner-note.md)
- 検証対象: [K1151 whole-record第二検証実験](../n11-residual72-replace9-whole-record-second-verification-20261120/README.md)
