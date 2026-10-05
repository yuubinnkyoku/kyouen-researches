# Implicit/Stateless QBF を共円へ移す場合の境界

Date: 2026-10-05

**11×11空盤勝敗はUNKNOWNのまま。**

Shaik et al., *Implicit State and Goals in QBF Encodings for Positional Games* (arXiv:2301.07345, ACG 2023/2024) は、Hex等のmaker-breaker配置ゲームをQBFへ符号化し、盤面状態を持たないstateless encodingも調べている。

共円はmaker-breakerではなく、両者が同じ安全集合へ一点ずつ追加し、合法手が無い側が負けるnormal-play impartial gameである。ただしstateless化の核心は移植できる。

## 厳密なstateless再帰

手 `m_1,...,m_t` のprefixが合法である条件は、盤面配列を保持せずに次だけで決まる。

- 各 `m_t` が盤内。
- 過去の手と重複しない。
- 選ばれた任意の4手の円・直線行列式が非零。

初手側の勝ちを表す再帰は、初手側の手番では `∃ m_t (legal_t ∧ F_{t+1})`、相手手番では `∀ m_t (legal_t → F_{t+1})` とすればよい。相手に合法手が無ければ含意が全て真になり、初手側に合法手が無ければ存在量化を満たせないので、normal-playの早期終局も自然に表現される。

## 11×11での式の骨格

一行に4石置くと4点共線で違反するため、安全集合は各行高々3石。従って **K_11≤33**、全ゲームは33手以内で終わる。この上界だけで完全ゲームQBFの深さを有限化できる。

11×11では座標を4+4 bitで持つと、概略は次になる。

- 量化block: **33**（∃/∀交互）
- move coordinate bits: **264**
- 異なる手であることのpair predicate: `C(33,2)=528`
- 4手安全性のdeterminant predicate: `C(33,4)=40,920`

determinant一個は高水準predicateとして数えただけで、QCIR/QDIMACSへbit-blastすれば多数のgateへ膨らむ。

さらにK_11≥21の安全配置が既知なので、実際のゲーム木には少なくとも21手まで続く枝が存在する。浅い10手程度のQBFだけで完全勝敗を閉じることはできない。

## 論文との照合

QBF論文自身、ゲーム深さがそのまま量化交代深さになり、これが主要な難所だと述べている。19×19 Hexの完全ゲームは現在のsolverでは解けず、浅いpuzzle/endgameが主対象だった。また、盤面を暗黙化して式を小さくしても量化交代を一つ増やす方式は、実験では明示盤面方式より一桁遅い傾向だった。

共円では盤面状態そのものより「40,920個の象徴的determinant制約」と33交代が重くなるため、現時点でQBFを主solverへ置き換える優先度は低い。

ただし用途は残る。

- s4/s5のごく浅い有限証明を第三の独立検証器として符号化する。
- cover certificateの小さい局所枝をQBFへ落としてC++ exact solverとクロスチェックする。
- determinant relationをBDD/DFAで圧縮できた場合、Compressed Game Solvingとの融合を試す。

したがってQBFは**本命探索器ではなく独立検証・小深さoracle候補**と判断する。

## 再現

`research/experiments/n11-literature-transfer-20261005/scripts/qbf_skeleton.py` がn=4..11の構造的predicate数を出力する。
