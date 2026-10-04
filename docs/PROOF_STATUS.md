# 証明方式と信頼境界

現在の盤面別status・coverageは[正本の解決状況](../research/knowledge/generated/solutions.md)を参照してください。
この文書は証明方式の読み方を説明します。

順位付きAND/OR証明書はwinningノードの合法な証人手、losingノードの全合法手、子への順位減少を記録します。
[独立C++検査器](../cpp/certificate/kyouen_certcheck.cpp)は局所条件を再検査し、
[Leanの一般健全性定理](../Kyouen/CertificateSoundness.lean)は局所条件から通常プレイの勝敗が従うことを示します。
[Leanのルール](../Kyouen/Rules.lean)は整数行列式による禁止四点組と合法手を定義します。

全安全局面のGrundy計算、空盤からの戦略証明、初手の完全分類は別の検証範囲です。
独立再計算、CSV構造監査、選択局面証明書の受理を、全探索の独立再求解へ読み替えません。
証明書形式は[AND/OR](CERTIFICATE_FORMAT.md)と[KYOENC4](KYOENC4.md)、具体的な留保は
[K0003](../research/knowledge/items/K0003-solution-and-evidence-levels.md)、
[K0009](../research/knowledge/items/K0009-lean-soundness-trust-boundary.md)、
[K0010](../research/knowledge/items/K0010-kyoenc4-selected-position-certificates.md)にあります。

当時の公開証明書検査の実行記録は[certificate-validation experiment](../research/experiments/certificate-validation/README.md)へ保存しています。
