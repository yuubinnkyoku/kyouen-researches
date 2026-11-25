---
id: K1172
title: "K1166（fold29証明書抽出外部第二検証）のpristine再実行第三検証"
kind: verification
status: verified
topics: [search-methods, certificates, verification]
aliases:
  - "fold29 cert-extract ext2 pristine re-execution third verification"
  - "K1166ハーネスbattery改変なし2巡・出版監査byte再現・隔離環境+PYTHONHASHSEED=randomでの決定性確認"
  - "第三検証record a6a3e048…・出版社監査正本 cf6a26ab… が2巡・3実行でbyte一致"
relations:
  - type: depends_on
    target: K1166
    note: "検証対象。byte 5点pin、pin commit 28d223a2d… からのmaster 61ファイル再構成、harnessのstage分割battery 2巡、監査正本 cf6a26ab…（15,549 bytes・gate 43）のbyte一致を再確認する。"
  - type: depends_on
    target: K1136
    note: "battery内のper-root fresh再実行対象の一つ（root 00000000000000043800000008180010・証明書 dbcb0bae…・13 gate PASS・証明書組立byte-identical・監査機3回+fresh記録差し替えで19/19）。"
  - type: depends_on
    target: K1137
    note: "同K1137（root 00000000000200003800200008180000・13 gate PASS）。"
  - type: depends_on
    target: K1139
    note: "同K1139（root 0000000800000000380000000810000a・13 gate PASS）。"
  - type: related
    target: K1165
    note: "fold24/K1164に対する第三検証と同一の手続き系列（byte pin・pristine再実行・tamper探針・決定的record）。"
  - type: related
    target: K1170
    note: "fold22/K1167に対する第三検証と同一の手続き系列。本項はfold receiptではなくWIN8-D10証明書抽出の外部第二検証への適用。"
artifacts:
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/README.md
    role: source
    note: "第三検証の対象・手順・結果・限界と2026-11-21のgate完全性追補"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/scripts/assemble_third_record.py
    role: verifier
    note: "byte決定的record組立機（stdlibのみ・gate 20・fail-closed・sorted keys・時刻/絶対path排除・SHA-256 2737e802…・7,044 bytes）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/scripts/reproduce.sh
    role: verifier
    note: "byte 5点取得・master再構成・両battery・record生成に加え、part gate完全性の回帰試験・補助検証器を呼ぶ再現手順（2026-11-21更新）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/third-verification.json
    role: audit
    note: "第三検証record正本（4,363 bytes・gate 20・status PASS・SHA-256 a6a3e048…・3実行byte一致）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/reproduction.log
    role: record
    note: "両batteryの実行記録・受入条件対照・負の制御（SHA-256 7f70b6b6…・4,902 bytes）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/battery1/harness-audit.json
    role: audit
    note: "battery 1巡目のharness監査（15,549 bytes・gate 43・SHA-256 cf6a26ab…・出版社正本とbyte一致）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/output/battery2/harness-audit.json
    role: audit
    note: "battery 2巡目（隔離cwd/HOME・PYTHONHASHSEED=random）のharness監査（battery 1とbyte一致・出版正本ともbyte一致）"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/scripts/verify_part_gate_completeness.py
    role: verifier
    note: "5 partの43 gateがpin済みauditを完全再構成するかをfail-closed検査"
  - path: research/experiments/n11-fold29-cert-extract-ext2-pristine-reexec-third-verification-20261120/tests/test_part_gate_completeness.py
    role: verifier
    note: "8種類の合成改変試験。欠落・余分・重複・値改変・battery差・JSON重複keyを拒否"
  - path: research/log/2026-11-21-n11-k1172-part-gate-completeness-guard.md
    role: log
    note: "第三検証record組立器のpart gate完全性の不足と補助検証器による補強"

---

# K1166（fold29証明書抽出外部第二検証）のpristine再実行第三検証

## 概要

単一オーナー宣言（commit `ec24b235f`・受入条件5項目・宣言時HEAD `1c42dcf25c…`）の下、
K1166（K1136/K1137/K1139 WIN8-D10証明書抽出の外部再実行第二検証・出版監査正本
`cf6a26ab…`・gate 43）を、repo出版byteのみを素材に第三の実行環境から完全再現し、
その決定性・入力pin・fail-closed防衛を独立確認した。K1165（fold24/K1164第三検証）・
K1170（fold22/K1167第三検証）と同一手続き系列の、証明書抽出第二検証への適用である。

## 主な結果

- **出版byte再pin**: K1166実験dirのbyte 5点（README `6605abff…`・fetch_master `c3c4c9ff…`・
  pin表 `949868e2…`・harness `ca662e57…`〔30,141 bytes〕・監査正本 `cf6a26ab…`〔15,549 bytes・
  gate 43・PASS〕）をmain固定commit `1c42dcf25c…` から再取得しSHA-256照合。
- **master再構成**: 改変なしの `fetch_master.py` でpin commit `28d223a2d…` から出版社3実験dir
  全61ファイルを2回（両battery）再構成し、git blob SHA照合 61/61（`all_blob_pins_ok: true`）。
