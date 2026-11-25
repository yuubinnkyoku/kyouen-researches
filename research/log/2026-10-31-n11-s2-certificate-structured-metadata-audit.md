# 2026-10-31：既存二石LOSS証明の構造化読み込みと境界数の照合

作業開始時main `691937b1ac93a8fd840a9792e39ef770e8e1024f`。AGENTS.md、knowledge README、K0023、10月31日のS3 LOSS guard・S5→S4証人、10月30日のS4 WIN5枝刈り、既存S2証明書と監査器、軽量CIの定義を確認。標準11×11空盤は **UNKNOWN**。

## 発見した監査上の抜け

`research/experiments/n11-s3-loss-guard-root-audit-20261031/verify.js` の旧 `parseProof` は、証明書JSON全体から `"key"` と `"root_move"` などを正規表現で抜き出していた。この方式では各証明書レコードの境界が保証されず、`third_move_witnesses[].s5_loss_children` と `used_s4_loss_classes[].s5_children` の宣言値を検査しない。実際の合法子を別途列挙する監査はあったが、証明書内の境界件数を改変しても検査条件に使われなかった。これは証明書メタデータの誤受理であり、既存の勝敗判定が誤っていたことを意味しない。

## 修正

- 64-bitの `key` / `s4_class` 配列だけをJSON解析前に文字列化し、`BigInt` で正確に復元する。元の証明書を小数精度のJavaScript `Number` で丸めてから再直列化しない。
- `used_s4_loss_classes` 32件、`third_move_witnesses` 119件をそれぞれ構造化して読む。重複、未登録クラス、石数・手番の不整合、根 `{60,27}` の変更、64-bit範囲外を拒否する。
- 各証人の `s5_loss_children` と参照先の宣言値を照合し、さらに32クラスの全合法5石子を幾何から列挙して `s5_children` と照合する。これにより宣言値の変更を幾何・cache側の実測から検出する。
- `s5_loss_children`、`s5_children`、`root_stones` の単独改変を拒否する負例を追加した。

修正コミット：`4ef4e24091788097c3565875214064c6b34dbb84`。branch / PRなしでmainに直接反映。

## 実施済み検査と残る境界

実際の固定証明書（blob `b52b6e2829f960e93393eac8fb930d415c37ac33`）を新しい構造化読込関数で処理し、**32個のS4クラス、119個の第三手証人、宣言件数の内部不一致0**を確認。証人件数・クラス件数・根・手番の改変を含む負例も独立したJavaScript実行で拒否を確認。ソース全体のJavaScript構文も検査した。

固定cacheを使った全3,297本のS4→S5境界の新監査はGitHub Actionsの軽量CIに任せており、ログ作成時点では実行中で成功未確認。従来の監査で報告済みの3,297本と新監査の実行成功を混同しない。

**信頼境界**：S5勝敗ラベルは引き続きsolver-trustedであり、終局までの独立再探索ではない。新規二石root閉鎖0。標準11×11空盤勝敗 **UNKNOWN**。
