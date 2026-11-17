# 2026-11-17 長期レーン: 証明書状態共有のD4正準化キー測定（v1測定の対称キー下訂正・71eはband間共有あり・11×11はUNKNOWNのまま）

## 何をしたか

本日出版の測定（`9f2422d3`）は「完全一致キーの測定下界」でD4正準化キーを未量化としていた。
その追加量化として、同一の3 band（73j・72d・71e・同一入力pin）の全証明書行状態をD4正準形
（11×11盤の8対称変換の最小hex）に写像して共有統計を再計算した。
script `measure_cert_state_sharing_d4canon_20261117.py` + output JSON
`class2-lane-cert-state-sharing-d4canon-measurement-20261117.json`
（2回実行byte-identical・md5 `6b133be2`）。正確性ゲート: 汎化canon関数が73j manifestの
**16件の出版d4_canon_root全件を再現**（うち非正準root含む）してから測定。

## 測定結果（v1との差分が本質）

1. **band内**: 3 bandとも **exact distinct == D4正準distinct（マージ0.00%）**。これは構造的帰結:
   証明書の行状態はrootの石をすべて含むため、同一band内で回転コピーが別rootの証明書に現れるには
   2 rootがD4同値である必要があり、**3 bandともroot間にD4同値対が存在しない**
   （manifestのcanon相互非重複検査と整合）。→ band内共有memoの評価はv1のexact値（重複行19.05-24.61%）が
   そのまま最終値。
2. **band間（v1の訂正）**: exactキーでは71eは72d/73jと共有0だったが、**D4キーでは
   71e∩72d = 7,315 states・71e∩73j = 17,301 states・3-way共通 = 258 states**が共有される。
   72d∩73j = 17,939はexactと同一（この対は向きも揃った共有のみ）。
   → **v1の「71eは深い位置でも全く共有しない」はexactキー観察であり、対称キーcacheでは不成立**。
   恒久cross-band cacheの価値は対称キー採用時に全band対に拡大する（71eのstatesの~1.7-4.1%が他bandと共有）。
3. **含意**: 対称キーverdict cacheは (a) 転送確認bit（73i 2.13%・73j 6.97%のコスト）の直接削減に加え、
   (b) 近接band対に加えて**離れたchild間でも~2-4%の共有を捕まえる**。73k証明書（73i/73j系と同コア構造）は
   72d/73jとの直接共有に加え71eとの対称共有も見込める。

## 解釈上の注意（interpretation guard）

- 効率測定のみで、いかなるmanifest行も閉じない。WIN7-D10証明書は**個別7石rootのdepth-10内先手勝ちのみ**を
  証明し、REFUTED-D10はLOSS証明ではない。**11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4 の勝敗はいずれもUNKNOWNのまま**。

## レジューム

1. 73i証明書のBigInt bytes再検証（並走の出版待ち・着手禁止）は本レーンの次の検証候補。
2. 73k証明書出版後のbytes再検証時、対称キー共有の予測（71eを含む全band対）を実測で検証できる。
