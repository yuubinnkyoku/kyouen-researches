# 2026-11-15 four-row frontier lane (rowY 2クラス被覆と (6,4) m=41)

## 背景

`four-six-row-q4-q5-band-extension-20261115`（最終push 00:28Z・セッション終了形）が
README の IN FLIGHT claim として残した5前線のうち、(5,5)（class-split レーンが
自動延伸中・M_{5,5} ∈ [26,336] に更新済み）を除く4前線を takeover した:
`(4,4) m=35`・`(4,5) m=21`・`(5,4) m=40`・`(6,4) m=41`。
実験dir `research/experiments/four-row-q4-q5-frontier-20261115/`（claim push 30f48a8f）。

## 方法論の進展: w=4 rowfixed 2クラス被覆補題

前レーンの rowY=0..3 full-lex INDET 記録は absence には使えなかった:
lex=V/HV は行 y ↔ 3−y を動かすため、{rowY=0,1} の2クラスでは
ミラークラス {2,3} を被覆しない。本レーンは
**rowfixed(0) ∧ lex=H と rowfixed(1) ∧ lex=H の2インスタンスで完全被覆**
できることを確認した（補題は実験 README に証明つきで記録）:
H は行を保存するので H-軌道の辞書式最小元は同じ rowfixed クラスに留まり、
V は行 0↔3・1↔2 を送るので deficient row ≥ 2 の witness は鏡像で ≤ 1 に移せる。
したがって2クラス UNSAT ⟹ その幅は witness-free（M の確定）。
lex=H 単独（V/HV なし）であることが本質。逆に SAT は lex によらず真の witness。

## 結果

1. **(6,4) m=41 SAT**（rowY=0・lex=H,V,HV・245.2s・8,226 conflicts・17石
   rows [2,3,3,3,3,3]）— witness 帯 m=6..41、**M_{6,4} ∈ [42, 1113]**。
   js+py 2系統検証に加え第3系統（純TS/BigInt verify_independent.ts verbatim・
   sandbox 実行）PASS、陽性対照（前レーン m=40 witness 再PASS）・陰性対照
   （1石移動→maxCirc=4 unsafe+10 uncovered を検出）つき
   （output/ts-verify-frontier.json）。
   直前の同一インスタンス実行が環境リセットでラッパーごと殺されたが、
   再実行が conflicts 8,226 bit-exact を再現（決定性の傍証）。
2. **(4,4) m=35**: lex=H rowY=0/1 2クラス（absence-capable sweep の初走査）
   ともに 600s INDET（324,870 / 230,642 conflicts・honest negative）。
   不在主張ではない。def-mode 317,151@260s（前レーン）と同規模の抵抗。
3. **(4,5) m=21**: lex=H rowY=0 600s INDET 6,924,496 conflicts
   （11.6k conflicts/s・honest negative）。rowY=1 600s INDET 7,286,846 conflicts（12.2k conflicts/s）。2クラス合計 ~14.2M でも未解決。
   前レーン rowY=3 full-lex 2.7M@200s を大きく上回る探索でも未解決。
4. **(5,4) m=40**: rowY=1 600s INDET 191,445 conflicts（honest negative）。
   m=39 rowY=1 SAT 21,147 と比べ1桁難化。前線は m=40 のまま。

## 運用メモ（環境）

- ラッパー (lean5.sh) は cap 到達の SIGTERM 直後に環境側で殺されることが
  多発したが、kissat 本体は cap まで完走し kissat.txt に最終 stats が残る。
  記録は kissat.txt から復元して push（records.jsonl の note に明記）。
- 実効 CPU は約1コア。2並列 kissat は互いに半減するため、逐次実行が最適。
- 完全リセット（作業dir消滅）が ~02:20・~03:19 に発生。push 済みの成果は
  影響なし。バッチごとの即 push が有効だった。

## 追記（第2セッション・バッチ7/8: (6,4) m=42）

1. **(6,4) m=42 rowY=0 SAT**（461.6s・16,942 conflicts・17石 rows [2,3,3,3,3,3]）—
   **witness 帯 m=6..42・M_{6,4} ∈ [43, 1113]**。js+py 2系統検証 + 第3系統
   （ts-verify-frontier-m42.json・陽性対照 m=40 再PASS は m=41 run と同一値・
   陰性対照 maxCirc=4 unsafe+7 uncovered 検出）PASS。前線は m=43。
   m=41 (8,226/245.2s) → m=42 (16,942/461.6s) は conflicts ほぼ2倍・時間1.9倍の
   穏やかな難化。CNF は vars 1,939,029 / clauses 6,437,821 / curves 185,453。
2. 第2統合（CSV・K0833・本 README・本 log）で反映済み。

## 追記（第2セッション続き・バッチ9/10: (6,4) m=43）

1. **(6,4) m=43 rowY=0 SAT**（cap 900s・581.1s・34,728 conflicts・17石
   rows [2,3,3,3,3,3]）— **witness 帯 m=6..43・M_{6,4} ∈ [44, 1113]**。
   CNF は vars 2,078,685 / clauses 6,900,670 / curves 198,980
   （cnf_md5 c10b5eb3…）。ラッパーが SAT 直後の decode 段階で環境リセットに
   より殺されたため、kissat.txt の model から lean5.sh の SAT 分岐
   （decode_verify.js + verify_witness.py）を手動再実行して records.jsonl
   を構成（jsVerify/pyVerify とも ok・note に復元の旨明記）。
