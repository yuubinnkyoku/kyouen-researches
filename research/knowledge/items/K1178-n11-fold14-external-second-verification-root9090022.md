---
id: K1178
title: "fold14 receipt fold（root 9090022）単体の外部第二検証（K1173系列）"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold14 external second verification root9090022"
  - "第21 receipt・4番目WIN8 receipt foldの第三実装再検証 880 gate"
  - "監査正本 fe6370f7…（3実行byte一致）・主張4行のWIN8候補fold初・closed-before-this-receipt行初出の28行分類確認"
relations:
  - type: depends_on
    target: K1109
    note: "検証対象証明書群。root 9090022のWIN8-D10証明書（b8a15f9a…・1,082,873 bytes・29,942行・主張4行のWIN8候補として初のfoldの抽出実験 residual65 series名はintentional）と19 gate監査（00836a6e…）をW pin・値単位再照合・tamperの対象。"
  - type: depends_on
    target: K1097
    note: "refsolve正本（2896deb0…・27 gate・win16 footprint 49行exactly-once・残余23行）がfootprint partition再照合の対象。"
  - type: related
    target: K1176
    note: "fold13外部第二検証（K1108対象）と同一手続き系列。K1176検証機（aeda41e1…）を土台にfold14固有の外科手術と定数差替で本検証機を構成。fold14機のrerun gate対象はfold13出版機（5c27f1ae…）・fold12出版機（706bfa7a…）・fold13 receipt（c2bf8051…）・fold12 receipt（0f73795c…）、機内fold11 rerun gate対象はfold11機（9b3e06c8…）とfold11 receipt（d7bf2cd5…）。"
  - type: related
    target: K1173
    note: "fold20外部第二検証（K1129対象）で確立したbyte pin・W再構成・pristine 4回・tamper・決定的監査の手続き系列に属する。"
artifacts:
  - path: research/experiments/n11-fold14-external-second-verification-root9090022-20261121/README.md
    role: source
    note: "対象・固定pin・実施内容と結果・再現手順・限界"
  - path: research/experiments/n11-fold14-external-second-verification-root9090022-20261121/scripts/reconstruct_fold14_inputs.py
    role: reconstruction
    note: "W14/pub14再構成機（静的raw URL固定commitのみ・api.github.com非依存・全pin fail-closed・fold11/fold12/fold13機pin表の部分集合性機械確認・SHA-256 62a72b36…）"
  - path: research/experiments/n11-fold14-external-second-verification-root9090022-20261121/scripts/verify_fold14_external_20261121.py
    role: verifier
    note: "第三実装検証機（K1176検証機を土台にfold14固有の外科手術と定数差替で構成: 880 gate・stdlibのみ・乱数・時刻なし・SHA-256 d966dad5…・58,352 bytes）"
  - path: research/experiments/n11-fold14-external-second-verification-root9090022-20261121/output/external-audit.json
    role: audit
    note: "監査正本（91,543 bytes・880 gate全PASS・SHA-256 fe6370f7…・3実行byte一致・observations欄にsource_record清潔パターン継続とclosed-before行初出の記録）"
  - path: research/experiments/n11-fold14-external-second-verification-root9090022-20261121/output/reproduction.log
    role: record
    note: "実行記録（X/V/T実行matrix・gate内訳・findings・解釈ガード）"
  - path: research/log/2026-11-21-n11-fold14-external-second-verification-single-owner-note.md
    role: log
    note: "単一オーナー宣言ノート（commit 2a6f14de95…・受入条件6項目）"
  - path: research/log/2026-11-21-n11-fold14-external-second-verification.md
    role: log
    note: "宣言から出版までの時系列記録・受入条件対照・実験事実"
---

# fold14 receipt fold（root 9090022）単体の外部第二検証

## 概要

単一オーナー宣言（commit `2a6f14de95`・受入条件6項目）の下、
fold14 receipt fold（第21 receipt・4番目WIN8 receipt fold・root
`00000000000000909002200080100000`・出版実験
`research/experiments/n11-residual62-win8-receipt-fold-root9090022-20261120/`）の
出版byte・W入力31 pin・チェーン簿記・幾何主張・fail-closed防衛を、repo出版byteのみから
**第三実装**の検証機で独立に再検証した。K1173（fold20/K1129対象）・K1175（fold12/K1106対象）・
K1176（fold13/K1108対象）と同一手続き系列のfold receipt外部第二検証であり、
**主張4行のWIN8候補として初のfold**、および**28 canonical行分類でclosed-before-this-receipt行
を初めて含むroot**（fold13 receiptが閉じた行 `00000000000000003800000008003000`・
二重閉鎖回避）の値単位確認を完了した。

## 主な結果

- **全880 gate PASS**（P 12 / I 54 / C 772 / X 26 / T 16）。監査正本 `fe6370f7…`
  （91,543 bytes）が同一cwd 2回＋隔離cwd/HOME＋`env -i`＋`PYTHONHASHSEED=random` の
  3実行でbyte-identical。検証機 `d966dad5…`（58,352 bytes）は1実行約53秒
  （fold14出版機単体pristine runは約11.4秒・機内fold11/fold12/fold13 rerun gate込み）。
- **W入力31 pin（12 Git blob SHA-1 + 19 SHA-256）をapi.github.com非依存で再構成**:
  K1175/K1176で確立した静的raw URL固定commit設計を直接適用し、fold14 receiptから
  機械読み取りしたpin表全件をfail-closed照合。
  fold11機pin表（12+10=22件）⊂fold12機pin表（12+13=25件）⊂fold13機pin表
  （12+16=28件）⊂fold14機pin表（12+19=31件）の部分集合性を機械確認。
