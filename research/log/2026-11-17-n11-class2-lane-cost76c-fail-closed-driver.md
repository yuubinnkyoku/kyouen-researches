# 2026-11-17：cost76c bit61用の証明書抽出をfail-closed化

## 起点

作業前のmainは `be687ae015357e84beffe9fad8bb842dd7db9ea1`。cost76cのv17確定判定はWIN7-D10がbit61/99、bit113はREFUTED-D10。v15とのcross-engine照合は完了している。head1472での候補marginalはbit61を第一候補、bit99を予備とし、bit113は除外。実際の証明書抽出と独立検証は未実施だった。

問題は抽出器 `class4_child1_cert_extractor_exact_v16.ts` のCLIが、`res.rows` が存在すれば `fatal` の有無を確認せず書き出すこと。内部のbounded forbidden-bit tableが飽和すると `fbt_drops>0` / `fatal='fbt_saturation'` でも部分rowsが返り得るため、そのまま証明書扱いすると危険だった。

## 変更

`research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/cert_driver76c.ts` を追加。探索本体は変更せず、`extractBatch` を呼ぶ薄い実行器として次をすべて満たしたときだけ出力する。

- raw childが正確に6石・盤内、選択bitが空。
- 防御手リストが空でなく、全bitが盤内かつ重複なし。
- 全防御手の `perMove.ok=true` かつ `capped=false`。
- rowsが非空配列で、`nRows` と要素数が一致し、重複なし。
- `fatal` が未設定、`fbt_drops===0`。
- 一時ファイルから同一ディレクトリ内のhard linkで公開し、既存証明書を上書きしない。

テスト `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/test_cert_driver76c_guard.mjs` を追加し、実際の抽出器を呼ばずにmock `extractBatch` で6ケースを実行した。成功ケースだけが出力され、fatal、drops単独、rows欠落、perMove未完了、選択bit占有はすべて拒否された。Node v22.16.0で6/6 PASS。

## 状態と限界

これは**抽出器の安全な呼び出し口を準備しただけ**であり、bit61の実抽出・証明書生成・BigInt/Bareiss独立検証・fresh-process byte比較はまだ行っていない。WIN7-D10判定やreceipt foldにも変更なし。head1472のmarginalは再利用せず、実証明書の検証後に再計算する。

cost76c claimはv6へ更新し、guarded driverとmock testのblobを記録した。bit61を唯一の第一候補として抽出し、bit99は予備、bit113は抽出しない。

11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。
