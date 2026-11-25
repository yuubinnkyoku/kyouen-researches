# 2026-11-20 n11 残余72行 WIN8 root 8003180 証明書抽出・三重検証

## 実行内容

単一オーナー宣言ノート（commit 0360f21a・先行出版）の下で、K1086 の
WIN8-D10 candidate 7根のうち greedy 計画順第一位
`00000000000000003800000008003180` の完全勝利戦略証明書を盲抽出し、
3方法で独立検証した。並走レーンが宣言済みの root `…8180000`
（commit 4496c888）とは別根。着手前の最新mainを取り直し、既存宣言との
重複がないことを確認してから着手した。

## 経過と確定事項

1. **verdict基盤**: runner v17（git blob c132cc6425…・pilot_d6 3,402制御）で
   対象rootの両AND順序depth-10 probeを各2回再現。出版値とnode-exact一致
   （903,977 / 1,146,417・両順序 loss=true uncapped・terminal [14,18]）。
2. **抽出器**: WIN7 repo正本抽出器（blob c267f260d1…）を8石root用に改変。
   v17のfbtOR修復適用（fbt_dropsは全53初手で0・修復path起動も0）。recordRow
   による同一局面選択手衝突のfatal化。初手ごと新規プロセス53本（Run A1）・
   同一cwd完全再実行（A2）・別cwd全53初手一括単一プロセス（B）の3実行で
   証明書bytes完全一致（byte-identical）。
3. **証明書**: 34,529戦略行・1,251,923 bytes・
   SHA-256 `1393128972a2ee2bd7586239c830caac967ee45166be8ed87107907c42f23e2c`。
   d = root−最小セットビット bit7 の分解も K1086 規約どおり。
4. **抽出費用**: A1総nodes 3,394,332（最大初手 m=66 250,205）・
   B総nodes 2,608,236（memo温存・戦略不変の実証）。
5. **独立検証**: (a) BigInt 3×3余因子（seventeenth検証器WIN8化）: 53/53
   sub-root PASS・union missing 0 / extra 0・terminals 13,364 [14,18]。
   (b) Bareiss 4×4（TS・独立sub-root走査）: root-check stones 8・
   loserMobility 53・53 sub-root PASS・consumed 49,509行（union一致）。
   (c) python第三方法（監査機械内蔵の独自全木走査）: 76,955 visited・
   winner 49,509・loser 14,082・応手辺 67,420・terminal 13,364 [14,18]
   で、(a)(b)と全数値一致。
6. **監査機械**: `assemble_win8_audit_20261120.py`（stdlibのみ・入力SHA pin・
   probe再現照合・root再導出・summary整合・証明書形式18 gate・fail-closed）。
   18/18 PASS・別cwd再実行でaudit JSON byte-identical（時刻/乱数入力なし）。
   監査正本SHA-256 `ad0d9fb3a30edbd76fcb5562ab01f1e7e51781381377a04fa4a195378eb887da`。

## 出版

実験dir `research/experiments/n11-residual72-win8-cert-extract-root8003180-20261120/`
（README・抽出器・検証器2本・監査機械・runner固定コピー・証明書・
入力pin・probe再現・summary 3実行分・検証記録・監査正本）をmainへ反映。
着地はGitHub git blob SHA-1とローカル計算の一致で確認（READMEのSHA参照）。

## 運用知見

- 8石rootの抽出は7石root（seventeenth: 総4.25M nodes）より安く、
  初手53本で総3.4M nodes・単一プロセスなら2.6M nodes（初手傍系のmemo共有で
  約23%削減）。fbt飽和は全 初手で起動0（FBS 1<<20 に対し遷移tripleが
  ~22K個で十分余裕）。
- 単一プロセス一括と初手毎プロセス分割で戦略が同一になることは事前解析
  （memoは位置の真偽事実のみ保持し順序付けはwscore固定）どおり実証された。
  大rootで1プロセス上限に達した場合は初手分割が正当なresume手段になる。
- **REFUTED-D10 は LOSS 証明ではない。pn/dn・solved数を勝敗として読まない。**
  **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
  すべて UNKNOWN のまま。** 本証明書単体では残余72行は1行も閉じない。

## 次の一手（着手時は単一オーナー宣言を要する）

- 残るWIN8候補（K1086残り5根〔並走宣言1根を除く〕+ K1089の3根 + K1091の3根）
  の証明書抽出。抽出器・検証器・監査機械はroot hex差し替えで再利用可能。
- 8石receipt被覆幾何（「8 D4像×2石除去」join）の設計とfold機械の実装・検証
  （主張被覆4行の閉鎖に必要・別宣言）。
