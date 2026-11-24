# b28 thirdimpl queue registry rev3 (2026-11-24)

queue registry (`research/experiments/n11-centralreply-class5343-b28win46-thirdimpl-queue-registry-20261124`) の純bookkeeping更新 (rev2 `e437af37…` → rev3 `334f6209…`)。solver実行・probe・cache書込なし。

## 変更内容 (機械検証済み)

- **P5 (claimed-5) 5行 thirdimpl claimed→done**: aa005/aa030/aa031/aa047/aa053。
  Part CX (原宣言 `1300c10d`・2026-11-24T00:49:31Z) は3.5h超停滞 (cx dir最終commit
  scaffold A `3185a672` のまま・outputs未出版) 後、takeover規約 (earliest_takeover
  2026-11-24T04:19:31Z以降かつ停滞・対抗宣言なし機械確認) に従い
  **takeover宣言 `c48aa56b`** (2026-11-24T04:20:09Z・observed HEAD `10b8e96d`) で
  実行主体交代・**完了 `46687096`**。
- queue_state_counts: thirdimpl_done_win **16→21**・thirdimpl_claimed_win **5→0**
  (open 25・loss系・win_total 46等は不変)。
- claimed5_do_not_retake_until_takeover_rule: **resolved** (outcomeフィールドに
  takeover・完了shaを記録)。
- thirdimpl_publications.CX: **done** (takeover・completion `46687096`・audit 178 gates
  all PASS×3 byte-identical・verdict agreements 5/5 (WIN=5)・replica 10/10
  node-exact・verdict不消費)。
- revision: rev3 (rev1 sha `8c4216c6…` / rev1 published `69e391a3` /
  rev2 sha `e437af37…` / rev2 published `fc537f3b` を明記)。

## 検証

- rev3 JSON: 54行のthirdimpl state集計 done 22 (WIN 21 + LOSS 1) / claimed 0 /
  open 32 (WIN 25 + L-optional 7) — WIN 46 = 21 done + 25 open と一致。
  JSON parse可能・外科的テキスト編集 (rev2のbyte列を基礎に5 claimedブロック置換+4 view更新のみ)。
- rev3 queue-registry.json sha256 `334f6209d0628cdf8f5c997e92bc5e5e63ae7f450345dc1a8393488941f1f6e9`。

## 意味と主張の限定

- **verdict不消費・閉鎖・被覆・secured・root勝敗の主張なし。** Part CXの成果は
  three-implementation corroboration (verdict一致+node-exact replica) のみ。
  batch-28 WIN46のうち交叉検証済みは21行 (残りopen 25行 = P2/P3/P4パッケージ)。
  次の候補はregistry記載どおり P2 (~est 152.7M) → P3 (~est 202.6M) → P4 (~est 373.8M)。
- **標準11×11空盤・class 5343 (54キーすべて) は本revの前後を通じてすべてUNKNOWN
  のまま。**