- **battery 2巡・出版社harness改変なし**: stage分割（pin → root k1136 → k1137 → k1139 →
  tampers → finalize・実測 91.1/52.1/111.8/9.3 s と 89.3/51.7/111.3/8.9 s・各stage 300秒上限内）で
  出版社harnessをbyteそのまま2巡実行し、**両巡とも43 gate PASS・監査JSONが出版正本
  `cf6a26ab…` とbyte-identical**（cmp一致）。per-rootのprobe（両AND順序×2＋pilot制御）・
  抽出A1/A2/B・証明書組立byte-identical・BigInt・Bareiss・出版監査機pristine 3回＋fresh記録
  差し替えの各gateも両巡全PASS。
- **環境独立性**: battery 2巡目は隔離cwd・隔離HOME・全stage `PYTHONHASHSEED=random` で実行し、
  監査JSONに加えて**per-stage parts 5点（pin・k1136・k1137・k1139・tampers）もbattery 1巡目と
  全byte一致**。K1166の「battery全体がbyte決定的」という主張を第三環境で監査JSON単位でなく
  parts単位まで確定した。
- **tamper 3件fail-closed**: harness内蔵の改変試験3件（証明書本文offset 300007・pin入力
  offset 1111・fresh nodes 2757→2758）が両batteryともreturncode 1・監査未書込で捕捉
  （t1は`bareiss --root-check`がreturncode 0を返す一方で出版監査機g16全木走査が捕捉する
  防衛の深さの再実測）。
- **第三検証recordの決定性**: `assemble_third_record.py` がbyte 5点pin・両battery全gate・
  監査byte同一性・battery間byte同一性をfail-closedで再検査してrecord正本
  `a6a3e048…`（4,363 bytes・gate 20・PASS）を生成し、**3実行（既定seed 2回＋`PYTHONHASHSEED=random`
  1回）でbyte一致**（時刻・絶対path排除設計）。
- **負の制御（本レーン独自offset）**: 出版監査正本offset 8888の1 byte XOR 0x01で
  assemblerがreturncode 1・record未書込でfail-closed捕捉、復旧後にrecord SHAが完全復元
  することを実測（出版社はoffset 8888を試験していない）。

## 実験事実

1. 出版社の第二検証battery（1巡約8分・重計算込み）は、出版byte取得・master再構成を
   含めて**300秒bash上限のstage分割で第三環境でも素直に完走**する。stage実測は
   k1136 91.1→89.3 s・k1139 111.8→111.3 s で、出版時実測（90.0/112.2 s・postpub記録）と
   環境差なしに整合する。
2. battery間のbyte一致は監査JSON（finalizeの出力）だけでなく、per-stageの
   parts JSONにも現れる。fail-closed gateを段階ごとに持つharness設計では、
   「最終監査のbyte一致」はその必要十分条件ではないが、parts一致はbattery全体の
   再現性を段階単位で直接立証する補強になる。
3. read_file系のchunk化転写を行わずfile_system.read_fileで1ファイルずつ直読みして
   push_filesに渡す方式（K1166第二検証レーンの知見）でpart1 12ファイルがpush 1回で
   fetch-back 12/12 byte一致（今回合計3出版すべてタイポ無し・訂正commit不要）。

## 出版

- 宣言ノート: `research/log/2026-11-20-n11-k1166-fold29-cert-extract-ext2-pristine-reexec-third-single-owner-note.md`
  （commit `ec24b235f`・fetch-back byte一致・SHA-256 `5777a519…`）。
- part1（実験dir 12ファイル）: commit `4eb2205e7fcb30e34fcbb8bdd658ad82c27c513e`・
  fetch-back 12/12 byte一致（README `77e96ec2…`・record `a6a3e048…`・log `7f70b6b6…`・
  battery監査2点 `cf6a26ab…`・published byte 5点は出版社SHA-256と同一）。
- part2（本item＋研究log）・part3（knowledge README末尾bullet）は別commit。

## 後続のpart gate完全性ガード（2026-11-21）

既存の `assemble_third_record.py` は各partについて「空でない・存在するentryがすべてpass」を検査していたが、欠落・余分・重複をpin済みauditとの完全一致で検査していなかった。これを補う `verify_part_gate_completeness.py` を追加し、5 partのgate数（1/13/13/13/3）・prefix・重複なし・結合辞書とaudit `gates` の値単位一致・JSON重複key拒否・battery間byte一致をfail-closedで確認するようにした。8種類の合成回帰試験を追加し、`reproduce.sh` は今後のbattery再実行時に試験と補助検証器を呼び出す。

**歴史的な第三検証record（20 gate・SHA-256 `a6a3e048…`）は変更していない。** 元のbattery part filesはGit管理されていないため、この補助検証を過去の2 batteryへ遡及適用したとは主張しない。合成43 gate fixtureで、正常分割PASS・欠落/余分/重複/値改変の拒否を確認したが、repoのunittest全件・実battery・全体CIはこの追補では未実行。詳細は [追補ログ](../log/2026-11-21-n11-k1172-part-gate-completeness-guard.md)。

## 解釈規約

本項はK1166第二検証batteryの再現性・入力pin・fail-closed防衛の第三検査であり、
行は1行も閉じない。残余行数・pool P⁗ 120,416根は不変。WIN8-D10証明書は当該8石rootの
ゲーム木に限られ、REFUTED-D10はLOSS証明ではない。nodes数・solved数を勝敗として読まない。
**標準11×11空盤・二石root `{49,60}`/`{59,60}`・S2 `{59,60}`・class 1/2/4は
すべてUNKNOWNのままである。**
