# 残余23行 零triple-provider第四幾何（K1156）pristine 再実行による第三検証（2026-11-20）

## 概要

[K1156](../../knowledge/items/K1156-n11-residual23-zero-triple-direct-fourth-geometry.md)（残余23行の3零行を行+2空き点直接生成で再導出する第四幾何・出版 commit `7c21ad16` 監査・item commit `1d1b185a`・2026-11-20T15:26Z 出版・direct fourth geometry レーン）の実験一式（検証機・3入力fixture・監査正本）をbyte単位で再取得し、pristine再実行による第三検証を行った。出版社は第四幾何レーンであるため、本検証の意味は「出版byteをGitHubから再取得するだけで、監査正本がpin＋入力のみから新規に再生成できること」（輸送・転写・ローカル記憶を介さない独立検証可能性）の確定にある。残余23行の幾何・被覆の全体像に新たな計算は追加しない。

単一オーナー宣言ノート: [`宣言ノート`](../../log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification-single-owner-note.md)（先着出版 commit `251523913cdc962c7f6d1eee581de9b641f0a866`・2026-11-20T15:49:00Z 宣言時刻）。

## 対象（出版pin・fetch commit 49e420fe で取得し一致確認）

出版実験dir: `research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/`

| ファイル | SHA-256 | bytes | 出版commit |
| --- | --- | --- | --- |
| 検証機 `scripts/verify_direct_fourth.py` | `850df34b4c01ecb44cd9a5b480be276b63ec0f8c7f5fc541acb9e7f182304156` | 14,771 | `3969a050` |
| 監査正本 `output/direct-fourth-geometry-audit.json` | `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f` | 7,627 | `7c21ad16` |
| 入力 `input/residual23-provider-input.json` | `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822` | 3,105 | `6f2c70e8` |
| 入力 `input/k1148-third-geometry-audit.json` | `526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573` | 4,418 | `261f4847` |
| 入力 `input/k1147-external-audit.json` | `17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb` | 11,150 | `ce13afe4` |

## 検証機（harness）

- `scripts/verify_k1156_reexec_third_20261120.py`（SHA-256 `315332ba00d78c4c65a142dc09ee790f9ffba8d64e1eaae0e232fde36eff5d83`・12,862 bytes）
- Python stdlib のみ。乱数・時刻・環境依存出力なし（監査JSONはsorted keys・実行時間を含まない）。fail-closed。
- 引数: `--root`（検証機・3入力・published-audit.json を含むstaging root）、`--output`（監査JSON出力先）。

## 手順と結果

1. **pin gate（machine+監査の2点 + 入力3点 すべて PASS）**: 検証機・出版監査・3入力fixtureのSHA-256 pin一致（出版検証機内部のfail-closed pin 3点と、harness側の独立pin 3点の二重照合）。
2. **pristine再実行（4/4 byte一致・新規生成）**: 各実行前に監査ファイルをtreeから削除した上で（正本の既存bytesに依存しない新規生成）、
   - 同一cwd 2回（ambient・PYTHONHASHSEED unset）
   - 隔離tree複写+隔離cwd+隔離HOME 1回
   - 隔離+PYTHONHASHSEED=random 1回

   全4実行で returncode 0・12 gate all ok・出力 SHA-256 `c4e55dbe…`（7,627 bytes）で出版監査とbyte-identical。1実行あたり約5秒（19,665生成事象・550,620子局面の再計算込み）。
3. **tamper gate（PASS）**: 複写treeで入力 `input/residual23-provider-input.json` のoffset 200（出版レーン検査済みのoffset 100とは異なる）の1 byte をXOR 0x01で改変（改変後 SHA-256 `f5c6a73d…`）→ returncode 1・出力未書込でfail-closed終了。
4. **harness自身の決定性（3実行 byte一致）**: 同一cwd 2回＋隔離cwd+隔離HOME 1回で監査JSON（本正本）byte一致。監査正本: `output/reexec-third-verification-audit-20261120.json`（SHA-256 `5810ceacb1b3a4d28df594834cff227272c7020ff6eb69dd0b3b5bcdcd3f2d68`・4,930 bytes・pin gate 5/5・run gate 4/4・tamper gate PASS・interpretation_guard 5文言同梱・status `k1156-reexec-third-verification-passed`）。

## 再現

```bash
S=49e420fe76c277b8669e2fc0c2a423c8df3a5d54
D="research/experiments/n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121"
B="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/$S/$D"
mkdir -p root/scripts root/input
curl -sS "$B/scripts/verify_direct_fourth.py" -o root/scripts/verify_direct_fourth.py
curl -sS "$B/input/residual23-provider-input.json" -o root/input/residual23-provider-input.json
curl -sS "$B/input/k1148-third-geometry-audit.json" -o root/input/k1148-third-geometry-audit.json
curl -sS "$B/input/k1147-external-audit.json" -o root/input/k1147-external-audit.json
curl -sS "$B/output/direct-fourth-geometry-audit.json" -o root/published-audit.json
# 上記pin表とSHA-256照合後:
python3 scripts/verify_k1156_reexec_third_20261120.py --root root --output audit.json
# 本正本と byte 一致するはず
```

## 解釈規約

本検証は残余23行のどの行も閉じない。第四幾何は8根被覆判定の被覆計画の簿記でありゲーム理論的証明書ではない。REFUTED-D10 は LOSS 証明ではない。node数・solved数を勝敗として読まない。本検証は出版記録の第三者による再生（re-execution）検証であり、DFPNエンジン自体の再実行と K1147 8根被覆判定の第三検証（宣言 `887e594d`・別レーン）は本検証の範囲外。**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**

## 関連

- item: [`K1157`](../../knowledge/items/K1157-n11-residual23-direct-fourth-geometry-reexec-third-verification.md)
- 研究ログ: [`研究ログ`](../../log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification.md)
- 単一オーナー宣言: [`宣言ノート`](../../log/2026-11-20-n11-residual23-direct-fourth-geometry-reexec-third-verification-single-owner-note.md)
- 検証対象: [K1156 第四幾何実験](../n11-residual23-zero-triple-provider-direct-fourth-geometry-20261121/README.md)
- 上流: [K1148 第三幾何](../n11-residual23-zero-triple-provider-reexec-third-verification-20261120/README.md)（第三検証・本レーン K1153）・[K1147 外部第二検証](../../knowledge/items/K1147-n11-residual23-eight-root-cover-decision-external-second-verification.md)
