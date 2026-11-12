# 2026-11-11 n11 S2 {59,60} milestone-2 manifest（greedy証明書1–5・blocker 7個・S6 orbit 10,988）

長期レーン。main = df791bf 開始。milestone-1（K0746、証明書2個・blocker 4個・
S6 orbit 4,262）を greedy順で証明書3番目以降に拡張し、**milestone-2**
（{5,115} → {27,93} → {71} → {82} → {104}、**60 blocker 中7個閉鎖**）の
S6 orbit worklist manifestを完全列挙した（78 FW oracle条件付き・K0675）。

## 確定値（単独実行で再現、artifact の script と出力が一致）

- 単独証明書S6 orbit: 2,191 / 2,150 / 2,421 / 2,516 / 2,563。
  累積union: 2,191 → 4,262 → 6,517 → 8,780 → **10,988**（全体41,842の26.3%）。
  すべてK0729/K0746と一致（第三系統の独立再現）。
- S5 orbit union: 261 / 1,447（18.0%）。greedy曲線（54,52,53,52,50の追加）と一致。
- cost（S7 raw辺数）: min 52 / p25 74 / 中央値 80 / p75 85 / max 101 /
  平均 79.61 / **合計 874,761 raw S7辺**。milestone-1（max 93・平均76.78）より
  重い帯が加わった。
- certs分布（S6 orbit 10,988）: 単一証明書由来が大半
  （certs=1:1,858 / 2:1,824 / 4:2,077 / 8:2,168 / 16:2,208）で、
  証明書3–5はmilestone-1とほぼ disjoint（ペア重なり80–95ずつ、A∩B=79は不変）。
  → 外部solverはmilestone-2を1バッチで消化してもcache衝突は少ない。
- **milestone-1とのsubset検証PASS**: milestone-1の4,262 S6鍵は本unionの
  certs&3≠0部分集合と**集合として完全一致**（501件はbits 3–5とも重複するだけ）、
  4,262件のcost全件一致、106 S5 rep全件含まれる。

## greedy ladder を証明書8番目まで延長した新規測定（同一幾何・別実行）

- {73}: S5 94 orbit / 義務7,890 / S6単独3,868（python invariantの7,890と同一規約）
  → {90,96}: S5 98 / 8,626 / 4,232 → {23}: S5 98 / 8,859 / 4,416。
- **累積S6 union: 10,988 → 14,134 → 17,395 → 20,534（全体の49.1%）**。
  S5 union 516 / 1,447（35.7%）。
- K0729の第6–8位の単体S6 orbit（3,868/4,232/4,416）と一致。
  相互union 11,794とも整合（20,534 − 10,988 + 共有2,248）。
- 証明書8個で12 blocker / 60。secured coverage曲線は当初予想どおり
  小証明書順が最良（1 orbitあたりS6コストは後続証明書ほど高い）。

## 訂正事項（K0729のmilestone-2義務数）

- K0729本文の「t=71: 義務9,684 / t=82: 10,156 / t=104: 10,348」は
  本再現（5,186 / 5,472 / 5,577）と一致しない。S6 orbit数・累積unionは全て
  完全一致するため、orbit层面の数値は正しく、K0729の義務数のみ
  別規約（または誤集計）と判断。本manifestのcertStatsを正とする
  （{73}の7,890がverify_conditional_s6_cover_46.pyと同規約であることが根拠）。

## 実装教訓

- bitmask filterは `v < 32` でなく `(v & 31) !== 0`（後続証明書と重複する
  orbitを誤って除外する）。milestone-1 subset検証で検出。
- 8証明書ladder+manifest同時生成はsandbox process safety deadline超過
  （2回とも）。5証明書manifest単独は成功。ladder数値は別実行で確定し
  script本文には含めない。
- manifest（minified 715,236 bytes・pretty 1.1MB）はreturn→ローカル保存→
  jq検証→pushで扱えたが、**push経路で注意点あり（追記参照）**。

## 追記: 大型ファイルpushの経路（実装教訓）

- **`tools.file_system.read_file` は64,000 bytesで打ち切られる**
  （`was_truncated` を必ず確認）。初回はこれに気づかず
  **64KBに切れたmanifestをcommitしてしまった**（b714e9d）。
  修復: `split -b 60000` で12チャンクに分割→各チャンクを
  `read_file`で結合→`push_files`で上書き（6c4384e）。
  リモート側を再取得して715,236 bytes・10,988 orbit・末尾まで一致を確認済み。
- **`create_or_update_file`（contents PUT）は~1MBペイロードで500/502**。
  **`push_files`（tree API）は単一715KBファイルで成功**。
  大型成果物はpush_files経路で。
- 反映コミット: bee326f（script+log+K0748）→ 6d1a255（truncated manifest、
  のちに修復）→ 6c4384e（フルmanifest 715,236 bytes）。

## 次の一手

- 外部solverでmilestone-2 manifest（10,988 S6 orbit、cost順）を消化し、
  S6 verdictを鍵単位でcacheに蓄積 → 5証明書のS5閉鎖判定 → 7 blocker閉鎖。
- 並行してgreedy 9番目以降（{31}/{89,97}は追加orbit 0）のS6 census・
  milestone-3 manifest拡張（~20,534 S6 orbit）の検討。

11×11空盤・二石root {49,60} は **UNKNOWN**。
