# seven-row-q5-q8-sat-frontier-20261115

IN FLIGHT (claim) — 高速レーン。7行 q≤w 族の各 witness 帯前線
（(7,5) 7×33・(7,6) 7×28・(7,7) 7×27・(7,8) 7×25）を sat3.js streaming census +
kissat 4.0.4 で SAT 探索し、SAT なら witness を dual-verify して下界を更新する。
INDET は honest negative として記録し不在主張とはしない。

## 現在の境界（着手時点・main）

- (7,5) ∈ [33, 1142]・witness 帯 m=5..32（7×32 は rowY=0 分割 SAT・129,923 conflicts）
- (7,6) ∈ [28, 862]・witness 帯 m=6..27（7×27 は rowY=3 分割 SAT・230,973 conflicts）
- (7,7) ∈ [27, 708]・witness 帯 m=7..26（7×26 は rowY=3 分割 SAT・1,951,966 conflicts）
- (7,8) ∈ [25, 651]・witness 帯 m=8..24（7×24 は rowY=3 分割 SAT）

上界はいずれも K0318 substitution（w7_upper_bounds.json）。

## 手法

- 生成器: sat3.js（q≤w 全三つ組census・streaming 節出力。
  `seven-row-q4-extension-band-sat3-20261115/scripts/sat3.js` md5
  18ab1e432bf85f293015922898bb765d を再利用・commit しない）。
  sat.js md5 0cc6021a4e523a0d7f4d5ea0f5f5d40c・decode_verify.js md5
  e355e4b51abe93f7c3f85886360f3baf・verify_witness.py md5
  0530d166572987988a01ec40dee12d4c も同実験dirから再利用。
- モード: def（全 w 行の OR・K0820 と同一の欠損極大完全符号化）および
  rowY=K（欠損行を固定するミラークラス分割・seven-row-q5-q6-frontier-row-split-20261115
  と同一技法）。rowY クラス 0..3 は行鏡映の全代表類（0↔6・1↔5・2↔4・3↔3）。
- ソルバ: kissat 4.0.4 official prebuilt（linux-amd64・md5 3a5eba830aa6008a604fcc9bbe99a325）。
  cap はインスタンスごとに記録。
- runner: scripts/rowfrontier.sh（本実験で新規・1インスタンス:
  生成 + kissat + JSONL record + SAT 時 decode + js/sat.js verifyConfig と
  verify_witness.py Python Fraction の2系統検証。CNF は実行後削除し cnf_md5 を記録）。

## 較正（着手時に実施済み）

- (7,23,5) def: CNF md5 155e6e4485b730147152a63237f118af・kissat SAT
  **1,200 conflicts bit-exact**（sat3 実験の calibration.jsonl と一致）。
- (7,32,5) rowY=0: CNF md5 e4850754f3a78e16d95e2673ccd1e754
  （rowsplit 実験の sat2 生成とバイト一致・sat3/sat2 rowfixed q5 の新規交差確認）・
  kissat SAT **129,923 conflicts bit-exact**（公開 record と一致・117.6s）。
  両 witness とも js+py 2系統検証 PASS。

## 結果（第1バッチ・2026-11-14T22:30Z 時点）

- **(7,6) 7×28 SAT**（rowY=3 分割・442,479 conflicts・137.0s・cap 250）:
  **34石単一欠損 witness rows [5,5,5,4,5,5,5]**・js+py 2系統検証 PASS
  （`output/q6-m28-row-split/`）。**(7,6) witness 帯は m=6..28 に延伸。
  M_{7,6} ∈ [29, 862]**（上界 K0318 U=862 は不変）。
- **(7,6) 7×29 空列延伸**: 同一34石配置が7×29盤でも js+py 2系統検証 PASS
  （`output/freecol-extensions/s7x29q6.witness.json`）。
  **M_{7,6} ∈ [30, 862]**。m=30 では cell (29,3) が未遮断で失敗。
- (7,6) 7×30 rowY=3: cap 280s INDET **929,785 conflicts**（honest negative・不在主張ではない）。
- (7,5) 7×33: rowY=0/1/2/3 全4クラス cap 250s INDET
  （399,206 / 399,144 / 344,970 / 345,432 conflicts）— クラス間の抵抗がほぼ一様
  （(5,6) m=22 class-split と同型）。不在主張ではない。次候補は長時間 cap か
  k×minpos 分解。
- **空列延伸の負記録（全家族前線）**: 各前線 witness の空列延伸は
  (7,5) m=32→33（cell (32,0) 未遮断）・(7,6) m=27→28（(27,3)）・(7,7) m=26→27・
  (7,8) m=24→25・(7,4) m=53 SA base→57（m=56 までは PASS・SA lane と一致）の
  いずれも1幅も延びない（`output/freecol-extensions/frontier-freecol-probe.json`）。
  (7,6) m=28 SAT witness のみ3幅…ではなく1幅（m=29 まで）延伸した。

## 結果（第2バッチ・900s cap・2026-11-15T00:10Z 時点）

- **(7,5) 7×33 SAT**（rowY=0 分割・**655,159 conflicts・835.7s・cap 900**）:
  **27石単一欠損 witness rows [3,4,4,4,4,4,4]**・js+py 2系統検証 PASS
  （`output/q5-m33-rowY0-900s/records.jsonl`）。第1バッチの全4クラス 250s INDET
  （345k..399k・クラス間抵抗ほぼ一様）は **cap 900s 延長で SAT に解決**。
  **(7,5) witness 帯は m=5..33 に延伸。M_{7,5} ∈ [34, 1142]**。
  m=34 への空列延伸は cell (33,0) が未遮断（not-maximal）で失敗
  （`output/freecol-m34/q5-m33-freecol.json`）。前線は 7×34。
- **(7,6) 7×30 rowY=3: cap 900s INDET・1,569,306 conflicts**（280s/929,785 の
  3.2倍 cap でも未解決・honest negative・不在主張ではない）
  （`output/q6-m30-rowY3-900s/records.jsonl`）。
- 運用: 900s 実行は setsid nohup バックグラウンド2並列（1コマンド wall ~290s
  上限の回避）。cap 到達時の conflicts は実行速度依存で変動しうる（bit-exact
  主張は cap 内完了インスタンスのみ）。生 kissat ログ（両インスタンス）は
  環境復旧後の後続バッチで追記する（records.jsonl の cnf_md5・conflicts が正本）。

## スコープ

有限機械検証（sat3 census は sat2 と9対照バイト一致済み、kissat 正確性）まで。
各幅の SAT はその幅の欠損極大安全配置の存在証明（witness 有限証拠）。
INDET は cap 到達であり不在を意味しない。上界の K0318 substitution は不変。
