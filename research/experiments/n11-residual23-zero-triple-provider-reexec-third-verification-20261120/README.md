# 残余23行 zero triple provider（K1148）pristine 再実行による第三検証（2026-11-20）

## 概要

[K1148](../../knowledge/items/K1148-n11-residual23-zero-triple-provider-third-geometry.md)（残余23行宇宙の zero triple provider 幾何・第三独立再構成、出版 commit `6564fded75038c887c095873c5d3e5633c4fcd35`・2026-11-20T14:28:01Z）の出版実験一式（検証機・入力fixture・監査正本）をbyte単位で取得し、pristine再実行による第三検証を行った。出版レーン自身が3環境実行済みであるため、本検証は出版後の別実行者による第三検証層に位置する（K1147=外部第二検証、K1149=K1146全probe再実行第二検証、K1151=K1146 whole-record第二検証と対になる、K1148相手の検証）。

単一オーナー宣言ノート: [`宣言ノート`](../../log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md)（先着出版 commit `75fde9d82854a1ff7b5b9ce09ff1956a3544c67f`・2026-11-20T14:53:03Z 宣言時刻）。

## 対象（出版pin・commit 6564fded75 で取得し全点一致確認）

出版実験dir: `research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120/`

| ファイル | SHA-256 | bytes |
| --- | --- | --- |
| 検証機 `audit_zero_triple_providers.py` | `cb8c95c8799e6c12bbc7fdb2cc9b6236f664724f29827e56d2e75de62a084892` | 14,225 |
| 入力 `residual23-provider-input.json` | `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822` | 3,105 |
| 出版監査 `third-geometry-audit.json` | `526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573` | 4,418 |

## 検証機（harness）

- `scripts/verify_k1148_reexec_third_20261120.py`（SHA-256 `6f016cd14fad787b7f6b1b5e8acb72b5da3625ed4b2a3d79d2f8bd989c0e7662`・12,221 bytes）
- Python stdlib のみ。乱数・時刻・環境依存出力なし（監査JSONはsorted keys・実行時間を含まない）。fail-closed（1 gateでも崩れれば非正常終了）。
- 引数: `--root`（machine.py・input/・published-audit.json を含む検証root）、`--output`（監査JSON出力先）、`--timeout`。

## 手順と結果

1. **pin gate（3/3 PASS）**: 検証rootの3ファイルが出版pinと一致。
2. **pristine再実行（4/4 byte一致）**:
   - 同一cwd 1回目・2回目（実行環境・PYTHONHASHSEED unset）
   - 隔離tree複写 + 隔離cwd + 隔離HOME 1回
   - 隔離 + `PYTHONHASHSEED=random` 1回
   - 全4実行で returncode 0・出力 SHA-256 `526eada2…`・出版監査との byte 一致・parsed object 一致。
   - マシン1実行あたり約4.2秒。
3. **tamper gate（PASS）**: fixture の offset 1552 の1 byte を XOR 0x01 で変更した偽入力（改変後 SHA-256 `dd3f3c48…`）で returncode 1・出力書き込まず fail-closed。出版機の pin が改ざんを捕捉。
4. **harness自身の決定性（3実行 byte一致）**: 同一cwd 2回 + 隔離cwd/隔離HOME 1回で監査JSON（本正本）byte一致。監査正本: `output/reexec-third-verification-audit-20261120.json`（SHA-256 `312966e890c800e9326d0c05d243ac13a3b9bf161237a2e1571f711d51a8f3dd`・3,613 bytes）。

## 再現

```bash
# 1) publish commit から3ファイルを取得（上のpin表とSHA照合）
S=6564fded75038c887c095873c5d3e5633c4fcd35
B="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/$S/research/experiments/n11-residual23-zero-triple-provider-third-geometry-20261120"
mkdir -p root/input
curl -sS "$B/scripts/audit_zero_triple_providers.py" -o root/machine.py
curl -sS "$B/input/residual23-provider-input.json" -o root/input/residual23-provider-input.json
curl -sS "$B/output/third-geometry-audit.json" -o root/published-audit.json
sha256sum root/machine.py root/input/residual23-provider-input.json root/published-audit.json
# 2) harnessを実行（--root は上記の root ディレクトリを指す）
python3 verify_k1148_reexec_third_20261120.py --root root --output audit.json
# 全gate PASS で監査JSONが生成される。本正本と byte 一致するはず
```

## 解釈規約

本検証は残余23行のどの行も閉じない。zero rows の列挙は残余行の勝敗決着ではない。nodes/solved 等の計数を勝敗として読まない。本検証は幾何の新規計算を含まない（出版機械のpristine再実行のみ）。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 関連

- item: [`K1153`](../../knowledge/items/K1153-n11-residual23-zero-triple-provider-reexec-third-verification.md)
- 研究ログ: [`研究ログ`](../../log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification.md)
- 単一オーナー宣言: [`宣言ノート`](../../log/2026-11-20-n11-residual23-zero-triple-provider-reexec-third-verification-single-owner-note.md)
- 検証対象: [K1148 第三幾何実験](../n11-residual23-zero-triple-provider-third-geometry-20261120/README.md)
