---
id: K0762
title: S2 {59,60} 証明書{73}のS6 worklistはK0675スイープで全て認定済み（新規S6計算ゼロ・残り39,507 orbit）・30証明書閉鎖ロードマップ
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0757
  note: 修正版milestone-4 manifestの証明書{73}（greedy step 6・bit 32・s6All 3,868・
    s5Reps 94・rawObligations 7,890）を対象とする
- type: depends_on
  target: K0675
  note: 94五石位置universe・3,868 S6スイープ（3,854 WIN/14 LOSS・感受性証明書fails 0）が
    証明書{73}のS5/S6集合と同一（key-for-key・算術・部分集合の3系統で機械照合）
- type: depends_on
  target: K0754
  note: milestone-3の{73}単体3,868・greedy順序（step 6）と一致
artifacts:
- path: research/experiments/n11-s2-5960-cert73-reuse-20261112/scripts/cert73_reuse_check.py
  role: source
  note: 修正版manifestとs6sweep（s5_verdicts.json・sweep_results.json）を読み、
    S5鍵一致・義務算術・S6数一致・14 LOSS部分集合・bit51計数・30証明書閉鎖ロードマップを
    全て再実行する標準ライブラリのみの検証スクリプト
- path: research/experiments/n11-s2-5960-cert73-reuse-20261112/output/cert73_reuse_summary.json
  role: data
  note: 機械可読の照合結果（94/94・7,813+77=7,890・14/14・残り39,507 orbit/3,196,057 cost辺・
    bit51 421・閉鎖prefix {73} 35,308）
- path: research/experiments/n11-s2-5960-cert73-reuse-20261112/output/cert_closure_roadmap.tsv
  role: data
  note: 30証明書の declared/seen/minCost/maxCost/sumCost/閉鎖prefix（cost昇順消化の到達順位・
    declared==seen 30/30）
- path: research/log/2026-11-12-n11-s2-5960-cert73-k0675-reuse.md
  role: log
  note: 実行記録・再現手順・blocker 73方向規約の未解決問題・実装教訓
scope: 修正版milestone-4 manifest（K0757）の証明書{73}に限定したworklist構造分析と既存verdictの再利用確認。blockerの勝敗認定・FW oracle自体の計画条件下での証明・S2/rootの判定は含まない。
evidence: >-
  修正版milestone-4 manifest（md5 452b4336edbe272a49dcd76c4a7764af・byte-exact再結合）の証明書{73}（step 6・bit 32）について、
  (1) s5Reps 94鍵がK0675の94五石位置universeと正規化後にkey-for-key完全一致（94/94）、
  (2) universe合法S6子合計7,813と対称性二重カウント差77（39→78・38→76）の和がrawObligations 7,890と完全整合、
  (3) s6All 3,868 orbitとK0675スイープ3,868 S6が同数（S6集合はS5 rep集合で決まる）で、
  loss_s6_coversの14 LOSS S6鍵が全てs6Allに含まれる（14/14）、
  を機械検証した。K0675のverdict（3,854 WIN-for-mover・14 LOSS-for-mover・感受性証明書4,288件独立監査fails 0）により、
  証明書{73}のS6 worklist消化に必要な新規計算はゼロである。残りworklistは39,507 orbit（−8.92%）・3,196,057 cost辺（−8.09%）。
  また43,375 orbitをcost昇順で消化する想定の30証明書閉鎖ロードマップ（閉鎖prefix・declared==seen 30/30）を算出した。
  cert {73}の3,868 S6のうち421 orbitがbit 51を含む（frontier 2,401 cacheとの重複候補の定量的下限）。
  blocker 73の閉鎖判定はデータreadyだが、S5 verdict→blocker verdictの方向規約が未確認のため本項では判定しない。
---

# 証明書{73}はK0675で解決済み・30証明書の閉鎖ロードマップ

## 発見

S2 {59,60}（best S3 r=61）のgreedy証明書{73}（step 6・bit 32）について、
そのS6 worklist（3,868 orbit）とS5義務（94 orbit・7,890）が
**K0675のs6sweepと同一の計算対象であることを3系統の機械照合で確認した**:

1. **S5鍵一致 94/94**（正規化後key-for-key）。
2. **義務算術一致**: 子合計7,813 + 対称性二重カウント差77 = 7,890。
3. **S6一致**: 同数3,868・14 LOSS鍵全件含有（14/14）。

K0675は3,854 WIN-for-mover / 14 LOSS-for-mover を認定済みで、感受性証明書4,288件の
独立監査はfails 0。**したがって証明書{73}の消化に新規S6計算は不要**である。
S2 {59,60}の完全worklistは43,375 orbit・3,477,178 cost辺から
**残り39,507 orbit（−8.92%）・3,196,057 cost辺（−8.09%）**に減る。

これはmilestone-3/4がK0675の94位置universeを「78 FW oracle」として条件扱いしていたのに対し、
証明書{73}に限ればそのS5/S6 verdictが機械検証済みの既存成果で閉じることを意味する。

## 閉鎖ロードマップ（cost昇順消化）

43,375 orbitをcost昇順で消化する想定で30証明書それぞれの閉鎖prefixを算出した
（declared==seen 30/30）。最速は{73}の35,308、次に{90,96} 40,410・{80,84} 41,123・
{27,93} 41,125・{5,115} 41,227・{91,95} 41,509、最大43,374（cert_closure_roadmap.tsv）。

## 未解決・レジューム

- **blocker 73の閉鎖判定は実行していない**。S5子のFIRST_WIN/SECOND_WINから
  blocker verdictへの伝播方向の規約が未確認で、q60のT1と単純パリティ推导が逆向きになる。
  鎖機械（s2_worklist系）のコードで規約を確認してから判定すること。勝敗は本項では一切断定しない。
- cert {73}の3,868 S6のうち**421 orbitがbit 51を含む**。frontier 2,401 cacheとの
  verdict再利用の定量的下限。
- 残り39,507 orbitのcost昇順消化（外部solver・共有cache）。

本項は78 FW oracle条件下のworklist構造分析である。いかなるblocker・S2・空盤の勝敗も含まない。
11×11空盤・二石root {49,60} は **UNKNOWN** のままである。
