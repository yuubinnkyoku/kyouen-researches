# 残余23行 8根被覆判定の外部第二検証の実行記録（2026-11-20）

単一オーナー宣言: [single-owner note](2026-11-20-n11-residual23-eight-root-cover-decision-external-second-verification-single-owner-note.md)
（commit `e8d6025745`・宣言 2026-11-20T13:29:51Z・着手権確保）。

対象は commit `b4d8b3ac52`（宣言 `cb31752551`）で出版された
[8根被覆判定](../experiments/n11-residual23-eight-root-cover-decision-20261120/README.md)
（K1097 更新: 残余23行のP‴上最小被覆 9根・interval [8,9]→[9,9]・数え上げ証明書つき）。
検証中の並走状況: 宣言時点（13:30Z）では未実施だったK1097「次の一手」第1項のgreedy 9根depth-10掃引が
13:35:51Z（commit `e9ea153bc4`）にK1146として着地した（宣言 `51bbb93880`）。本検証はそれとは独立の、
判定機・出版正本・入力pin鎖の外部確認であり、着手権・既存成果には影響しない。

## 発見順

1. **入力取得とpin検証（13:29Z）**: 判定機（`da51063c…`・39,301 bytes）・判定正本（`c5aaf83e…`・
   16,324 bytes）・K1097再解決正本（`2896deb0…`）・下界強化監査正本（`1310ef74…`）をcommit pin付き
   raw URLで取得しSHA-256照合。K1102第二検証正本（`d0b5d845…`）は判定機のREADMEに記載のrepo path
   （`n11-residual72-refuted50-refsolve-second-verification-20261120`）から取得し照合。5 pin全一致。
2. **pristine再実行 pass A（13:30〜31Z）**: 同一treeで2回実行（各41〜42秒）。出力はいずれも出版正本と
   SHA-256一致・byte-identical。実行統計（UNSAT・gates 18 all ok・cover3呼び出し451・メモ211・
   Shape B試行100）も出版READMEの記載と同一。
3. **pass B（隔離）**: 別tree・隔離HOME・`env -i`・入力は別pathのコピーとして再実行（42秒）。
   byte-identical。さらに `PYTHONHASHSEED=random` を明示した隔離実行（pass B'）もbyte-identical。
   出版社の3実行ではhash seed明示はなかったため、決定性の追加支持。
4. **外部検証機 `verify_external_cover8_decision_20261120.py`**: 出版機と別実装として、4正本＋4再実行出力
   だけを入力に記録レベル交差検証を構成（71チェック・fail-closed・stdlibのみ）。主な検査:
   - 23行集合の4文書一致（hex32形式・一意性）
   - per-row demand がK1097/K1102/判定gate記録で全行一致し、総和 50,670 == 40,065·1+4,857·2+297·3
   - provider hist 総和 == 45,219 == 監査 providers_touching_residual23・eligible 5,154 == 4,857+297
   - **triple availability表（23行）の総和 891 == 3×297**: 各triple providerは3行を被覆するので
     availability の行和は hist{3} の3倍に厳密に一致しなければならない。出版READMEには未記録の
     交差恒等式で、出版正本内部の整合を独立に固定する。
   - 生成事象 150,765 == 23×C(115,2)・触れる宇宙 137,959 == safe8 45,263 + unsafe8 92,696・
     providers == 45,263 − 44・除外50根 == 44接触+6非接触
   - greedy 9根がK1097/K1102で選定順・covered_rows・gains {3:6,2:2,1:1} 完全一致、covered 23行が
     残余23行のexactly-once分割・matching 23の3文書一致・Kuhn記録23
   - gate 18件全ok・interval [8,9]/[9,9]の監査・判定間一致・下界8==ceil(23/3)再計算
   - pin鎖: 判定→3入力・監査→K1097/K1102・K1102→K1097
   - 数え上げ証明書: 3行provider零の3行がavailability表で0であること、k_min=ceil(3/2)=2、
     k_max=3·8−23=1、両導出（`2k+3(8−k)≧23` と `21−k≧20`）がk=0..8の全kで解なし、を再計算
5. **検証機の環境依存性の捕捉・修正（出版前）**: 初版は出力JSONのdetailフィールドに入力の絶対pathを
   そのまま記録し、隔離実行（別path）でのみbyte差分が発生した（隔離実行との比較で byte 1514 / line 39 に差分）。
   path正規化（basename・index）に修正し、同一cwd 2回＋隔離cwd/HOME/別path 1回の3実行でbyte-identical
   （監査正本 SHA-256 `17dbd6ab…`・71 checks all ok）を確認してから出版した。出版正本の環境非依存性は
   repo規約（これまでの輸送破損・環境依存事故の教訓）で、検証機も例外にしない。
6. **新規外部観察（構造説明ではなく測定の記録）**: per-row triple availability分布は範囲 0..140・
   平均 38.74。零行は3行（`00000000000000003800000008002010`・`0000000000000000380000000a080000`・
   `00000000020000801202000000100000`）、低availability（<5）行はさらに2行
   （`00000000000000103800000008080000` が2・`00000010000000801202000000000400` が3）。
   上位6行（値 140/139/131/126/120/115・合計771）はすべて `…82108…` 型で全triple被覆の86.5%を占める。
   残余23行のtriple需要は「82108族に集中する行」と「triple providerにほぼ到達できない行」の2族に
   二極化している。3行provider零の構造理由（判定実験READMEの次の課題3）を考える際の材料になる。

## 実行環境

- Python 3.12（出版社の実行環境とは別ホストの別プロセス）。stdlibのみ。
- 判定機の4実行は GPU不使用・並列なし・各41〜42秒（出版社の約41秒/runと一致）。

## 解釈規約

本検証は record-level の交差検証・算術再計算・再実行決定性の確認である。触れる宇宙・safe8述語・
provider幾何の第三実装による再導入は行っていない（判定機が2独立述語で全数実施済みで、それ自体は
4回のbyte-identical再実行で決定性を確認）。被覆数は候補root計画の簿記であり証明書ではない。
REFUTED-D10はLOSS証明ではなく、nodes数・solved数を勝敗として読まない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWNのまま。**

## 次回への引継ぎ

- 本検証で閉じた工程はない（行は1行も閉じない）。残余23行の次の一手はK1146掃引のWIN8-D10候補
  `00000000010000809002000040002001` の証明書抽出（着手時単一オーナー宣言必須）と第5ラウンド再解決
  （pool 120,416根・被覆対象20行）、fold26（先行レーン所有）の出版待ち。
- triple availability二極化の構造説明（82108族の集中と零行族の欠落の幾何学的理由）は未着手。
- fold26出版後は本検証と同様の 出版byte pin → pristine再実行 → 記録交差 の外部検証が再利用可能。
