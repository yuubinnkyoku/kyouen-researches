---
id: K0909
title: cost73kバンドのworker分割メモmergeは衝突0で安全・merge seed band実行はband ms24比80.2%
kind: verification
status: verified
topics: [certificates, verification, search-methods]
aliases: []
relations: []
artifacts:
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split_memo_merge_73k_20261117.py
    role: verifier
    note: オーケストレータ（worker実行・KYOENWM1 dump・sortベースmerge・衝突検出・KYOENWM2 seedrun・record恒等式ゲート・全gate判定）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/measure_worker_split_memo_73k.ts
    role: source
    note: worker/seedrunドライバ（per-bit snapshot+clearRows・dumpMemo/seedMemo）
  - path: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/worker-split-memo-merge-73k-20261117.json
    role: data
    note: 測定JSON（全gate合格・prior session値との差分記録入り）
---

# K0909: worker分割メモmergeの安全性（cost73kバンド・verbatim engine）

## 主張（有限測定の検証）

cost-73kバンド（child `00000000000000801206000000000400`・22 WIN7-D10 root・manifest blob `0892aed0`）の
証明書抽出メモ（位置keyed・engine verbatim blob `52bcaf50`・K0907監査済みの2欠陥を含むまま）について:

1. **2 worker分割（73/76境目・各11 bit・band内共有・MS=1<<23）の実行**は
   合計119,962,147 nodesで、band ms23単一プロセス121,186,659の0.9899。
   worker A（bits 0..73）はband ms23プレフィックスとper-bit完全一致（48,482,011 nodes・
   最終占有率slot 5,263,320）。分割は85%負荷の単一テーブル後半bitの汚染を避けつつ
   worker内共有を保持するため、ms23単一プロセスよりむしろ1.0%有利。
2. **KYOENWM1全slot dump（A 5,263,320レコード/B 6,242,804レコード）のsortベースmerge**
   （win=min・lose=min・nowin=max・nolose=max・255=非bound結合）は
   distinct A 2,619,833 + B 2,554,155・cross共有882,089・merge後occupied_after 4,291,899。
   **内部衝突0・cross衝突0**（衝突定義は両側255非boundを考慮：win<255∧lose<255・
   win<255∧nowin<255∧nowin>=win・lose<255∧nolose<255∧nolose>=lose）。
   重複キー（符号キーバグによる重複挿入）は全てhigh-bitで最大64コピー。
   つまりworker間でメモ値は大域的に一貫しており、**worker cacheの安全merge
   （WIN/LOSS矛盾の即時検出）が出版engineの実測で裏付けられた**。
   merge自体は2回実行でbyte同一（決定的）。
3. **merge表（KYOENWM2・4,291,899レコード）をseedとしたMS=1<<24全22 bit band実行**は
   85,747,496 nodes（未seedのband ms24 106,861,135の80.2%・fresh ms23電池108,499,241の79.0%）・
   最終占有率slot 10,614,912（負荷率63.3%・merge後load設計どおり）。
   seed 4,291,899件中1,448件（0.034%）は64-slot探査窓飽和で挿入失敗
   （25.6%初期負荷でのverbatim hash clustering由来・性能のみで健全性無影響）。
   **証明書22/22 byte同一**。最終dumpのrecord恒等式ゲート：挿入成功4,290,451 keyは
   全て残存し結合値はseed値と同等以上（違反0）、欠損は挿入失敗1,448件ちょうど。
   bit95は11,857,737 nodesで全構成と一致（memo-state-invariant root・K0907と同じ観察）。

## 測定上の注意

- 前セッション（2026-11-17早く）の同一測定はスクリプトを環境リセットで喪失。
  本測定は新規実装による再構築で、worker合計119,962,147 nodesは前セッション記録値と
  完全一致したが、merge後occupied_afterは前セッション記録4,291,129に対し4,291,899
  （+770・0.018%）。前実装の詳細は失われているためこの差は実装差として記録する
  （本実装はoccupied_after = distinctA + distinctB - shared を厳密に計算）。
- 実装中に発見した自分のバグ3件（実験事実として記録）: (a) 結合関数のtuple index誤り、
  (b) dump header行がsortを通ってしまいrecord parserが落ちる、(c) chunk分割sortの
  `sort -m`に`-k2,5`を付け忘れslot順の「整列」ファイルができrecord恒等式ゲートが
  368万key「欠損」と誤検出（ゲートが実装バグを捉えた好例・修正後は欠損=挿入失敗1,448件ちょうど）。
  (d) 255 sentinelをbound扱いする衝突定義は誤り（verbatim engineの負境界は死んでおり
  nowin/noloseは常に255・衝突は起こり得ない）。
- 環境のサイレントなプロセスkill（推定）で630MB dumpの単発sortが2回中断されたため、
  chunk分割sort+resume方式に切り替えて完走。

## 解釈ガード

測定・検証のみ。新規WIN/LOSS verdict無し・manifest行は1行も閉じない・証明書bytes不変。
repo-verbatim extractorはrepo上未修正のまま（出版決定性チェーン）。WIN7-D10は個別7石rootの
深さ10以内の先手勝ちのみを証明し、REFUTED-D10はLOSS証明ではない。
11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はいずれもUNKNOWN。
