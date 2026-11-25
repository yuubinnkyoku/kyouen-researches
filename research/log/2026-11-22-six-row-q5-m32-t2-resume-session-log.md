# 2026-11-22 six-row (6,5) 6x32 t2 remaining 23 bases - session log

- オーナー: 高速レーン (本セッション)。宣言: b1afb181aa (02:2xZ・宣言時HEAD 05785cdfa5)。
- 前段: K1216 (6x31 band extension・880e288663) のresumeノート課題「6x32 t2残り23 base」。

## やったこと

1. kit整合性確認: surgery_gen.js sha256 dfc97506… (K1216出版pin一致)・
   surgery_deep.js 851e5b7b… (publish/ とbyte同一)・config_w32_u3.json add8c82f…
   (publish/ とbyte同一)。
2. 作業tree /home/user/work/m32t2/ でkit出力dirへのsymlink運用でt2掃引を実行。180s/呼び出し
   budget + 16-removal checkpoint。base-001 で budget-stop→resume の doneIdx継続を確認。
3. 02:25Z頃〜03:5xZ頃: 単独→2並列実行で11個のbaseを完走 (全0 witnesses) + 12個を部分走査
   (checkpoints保存)。
4. 03:5xZ頃〜: 実行環境 infra failure。bash/filesystem系toolが unavailable となり継続不能。
   GitHub API系toolは稼働。~15分の復旧pollingの後、stdout記録値ベースで進捗を出版 (本logと
   実験README)。raw file群はkit側に全保存。

## 結果 (stdout記録値)

- t2 DONE・全0 witnesses: 001 c009@off4 (pairs 9045), 002 c008@off0 (7850),
  003 c008@off1 (6392), 004 c008@off2 (7311), 005 c009@off2 (8175), 006 c009@off5 (7635),
  007 c011@off4 (6627), 008 c011@off5 (dsizes/pairsはkitのdone json), 009 c011@off6 (8457),
  010 c004@off7 (5572), 017 c009@off1 (7298)。
  → これらのbaseの6x32 rem3add2 (targeted-complete) witnessは存在しない。
- part進捗 (最終stdout時点・すべて witnesses=0): 011 (1200/1771), 012 (384), 013 (368),
  014 (352), 015 (336), 016 (832), 018 (400), 019 (320), 020 (336), 021 (320), 022 (320),
  023 (384)。checkpoint resumeで各1-3呼び出しで完走可能。

## 判定規約の遵守

- witnesses=0 は targeted-complete 陰性の主張で、6x32全配置の不在主張ではない。
  M_{6,5}∈[32,658] 不変・6x32 UNDETERMINED 不変。
- K item は作成しない (有界編集近傍のbaseごと陰性に留まり、独立に参照したい一般則が
  ないため・AGENTS「実験1回につき1Kを作らない」)。
- pairs/dsizes は列挙サイズの記録であり勝敗ではない。

## 次レーンへの引き継ぎ (着手前に必ず最新main再取得・hourly並走に注意)

1. node scripts/surgery_deep.js config/config_w32_u3.json <i> <j> t2 (endBaseは排他的)・
   作業treeのoutputをkit dirへsymlink運用・bash呼び出し時にtimeout秒を必ず指定、で
   011..016, 018..023を完走 (各1-3呼び出し・計~70分)。
2. kitのraw (.t2.json 完走分全base・.t2.part.json・.stats.json更新分) をsha256付で
   research/experiments/six-row-q5-m32-t2-remaining-bases-20261122/output/ へ再掲。
3. 全24base DONE時点で README の「未完」表を解消し、r0s..r4a1 + t2 の全クラス陰性と
   して24base編集近傍の限定陰性を確定記録する。
4. witnessが1つでも出たら: K1216と同一の3系統検証ゲート → 下界 M_{6,5}∈[33,658] 出版。
5. 6x33 (unblocked_w33.json・config_w33構築) は別宣言スコープ。

## 器材

knowledge/kyouen-research/_q65-band-m31plus-kit/ (scripts+config+census+output/w32-u3-scan
checkpoints・publish/ はrepo刊行物とbyte同一)。repo側が正式。
標準11x11空盤・二石root・S2・class 1/2/4は本レーン非接触でUNKNOWNのまま。