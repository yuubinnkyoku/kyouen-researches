# 2026-11-17 W39: SAT側深掘り段のパイロット実装＋限定実行

成果物は本log 1件のみ（push なし・長時間探索なし・知識項目変更なし）。
数値はすべて実測ファイル（`output/walksat-deep-pilot-20261117*/`下のJSON / log）からの転記。
推測には `[INFERENCE]` を付ける。

## 0. 出典

- W35 設計: `research/log/2026-11-17-a2647-sat-side-deep-design-omp.md`（D1 = Tier 1
  {602, 1166, 488, 717, 147} × 6 seed ペア × noise 0.1/0.2 ≈ 12.8 h。再起動耐性は
  (d, seed, noise, run) 単位の分割保存で）
- W32 パイロット: `research/log/2026-11-16-a2647-sat-side-pilot-omp.md`（評価器 3 系統
  検証、λ=1000 必須の経緯、10^6 flips での最良違反 20〜44）
- 実装: `research/experiments/parabola-ternary-selection-20261109/walksat.cpp`,
  `walksat_pilot.py`

## 1. 実装（walksat.cpp / walksat_pilot.py の差分）

W35 §5 の設計どおりの最小差分。評価器の意味論（全要求一致で違反）は W32 で
検証済みのものをそのまま流用し、変更していない。

walksat.cpp（SHA-256 `52eacd159bb172dfa263bbd3618ffb7559b7e2040c9d879106f1c4a4e03a058e`）:
- `--restart-every N`（N flips ごとに初期化し直す再起動。初期状態は warm → random 交互、
  `--init` が無い場合はすべて random）と `--stagnation N`（global best が N flips
  不更新でセグメント打ち切り、予算内で再初期化して継続）を追加。
- best 状態は改善のたびに `--best-state` へ flush（VM 再起動で直近 best が消えない。
  最終行出力前に再 flush）。
- trace 出力に `restart <n> <flipsRun> <viol> <empties> <W|R>` 行（再起動境界）を追加。
- JSON 出力に `flips_run`, `restarts`, `init_per_restart` を追加。

walksat_pilot.py（SHA-256 `fb584eec83623eabf52ad8342104989598d2acd939eea4a39bba49fcd13ccc25`）:
- `deep` サブコマンド: 1 ユニット = (d, seed, noise, run) = `--flips-per-run` flips
  （D1 では 10^7）。run 偶数 = warm、奇数 = random（W35 §2 の交互政策を
  プロセス単位で実装。per-unit seed = `seed * 1000003 + run` で再現可能）。
- 各ユニットの result は `deep-d{d}-seed{s}-noise{n}-run{rr}.json` に **アトミック書き込み**
  （tmp → rename）。VM 再起動で失うのは実行中ユニット 1 件まで。
- `--resume`: 存在するユニット JSON はスキップ、未完ユニットから再開。ブロック内の
  streak（d 単位 global best 不更新回数）は `block_progress` が既存 JSON を run 順に
  replay して再構築するので、resume が streak を失わない。
- `--block-patience N`（既定 3）: streak 到達で `deep-stop-…-seed…-noise….json` 停止
  マーカーを書いてその (d, seed, noise) ブロックを打ち切り（W35 §2）。
- `--max-seconds S`: ジョブ上限。到達時は実行中でないユニット境界で cleanly 終了
  （`stopped_by_time_cap` を summary に出力）。残りは同じコマンドの resume で継続。
- `solved=true` があれば候補点列を保存して即終了（§4 の W35 手順入口）。
- `deep-report` サブコマンド: 完了ユニットの集計（fps 分布、d 別 best、予算投影）。

実行バイナリは experiment 内 `output/…/bin/walksat` にビルドした。

## 2. 評価器の再検証（d=602）

W32 と同一手続きを深掘り版でも実施: walker (`--eval`) / literal 検査器 /
encoded 検査器の 3 系統一致 + 保存済みラダー CNF との base 接頭辞一致。

- 結果: `output/walksat-deep-pilot-20261117-w39/eval-check/eval-check.json`
  および `-w39b` 側も同じ: `{"all_ok": true, "states_total": 10,
  "saved_cnf_prefix_match": {"602": true}}`（10 状態 = warm 1 + random seed×3×3）。

## 3. 限定パイロット実行（d=602）

