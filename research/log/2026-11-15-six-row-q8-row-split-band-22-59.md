# 2026-11-15 (6,8) row-split band 22..59 セッションログ（高速レーン）

- K0829 の後継として 6x22 を 3鏡像 rowY 分割で決着した後、同一機械で帯を掃引した。
- **m=22..59 の全38幅で 3 rowY クラス UNSAT + 各幅 lex=H 交差確認 UNSAT**
  （sat2.js + kissat 4.0.4・全幅 exit 20・INDET 0）。witness-free 幅集合は
  {19,20,21} → **{19,...,59}**。M_{6,8} = 19 or ≥ 61（K0821 監査規約の鋭い形）。
  上界 371（K0318 代入）不変。仮番号 K0848 として項目化。
- 難度形状: 最難クラス系列は 2,862,649 (m=21) → 2,162,296 (m=22) → … →
  54,643 (m=43) と約52分の1まで崩壊し、m=44 以降は最難クラスが y=0/y=1 で
  交互。deciding 合計は 4,291,607 (m=22) → 局所最小 149,978 (m=48) →
  m=49..55 で再上昇 → m=56..59 で 195,970..235,196 の平台に。SAT witness は帯内皆無。
- **sat2.js 生成壁の解明**: m=53 で V8 デフォルトヒープ OOM（7行レーンの
  n=196 rc137 から外挿した「m≈32-33 壁」より遅い——あれはヒープ制限アーティファクト）。
  `--max-old-space-size` で突破し m=53..59 を生成。**m=60 で実 RAM 上限に到達**
  （heap 900 では kernel kill rc137・1400 は即 kill・800 は 585MB で JS-OOM）。
  すなわち sat2.js 帯frontier は m=59 で、m=60 は「ソルバー難度ではなく生成メモリ」で阻まれている。
- 環境リセット越え: m=45..47 sweep 直後にローカル作業dir全消滅。repo から機材を
  再取得し hash 検証（sat.js 6c3262d6・sat2.js edfae1d2・verify_witness.py ea7203a3・
  decode_verify.js ef5390509b・kissat md5 3a5eba83…）し m=45..47 を再実行、
  全 conflict 数がリセット前と bit-exact（cross-reset 較正 PASS）。
- push 輸送の教訓: read_file は行ベースで、単一行の巨大 JSON は next_offset=null で
  ページング不能（d311cbe2 切詰め事故と同根の機構）。バッチは staging.jsonl
  （1ファイル1行）経由で。run_typescript の 16MiB op 記録上限に注意
  （push_files が done の後に MemoryLimitError が出ても push 自体は成功している）。
- **並走整理**: `six-row-q8-band-closure-22-370-20261114` が IN FLIGHT claim 済み
  （genfast3.js・q≥w+2・CNF byte-identity 較正 6/6・instance-identity 2/2）。
  よって本レーンは m=59 で停止し、m≥60 の帯掃引は同レーンに譲る
  （genfast3 は O(C(w,2)·m²·w) で m=370 まで秒級・全三つ組 census を使わず
  RAM 壁の影響を受けない）。実験 README の wall 節にこの協調を明記。
- 反映: 実験 output に m=26..59 の生ログ計 136 本 + records.jsonl 155 レコード
  （バッチ4回・全 remote blob sha をローカル sha1 と照合し一致）、実験 README を
  帯表 m=22..59 に更新、K0848・CSV (6,8) 行・固定幅README (6,8) 段落を更新。
  旧 CSV/README の (6,8) 行は K0829 の 6x21 が未反映のまま残っていたため
  あわせて解消（{19,20},22..371 → {19..59},61..371）。
- 11x11 空盤・二石 root・S2・class2/class4 は UNKNOWN のまま（影響なし）。
- 次候補（他レーンまたは次回）: band-closure レーンによる m=60..370 掃引
  （全幅 UNSAT なら K0318 上界と合わせ M_{6,8}=19 exact・w=6 で初の完全決着）。