- **fold14出版機pristine再実行4回**（同一W 2回・隔離copytree W/cwd/HOME・隔離+
  `PYTHONHASHSEED=random`）すべて、receipt出力が出版正本 `ed3159fd…`（19,295 bytes）と
  byte-identical。各回の機内fold11 rerun gate出力（`d7bf2cd5…`）も出版正本とbyte一致
  （機内fold12/fold13 rerun gateは隔離W複写上で実行されreturncode 0で通過）。
  加えてfold13出版機を隔離W複写上で検証機側から独立実行し `c2bf8051…`（20,416 bytes）
  を再現・機内fold11 rerun `d7bf2cd5…` byte一致（宣言受入条件3の外側確認・V vr13段）。
- **チェーン全段の第三実装再構成**: base worklist 6,438行（cost 509,109）から
  globalFold 6,259/495,507 → cost78c/79c → first → second-third → fourth →
  fifth-sixth → seventh → eighth → ninth-twelfth（4 receipt）→ windfall4 13th-16th →
  seventeenth fold10 → WIN8 fold11（6,201/491,110）→ fold12（6,193/490,526）→
  fold13（6,184/489,813・solved 1,664・incidence 11,775・残余62・target 50）までの
  10出版記録連鎖を段ごとに再計算しpublished値と照合（fold4〜fold13）。
- **fold14 receipt主張の値単位再導出**: 28 canonical行=2方法一致
  （8 D4像×C(8,2) 224操作とC(8,6)=28部分集合・D4同変性）、分類 open-frontier 5/
  not-in-worklist 22/closed-before-this-receipt 1（初出・二重閉鎖回避を機械確認）、
  coverage 5行=K1109 g07主張4行＋余剰1行 `00000000000000889002400000000000`
  （cost 80）・closed edge cost 373・影響4親（全c2: 22→20/23→21/67→64/63→60・
  合計10 row-closings・完全閉鎖0）、frontier_after 6,179/489,440・solved 1,669・
  incidence 11,765・needed 4,487/355,888、五親target 50→54・残余62→58
  （58行hex全列挙照合）、win16候補 13→12根（主張39→35行・retired root `…9090022`
  4行・残り11根の35行全てopen・残余23行不交差）、root合法手50のsurvival規約独立再導出
  （quadruple-free・D4正準込み）、K1109 19 gate主要値
  （g06 uncapped probes nodes 512,590/614,246・g13 nodes 6,102,650/6,102,650・
  証明書 1,082,873 bytes 29,942行 sorted unique・third_method terminal 10,239/
  visited 65,134/winner 42,115/loser 12,780/応手辺 58,084・terminalRange [14,18]・
  subroot mobility 50）とK1097 27 gate・49行exactly-once partition
  （root 9090022行の intrinsic == claimed == 4行）。
- **tamper 2件fail-closed**（本レーン選択・出版社未試験offset・K1176レーンと別位置）:
  worklist @200,222（blob pin）・K1109証明書 @888,222（sha256 pin・1,082,873 bytes内）の
  1 byte XOR 0x01がrc≠0・fold14/fold11 rerun出力とも未書込・WT内pinned fold13 record
  無改変で捕捉。本番Wは実施後に無改変再照合。
- **source_record清潔パターンの継続確認**: fold14 receiptの
  `independent_verification.source_record` はK1109証明書抽出実験
  （`n11-residual65-win8-cert-extract-root9090022-20261120`・root 9090022・
  dir名のresidual65は実験series名でintentional）を正しく指す。fold12 receipt
  （K1175監査でerratum記録）と異なり記載エラーなし。この対照を監査JSONの
  observations欄に記録した（文書フィールドの検査であり、receiptのbyteは変更しない）。

## 実験事実

1. W14再構成はapi.github.com非依存の静的raw URL設計の直接適用で、quota枯渇条件下でも
   待機ゼロで完了した。fold14 receiptの `source_blob_pins`/`source_sha256_pins` から
   機械読み取りした31 pinに加え、rerun gate対象（fold11機・fold12機・fold13機・
   fold12 receipt・fold13 receipt・K1109監査・K1109証明書）を配置SHA照合込みで再構成。
2. K1176検証機（774 gate）を土台にしたfold14固有の外科手術で、チェーン再構成を
   fold13レコードまでの10段に拡張し、coverage照合を主張4＋余剰1の計5行に、
   4親影響gateを全c2・10 row-closingsに、K1109 19 gate値・レシート定数群
   （合法手50・root 9090022・証明書29,942行・controls 29）を差し替えた。
3. tamper offset（@200,222/@888,222）はfold13 ext2レーンのもの（@117,777/@777,777）と
   独立に選んだ。いずれも出版社が未試験の位置である。
4. fold14 rootの28行分類はWIN8 receipt foldで初めてclosed-before-this-receipt行を1行含み
   （fold13 receipt閉鎖済みの `…8003000`）、同を行がcoverageに含まれないことを
   分類・coverage双方のgateで機械確認した（二重閉鎖回避）。

## 出版

- 宣言ノート: `research/log/2026-11-21-n11-fold14-external-second-verification-single-owner-note.md`
  （commit `2a6f14de95`・fetch-back byte一致）。
- part1（実験dir 5ファイル）: commit `23de00dc`・fetch-back 5/5 byte一致。
- part2（本item・研究log）・part3（knowledge README末尾bullet）は別commit。

## 解釈規約

本項はfold14出版の簿記・決定性・入力pin・fail-closed防衛の再検査であり、行は1行も
閉じない（fold14時点残余62→58行は当該receiptの既出版簿記・pool 120,416根は不変）。
WIN8-D10証明書は当該8石rootのゲーム木に限られ、REFUTED-D10はLOSS証明ではない。
nodes数・solved数・coverage数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4はすべて
UNKNOWNのままである。**
