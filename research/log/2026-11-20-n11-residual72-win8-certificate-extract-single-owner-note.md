# n11 残余72行 WIN8-D10 candidate の証明書抽出・独立検証 単一オーナー宣言（2026-11-20）

本レーンは K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）で
両AND順序 uncapped WIN8-D10 candidate として確定した7根のうち、
`00000000000200003800200008180000` の証明書抽出・独立検証を担当する。
宣言時の main は `737f2f35bef74fc2859b6d36f66c94aaf159b2bd`。

## 範囲

- K1086の正本をSHA-256 pinで読み、対象root・両順序のWIN8-D10 probe・pilot制御を再確認する。
- 既存の repo-verbatim WIN7 extractor の探索核を再利用し、8石root（second mover to move）から
  全合法な初手を展開するWIN8戦略証明書をblind抽出する。証明書はroot・全winner-to-move局面・選択手を完全収録する。
- 抽出を別プロセスで再実行し、証明書bytesと要約が一致することを確認する。
- 探索器をimportしない独立検証器で、rootの全合法なsecond-mover初手・各winner応手・全second-mover応手・終局条件・証明書行集合の過不足を検査する。可能な限り異なる整数行列式実装を併用する。
- 機械・入力・証明書・検証結果・失敗や打切りをrepoに再現可能な形で記録する。

## 対象外

- 新規depth probe / sweep、他の6 WIN8候補の抽出、safe8 pool再解決、receipt被覆幾何、receipt fold、S6行の閉鎖、二石rootや空盤の勝敗判定は行わない。
- 本証明書は指定8石rootのゲーム木だけを証明する。S6親行の閉鎖には別途、二手の量化を正しく扱う被覆・receipt証明が必要である。
- REFUTED-D10、節点数、solved数をLOSSや勝敗と解釈しない。

safe8 pool再解決は既存の単一オーナー宣言
`2026-11-20-n11-residual72-safe8-refuted16-refsolve-single-owner-note.md`
の範囲であり、本レーンはそこへ着手しない。

**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は UNKNOWN のままとする。**
