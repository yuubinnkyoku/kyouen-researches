# 残余23行の三つの零triple-provider行を第四の幾何計算で再導出（2026-11-21）

単一オーナー宣言: [研究ログ](../../log/2026-11-21-n11-residual23-zero-triple-provider-direct-fourth-geometry-single-owner-note.md)（commit `b0db8dfec12b163ec51292922fc5fab4fac3ff66`）。

## 結果

K1147の8根被覆不可能性証明書が使う「残余23行のうち3行には、候補pool P'''上の三行被覆根がない」という前提を、K1148とは異なる第四の幾何計算で再導出した。

K1148は異なる3行の全組と各行の8³向きを列挙した。本検査はその列挙を使わず、**各零行に盤上の空き2点を直接加える**。各行について `C(115,2)=6,555` 通りを生成し、D4正準化した8石根の全28個の6石子局面を再構成する。安全性は `(x,y,x²+y²,1)` の4×4整数行列式を24置換で展開して判定した。既存の二つの3×3行列式述語は呼び出していない。

| 零行 | 生成事象 | D4根 | 子局面の被覆数分布（1/2/3行） | 三行候補 | 安全だが除外済み | 共円四点あり | P'''候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `00000000000000003800000008002010` | 6,555 | 6,555 | 6,188 / 363 / 4 | 4 | 1 | 3 | 0 |
| `0000000000000000380000000a080000` | 6,555 | 6,555 | 6,188 / 362 / 5 | 5 | 2 | 3 | 0 |
| `00000000020000801202000000100000` | 6,555 | 6,555 | 6,183 / 367 / 5 | 5 | 1 | 4 | 0 |

合計19,665生成事象、550,620個の6石子局面を検査した。三行候補根の和集合は8根で、内訳は**共円四点を含む5根、安全だがREFUTED-D10除外集合に入る3根**。P'''に残る三行被覆根は0。8根すべての被覆行・分類・最初に見つかった共円四点の座標がK1148の第三幾何正本と完全一致した。

K1147の外部監査71/71 PASS、K1148の第三幾何監査、両方の入力pin鎖も検査した。12 gateすべてPASS。通常実行・別作業場所・`PYTHONHASHSEED=random` の3実行で監査JSONはバイト単位で一致した。入力fixtureの1 byte改変（offset 100、XOR 0x01）はSHA-256 pinで検出され、終了コード1・出力未作成となった。

監査正本 SHA-256: `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f`（7,627 bytes）

## 再現

```sh
python3 scripts/verify_direct_fourth.py \
  --input input/residual23-provider-input.json \
  --k1148-audit input/k1148-third-geometry-audit.json \
  --k1147-audit input/k1147-external-audit.json \
  --output output/direct-fourth-geometry-audit.json
```

| 入力・検証器 | SHA-256 |
|---|---|
| `input/residual23-provider-input.json` | `51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822` |
| `input/k1148-third-geometry-audit.json` | `526eada2c94457f06a7cf27a86011586e394c342687e539a6b545b42577b9573` |
| `input/k1147-external-audit.json` | `17dbd6ab3a9a9b5aef1cf1cf517a5a0fd216dff755f0ed86fcf029e1612cabcb` |
| `scripts/verify_direct_fourth.py` | `850df34b4c01ecb44cd9a5b480be276b63ec0f8c7f5fc541acb9e7f182304156` |
| `output/direct-fourth-geometry-audit.json` | `c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f` |

## 解釈の境界

この検査は3つの零行を含む8石根を全数再導出したもの。全P''' providerの最大被覆数3とREFUTED-D10除外集合は、pin済みのK1147/K1148記録から受け継ぐ。K1147の算術証明書では、零行3つを被覆する根は各2行以下を覆うため、8根中少なくとも2根が必要になる。残り20行に使える枠は最大 `2×2−3 + 3×6 = 19` で、1行不足する。よってP'''上の8根被覆は不可能であり、K1097/K1102のgreedy 9根上界と合わせた条件付き最小被覆9という結論を補強する。

ただし、被覆は候補根の計画簿記であり、ゲーム証明書ではない。REFUTED-D10はLOSS証明ではない。新規probe・証明書抽出・receipt fold・S6行閉鎖は行っていない。

**標準11×11空盤・二石root `{49,60}` / `{59,60}`・S2 `{59,60}`・class 1/2/4はすべてUNKNOWNのまま。**
