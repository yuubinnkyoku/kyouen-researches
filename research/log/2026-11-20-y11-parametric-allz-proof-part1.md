# y=11族パラメトリック全称証明 part1（正本検証器12チェック）（2026-11-20 高速レーン）

単一オーナー宣言（[宣言ノート](2026-11-20-y11-two-token-skeleton-single-owner-note.md)・
2026-11-20T11:58:00Z・commit ed778278）に基づく y=11 族着手の第二段階（正本監査 part1）の記録。
正本は[実験dir](../experiments/vertical-fiber-two-token-y11-parametric-allz-proof-20261120/report.md)。
対象は [K1143](../knowledge/items/K1143-two-token-y11-parametric-closed-form-fit.md)
（fit・status observed・2026-11-20T12:15:50Z 出版 commit 27944a94）。

## 採番衝突の記録（次回統合への引き継ぎ）

本 part1 の push 準備中に採番衝突を検出した。K1143（y=11 fit・先着・12:15:50Z）に対し、
remo レーンが `items/K1143-remo-survivor-minimal-period-r33to48.md` を
12:30:33Z に出版した（コミット 0aa9f2a8・56fe3f0e・19c002a3。README bullet は
同名 K1143 を付す）。AGENTS.md「K番号」規則（main に既に存在する番号は変更しない・
衝突する新規項目を再採番し参照も更新・生成物は再生成）によれば両者のうち後着の
remo 項目が再採番対象だが、`research/knowledge/generated/` の再生成には repo の
ビルドツール（uv/build.py）が必要で本実行環境からは利用できないため、
本 run では再採番を実行せず記録のみ残して先着 K1143 の path
（`items/K1143-two-token-y11-parametric-closed-form-fit.md`）で一意に参照する。
次回の統合で (a) remo 側が再採番済みなら確認のみ、(b) 未解決なら K1144 以降の
空き番号への再採番（item 改名・id/alias・README bullet 参照の更新・
generated 再生成）を y=11 レーン側から実施する。

## part1 検証器の構成（2026-11-20T12:35-12:55Z）

1. K1141 出版正本検証器 verify_y10_universal.py（SHA-256 f9169449…）から
   生 2エンジン（H_ordered/H_canonical）・K0832 単一トークン表を逐語転写し、
   同ファイルの cand10 saver ブロックを Y→Y10 改名のうえ併置（B子・x=11 合流子用）。
   cand11 は出版 cand11.py（K1143 fit・SHA-256 8a083400…）から fit driver を除き
   逐語転写。opts11/identity_ok11 は A子 = cand11(z,x-1,R-1)（x=11 は合流子
   (10,11)≡(11,10) で cand10(z,11,R-1)）・B子 = cand10(z,x,R-1)・
   C子 = 1⊕cand11(z-1,x,R-1)、T/P overlap fail-closed assert 付き。
2. 型機械は clip 窓 2y+2=24・番兵±25・同一自由座標 box ±60（y=10 機の +1 シフト）。
   C4t は clip 23/番兵24 で tightness 判定。
3. checks: C1（z=0..14・x=11..29・R<=x+z+46）・C1b（単一トークン+出版 B子+
   x=11 合流子）・C2（z=0..48・x=11..56・R<=x+z+40）・C2b（深 z 8行）・
   C3（選択肢分解生列挙照合）・C4/C4t・C7（seed 20261131・200k）・
   C8（境界多様体 z<=3000・dx∈[-24,15]）・C9（v シェル [61,64]/[89,92]/[117,120]）・
   C11（生 census z=0..79・x=11..70・R<=x+z+12 両エンジン）・C12（深格子
   z=0..120・x=11..120・R<=x+z+16。C1d は y=10 と同じく part2 に送り12チェック）。

## 結果

- C1/C1b/C3 は初回で bad 0。C2/C4 も bad 0。
- **C4t: clip 23 で 4,127 収束違反・clip 24 で 0 違反 → clip 窓 2y+2=24 が tight
  （2y+2 tight は7族連続 y=5..11）**。K1143 の次段階課題（型機械 tight 判定）が確定。
- フル12チェック1回目は C11 内で異常終了した。原因は C1/C1b/C3 からの温かい
  lru_cache との合算でメモリ枯渇したものと特定し、C11 冒頭に両エンジンの
  cache_clear を追加（監査内容は影響なし・単体 C11 は 50.5秒 PASS 済みだった）。
- 修正後フルラン: **overall PASS・総照合点 6,270,161・全 bad 0・型 155,182・約90秒**
  （C1 21,090 / C1b 42,935 / C2 219,765 / C2b 18,788 / C3 1,095 / C4 621,365 /
  C4t 621,365 / C7 200,000 / C8 829,503 / C9 918,090 / C11 892,800 / C12 1,883,365。
  merge corollary 1,443,824点・tail corollary 246,792点 それぞれ不一致0）。
- 同一 cwd 2回＋別 cwd 隔離 copy 1回の3回で output/audit.json byte-identical
  （SHA-256 2ad3b750…・検証器 SHA-256 c57baf5c…）。

## trust 境界・次回（part2）

part1 は機械構成段階であり **K1143 の status は observed のまま**。part2 では
C1d（出版 z=8/9/10/15/16/17 切片の y=11 特殊化・事前 preflight 必要）と
census_rows.py（第三実装・出版 census.txt・cand11 独立照合）を構成して
全チェック PASS + 3回 byte-identical で昇格判定する。3トークン以上・y>=12 族・
固定幅・q点版安定化長・標準 11×11 の勝敗は範囲外のまま。
