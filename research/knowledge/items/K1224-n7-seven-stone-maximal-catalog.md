---
id: K1224
title: 7×7の7石極大安全配置の完全カタログは16配置・2 D4軌道
kind: computation
status: computed
topics: [maximal-safe, geometry]
aliases: ["n7 seven-stone catalog", "7x7 minimal maximal catalog 16 configs 2 orbits"]
relations:
- type: depends_on
  target: K0031
  note: s_7=7の値と証人[1,9,22,23,27,44,45]（カタログ第1軌道代表）
- type: depends_on
  target: K0030
  note: 5×5/6×6の出版分布を較正対照として完全再現
- type: depends_on
  target: K0057
  note: 禁止四点組カタログのアンカー（F_5=826,F_6=2491,F_7=6364）
- type: depends_on
  target: K1221
  note: SAT全解列挙のlex-leader機材規約（enc_sat2 v2.1）
- type: contrasts
  target: K0032
  note: n=8カタログ408配置・51軌道との対照点（n=7は16配置・2軌道）
- type: related_to
  target: K1220
  note: n=10十石witness既知類数（≥5・不全）との規模対比
artifacts:
- path: research/experiments/n7-seven-stone-maximal-catalog-20261122/README.md
  role: source
  note: 主張・方法・検証・trust boundary
- path: research/experiments/n7-seven-stone-maximal-catalog-20261122/output/classify_n7.json
  role: data
  note: 16配置全リスト・軌道分類・特徴
- path: research/experiments/n7-seven-stone-maximal-catalog-20261122/output/verify_catalog_n7.json
  role: verification
  note: 独立幾何検証・SAT照合・詳細記録
- path: research/experiments/n7-seven-stone-maximal-catalog-20261122/output/sat_enum_n7k7.json
  role: verification
  note: at-most-7 SAT全解列挙2モデル（n7k6は0モデル=UNSAT再照合）
- path: research/experiments/n7-seven-stone-maximal-catalog-20261122/scripts/enum_catalog.mjs
  role: verifier
  note: DFS完全列挙器（健全性/完全性スケッチ込み）
- path: research/log/2026-11-22-n7-seven-stone-maximal-catalog-session-log.md
  role: history
  note: 経過・規約読み違いの訂正・採番調整
---

# 7×7の7石極大安全配置の完全カタログは16配置・2 D4軌道

標準共円盤（q=4）の 7×7 盤について、7石（= s_7）の極大安全配置を完全列挙した。
**全16配置、D4軌道はちょうど2つ**（両軌道サイズ8・安定化群位数1）。

- 軌道O1代表（石リスト辞書式最小・点番号 c=x+7y）: `[1,9,22,23,27,44,45]`
  — K0031 の出版証人そのもの。O2代表: `[3,10,22,23,30,32,38]` — 既刊に明示
  witness のない軌道（新規記録）。SAT符号化規約（指示ベクトル 0<1 辞書式最小）の
  代表は O1: `[10,13,14,17,19,21,45]`、O2: `[18,21,22,26,31,32,38]`。

機械検証の backbone:
1. 禁止四点組カタログが出版 census 機材（K0057 アンカー自己検証）と独立 Python
   検出器（全 C(49,4)=211,876 組み合わせ・Leibniz 4×4 行列式）で byte 一致
   （F_7=6364・正準テキスト sha256 `7bf55548…`）。
2. DFS 列挙器（増分 cov 計数・健全性/完全性スケッチ実験README §2）が
   K0030 出版分布を行単位に完全再現（n=5 k=5..8 = 4/1,136/11,280/4,340、
   n=6 k=6..8 = 8/3,952/115,496・7行全一致、6×6 k=8 本体は sha256 記録のみ）。
3. n=7 k=7 の 3 shard（first stone 分割・計 38,798,535 nodes・決定性再現
   cfg 行 byte 一致）が 16 配置を返し、k=3..6 は全て完全負 → **本機材による
   s_7=7 の完全再導出**（K0031 の値更新ではない）。
4. 全16配置が独立幾何（Leibniz）と出版 pinned verify_witness.py の両方で
   SAFE+MAXIMAL。一石除去 112/112 で極大が破れる（6石極大安全との整合）。
   K0031 証人含有・tamper 対照 9/9 拒否。
5. SAT 全解列挙（v2.1 lex-leader + kissat ブロッキングloop）が 2 モデルのみ
   （いずれも7石）で DFS 側軌道代表と完全一致、n7k6 は 0 モデル（UNSAT）。

特徴量は n=8 出版カタログ（round10・K0032/B371）で意味論検証済みの同一パイプライン
（ecc 出版値 51/51 一致・「一方向だけ24個」再現）で計測:
- 全16配置が三点共線を持つ（B371 の n=7 版: 真）。ただし「三点共線1組のみ」
  配置は存在しない（n=8 には24個 → B372 の n=7 類似は偽）。
  トリプル数 {2:8, 3:8}・方向数 {2:8, 3:8}・ecc {12:8, 13:8}。
- 最小極大 witness の軌道数の列: n=5:1（安定化群位数2）→ n=6:1 → **n=7:2** →
  n=8:51 → n=10:≥5類既知（不全）。n=7→n=8 の急増（2→51）が確定データ点。

trust boundary: 完全性は健全性/完全性スケッチ + 有限較正全一致 + 独立SAT全解
列挙一致に基づく有限計算の主張（形式的証明ではない・実装と言う trust を含む）。
6×6 k=9..11 の較正行と n=9/n=10 カタログは未実施。n=9 以上への外挿をしない。

標準 11×11 空盤・二石 root・S2・class 1/2/4 は本成果と無関係に UNKNOWN のまま。
