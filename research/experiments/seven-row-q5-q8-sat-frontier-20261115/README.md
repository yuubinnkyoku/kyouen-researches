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

## スコープ

有限機械検証（sat3 census は sat2 と9対照バイト一致済み、kissat 正確性）まで。
各幅の SAT はその幅の欠損極大安全配置の存在証明（witness 有限証拠）。
INDET は cap 到達であり不在を意味しない。上界の K0318 substitution は不変。
