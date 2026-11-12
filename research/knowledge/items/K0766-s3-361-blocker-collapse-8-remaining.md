---
id: K0766
title: S3 {59,60,61}のblockerは全D4像照合で102/110が即W4閉鎖・残り8個（3 V4類）・残work新規S6 7,880/cost 616,491・judgedS6矛盾（4,342 vs 3,868）はhex転写破損と確定
kind: computation
status: computed
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0675
  note: 94五石位置オラクル（FW 78+SW 16・3,868 S6 verdict）をD4像込みで再利用する
- type: depends_on
  target: K0757
  note: published ladderの61 blocker（raw一致のみ）は全D4像照合で8 blockerに訂正縮小される
- type: depends_on
  target: K0762
  note: judgedS6 3,868の再確定と方向規約の確認により「blocker 73閉鎖判定はデータready」の前提が確定した
artifacts:
- path: research/experiments/n11-s3-361-blocker-collapse-20261112/scripts/blocker_collapse_audit.ts
  role: source
  note: オラクル94位置を埋込み（s5_verdicts.json由来）・全錨（94/7,890/3,868/110/102/8/3類・
    per-representative統計・union 8,340/460/7,880/616,491）をassertする自己完結TS検証script
- path: research/experiments/n11-s3-361-blocker-collapse-20261112/output/blocker_collapse_summary.json
  role: data
  note: 機械可読の照合結果と3件の訂正記録（judgedS6破損・{23}統計・61→8 blocker）
- path: research/log/2026-11-12-n11-s3-361-blocker-collapse-judgeds6-correction.md
  role: log
  note: 実行記録・矛盾解消の経緯・実装教訓（hex定数の手再埋込み禁止・fetch由来埋込み）
scope: S3 {59,60,61}のS4子110個のW4閉鎖構造と残8 blockerのworklist会計。blocker自体のW4/second-win判定・S2/root/空盤の勝敗は含まない。
evidence: >-
  K0675の94五石位置オラクル（FW 78・SW 16・repo s5_verdicts.json直接fetch）を全D4像照合に拡張し、
  S3 {59,60,61}の合法S4子110個について (1) 102個がオラクルFIRST_WIN像を直接持ちW4即閉鎖、
  (2) blockerは8個 {5,23,27,31,89,93,97,115} のみで3 V4類 {5,115}/{27,93}/{23,31,89,97} を形成、
  (3) V4類内の統計は完全一致（{23}≡{31}: S5 100・oblig 9,014・S6 4,417）、
  を機械検証した。4代表blockerのS6和集合は8,340 orbit、うちjudged 460（K0675 3,868 S6と一致）・
  新規S6 7,880・cost 616,491（S7合法辺）。前回セッションのjudgedS6 4,342は埋込みhex定数の
  転写破損（先行ゼロ過多でビットずれ）によるartifactであり、正しくは3,868（7,890 raw edges）。
  方向規約はchain_audit.py機関で確認済み（W4(S4)=∃FIRST_WIN S5子・S3 proven-first⟺全S4子W4）。
---

# S3 {59,60,61} blockerの102/110即閉鎖と残り8個・judgedS6矛盾の解消

## 発見

S3 {59,60,61}（S2 {59,60}のbest S3）の証明に必要なS4子のW4判定について、
K0675の94五石位置オラクルを**D4像照合**（raw一致のみでなく8対称像すべて）で使うと:

- 合法S4子は110個、うち**102個がFIRST_WINオラクル像を直接持ちW4即閉鎖**。
- **残blockerは8個のみ**: {5, 23, 27, 31, 89, 93, 97, 115} = 3 V4類
  （{5,115}・{27,93}・{23,31,89,97}）。V4類内で統計完全一致を機械検証。
- K0757のpublished ladder（61 blocker・raw一致のみ）は8 blockerに訂正縮小。
  greedy証明書{71},{82},{104}等の大半はblocker閉鎖に不要。

4代表blocker（5, 27, 23, 31）のS6 worklist会計:

| u | S5 | oblig | S6all | judged | 新規S6 | cost |
|---|----|-------|-------|--------|--------|------|
| 5 | 54 | 4,795 | 2,191 | 159 | 2,032 | 159,266 |
| 27 | 54 | 4,698 | 2,150 | 77 | 2,073 | 157,179 |
| 23 | 100 | 9,014 | 4,417 | 234 | 4,183 | 330,227 |
| 31 | 100 | 9,014 | 4,417 | 234 | 4,183 | 330,227 |
| 和集合 | — | — | 8,340 | 460 | **7,880** | **616,491** |

S2 {59,60}の完全worklist 43,375 orbit（K0762）に対し、S3 {59,60,61} proven-firstに
必要な新規計算は約7,880 S6・616,491 cost辺（**約82%削減**）。

## judgedS6矛盾（3,868 vs 4,342）の解消

前回セッションで同一94位置のはずのS6子集合が3,868と4,342の2通りに計算された矛盾は、
**4,342側の埋込みfwHex/swHex定数が転写破損していた**（先行ゼロ過多で約8ビットずれた位置。
6軌道がsweep frontierと不一致・raw edges 7,882≠7,890）ことによるartifactと確定した。
repoのs5_verdicts.jsonを直接fetchして再計算するとjudgedS6=3,868（7,890 raw）が
manifest・sweep・K0675と完全一致する。以後、hex定数の手再埋込みは禁止し
fetch由来の埋込み+自己assert（本項の検証script方式）を用いる。

## 副次の訂正

- 前回のper-blocker統計「{23}=98/8,859/4,416」は誤り。{23}は{31}と同一V4類で
  100/9,014/4,417（類内完全一致の機械検訳込み）。
- K0672の「cert {73} worklist ≡ K0675 sweep」一致はblocker 73 = rot180(blocker 47)・
  オラクル位置がblocker 47（S4 {47,59,60,61}）の子であることでも説明がつく。
  blocker 73∈fc（W4閉鎖済み）であり、K0762の「blocker 73閉鎖判定はデータready」の
  方向規約もchain機関で確認済みのため閉鎖判定可能。

## 未解決・レジューム

- 残8 blockerのW4/second-win判定（新規S6 7,880の実計算）。cost昇順バッチmanifest生成が次段。
- 8 blocker閉鎖でS3 {59,60,61} proven-first → S2 {59,60}条件付き判定へ。
- 同一D4像議論の他S2（q60 classA 8 S2）への適用。

S2 {59,60}・二石root・11×11空盤の勝敗は本項では一切判定しない。**UNKNOWNのままである**。
