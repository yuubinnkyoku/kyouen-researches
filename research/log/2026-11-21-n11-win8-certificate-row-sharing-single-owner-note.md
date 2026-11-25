# 単一オーナー宣言: 既刊WIN8-D10証明書のD4正準戦略行共有監査（2026-11-21）

本ノートは、既刊の8石WIN8-D10証明書を対象に、戦略局面のD4正準化後の重複・共有率・証人手の相違を測定し、位置キー共有cacheの有効範囲と安全な統合規約を定量化する独立解析の単一オーナー宣言である。

- 宣言時点の main HEAD: `a2a374cce3e08f689bb5d97e3c16b6af4163731f`
- 対象: 以下の10証明書。すべて宣言時点のmainに存在する既刊正本であり、各K項目が個別の三重検証または同等の独立検証を記録している。
  - K1096: `research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/certs/win8-root-00000000000000003800000008003180-20261120.n11`
  - K1106: `research/experiments/n11-residual72-win8-cert-extract-root8005021-20261120/certs/win8-root-00000000000000003800000008005021-20261120.n11`
  - K1108: `research/experiments/n11-residual65-win8-cert-extract-root9840004-20261120/certs/win8-root-00000000000000003800000009840004-20261120.n11`
  - K1109: `research/experiments/n11-residual65-win8-cert-extract-root9090022-20261120/certs/win8-root-00000000000000909002200080100000-20261120.n11`
  - K1113: `research/experiments/n11-residual58-win8-cert-extract-root8890020-20261120/certs/win8-root-00000000010000889002000080100000-20261120.n11`
  - K1114: `research/experiments/n11-residual58-win8-cert-extract-root120000038-20261120/certs/win8-root-00000000012000003800080009000000-20261120.n11`
  - K1117: `research/experiments/n11-residual55-win8-cert-extract-root22081000-20261120/certs/win8-root-00000000000000801202000022081000-20261120.n11`
  - K1139: `research/experiments/n11-residual29-win8-cert-extract-root0810000a-20261120/certs/win8-root-0000000800000000380000000810000a-20261120.n11`
  - K1136: `research/experiments/n11-residual29-win8-cert-extract-root438000000818-20261120/certs/win8-root-00000000000000043800000008180010-20261120.n11`
  - K1137: `research/experiments/n11-residual29-win8-cert-extract-root00000000000200003800200008180000-20261120/certs/win8-root-00000000000200003800200008180000-20261120.n11`
- 固定参照: `a2a374cce3e08f689bb5d97e3c16b6af4163731f`。各証明書のSHA-256・byte数・戦略行数・root/headerは取得時に再計算してpinする。
- 受入条件:
  1. 10証明書の全pin・header・root・行数・重複なしを確認する。
  2. 11×11の8個のD4変換を直接適用して各局面を正準化し、同じ変換で証人手も正準座標へ写す。
  3. 位置の共有次数、石数層別、全組合せの重複、既刊順の増分cache hit、同一局面における証人手の相違を機械集計する。証人手の相違はWIN/LOSS verdict conflictと混同しない。
  4. 証人手が異なる共有局面について、正準局面の安定化群による同値も検査する。
  5. 別作業場所で再実行し、監査JSONがbyte-identicalであることを確認する。
- 対象外: 新規DFPN probe、depth-10 sweep、証明書抽出、receipt fold、S6行閉鎖、frontier簿記更新、二石rootや空盤の勝敗主張。
- 並行作業との分離: fold24外部第二検証（先行宣言 commit `434d53f3`）、fold25外部第二検証、fold26、round-5 refsolve、root `00000000010000809002000040002001` の証明書抽出、36-witness sweepには着手しない。これらの入力を変更せず、既刊証明書の読み取り専用解析に限定する。
- 解釈境界: WIN8-D10証明書は各8石rootのゲーム木を証明する。本解析はその証明書の行集合・証人手の共有構造を測るだけであり、共有cacheのverdictを新規に証明したり、行のゲーム理論的勝敗を変更したりしない。標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はUNKNOWNのまま。

失敗・取得不能・pin不一致はそのまま記録し、部分集計を成果として出版しない。