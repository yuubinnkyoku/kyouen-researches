# 2026-11-15 n11 class4 certificate extractor v16 memo repair

## 作業開始時の状態

- 作業開始時の最新 main: `30d2dd47619a68b3677bb9a0f87fd853ecee0680`。
- root `AGENTS.md` と `research/knowledge/README.md` を確認。実験・ログは一次資料として保持し、mainへ直接反映する方針を確認した。
- 現行の11×11知識は K0783 と K0023 を確認。空盤、二石root `{49,60}` / `{59,60}`、S2 `{59,60}` は UNKNOWN。
- class2 laneのcost63f（S6 child `00000000000080809002000000000800`、63候補）は既にmainでin-flight claim済み。重複探索は起動しなかった。
- K0783のheadは `1195/6652/524884/4922/388607`。今回の変更はこの帳簿に影響しない。

## 発見した実装上の問題

現行の探索runner v16（`class4_child1_runner_v16.ts`）には、2026-11-14に修正されたmemoの2問題がある。一方、証明書抽出器 `class4_child1_cert_extractor_exact.ts` はv15のままで、同じ問題を残していた。

1. **符号付き比較によるmemo hit欠落**  
   状態語はsigned Int32、保存先の `mK0..mK3` はUint32Array。上位bitが立つ語をそのまま厳密比較すると、保存値はunsigned、検索値はsignedとなり、同一局面でも一致しない。これは誤ったhitではなく、hitを失う性能問題。
2. **255番sentinelによる負の深さ境界の未記録**  
   `mNoWin` / `mNoLose` は255で初期化されるが、旧条件 `d > mNoWin[h]` / `e > mNoLose[h]` は探索深さ10以下では常に偽。証明済みの「この深さ以内では勝てない／負けない」境界がmemoへ保存されず、再探索が増える。これも勝敗を誤る問題ではなく、枝の再訪を増やす問題。

## 変更

歴史的再現性を保つため、v15の元ファイルは変更せず、同じ抽出処理を複製した `class4_child1_cert_extractor_exact_v16.ts` を追加した。

- memo検索・登録の2箇所を `M_i >>> 0` と比較するよう修正。
- noWin/noLoseの両更新を、255 sentinel未設定時または既存境界より深い場合に更新する形へ修正。
- それ以外の探索規則・幾何判定・証明書形式・kill tableは元ファイルから保持。
- v16 runnerと同じ修正意味論を使う。

回帰試験 `class4_child1_cert_extractor_exact_v16.test.ts` を追加。既に独立検査済みのbit7証明書を50個の相手初手に分解して再抽出し、行数30,947、FBT drop 0、終局石数13〜17、および公開証明書全体のMD5 `0f1fedfe06c658acdd02577f9d7da9d2` を照合する。rootにはcell 31が含まれ、M0の符号bitを実際に踏む。

`.github/workflows/ci.yml` にNode 22でこの回帰試験を実行する手順を追加した。今回の確認時点ではcommit status APIにstatus項目が返らず、**全50 sub-rootのgolden replay成功はまだ確認できていない**。CIの結果をPASSと先取りしない。

ローカルで実行した小さな意味論試験はPASS。Uint32Arrayが `-2147483648` を `2147483648` として保持し、signed比較がmiss、unsigned比較がhitとなること、および255 sentinelの旧更新条件が深さ10で成立せず、新条件なら10/9を記録することを確認した。

## 未修正の旧版コピー

GitHub上のコード検索で、同じ旧比較・sentinel形を残す次のファイルを確認した。今回の対象外として変更していない。今後これらを再利用する場合は個別の回帰監査が必要。

- `class4_child1_runner.ts`
- `class4_child1_sweep_engine.ts`
- `class4_child1_chunk_prover.ts`
- `class4_child1_cert_extractor.ts`
- `research/experiments/n11-fbt-saturation-audit-20261114/scripts/runner_instr.ts`
- `research/experiments/n11-fbt-saturation-audit-20261114/scripts/runner_fbs20.ts`

現在のclass2 sweep claimはv16 runnerを指定しているため、今回の抽出器修正は証明書生成段階の再利用効率を改善するもの。既存の証明書やWIN/LOSS判定を書き換えない。

## 成果物と反映

- `scripts/class4_child1_cert_extractor_exact_v16.ts`
- `scripts/class4_child1_cert_extractor_exact_v16.test.ts`
- `.github/workflows/ci.yml` のNode 22回帰試験
- 本ログ

mainへ直接反映。branch / PRは作成していない。S6 frontier、S5費用、証明書被覆数は変更なし。今回、新しいゲーム勝敗は得ていない。
