# 単一オーナー takeover 宣言: seven-row q=5 前線 7x38 class-split 直接評価 (停滞レーンの引継ぎ・publish-then-execute)

- 宣言日時: 2026-11-28T03:50Z 前後。宣言時 HEAD: `954fc7eb` (2026-11-28T03:42:31Z)。
- 引継ぎ元: [2026-11-23 seven-row-q5-m38-class-split-single-owner-note](2026-11-23-seven-row-q5-m38-class-split-single-owner-note.md)
  (宣言 2026-11-23T15:20Z・cap 7,200s/instance 計画のまま 5日間停滞・成果物出版なし)。
- 対象: (7,5) 前線 7x38。witness 帯 m=5..37・M_{7,5} ∈ [38, 1142]・上界 1142 (K0318) 不変。
  前段の 2編集surgery完全負記録 (seven-row-q5-m38-surgery-negative-20261115) の次段として、
  K0827 が挙げた sat による直接評価。
- 手法: 単一不足行 witness の row-mirror 正準類 rowY ∈ {0,1,2,3} (0<->6, 1<->5, 2<->4, 3<->3)。
  `sat2.js 7 38 5 --rowY=Y` (streaming all-triples census・rowfixed: row Y 以外を full に固定) の CNF 4本を
  kissat 4.0.4 公式 linux-amd64 バイナリ (sha256 先頭 21da5d98... pin) で評価。
  SAT なら decode + 2系統検証 (sat.js verifyConfig〔census 不使用〕 + verify_frac.py Python Fraction) までを実行。
- 較正 (宣言前に本hostで実施・全項目出版記録と一致・開示):
  - (7,32,5) rowY=0 CNF 再生成 vars 193,644 / clauses 676,415 / curves 9,801・kissat rc=10 SAT
    conflicts 129,923 bit-exact (出版 q5-m32-row-split records.jsonl および停滞宣言の較正と完全一致)。
  - 7x38 CNF 4本の md5 が停滞宣言の事前登録値と 4/4 byte 一致:
    rowY=0 `51bf641322378b28d6e7aaecd80fd90f` / rowY=1 `505a17f56ce874cd081644cce5592587` /
    rowY=2 `e69fe113ac00459b74e8fd5b8afba601` / rowY=3 `f50729ed20a68e8fa1f7e09151e25164`
    (vars 288,546 / clauses 1,007,501 / curves 14,705 共通)。
- cap 方針 (元宣言 7,200s からの環境制約による変更・開示): 本環境は 1コマンド 300s 上限のため
  1 piece あたり wall cap 260-270s・逐次実行。cap 到達は INDET として正直記録する。
  全 4 rowY INDET の場合は krow/minpos (sound H-split) の部分分解に継続する
  (sat3.js --class=Y --krow=Y:3 --minpos=P・P=0..18、必要なら k=2,1,0)。
- 判定規約: SAT witness → M_{7,5} >= 39 (レンジ [38,1142]→[39,1142])。
  4 rowY とも UNSAT の場合のみ「7x38 単一不足行 witness-free」を記録。
  INDET は honest negative・不在主張ではない。深不足 (2行以上の不足) 類は本 sweep の範囲外で
  未掃引のまま (不在主張なし)。
- 報告: 判定時に experiment dir (seven-row-q5-m38-classsplit-takeover-20261128/) + records + 完了log +
  K0827 追記 + CSV (7,5) 行更新として main へ反映。
- 範囲と限界: 有限機械評価。census 完全性とソルバ正確性までを保証し、数論的証明ではない。
  標準 11x11 空盤・19 central-reply roots・二石 root {60,27}・第三手 {100,108}・S2・全 closure class は
  本レーンと無関係で全時点 UNKNOWN・verdict 不消費・conflicts は bookkeeping。
