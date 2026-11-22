# 2026-11-21 五行 q6/q5 m=23/m=27 sd≤6 前線サージェリー・セッションログ

高速レーン。宣言 `research/log/2026-11-21-five-row-q6-q5-m23-m27-sd6-surgery-single-owner-note.md`
（commit `ac118f45`、宣言時 HEAD `bab006adc7`）に基づく単一オーナー実装・実行・公開。
対応実験: `research/experiments/five-row-q6-q5-m23-m27-sd6-surgery-20261121/`。

## 経緯

- 前セッション（同日内）でツール取得・census ゲート・シード健全性・自己補完対照・
  q6 id@0 (3,3) の実測（5,162,142 leaves @ 37.8s・0 witness）まで進んだ状態で、
  12実行を单一 bash に束ねたキャンペーンが 300s 上限で環境リセットを起こし
  `/home/user/work` 下の中間成果を喪失。実験ツリーを knowledge 配下
  （リセット耐性あり）に再構築して全工程を最初からやり直した。
- 再構築は完全再現: q6 id@0 の leaf 数 5,162,142 はリセット前実行と一致
  （決定論の二重確認も兼ねる）。ただし独立 Python 検証器 `verify_general.py` に
  **重大バグを発見・訂正**（円の点数え上げが中心一致を数えていた。r² 比較に修正し、
  合成 r=5 円 tamper で陰性（UNSAFE 検出）確認済み。旧版は seed の安全 PASS は
  Nagative 側では無力だった点、訂正後に再検証）。

## 較正・対照（全て PASS・実験 output/ に記録）

1. C4 census 完全性 @ (5,12,6)/(5,15,5)/(5,23,6)/(5,27,5): 212/629/996/2355 曲線、双方向差 0。
2. シード健全性: m=22 witness・m=26 witness がホーム盤で sat.js verifyConfig + 修正済み
   Python Fractions 検証器 + safety_only.js（新規・sat.js primitives のみ）の3系統 PASS。
3. 改ざん対照: r=5 円 6点/5点 → 全系統 UNSAFE/FAIL。not-maximal 対照: 対象盤に置いた
   シードは not-maximal で FAIL（22,0)/(26,0)）。※ tamper seed 最初の版に円外誤点が
   あったのを検出・修正したことも記録（数え上げ系の陽性対照の重要性）。
4. 自己補完陽性対照: minus2 シード → q6 は公開 witness + 近傍3つ（計4）、q5 は公開 witness 唯一。

## 主成果

- **矩形対称性クラス簡約（補題・全称）**: 手術列挙クラス・census・safety・maximality は
  矩形対称群で不変。span s の bbox 鏡像では id@t = H@t = V@(m−s−t) = HV@(m−s−t)。
  したがって 12/32 配置は 3/8 類に崩壊。宣言グリッドを全実行して機械検証:
  **全 44 実行でクラス内4実行の key invariant が完全一致（11/11 クラス）**。
  failStats の帰属のみ列挙順依存で差異。将来の bbox グリッドキャンペーンは代表点のみで
  1/4 の計算で済む（11x11 系にも有効な枝刈り）。
- **(5,6) 5x23 sd≤(3,3) 完全負**: 12配置 61,871,100 final-state leaves、0 maximal、0 witness。
  公開 sd≤2 negative を sd≤6 に拡張。
- **(5,5) 5x27 sd≤(3,3) 完全負**: 32配置 112,307,168 leaves、0 maximal、0 witness。
  同様に sd≤2 → sd≤6 拡張。
- 合計 174,178,268 leaves。両方とも「不在主張ではない」局所負（README のクラス記述通り、
  deficit 曲線外の自由削除は機械設計によりスコープ外）。
- M 境界不変（M_{5,6} ∈ [23,249], M_{5,5} ∈ [27,336]）。witness なしのため csv の
  M 列は変更なし、note/source 列のみ拡張（行全体置換・同時刻 main を再取得して適用）。

## 次の実行可能課題（このレーンの後継候補・宣言必要）

- sd≤(4,3)/(3,4) 部分クラスの絞り込み（4追加系の nP は supported で machine はそのまま
  動く; leaf 数は約 maxP 倍増で単発 2-3 分 の予想）。
- 異種シード（q6 なら m=21 witness とその3変種、q5 なら m=25 witness）由来の
  对象盤手術。witness jump ≥14 石の先行観測と整合するなら負が続くと予想。
- 今回の対称性補題の K 昇格案（実験1回につき K を作らない規約に従い、
  bbox グリッドレーン全体の方法論として次回統合時に提案）。

## 運用メモ

- bash 1呼び出しに手術 2〜3 実行（各 36〜38s）まで。4 実行を含む batch は 300s 危険域。
- 環境リセット後は `/home/user/work` は消える。実験ツリーは knowledge 配下 kit に
  置いてから実行する設計が正解だった（今回の再構築 7 分で済んだ）。
- push_files の BOOL 報告はあてにならない: push 後必ず HEAD/blob で fetch-back 検証。
