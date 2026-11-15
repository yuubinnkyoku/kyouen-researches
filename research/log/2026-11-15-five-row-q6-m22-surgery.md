# 2026-11-15 (5,6) m=22 surgery・class-split resume・(8,9) m=29 部分記録 セッションログ

- 第1セッション（five-row-q6-m22-surgery-20261115・完了）: K0815 の m=21 witness
  （24石）を種に 5x22 bounded-edit surgery を sd<=6 まで完全列挙（両 x-offset 埋め込み
  offX=0/1・環境再構築後に再実行して事前記録と bit-exact）。
  - final-state leaves: offX=0 (2,2) 25,158 / (3,3) 4,227,320・offX=1 (2,2) 24,976 /
    (3,3) 4,180,654。すべて nSafe=nRmLeaves・witness 0・T' 単一セル。
  - **系: 5x22 の全 24石以下 deficient-maximal 配置（K0852 witness 含む）は m=21 種の
    両埋め込みから対称差 >=7**。
  - C4 census 完全性 PASS @ (5,6,21)/(5,6,22): chord-pair ≡ all-triples
    （810/902 曲線 = 805/897 円 + 5 行）。1-double-row 6点円は 5x21/5x22 に存在しない。
  - CTRL-1 PASS: 5x21・seed-(5,1) 23石 → (2,2) surgery → nRmLeaves 6,841・witness 3つ
    （seed + 1-swap 変種2つ (10,2)->(11,2)/(12,2)）を再発見。
  - witness ジャンプ幾何: K0852 m=22 witness と m=21 種の全 8 埋め込み
    （4 isometries x offX 0/1）の対称差 = min 28（id@0/H@0）→ 最低 14 石移動。
    (5,5) m=24->25 precedent・K0852 の 5x23 surgery 負と一貫。
  - 副次発見: m=21 witness の sd<=2 球内にちょうど 3 つの witness（完全列挙・2変種は
    独立 all-triples 系で安全・極大 PASS・rows [4,5,5,5,5]）。
  - 反映: README・output/（records.jsonl 5行・c4_census_check.json・
    c4_census_check_5x21.json・ctrl1.jsonl・m22_off0_pp2.jsonl・m22_off0_pp3.jsonl・
    m22_off1_pp2.jsonl・m22_off1_pp3.jsonl・sd_k0852.json・verify_variants_5x21.json）・
    seeds/（seed_w56_21.json・ctrl1_seed.json）を c559a839 で、scripts 4ファイル
    （census_extract.js は surgery.js からの機械抽出・転写 md5 検証済み・
    c4_census_check.js・sd_k0852.js・verify_variants_5x21.js）を e898a9a0 で push。
    surgery.js 自体は eight-row-q9-m29-surgery-20261115/scripts/surgery.js
    （md5 94baa517b788efa02dc761b892fc8440）と verbatim 同一として README 参照。
- 第2セッション（five-row-q6-m22-class-split-20261114 の修復+resume 完了）:
  - report.md が 2026-11-15 06:23Z の自分の IN FLIGHT push（e2750cb3）で
    「undefined + 追記断片」に破損していたのを発見。親 commit d4ceb255 から原寸復元し、
    追記を完了版に差し替え（破損経緯は report.md に注記）。
  - 残り 11 canonical class の 250s sweep 完了: 全 19 正準類 attempted・すべて INDET。
    事前 conflicts（マシン共有下の下界を含む）: {0,3}=1,129,613・{0,4}=1,176,424・
    {1,2}=1,805,810・{1,3}=1,943,081・{0,1,3}=1,965,748・{0,1,4}=1,950,137・
    {0,2,3}=1,906,539・{0,2,4}=1,964,640・{1,2,3}=1,865,242・{0,1,2,4}=1,829,327・
    {0,1,3,4}=1,826,041。
  - {0,3}/{0,4} のクリーン再実行（高速環境・単独実行）: 3,456,380 / 3,513,305
    conflicts・いずれも INDET。対照 5x21 class {0} SAT 330,743 conflicts bit-exact
    （19.91s 完走・decode verifyConfig PASS・CNF md5 bf88b550...）。
  - 旧 sweep の {0} 3,556,467 / {0}krow0:4 2,019,686 は K0852 が {0} を SAT 解決した
    ことで witness 直前で time-cut していたと確定。
  - 反映: report.md 修復+追記・output/records-resume-20261115.jsonl（14行）・
    raw/（c03_tail.txt・c04_tail.txt・ctrl5x21_c0_tail.txt）を 1e398da0 で push。
- 第3セッション（eight-row-q9-m29-frontier-20261115・部分記録のみ）:
  - rowY=3: kissat 4.0.4 が INDET 25,375,195 conflicts / 1665s で環境リセットにより
    2回 kill。cap 5400s の再実行は bash 280s 制限で不可 → 長期レーンへ。
    rowY=0/1/2 の CNF 未生成。IN FLIGHT claim 継続・判定結果なし。
- CSV 反費: results/fixed-width/mwq_stabilization.csv の (5,6) 行を更新（source 列に
  five-row-q6-m22-surgery-20261115 を追加・note に 19/19 resume・sd<=6 完全負・C4 PASS・
  K0852 sd=28・m=21 witness sd<=2 球内 3 witness を反映・行全体置換）。