指定どおり、Tier 1 先頭 d=602、warm と random 各 1 seed（seed=1）、
各 run 10^7 flips（W32 の 10 倍）、λ=1000, bound=3, noise=0.1。
正本ディレクトリ: `output/walksat-deep-pilot-20261117-w39/`（同一パイロットの再実行
`-w39b`, `-prev-1509`, `-w40/pilot` は**同一設定で best_step も byte 同一**
  （run00: best_step 1,869,263 / viol 19、beststate も `cmp` で一致）を確認した
  決定論性チェック[INFERENCE: 二 volatility を排除できたという意味]）。

- run00 (warm, seed 1·1000003+0): **base_violations_best = 19**, empties 3,
  best_step 1,869,263, 58.0 s, **fps 172,403**, restarts 1。
- run01 (random, seed 1·1000003+1): **base_violations_best = 21**, empties 3,
  best_step 9,751,830, 41.1 s, **fps 243,145**, restarts 1。
- 両ユニットとも `solved=false`。空数は best で 3（bound ちょうど）を維持。

### 3.1 観察

- **10^6 → 10^7 で best 違反 20 → 19 に改善**（W32 の d=602 最良は 20）。
  run00 の best_step が 1.87M（= 10^6 flips 予算外）なので、予算 10 倍が効いた
  改善である。ただし改善幅は +1 で、「違反が一桁へ減る」という W35 §3 の
  期待が満たされているわけではない（1 ブロック 2 ユニットの限られた観測[INFERENCE]）。
- 10^8 flips（10 runs × 10^7）フルブロックをまだ実行していない。上記はブロック先頭
  側のみ（本パイロットの指定範囲どおり）。

## 4. 実測速度と W35 見積もり判定

- パイロット 2 ユニット実測: fps 172,403 / 243,145。
- テスト一式を含む d=602 の 10^7 flips ユニット 24 件（kill-test, cap-test,
  resume-test, blocktest デモ 500k flips 2 件除く実測）の分布:
  **min 102,919 / median 195,628 / max 243,145**。低fpsのものは他ジョブ並走時の
  実測（kill-test で 103k 級）で、単独時は 165k〜243k。
- W32 の 1M flips ラン（128k〜217k, median 167k）と比べ、10^7 flips 単独ランでは
  cache効果低下は見られず、むしろ単独時のmedianは上积み気味[INFERENCE]。

W35 の見積もりは保守 130,000 fps で D1 = 6×10^9 flips ≈ **12.8 h**。

判定: **合わないとは言えないが、 busy 時の実測 min が 103k まで下がるため
130k 保守値は維持しつつ実際の計画は幅を持たせるべき**。

修正見積もり（D1 上限値 = 600 ユニット × 10^7 flips 全部走り切る場合）:
- 実測 min 102,919 fps（並走時）で **16.2 h**。
- 単独時 median 195,628 fps で **8.5 h**。
- 単独時観測で妥当な計画保守値 110,000 fps → **15.2 h**。
- ただし block-patience 3 が効くので実際は 10^8/block を使い切らない打ち切りが
  出る可能性があり、これらは上界[INFERENCE]。

**修正結論: D1 の計画値は 12.8 h から 8.5〜16.2 h（代表値 ≈15 h）へ広げる。
  VM 再起動を挟む運用で --max-seconds ジョブ分割する前提なら 16 h 見積もりで
  進め、早く終われば D2 を前倒しとする。**

## 5. 再起動耐性の実テスト（指定validation）

1. 通常再開: `output/walksat-deep-pilot-20261117-w39/resume-test/`
   （seed=7）: `--resume` 再実行で run00 は既存 JSON を skip、run01 から継続、
   正常に完了。`-w39b` 側でも同内容（viol 19 / 21 再現、既定どおり）。
2. `--max-seconds` 打ち切り: `output/walksat-deep-pilot-20261117-w39/cap-test/`:
   時間上限で cleanly 終了、完了ユニット JSON は保存済み。
3. SIGKILL 強制終了（VM 再起動相当）: `walksat-deep-pilot-final-20261117/resume-test/`:
   job1 は run01 実行中 walker プロセスごと SIGKILL（`resume-test.job1.log` の
   traceback = `Signals.SIGKILL: 9`）。run00 の JSON は無事保存済み。job2 は同一
   `--resume` コマンドで起動し、run00 を skip して run01 を再実行、2 ユニット完走
   （`resume-test.job2.log`: viol 21 / 20、`job_seconds 84.6`）。
   **kill で失われたのは run01 のみ、中断ユニットの切れ目から再開できた。**
   `resume.pid`（1073741834）は killed された job1 の PID。
