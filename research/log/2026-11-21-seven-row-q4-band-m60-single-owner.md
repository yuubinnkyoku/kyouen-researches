# 単一オーナー宣言: 7行 q=4 witness band の m≥60 延伸（近傍列挙・seeded SA・有限構成）

- 宣言時刻: 2026-11-21T11:35Z
- 宣言時 HEAD: `e0d072fb52aa92af35dafa3e3c371cf7d3781fa8`
- レーン: 高速レーン（自実行）
- 前段: K0827 は現在 **M_{7,4} ∈ [60, 1929]**（7×4..7×59 に行欠損極大安全配置・上界は K0068 の T_7 = 1929）。
  幅59は width59-two-swap レーン（2026-11-15）が幅53証人の 2-for-2 近傍完全列挙で構成済み。
  同レーン README が明記した次の実行可能課題「**幅59証人の3-for-3近傍、または幅60の新しい基礎配置探索**」
  （3石以上の交換・別の基礎配置・別の行占有率型は未調査）を本宣言の対象として取得する。

## 対象・手段（すべて有限的な witness 存在探索のみ）

1. **既刊 witness pool に対する 2-for-2 近傍の完全列挙**を幅 60..63 で実行する
   （基礎配置 pool: SA 6基礎 42/44/45/47/50/53 + 7×57 2証人 + 7×59 証人 + sat3 36..41 証人）。
   2-for-2 列挙器は pinned `audit_two_swap.cpp`（md5 `cdcc3649…`）と同じ包除原理・整数幾何判定を
   Node.js で独立実装し、**出版計数（base53@57 2件・base53@60 0件・B59@60 0件・capacity/safe候補数）との完全一致を較正**
   してから本番に使う。
2. 拡張ムーブ: **1-for-0**（19石型 [3,3,3,3,3,2,2] の直接極大性判定）、**3-for-2**（19石型: 行1..2の欠損配置）の完全列挙、
   および追加セル位置を制限した **restricted 3-for-3** 近傍。
3. **seeded deterministic SA**（pinned `search_seeded.js` md5 `a2ba8427…` を原版どおり使用・複数 seed・長時間 budget）
   による幅 60+ の新基礎配置探索。
4. 発見された witness は **空列延伸チェーン**でさらに延伸できるか機械確認する。

## 受入条件（本レーンの出版は以下を満たす場合のみ）

1. pinned 原版（scripts 7種・既存 witness/output 群・md5 台帳どおり）は 1 byte も変更しない。
   新規ツール・出力は新規実験 dir `research/experiments/seven-row-q4-witness-band-60plus-20261121/` のみに置く。
   既存実験 dir への追記はしない。
2. witness の独立性: 列挙器/探索器とは独立した (a) 正規化整数直線・円方程式による Python 検証器
   （pinned `verify_witness.py` 方式の一般化・新規ファイル）と (b) 第三系（整数外積・4点行列式の別実装）の
   2系統で safe + 極大 + 行欠損を検証。浮動小数点は使わない。
3. 主張は「有限幅の witness による下界更新」のみ。**幅60以上のいかなる不存在主張もしない**。
   近傍列挙の 0件結果は列挙範囲を明記した honest negative として記録する。
   M_{7,4} の上界 1929 は不変。witness band の幅単調性は主張しない。
4. K0827 の更新（title の band 上端と artifacts 追記）は m ≥ 60 の witness が独立検証を通過した場合のみ行う。
   不発の場合は session log に honest negative として残し、K 番号・K0827 は更新しない。
5. 他レーンの着手宣言ファイルに触れない。m32 治具拡張(`3aa6fb7f`)・four-row q5 m23 class-split(`d92c8f51`)・
   three-row q4 blocking-counting(K1202)・MIN_MAXIMAL・knowledge corpus 修理(`c035d99a`)・n11 系はすべて非接触。
6. 出版は part 分割・各回 fetch-back byte 照合。push 直前に必ず最新 main を再取得し、
   push 競合・取得失敗時は無理せず状況を記録して次回へ回す。
7. 標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は本レーンと無関係で UNKNOWN のまま。
   nodes・conflicts・探索回数を勝敗として読まない。

## 想定する成果物

- 新規実験 dir: README（結果・方法・較正・限界・再現手順）、scripts/（JS 2-for-2・拡張ムーブ列挙器、
  Python 検証器、seed 一覧を固定した SA 実行記録）、output/（列挙結果 JSON・witness JSON・検証 JSON・honest negatives）。
- 進展があった場合: K0827 更新 + 研究ログ（session log）+ knowledge README の該当行（固定幅Bullet の
  M_{7,4} 区間表記）の最小限更新。不発の場合: session log のみ。
