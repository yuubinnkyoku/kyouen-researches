# K1146代替9根depth-10掃引 全probe再実行第二検証の実行記録（2026-11-20）

単一オーナー宣言ノート
`research/log/2026-11-20-n11-residual72-replace9-d10-sweep-reexec-second-verification-single-owner-note.md`
（commit `3f340466218bb47a08d1f7421947ff720bc52b85`・先行出版）の下で実施した。
対象は [K1146残余23行代替9根depth-10掃引](../experiments/n11-residual72-replace9-d10-sweep-20261120/README.md)
（commit `e9ea153bc4` 出版・掃引正本 SHA-256
`e8f5d6749032c4ad95136d2915c03ce7e997fe494bf3eebf7f912cccc88ded1e`）の出版probe事実
18 probes（9根×両AND順序）。出版時のspot-checkは4 probesだったため、K1144が上流4掃引
（132 probes）で確立した「全probe再実行による第二検証」の replace9 版として全18 probesを
再実行した。

## 実行経緯

- 着手時に最新mainを取り直し、単一オーナー宣言・経路不競合を確認（以降到着手時点までの
  新コミットはK1058バグ修正系のみ。fold26 receipt fold は宣言 `e53cc60c87`、新WIN候補の
  証明書抽出は宣言 `63877ffd2e`、第5ラウンドrefsolve計画簿記は宣言 `ace38772d9` の各先行
  レーンが着手済みのため本レーンはいずれも着手しない）。
- 検証機 `verify_replace9_reexec_20261120.py`（41,175 bytes・955行・stdlib＋Node.js
  runner・乱数・時刻・環境依存出力なし・resume-safe）を新規実装。入力は上流6正本＋K1146
  出版2正本＋掃引機械の計9 pinをSHA-256/git blobでfail-closed読み出し。
- pass A（本tree・4 worker・実行約13.0秒）で18/18 probe完走。pass B（機械一式と入力を
  複写した隔離cwd/HOME・別tree・実行約12.7秒）で18/18 probe完走。
- assembleは同一cwd 2回＋隔離cwd/HOME別tree 1回の3実行でbyte-identical
  （監査正本 11,242 bytes・SHA-256
  `27fc420c58ac0c979e09c3a35b0b0b886fe1b521efea9de8f9f98e51e6264072`）。
- 残余23行宇宙はK1085→K1086→K1089→K1091→K1095の連鎖（72→49→40→30→23・各段
  distinct/disjoint/union partition検査）を検証機内の独立実装（fresh D4正準形表・
  4x4 Bareiss exact行列式）で再導入し、K1097帳簿crosscheck・9根被覆幾何
  （popcount8・quadruple-free・D4 min-canonical・23行exactly-once・
  gains {3:6,2:2,1:1}・child=root−最小セットビット）を全数検査。
- 出版掃引機械（SHA-256 `d163b2a1…`）を隔離treeで出版probe-records入力により
  pristine再実行し、20/20 gate・出力が出版正本とbyte-identicalであることを確認。

## 結果の要点

- **24/24 gate PASS**（入力pin 8種・runner blob pin・probe計画再導入×出版記録突合・
  出版内部整合（JSONL vs 正本per_root）・出版分類pin・残余宇宙連鎖再導入4段・
  K1097 crosscheck・被覆幾何2種・exactly-once・gains hist・passA/passB各fresh突合・
  passA-vs-passB・pristine再assemble byte-identical）。
- pass A・pass Bとも18/18 probeでnodes/loss/capped/terminalStoneRangeが出版記録と
  全件一致（nodes総計 3,574,172 == 出版値・capped 0・error 0・pilot_d6制御36/36 PASS）。
- fresh再分類はWIN8-D10 candidate `00000000010000809002000040002001` ただ1根
  （両順序 uncapped loss=true・nodes 608,293/691,784）＋REFUTED-D10 8根・
  順序間矛盾0で、出版分類pinと完全一致。
- passA vs passBの決定性字段不一致0。

## 発見: knowledge README K1146 bulletのSHA-256転写ミス1件

- knowledge READMEのK1146 bullet（327行目）に掃引正本SHA-256の1文字転写
  （`…bf3eefbf…`・正しくは `…bf3eebf…`）があった。本検証機のfail-closed pin
  （SHAを正本実byteから再計算して突き合わせ）がこれを捕捉した。
- 出版実験README・K1146 item・監査正本の各値は正しく、誤りはREADME bulletの転写のみ。
  実正本byte（15,403 bytes）のSHA-256再計算で確定し、本次回のknowledge README更新
  （K1149 bullet追記）と同時に修正する。
- 同一転写ミスが、着手時点以降に出版されたwhole-record独立第二検証の単一オーナー宣言
  ノート（commit `edc23121`・宣言 14:29:00Z・本レーンの再実行検証とは不競合の枠組み）にも
  引き写されている。同レーンは SHA-256 pin を fail-closed で実byteに照合する設計のため、
  実行時に自ら捕捉すると想定するが、注意喚起としてここに記録する。
- 出版経路のSHA pin管理におけるfail-closed設計の有効性の実証として記録する。

## 意味

- K1146のprobe事実（WIN8-D10 candidate 1根・REFUTED-D10 8根・nodes総計・分類・
  probe計画幾何）は、出版機械から独立の環境・独立の再実装による全件再実行で再現された。
  第5ラウンドrefsolveの前提入力（掃引volume・probe-records）が二重固定された。
- 本検証で行は1行も閉じない。WIN候補の証明書抽出・receipt foldは別工程・別宣言のまま。
  REFUTED-D10 は LOSS 証明ではなく、nodes数・solved数を勝敗として読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
UNKNOWN のまま。** 残余23行は全行open。

## 次回への引継ぎ

- 第5ラウンドrefsolve計画簿記（宣言 `ace38772d9` 所有）の到着後に、pool P⁗
  （120,416根）上の残余20行greedy・下界・最小性を再解決する。
- 新WIN8-D10 candidate `00000000010000809002000040002001` の証明書抽出（宣言
  `63877ffd2e` 所有）出版後のreceipt fold。fold26（宣言 `e53cc60c87`）は先行レーンの
  ままで着手しない。
- 掃引系の SHA-256はREADME bullet由来ではなく実byte pinから参照すること
  （本件の転写ミスは読み取り側のfail-closed pinでしか捕捉できない）。
