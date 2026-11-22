# 7×7 極大安全配置 k=8 行の非空虚判定と bounded census（2026-11-22）

単一オーナー宣言: [2026-11-22-n7-rows-k8plus-sat-single-owner-note](../../log/2026-11-22-n7-rows-k8plus-sat-single-owner-note.md)。
セッションログ: [2026-11-22-n7-rows-k8plus-sat-session-log](../../log/2026-11-22-n7-rows-k8plus-sat-session-log.md)。

標準共円盤（q=4・禁止四点組=同一線上または同一円上の4点）の 7×7 盤について、
**石数ちょうど k=8 の行（8石極大安全配置全体）の非空虚** を機械完結で確定し、
**最低でも331個の D4 軌道**（bounded enumeration・完全性は不主張）を独立検証した。
7×7 の8石行はこれまでどのレーンでも触れておらず、本実験が最初の記録である
（K0030分布は6×6まで、K1224は7石行、K1225は3×3〜6×6全行）。

## 結果（有限計算・機械検証）

1. **7×7 の k=8 行は非空**（初の8石極大安全配置の明示 witness）:
   - witness（石の (x,y) 座標・辞書式最小 indicator-vector lex-leader）:
     `[[3,2],[5,2],[1,3],[5,3],[6,3],[0,4],[2,4],[3,4]]`
     （cell index c = x + 7y では `[17,19,22,26,27,28,30,31]`）。
   - **M_7 ≥ 8**（7×7 の極大安全配置の最大サイズの下界。これまで M_7 は
     M_7 ≥ s_7 = 7 しか知られていなかった）。
   - 2ショット（default と `--shuffle=42` の独立変数順序）とも SAT で同一 witness。
     単価は default 0.37s / shuffle 0.39s。
2. **8石行の D4 軌道数は ≥ 331**（bounded census・完全性不主張）:
   lex-leader 全列挙を 230 秒の壁で打ち切り、331 leader を列挙。
   331件すべてを独立 Python 検証器（Fraction 4×4行列式・3点共線と円を同一視する
   DELETE-oracle）で再検証: **331/331 SAFE+MAXIMAL、331/331 が自分の軌道の
   indicator-lex-min、重複軌道ゼロ**。軌道サイズは 8 が 330 件・**4 が 1件
   （安定化群位数2・180度回転で固定される初の8石行配置）**。
3. **構造特徴**（331 leader のみ・全体ではサンプル）:
   - 三点共線トリプル数ヒストグラム: {0:2, 1:34, 2:119, 3:131, 4:36, 5:8, 6:1}。
     **trip=0（三点共線を持たない8石極大安全配置）が2軌道存在**
     `[10,12,15,20,25,27,42,45]`・`[10,12,14,23,39,40,45,46]`
     — 7石行の全16配置が三点共線を持つ（K1224）ことと対照的。
   - 方向数ヒストグラム: {0:2, 1:40, 2:126, 3:123, 4:36, 5:3, 6:1}。
   - 安定化群位数2 の配置: `[3,6,14,19,29,34,42,45]`（180°回転 (x,y)→(6−x,6−y) で
     3↔45, 6↔42, 14↔34, 19↔29 と不変）。

## 方式と健全性

- 符号化: 出版正本 `enc_sat2.mjs` v2.1（S1 safety 4リテラル節・Z完全Tseitin・
  per-cell maximality・LX完全二方向 lex-leader 鎖・S4 Sinz at-most-k）。
  n=7 k=8: 26,240 変数・111,105 節。census anchors は K0057 出版値
  （F=6364, D=660, C=5704）と一致。
- **行/umd判定方式（leader blocking）**: at-most-k のモデルで石数 ≤7 のものは
  K1224 出版カタログ（16配置・2軌道）により O1 `[10,13,14,17,19,21,45]` と
  O2 `[18,21,22,26,31,32,38]` の2つの lex-leader に限る。この2割当を禁止する
  7リテラル節2本を付加した CNF のモデルはちょうど8石。UNSATなら行は空、
  SATなら witness。「極大安全族は反鎖」等の構造補題は使わない。
- 較正（acceptance condition 1）:
  - ブロックなし at-most-7 は SAT でモデルは O1 そのもの（24.8s・陽性対照即命中）。
  - O1・O2 をブロックした at-most-7 は **UNSAT**（51.8s）: ≤7石モデルが
    O1・O2 のみであることを本環境で再導出（出版カタログのモデル水準再現）。
- kissat 4.0.4 は公式 linux-amd64 binary を md5 `3a5eba830aa6008a604fcc9bbe99a325`・
  sha256 `21da5d98…93a1` でピン（repo内再出版なし・n7カタログ実験と同一 binary）。
- CNF 本体は非刊行（サイズ方針）で、sha256 を `output/determinism.json` と各 meta に
  ピン。決定的再生成手順は determinism.json 記載のとおり。
- census の決定性スポット検査: 空の状態から再実行した先頭20反復の leader 列は
  本走行と完全一致（`output/detcheck_k8_prefix20.json`）。

## 検証（acceptance condition 3）

- witness は出版正本 `verify_witness.py`（整数 4×4 行列式・独立実装）で
  SAFE+MAXIMAL（70四点組すべて安全・41/41 空点 blocked・各空点の証人トリプル明示）。
- tamper 対照: 8石それぞれの1石除去がすべて SAFE かつ NOT-MAXIMAL
  （未カバー点 3〜13 個・`output/tamper_k8_summary.json`）。
- census 331 leader の独立検証: `scripts/verify_census8.py`（幾何oracleの単体検査込み:
  円・直線・非共円・正方形＝共円の4事例で全PASS）で 331/331 SAFE+MAXIMAL・
  軌道lex-min・重複なし。O1/O2 を含むリーダー0件（整合ゲート）。

## 非主張

- census は打ち切り（331 leader・列挙239秒超過で継続予算なし）。**8石行の軌道数は
  ≥331 が正しく、spanning census ではない**。trip/dirs/stab の各ヒストグラムは
  「331 leader についての値」であり行全体ではない。
- M_7 の上界は扱わない（k=9..13 行は未着手・UNSAT を1つも得ていない）。
- 行の非空虚・witness・各leaderの配置検証は有限計算であり形式証明ではない
  （実装・kissat・符号化の trust 込み・K1224 と同水準）。
- 標準 11×11 空盤・二石 root・S2・closure class は本レーン非接触で UNKNOWN のまま。

## ファイル

- `scripts/block_lift.mjs` — leader ブロック節付加（shuffle 変数順序の完全再現込み）
- `scripts/census8.mjs` — lex-leader bounded 全列挙（resume 対応）
- `scripts/verify_census8.py` — census leader の独立幾何・軌道検証
- `pinned/` — census.mjs / enc_sat2.mjs / decode_model.mjs / verify_witness.py
  （いずれも n7カタログ実験 pinned と byte 同一）
- `output/` — 各種 meta（CNF sha256 ピン込み）・解・witness・tamper・census state・
  検証記録・determinism.json（MANIFEST-sha256.txt に全 file の sha256）