2. **第3系統検証 PASS**（ts-verify-frontier-m43.json・nCircles=672/nQ1Curves=690・
   陽性対照 m=40 再PASS は m=41/m=42 run と同一値・陰性対照 maxCirc=4
   unsafe+8 uncovered 検出）。
3. 難化トレンド: m=41 8,226/245s → m=42 16,942/462s → m=43 34,728/581s
   （conflicts ほぼ2倍/幅・cap 900s が効いている）。m=44 は cap ~1200s 級の
   見込みで、本レーンの運用上限（コマンド120s・リセット~10-17分）では
   ポーリング継続が必要。
4. 第3統合（CSV・K0833・本 README・本 log）で反映済み。

## 追記（第2セッション続き・バッチ11/12: (6,4) m=44）

1. **(6,4) m=44 rowY=0 SAT**（cap 1200s・493.9s・12,816 conflicts・17石
   rows [2,3,3,3,3,3]）— **witness 帯 m=6..44・M_{6,4} ∈ [45, 1113]**。
   CNF は vars 2,224,351 / clauses 7,383,478 / curves 213,086。
   今回はラッパーが decode・js/py 2系統検証まで完走し lean5.sh が直接 record 生成。
2. **第3系統検証 PASS**（ts-verify-frontier-m44.json・nCircles=672/nQ1Curves=690・
   陽性対照 m=40 再PASS は m=41/42/43 run と同一値・陰性対照 [16,0]→[17,0] で
   maxCirc=4 unsafe+7 uncovered 検出）。
3. 難化トレンドの反転: m=43 34,728/581s → m=44 12,816/493.9s。conflicts が
   幅あたり ~1/2.7 に減少し、難化が単調でないことが判明（m=41 8,226 → m=42 16,942
   → m=43 34,728 のほぼ2倍トレンドは m=44 で途切れた）。cap 1200s は
   十分な余裕をもって充足。
4. 第4統合（CSV・K0833・本 README・本 log）で反映済み。

## 追記（第2セッション続き・バッチ13〜15: (6,4) m=45 SAT と m=46 構成 witness）

1. **(6,4) m=45 rowY=0 SAT**（cap 1200s・272.1s・10,066 conflicts・17石
   rows [2,3,3,3,3,3]）— **witness 帯 m=6..45・M_{6,4} ∈ [46, 1113]**。
   CNF は vars 2,376,539 / clauses 7,887,805 / curves 227,839。
   第3系統検証 PASS（ts-verify-frontier-m45.json・nCircles=670/nQ1Curves=692・
   陽性対照 m=40 再PASS は m=41..44 run と同一値・陰性対照 [21,0]→[22,0] で
   maxCirc=4 unsafe+1 uncovered 検出）。conflicts は m=43 34,728 → m=44 12,816
   → m=45 10,066 と減少継続 — m=43 が局所ピーク。
2. **(6,4) m=46 witness が構成的に確定**（free-column append・ソルバ不使用）—
   **witness 帯 m=6..46・M_{6,4} ∈ [47, 1113]**。m=45 witness をそのまま 6×46
   ボードに置くと新列 45 の全点が既存の 3石曲線でブロックされる（純TS
   full-board 走査 PASS: safe maxLine=3/maxCirc=3・uncovered=0・rows [2,3,3,3,3,3]）。
   これが本レーン初の「SAT 前線の先のソルバ不使用 witness」。free append は
   m=47 で停止（(46,0) 未カバー）。output/q4-w6-construct-m46/records.jsonl
   （js+py 2系統検証は bash 環境復旧後に実施予定と明記）。
3. 周辺分析（純TS・m=47 目標の bounded-edit surgery）: (46,0) を通る既存2石
   円/直線上の追加候補 63 点のうち safe は 0（3 unsafe + 60 nonmaximal）。
   1石移動（remove 1 + add 1）は safe 77 組合せすべて nonmaximal。
   m=42..44 witness の free-append 到達幅は m0+1 で停止（右端 (m-1,0) が
   未カバー）— m=45 witness のみ +1 到達。いずれも local negative・不在主張ではない。
4. 環境: 実行環境（bash）が ~04:21Z に完全利用不可になり、以降の作業は
   run_typescript の GitHub ツールと純TS計算だけで完結（batch 13-15 と本統合は
   この状態で push）。kissat 実行は bash 復旧後に再開。
5. 第6統合（CSV・K0833・本 README・本 log）で反映済み。

## 次課題

- (4,5) m=21 / (4,4) m=35 の2クラス UNSAT には更に長い cap（~30M conflicts 級）
  か class-split（sat3 --class）の併用が必要。両クラス INDET の間は M は
  [21,140] / [35,237] のまま。
- (6,4) m=47: bash 復旧後に lean5 cap 1200s で試す（2石移動 surgery も候補）。(5,4) m=40 rowY=0/def-mode の掃引。m=46 witness の js+py 検証。
- (4,21,5) は CNF が小さい（84点・542曲線・36,910節）ため、CDCL 以外の
  アプローチ（局所探索・構成的延伸・K0827 型 blocking-coverage）も
  併用価値がある。
