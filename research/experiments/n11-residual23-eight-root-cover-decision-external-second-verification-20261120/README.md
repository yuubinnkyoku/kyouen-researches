# 残余23行 8根被覆判定の外部第二検証: 4実行 byte-identical・71チェック全PASS（2026-11-20）

単一オーナー宣言: [../log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification-single-owner-note.md](../log/2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification-single-owner-note.md)（commit `e8d6025745`・先行出版・宣言 13:29:51Z）

対象: commit `b4d8b3ac52`（単一オーナー宣言 `cb31752551`）で出版された
[8根被覆判定実験](../n11-residual23-eight-root-cover-decision-20261120/README.md)
（K1097 更新: UNSAT・P‴上の最小被覆 9根・interval [8,9]→[9,9]・数え上げ証明書つき）。

判定が確定した「greedy 9根計画は P‴上で候補根数最小」は、本検証の実行中に並走レーンが
K1146（replace-9 depth-10掃引・WIN8-D10 candidate 1根＋REFUTED-D10 8根・13:35:51Z着地）として
実行済みとなった。本検証はその計画の最小性根拠（判定機・出版正本・入力pin鎖）の独立確認であり、
K1146の実施内容には一切影響しない。

## 実施内容と結果

1. **出版byte完全性（fail-closed pin 5件）**: main（commit `fcabb2f585` 時点の正本byte）から取得した
   - 判定機 `eight_root_cover_decision_20261120.py`（SHA-256 `da51063c…`・39,301 bytes）
   - 判定正本 `residual23-eight-root-cover-decision-20261120.json`（SHA-256 `c5aaf83e…`・16,324 bytes）
   - K1097再解決正本（`2896deb0…`）・K1102第二検証正本（`d0b5d845…`）・下界強化監査正本（`1310ef74…`）

   の5ファイルすべてのSHA-256が出版pinと一致。輸送破損・打ち切りなし。
2. **pristine再実行4回・全てbyte-identical**: 判定機を1byteも改変せず
   - pass A: 同一tree 2回（各41〜42秒）
   - pass B: 隔離tree・隔離cwd・隔離HOME・入力は別pathのコピー（42秒）
   - pass B': pass Bに加えて `PYTHONHASHSEED=random`（hash randomization明示）

   出力は**4回すべて出版正本とbyte-identical（SHA-256 `c5aaf83e…`）**。判定 UNSAT・18 gate PASS・
   cover3呼び出し451・メモ211・Shape B試行100も全実行で同一。出版社の3実行（同一cwd2回+隔離1回）に加え、
   hash randomization明示環境を含む4実行反復で決定性を追加支持した。
3. **記録レベル交差検証71チェック（外部検証機・出版機と別実装）**: 判定正本・K1097・K1102・監査の4正本
   および4回の再実行出力だけを入力とし、
   - 残余23行の行集合が4文書で一致（hex32・一意）
   - per-row demand が K1097/K1102/判定gate記録で全行一致し、総和 50,670 == hist重み付き和
     40,065·1 + 4,857·2 + 297·3
   - provider hist {1:40,065, 2:4,857, 3:297} の総和 == 45,219 == 監査の providers_touching_residual23
   - **triple availability表（23行分）の総和 891 == 3×297**（各triple providerは3行を被覆することによる
     交差恒等式（出版READMEには未記録）
   - 生成事象 150,765 == 23×C(115,2)=23×6,555・触れる宇宙 137,959 == safe8 45,263 + unsafe8 92,696・
     providers 45,219 == 45,263 − 44（除外50根のうち44根が23行に接触）・44+6 == 50
   - greedy 9根の選定順・covered_rows・gains hist {3:6, 2:2, 1:1} がK1097/K1102で完全一致し、
     covered 23行が残余23行のexactly-once分割（和23・重複0）
   - matching 23（K1097/K1102/判定機Kuhn）の一致
   - gate 18件が全てok・監査interval [8,9]と判定interval_before/after [8,9]/[9,9]の一致・
     下界8==ceil(23/3)の再計算
   - pin鎖（判定→3入力・監査→K1097/K1102・K1102→K1097）の再確認

   を検査し**71/71 PASS**（外部検証機はfail-closed: 1件でも不一致でexit非零）。
4. **数え上げ証明書の外部再計算**: 3行provider零の3行
   `00000000000000003800000008002010`・`0000000000000000380000000a080000`・`00000000020000801202000000100000`
   がavailability表で0であることから、(a) 3行を被覆する根は高々2行であること、(b) k_min = ceil(3/2) = 2、
   (c) 容量 k_max = 3·8−23 = 1、(d) 判定機記録の2通りの導出（`2k+3(8−k) ≧ 23` と `21−k ≧ 20`）が
   k=0..8の全kで解を持たないこと、を発見順とは独立に外部実装で再計算して一致。
5. **新規外部観察（記録であって構造説明ではない）**: per-row triple availabilityの分布は
   範囲 0..140・平均 38.74・最小3行は上記3行で、低availability（<5）行はさらに2行
   （`00000000000000103800000008080000` が2・`00000010000000801202000000000400` が3）。
   上位6行（値 140/139/131/126/120/115・合計771）はすべて `…82108…` 型の行で全triple被覆の86.5%を占める。
   残余23行のtriple需要はこの2族に強く二極化しており、3行provider零の構造理解（判定実験READMEの次の課題3）に
   対する材料になる。

## 外部検証機と決定性

- 検証機 `scripts/verify_external_cover8_decision_20261120.py`
  （SHA-256 `7bee45ec…`・stdlibのみ・乱数・時刻・出力への環境依存要素なし）
- 監査正本 `output/external-verification-audit.json`
  （SHA-256 `17dbd6ab…`・71 checks all ok・interpretation_guard 5文言同梱）
- 同一cwd 2回 + 隔離cwd/HOME・入力別path 1回の3実行でbyte-identical。
  初版は出力JSONのdetailに絶対pathを混入させ隔離実行でbyte差分が出たため、path正規化を行った
  （出版正本の環境非依存性はrepo規約。検証機・正本とも修正後のみ出版）。

## trust境界

- 本検証は出版記録の交差検証・算術再計算・再実行決定性の確認である。触れる宇宙・safe8/unsafe8述語・
  provider幾何の第三実装による再導入は行っていない（判定機が2独立述語で137,959根全数を実施済みであり、
  それ自体は再実行で決定性のみ確認）。
- 被覆数は候補root計画の簿記であり証明書ではない。証明書抽出・receipt foldは含まない。
  REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。
- 監査下界8は任意の宇宙で有効なまま（9はP‴に特有）。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次の一手への影響

なし。fold26（先行レーン `e53cc60c` 所有）、36-witness掃引（`c427979aff` 所有）、K1146掃引の
WIN8-D10候補 `00000000010000809002000040002001` の証明書抽出・receipt foldはそれぞれ別の
単一オーナー宣言を要する別工程であり、本検証はいずれの着手権にも影響しない。行は1行も閉じていない。
