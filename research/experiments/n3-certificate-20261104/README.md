# 3×3 空盤 KYOENC3 証明書の再生成と軌道検証（2026-11-04）

## 目的

K0013（3×3は先手必勝）の証拠は ranked-and-or certificate＋独立C++検査である。
本実験は、その証明書ファイル `kyouen-3x3.cert` を決定的に再生成し、
独立したPython実装で検証した記録である。

成果物は証明書ファイルと、それが「全証明DAGノードの局所条件を満たす」ことの
再検証である（Leanの形式化は別作業）。

## 再現

```sh
# 証明書の生成（cmake Releaseビルド）
cmake -S . -B build-n3 -DCMAKE_BUILD_TYPE=Release
cmake --build build-n3 --target kyouen-certgen-1-to-8 --parallel
build-n3/kyouen-certgen-1-to-8 3 kyouen-3x3.cert

# 検証
python3 inspect_cert.py kyouen-3x3.cert   # ヘッダと全エントリを表示
python3 validate_cert.py kyouen-3x3.cert # 全軌道ノードの局所条件を検査
```

## 証明書の内容

この証明書は、KYOENC3 形式で「空盤面を根とし、各ノードが合法手で到達可能な
局面に対応する」AND/OR 証明である。保存されるノードは D4 対称で canonical化
された局面（マスクの最小値）であり、全部で28エントリである：

| 勝敗 | ノード数 |
|---|---:|
| winning（先手必勝ノード） | 18 |
| losing（後手必勝ノード） | 10 |
| **計** | **28** |

足すと `forbiddenCount = 14`（3×3 の禁止四点組の総数、K0006 の歩行と一致）、
最大深さ 5、空盤面はwinningで根ノードである。

## 軌道検証

28エントリの D4 軌道展開（8変換）で **175ノード**すべての局所条件を、3x3に
特化した決定的に評価可能なPython実装で検査した：

- winning: 小さいランクの losing 子が証明書内に少なくとも1つある
- losing: 合法な全ての子が証明書内にあり、winning でランクが小さい

結果: **PASS**（軌道ノード175、うち winning 111 / losing 64）。

独立検査の方法: `validate_cert.py` は、証明書の再生成にも既存の検証器にも
依存せず、Python標準ライブラリのみで書かれた別実装である。禁止四点組判定、
合法手生成、D4軌道展開、順列局所検査をそれぞれ独立に実装し直している。

## 信頼境界と限界

- これは「証明書が正しいこと」の検証であり、**証明書の完全性（ゲーム全局面分類）
  を証明するものではない**。条件は局所的で、証明書の外側の局面については何も
  言わない。
- Lean への形式化は未着手（K0103 相当）。`SquareCert2x2.lean` と同型の証明を
  3×3 に展開するには、順列不変性の補題が必要で、本実験の範囲外である。
- SHA256は `569c18efa58d71b7d9e08bcac3b66e0ea9593a76b2765f1f872e3e7e6f557dfc`
  で、`results/certificates.csv` の3×3エントリと一致する。
