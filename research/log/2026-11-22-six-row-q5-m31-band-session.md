# 2026-11-22 six-row (6,5) 6×31 band extension session log

高速レーン・(6,5) 帯延伸セッション（単一オーナー）。宣言 `bc11e28b`
（2026-11-22T01:05Z付近・宣言時HEAD `bcc39add`・受入条件は宣言ノート参照）。

## タイムライン（概算・UTC）

- 00:57–01:06 前セッションからの続行: staging kit（`_q65-band-m31plus-kit`）のcensus
  （c000..c014・pool.json・maxw=50）とunblocked ranking（w32/w33）が既に確定済み、
  witness候補（L2+1並進）は3系統検証済みの状態から開始。
- 01:05 宣言ノート push（`bc11e28b`）。
- 以降、本セッションの実行:
  1. `surgery_deep.js` 新規作成（core は surgery_gen.js と byte-verbatim・
     remKadd0/add1 完全クラス + rem3add2 targeted-complete + per-base/16-removal checkpoint。
     構文・ロジック修正: truncation 経路の stats 欠落、resume 後の complete 判定バグ
    （endIdx で追踪）、rKa1 クラス一般化、remKadd0 による再加算還元の閉包。
     最終 sha256 `851e5b7b…`）。
  2. 6×32 close bases 設定（`config_w32_deep_v1.json`・≤2 unblocked 10 base・
     最良 c009@off3 は unblocked 1 = (31,5)）と u3 設定（`config_w32_u3.json`・≤3 unblocked 24 base）を構築。
  3. c009@off3: r0s/r1a1/r2a1/r3a1/r4a1 完全走査 → 全陰性。
     t2（rem3add2 targeted-complete）: D(31,5)=74 → 9,731 pair × 1,771 removals =
     17,233,201 候補 → **0 witness**（180s budget × 3呼び出し・環境リセット1回を
     checkpoint resume で吸収）。c009@off3 の ≤4R≤1A + 3R2A 編集近傍は完全陰性。
  4. 24 base 全てで r0s/r1a1/r2a1/r3a1/r4a1 完全走査 → 全陰性
     （検証速度 ~20.5µs/candidate・r4a1 1.5M候補/base）。
  5. witness 出版ゲート再実行（`run_verify_suite.sh`・run A/B byte 一致）:
     3系統 PASS・tamper×2 全系統 FAIL（tamper1 は maxcirc 5 で unsafe 可視化）・
     5同行 FAIL・L2 6×30 陽性対照 PASS。
  6. 統合機械記録（`output/verify-w6x31-three-systems.json`・
     `translation-census-summary.json`・`w32-bounded-edit-negatives.json`）作成。
  7. 出版: 実験dir・K1216・README bullet・本ログ。

## 結果

- **M_{6,5} ∈ [32,658]**（6×31 witness 出版・下界のみ）。
- 単一石集合で幅[26,31]の6連続 staircase（(6,5) 単一集合記録更新）。
- 6×32: 24 base × (rem k≤4 add1・完全) + c009@off3 の 3R2A targeted-complete 全陰性。
  UNDETERMINED 不変・不在主張なし。

## 残作業（次回実行への引き継ぎ）

- **6×32 t2 resume**: `config_w32_u3.json` の残り23 base（`surgery_deep.js <cfg> <i> <j> t2`・
  budget 180s/呼び出し・`output/w32-u3-scan/base-XXX.t2.part.json` から resume）。
  続き: c009@off4（1 target）→ c009@off2/off5（y=5 2連target・pair制約強く有望）→ c008/c011群。
- **6×33**: `unblocked_w33.json` 既にcensus済み（最小 unblocked 2・c009@off4 等）。
  6×32 で配山した base の D4/offset 対応から設定構築可能。
- t2 の理論的 straightforward 拡張: rem3add3 targeted（23石 witness・D制約+第2 add自由は候補爆発の
  ため別の絞り込みが必要）。
- 次の独立課題候補: 13×13 k=11 witness hunt（`_s1213-lane-kit`）、r4a2 級の込み入った手術。

もっとも価値が高いのは 6×32 t2 の消化（21/22石 witness は成立すれば即下界更新）。

## 備考

- 1回の実行環境リセット（290s timeout）が発生したが per-class checkpoint 設計で成果は無事。
  以降 bash 呼び出しは 180–290s budget + resume で運用。
- 並走レーンは n11 s4bd のみアクティブ（01:33Z HEAD `2b7b4db`）。他レーンの占有物
  （(6,6) m=25 crunch・(6,7) 6×22）には非接触を維持。
- 今回の K 番号: K1216（HEAD `2b7b4db` 時点で未使用を確認済み）。
