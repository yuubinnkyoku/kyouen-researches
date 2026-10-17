# Lean基礎定理の追加 — 2026-10-17

作業開始時に `git fetch origin main` でGitHubを確認し、ローカルmainを `89fe3b7f` までfast-forwardした。
既存の未コミット変更（Rules、CertificateSoundness、Main、SmallCertificates、UniformCapacity等）は保持し、今回の定理は独立したモジュールへ追加した。

## 実装判断

第1段階としてK0337の抽象十分条件と整数行列式の幾何方程式への接続を実装した。
標準ライブラリだけで構成されたrepoの依存を増やさず、円は分母を払った二乗距離式で定義した。
実数型上の距離・平方根との同値、K0337の幾何学的ブロック条件、反例族の最小性までは形式化していない。
K0352、K0384、839局面証明書はこの作業の実装対象に含めていない。

K0337ではブロックの対合不変性だけで十分だと誤認しないよう、鏡像二点を含むブロックの不変性を独立した仮定にした。
安全な対称局面から、未使用の鏡像への応手が安全であり、その後に再び対称になることを示す。
占有点数が盤面サイズ以下であることを使って帰納し、既存の `Losing` へ接続した。

整数幾何では最初の三点の非共線性を仮定しない。第一・第二点だけの相異性の下で三点外積を場合分けし、中心または直線を構成する。
既存行列式との一致と盤面座標の単射性を別々に証明し、最後に `ForbiddenFour` の同値へ接続した。

## 検証

Lean 4.35.0で以下を実行した。

```sh
lake build Kyouen.OddInvolution Kyouen.IntegerGeometry Kyouen.FormalizationChecks Kyouen.MaximalParity
lake build
```

`FormalizationChecks` には実際に禁止ブロックが発生する奇数qの例、偶数qで鏡映の結論が破れる例、共円・共線例、最初の三点だけが共線の非共円例、2×2盤のルールへの接続例を置いた。
主要3定理の `#print axioms` は `[propext, Classical.choice, Quot.sound]` のみで、`sorryAx` や `native_decide` の信頼拡張を使っていない。
この公理一覧を `#guard_msgs` で固定し、依存公理が変わるとCIのビルドも失敗するようにした。
既存の未コミット変更への依存を排除するため、HEADのRules・CertificateSoundness・Main等と追加3モジュールだけを別の一時packageへコピーし、上の明示ビルドが通ることも確認した。
追加モジュールと例を明示ビルドする `.github/workflows/lean-foundations.yml` を追加した。長時間探索workflowは起動していない。

knowledge更新後には規約の `uv sync --locked`、knowledge checker（429項目、エラー・警告0）、unittest（33件成功）、生成器を実行し、生成結果を確認した。