4. block 停止マーカー: `walksat-deep-pilot-20261117-w40/blocktest/`
   （500k flips/unit の短縮デモ）: streak 1 で run01 が run00 の best（32）を
   超えられず `deep-stop-…-seed1….json`（streak 1, next_run 2, d_best 32）が
   書かれた。実運転では patience=3 で同様に動く。
5. best flush: `walksat-deep-pilot-20261117-w39b/test-restart-best.txt` は
   run00 の `--best-state` 途中断片で、viol 24 / empties 3 を `--eval` で確認できる
   （= walker が kill されても flush 済み best 状態だけは正しく読める）。

## 6. フル D1 投入手順（再現可能コマンド）

前提: d=602 の problem / warm が事前生成済み。他 d は `deep` が初回実行時に
generate する（`problem-d{d}.txt`, `warm-d{d}.txt`）。

```sh
cd research/experiments/parabola-ternary-selection-20261109
# 事前ビルド・評価器検証（1 回だけ）
g++ -O2 -o output/walksat-d1-20261117/bin/walksat walksat.cpp
python3 walksat_pilot.py check-eval --ds 602 1166 488 717 147 \
  --seeds 1 2 3 --states 3 --output output/walksat-d1-20261117/eval-check \
  --exe output/walksat-d1-20261117/bin/walksat \
  --cnf-dir output
```

（`check-eval` は `--output` 直下に eval-check.json を書く。all_ok true を確認。）

ジョブ起動（1 ジョブ 90 分 = 5400 s 上限で VM 再起動前に切る）:

```sh
nohup python3 walksat_pilot.py deep \
  --ds 602 1166 488 717 147 \
  --seeds 1 2 3 4 5 6 \
  --noises 0.1 0.2 \
  --runs 10 --flips-per-run 10000000 \
  --lam 1000 --bound 3 \
  --block-patience 3 --max-seconds 5400 \
  --trace-every 1000000 \
  --output output/walksat-d1-20261117 \
  --exe output/walksat-d1-20261117/bin/walksat --resume \
  >> output/walksat-d1-20261117/job.log 2>&1 &
```

再起動後の再開: **上の起動コマンドをそのまま再実行するだけ**（同一コマンドである
こと。`--resume` あり）。runner が:

- 完了済み `deep-d{d}-seed{s}-noise{n}-run{rr}.json` を skip
- `deep-stop-…` マーカーのある (d, seed, noise) ブロックごと skip
- 停止マーカーの無いブロックについて `block_progress` が停止・再開前の streak を
  replay 復元し、**未完の最初の run 番号**から walker を起動
- 途中で kill されても欠けているのは実行中だった 1 ユニットの walker 結果のみで、
  walker の best-state は改善毎に flush されている

進捗確認（いつでも）:

```sh
python3 walksat_pilot.py deep-report \
  --ds 602 1166 488 717 147 --seeds 1 2 3 4 5 6 \
  --noises 0.1 0.2 --runs 10 --flips-per-run 10000000 \
  --output output/walksat-d1-20261117
```

`deep-report.json` に完了ユニット数、d 別 best、fps 分布、全単位投影が出る。
`solved=true` があった場合は `deep` が即終了し W35 §4 の手順（best → candidate →
`verify_subset.cpp` 独立幾何検査 → A(2647)=1322 確定判定）に入る。

## 7. まとめ

- `deep` runner（(d, seed, noise, run) 単位の分割保存・resume・block-patience・
  時間上限）と walker の restart/stagnation 機能を実装した。d=602 で評価器 3 系統
  再検証 all_ok=true。
- 限定パイロット（d=602, warm/random 各 1 seed, 10^7 flips）: 最良違反 
  **19**（warm, best_step 1.87M）と 21（random）。10^6→10^7 で 20→19 に 1 改善、
  solved なし。
- 再起動耐性は実テストで確認: SIGKILL で実行中ユニット 1 件のみ損失、
  同一コマンド resume で正確に継続、best-state 途中 flush 有効。
- 実測 fps 102,919〜243,145。W35 の 12.8 h（130k 前提）は busy 時の min 実測に対して
  楽観側なので、D1 の計画値は **8.5〜16.2 h（代表 ≈15 h）** に修正。
- UNSAT の根拠は何も得られていない（W35 §4 の境界の継承）。

（完）
