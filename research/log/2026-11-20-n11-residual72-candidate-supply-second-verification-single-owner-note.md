# n11 残余72行候補供給正本の独立第二検証: single-owner declaration

K1075（残余72行のfull cache-join候補供給再構築）の出版正本に対する、出版済み記録のみを用いた独立第二検証を本ノートの管轄とする。

- **担当レーン**: 本実行（2026-11-20）。
- **目的**: K1075の出力JSON・resolve7・fold9/fold10等の出版正本をSHA-256で固定し、残余72行の出自、36-root witnessの幾何被覆、D4正準形、7石安全性、1回被覆、最大matchingの下界・上界一致、K1075出力の主要集計値を、K1075本体のcandidate-universe構築関数を再利用せず独立に検査する。
- **検証方式**: 独立実装によるD4変換・全単石削除・厳密整数determinant（四点共円判定）を用いる。各witness rootの被覆行を再導出し、36本が72行を重複なく被覆することを確認する。最大matchingは各rootが高々2行を覆うという上界36と、実際の36本・72行の完全matchingで証明する。
- **入力pin**: K1075候補供給正本 SHA-256 `49b6f85f6b51cfdd8a59c7797223da3d8797885d3c992ce67dc9dae629a883fa`、resolve7正本 `207f4094a906817ebb4bbc5ad9b90c203c6a334ee6c8d9a501661257a0e1ce3f`、fold9正本 `24db2352ad0d94ee4a76ec3de294f02cbdac7899f0b6ef64ea695d261017cdc2`、fold10正本 `bed7d33193299a0aa06ea4e076562dfa46251d20d5c3c4ca7fd231ffe854908a`、第17証明書検証正本 `c1073bae1d056db7f56d04a77fd9889d1e297a82a07537ddcd02c00d329dbabc`、39-live掃引正本 `22953ae16a6002d87638531f2ca9fd286f6736b834fa296e5648505ada9074dc`。
- **管轄外**: K1075のfull corpus/cache join再実行、候補根の新規判定、depth-10 sweep、証明書抽出、receipt fold、add-two-stones、depth>10探索。36-root sweepは既存の単一オーナー宣言（`2026-11-20-n11-residual72-36witness-sweep-single-owner-note.md`）に属し、本検証はこれを実行・変更しない。
- **解釈**: matching・被覆は条件付き探索計画の幾何検査であり、証明書や勝敗ではない。REFUTED-D10はLOSS証明ではない。標準11×11空盤・二石root・S2・class 1/2/4はUNKNOWNのまま。

検証が完了したら、再現コード・機械可読結果・研究logを独立experimentとして追加し、既存K1075を追記更新する。branch/PRは作らない。
