# ルールと再現手順

共円ゲームでは未使用の格子点へ交互に石を置き、同一円または直線上に4点を作る手が禁止されます。
完全指摘・通常プレイでは合法手のない手番側が負けます。
正確な定義は[K0001](../research/knowledge/items/K0001-complete-call-rules.md)、
記号・Grundy数は[K0002](../research/knowledge/items/K0002-grundy-and-first-move-conventions.md)を参照してください。
q点版、misère、有限パスなどの条件を標準ルールと混同しないでください。

## C++と小盤証明書

repo rootで次を実行します。探索器と検査器は別の実装です。

```sh
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel 2
./build/kyouen-certgen-1-to-8 5 /tmp/kyouen-5.cert
./build/kyouen-certcheck /tmp/kyouen-5.cert
```

1〜6の生成・検査は通常CIで実行します。大きな公開証明書の取得とhashは
[release-assets](../release-assets/README.md)、全公開証明書検査は
[check-all-certificates.sh](../scripts/check-all-certificates.sh)を参照してください。
CMakeのBUILD_RESEARCH_SOLVERSをONにすると追加solverをビルドできます。

## 研究回帰

各[experiment](../research/experiments/README.md)のREADMEは保存された入力・出力、共有コード、検算コマンドと範囲を示します。
通常の回帰では巨大探索を繰り返しません。既存の有限証人検査・軽量な完全検算・コンパイル検査を行います。
現行CIの手順は[ci.yml](../.github/workflows/ci.yml)を参照してください。

## Lean・Rust

```sh
lake build
lake exe kyouen-classification-demo
cd rust/independent-verifier
cargo test --release
cargo run --release --bin kyouen-verifier -- self-test
cargo run --release --bin kyouen-verifier -- audit-evidence evidence-sample
```

Leanは証明書方式の一般健全性を形式化し、具体的な巨大証明書の全局所条件は独立検査器が検査します。
各盤面の現在の検証範囲はknowledgeのsolution metadataを参照してください。
