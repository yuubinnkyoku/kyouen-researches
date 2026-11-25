# 2026-11-21 n11 K1178 fold14 ext2 pristine re-exec 第三検証（単一オーナー・part1〜3）

## 経緯

- 前回まで: fold12/K1184・fold13/K1185の第三検証が出版済み。fold12〜16単体ext2第二検証群
  （K1175/K1176/K1178/K1179/K1180）の第三検証は第三号のfold14が次の対象。
- K1178対象の固定値: root `00000000000000909002200080100000`〔root 9090022〕・pin commit
  `23de00dc`・出版社監査正本 `fe6370f7…`（91,543 bytes・gate 880）・W再構成機 `62a72b36…`
  （11,543 bytes）・第三実装検証機 `d966dad5…`（58,352 bytes）・README `0d3b4e06…`（6,534 bytes）・
  reproduction.log `5d28aa0e…`（3,065 bytes）。
- 単一オーナー宣言: `research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `369b0c3030…`〔短縮 `369b0c30`〕・宣言時HEAD `eda86d47`・受入条件5項目）を先に出版。
- 実験dir: `research/experiments/n11-fold14-ext2-pristine-reexec-third-verification-root9090022-20261121/`。

## 実施（受入条件対照）

宣言の受入条件5項目に対する実施結果:

1. **出版byte 5点pin** — harness pin stageがpin commit `23de00dc`から実験dir 5ファイルを自力取得し
   SHA-256+byte数10 gate PASS（K1178 part1の実態は検証機・監査・README・reproduction.log・再構成機の5点を
   単一push_filesコミットで出版しており、pinの粒度はK1176（K1185）時と同一設計）。
2. **W再構成2実装参照** — ref_b `eda86d47`（宣言時HEAD）�・ref_a `369b0c30`（宣言commit）の両pinned ref
   で改変なし再構成機を2回実行し、W tree（12 blob + 19 SHA-256 = 31 pin + fold11/12/13/14の4 chain機・
   35ファイル）を再構成、`diff -r` byte一致。subset-checkはfold11 pins 12/pin256 10・fold12 pins 12/pin256 13・
   fold13 pins 12/pin256 16がfold14 12+19の部分集合として機械確認され最終行
   「RECONSTRUCTED W at … PINS 12 PIN256 19」。
3. **出版検証機pristine 4回/battery×3** — 同一base 2巡（計8回）・隔離base+copytree W/cwd/HOME
   +`PYTHONHASHSEED=random` 1巡（4回）の計12回すべてrc=0・`ALL 880 GATES PASS`・
   出力監査JSONが出版正本 `fe6370f7…` とbyte-identical。battery内4回間でもbyte一致。
   1回53.1〜53.4秒（fold13機の約1.8倍）・1 battery 約4分20秒。
4. **tamper探針fail-closed** — 本レーン選択offsetのworklist @333,444（blob pin）・K1109証明書
   @999,111（sha256 pin）1 byte XOR 0x01がbattery全3巡でrc=1・`GATE FAILED`・監査未書込。
   出版試験位置@200,222/@888,222はverifier自身の機内断続探索で毎battery再確認。
   手動でfold12第三レーンoffset@150,000・fold13第三レーンoffset@222,999でもfailを確認
   （両隣レーンに寛容でない）。本番Wは探針後に無改変再照合。
5. **監査byte正本の固定** — 第三検証harnessの監査 `output/harness-audit.json` がbattery 3巡で
   byte一致（`717b7c9b…`・6,723 bytes・gate 53〔pin 10・recon 16・rerun 19・tampers 8〕・
   all_gates_pass true）。per-stage partsはwall_ms保持でbyte再現対象外。

追記事実（K1185セッションで実測済みの手法の本レーン适用于の留意）:

- **検証機内部scratchの絶対path** `/home/user/work/f13ext/runs14` は出版byteの一部のため、harnessは
  検証機実行を逐次化し、隔離巡でもscratch path混入が監査byteに影響しないことを実測した
  （K1185の実験事実①と同根・fold14機でも同一設計）。
- **api.github.com枯渇の影響圏外**: pin・recon・tamper・手動探針・fetch-backすべてraw固定commit URLのみ。
  6回のW再構成・12回の検証機実行すべて待機ゼロの冪等運転。

## 実験事実

1. fold14検証機はgate 880・1回約53.1〜53.4秒。W tree 35ファイルはfold11〜14の全4 chain機がWに含まれる
   初の規模で、第三検証のrecon stageはfold13時（24ファイル）より11ファイル増加した。
2. worklist `inputs/worklist.csv`（`6d8a449e…`・360,834 bytes）はfold12/13/14の3レーン連続同一series再利用。
   第三検証レーンのtamper探針位置は3レーンで互いに別々（@150,000・@222,999・@333,444）。
3. **K1185セッション中に実行環境リセットが1件発生**（battery 3巡完了直後）し、ローカル成果物が一時全喪した。
   この影響はK1185側の実験事実として当該研究logに記録済みであり、fold14側の研究成果物は宣言・part1が
   repo出版済みで失われていない。本logのbattery 3巡はリセット後の再構成harness（記録済みソースと
   byte数照合、24 bytesの`PARTS.mkdirs = None`タイポ除去を含む再構成）による再実行で、
   監査byteが出版part1の `717b7c9b…` と一致することを本レーンが第三の環境から再確認した。
4. 出版検証機の12回実行・3 batteryすべてで監査byteが出版正本とbyte一致したため、
   「fold14の外部第二検証は（監査byteとして）環境非依存に決定的である」ことが第三実装・第三環境から確認された。

## 結果と限界

- 結果: K1178の出版全成果（W pin・検証機・監査正本）が第三実装harnessによりbyte単位で再現され、
  fail-closed防衛が計20件のtamper（battery 3巡×〔2本レーン+2出版〕+手動2件）で全件捕捉された。
  受入条件5項目はすべて満たされている。
- 限界: 行は1行も閉じない。fold14時点の残余62→58行減は当該receiptの既出版簿記であり、
  pool 120,416根は不変。WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
  **標準11×11空盤の勝敗・二石root {49,60}/{59,60}の値・S2 {59,60}の値・class 1/2/4はすべてUNKNOWNのままである。**
  per-stage partsのwall_msは再現対象外。api.github.com枯渇下ではraw固定commit URL依存のみで運転する設計が
  本質的であることが実測された。

## 出版

- 宣言: commit `369b0c30`（`research/log/2026-11-21-n11-k1178-fold14-ext2-pristine-reexec-third-single-owner-note.md`）。
- part1: commit `4f869535`（実験dir 4ファイル〔README・harness・harness-audit.json・reproduction.log〕・
  fetch-back 4/4 byte一致）。
- part2: 本item（`research/knowledge/items/K1186-n11-fold14-ext2-pristine-reexec-third-verification.md`）・
  本log（単一push_filesコミット）。
- part3: knowledge README の末尾へのK1186 bullet追記（別コミット）。

harness（`scripts/verify_k1178_fold14ext2_third_20261121.py`）: stdlibのみ・stage分割
pin/recon/rerun/tampers/finalize・fail-closed・SHA-256 `2caa5516…`（18,921 bytes）。
監査正本 `output/harness-audit.json`: `717b7c9b…`（6,723 bytes・gate 53・all_gates_pass true）。
