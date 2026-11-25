# n11 残余72行 WIN8-D10 candidate `00000000000000003800000008003180` の証明書抽出・独立検証 単一オーナー宣言（2026-11-20）

本レーンは K1086（残余72行 add-two greedy 23根 depth-10 sweep、正本 SHA-256
`3045e15295af9b85b86578b5e8d55a8b325466eac576ee15b8450f6acb9b9ced`）で
両AND順序 uncapped WIN8-D10 candidate として確定した7根のうち、
`00000000000000003800000008003180`（greedy計画順第一位・主張被覆4行）の
証明書抽出・独立検証を担当する。宣言時の main は `99b940d57ba84edc9d51f5f68f94bc9e7ccc98f1`。

並走レーンの既存宣言
`research/log/2026-11-20-n11-residual72-win8-certificate-extract-single-owner-note.md`
（commit 4496c888・対象root `00000000000200003800200008180000`）との重複はなく、
本宣言の対象は上記1根に限定する。

## 範囲（やること）

- K1086正本をSHA-256 pinで読み、対象root・両AND順序のWIN8-D10 probe
  （nodes 903,977 / 1,146,417・pilot_d6制御 nodes 3,402）を runner v17
  （git blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`）で再現する。
  2026-11-20時点の本レーン再現: 両順序 loss=true uncapped・nodes 903,977/1,146,417・
  terminal石数 [14,18] で出版値と完全一致済み。
- repo-verbatim WIN7 extractor（seventeenth 実験 `class4_child1_cert_extractor_exact_ms23.ts`・
  git blob `c267f260d1d6fcc49ed5367509e854c81822497e`）の探索核を8石rootに拡張する。
  fbtOR には runner v17 の saturated-chain 直接計算修復を適用する
  （fbt_drops==0 を構成で保証。一つでも欠落 triple があれば fatal 扱い）。
  盲抽出（kill tableなし pref=null）・乱数・時刻依存なし・決定的順序。
- 証明書は n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS 形式:
  root行 + 全winner-to-move局面の選択手行（boards昇順・一意）。各行は残りdepth-9予算内の
  uncapped勝利で裏付けられる（extractorは自己検査付き: 深さ打切りで証明できない
  loser応手が1つでもあれば fatal）。
- 抽出を同一cwd 2回 + 別cwd別プロセス1回で再実行し、証明書bytes完全一致を確認する。
- 探索器をimportしない独立検証器（BigInt 3x3余因子展開・seventeenth検証器の8石拡張:
  root安全性・root mobility・全winner-to-move局面の行存在・選択手合法性・
  全loser応手展開・終端条件・被覆union過不足・行昇順一意・終端石数域fail-closed検査）
  で独立検証する。可能な限り第2方法（Bareiss 4x4整数行列式）を併用する。
- 機械・入力・証明書・検証結果・失敗や打切りをrepoに再現可能な形で記録する。

## 対象外（やらないこと）

- 他のWIN8候補（残り5根）の抽出、safe8 pool再解決、round-3再解決
  （いずれも既存宣言どおり並走レーン保有）、receipt被覆幾何・receipt fold、
  S6行の閉鎖、二石rootや空盤の勝敗判定は一切行わない。
- 対象root以外の新規depth probe / 掃引は行わない。
- REFUTED-D10、節点数、solved数をLOSSや勝敗として解釈しない。

## 解釈規約

本証明書は指定8石rootのゲーム木だけを証明する。S6親行の閉鎖には別途、
二手の量化を正しく扱う被覆・receipt証明が必要である。
**標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 は
すべて UNKNOWN のままとする。**
