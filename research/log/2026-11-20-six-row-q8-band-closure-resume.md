# 2026-11-20 six-row q=8 band-closure resume（高速レーン・m=60..108 掃引・witness-free 19..108）

## 概要

IN FLIGHT 実験 `research/experiments/six-row-q8-band-closure-22-370-20261114/` を
単一オーナー宣言（commit `7bc633a6bc5094b04b8bd5e36a33e87662f85852`・先行出版）の下で再開した。
K0848 が残した witness 探索フロンティア 6x60 から def-mode 掃引を実行し、
**m=60..108 の49幅すべて UNSAT（欠損極大非存在の完全証明）**・m=106 は --lex=H 交差符号化でも
UNSAT。witness-free 幅集合は {19..59} から **{19,...,108}** に拡大し、
K0821 監査規約の鋭い形は **M_{6,8} = 19 or M_{6,8} >= 110**（上界 371〔K0318/K0806〕不変）。
掃引は m=109..370（262幅）を残して IN FLIGHT 継続。

## 環境再構築と較正

- kissat 4.0.4 official linux-amd64 を GitHub release `rel-4.0.4` の同梱バイナリから取得。
  md5 `3a5eba830aa6008a604fcc9bbe99a325` は five-row-q7 band-closure 再開時および
  K0848 記録の pin と同一。GCC が使えない本次実行環境では source build の代わりに
  release バイナリを用いた（pin 値が同一なので決定性は失われない）。
- genfast3.js（md5 `12c2bd9cb3b24887fc3896f7ea9bcadf`）・lean6q8.sh・decode_verify.js は
  band 実験dir正本を raw 直取得（実験dirは2026-11-14/15以降不変）。sat.js
  `0cc6021a4e523a0d7f4d5ea0f5f5d40c`・sat2.js `282ae832efa0080127c6c153e65e1c3c`・
  verify_witness.py は seven-row-inband-families 実験dir等の正本から取得。
- **較正**: m=45 def CNF 再生成 meta が既刊 band2 record と完全一致
  （vars 31,422・clauses 112,417・curves 816）・kissat 再実行 **UNSAT rc=20・conflicts 518,261**
  が既刊（2026-11-14T21:18:15Z・518,261）と bit-exact 一致（24.3s）。これで宣言ノート記載の
  較正を再確認した。

## 掃引実績

- 幅: m=60..108（49幅）・def-mode 単一インスタンス（lean6q8.sh・230s cap）。
  全幅 UNSAT・INDET 0・SAT 0。conflicts 系列 min 448,269（m=61）・max 1,048,030（m=83）。
  時間 26s..79s/幅・総 2,732s。曲線数は 1,216（m=60）→ 2,940（m=106）。
- **交差符号化**: m=106 は --lex=H（列鏡映 lex-leader・別符号化）でも UNSAT
  （conflicts 542,986・54.4s）。
- records.jsonl は lean6q8.sh が実行毎に追記し、出版正本は50行
  （m=60..108 の49行 + lex=H の1行）。
- 出版物: output/band3/（records.jsonl + 49幅×kissat生ログ/meta + lex=H 1組）・
  全101ファイルの着地検証は GitHub 側一覧(fields name/sha/size)の git blob SHA と
  ローカル sha1(\"blob len\\0\"+bytes) 表の完全一致（101/101）で機械確認済み。

## 事故と再実行（決定性の裏付け）

- 1回目の掃引（06:37..07:19Z・m=60..108 中 m=60..106 まで完了）は実行環境の 2度の
  リセット/アーティファクト同期失敗でワークスペースごと喪失した
  （/home/user/work・/home/user/krwork 消滅・レコードは transcripts にのみ残存）。
  3.4GB tarball 再取得もタイムアウトしたため、実験dir正本の raw 直取得＋release バイナリで
  最小環境を再構築し、**m=60..108 を最初から再実行**した（07:34..08:25Z）。
- 共有47幅（m=60..106）の conflicts は1回目・2回目で**完全一致**（例: m=60 490,889・
  m=83 1,048,030・m=106 656,069）。二重実行 bit-exact 性の裏付けになる。
- 1回目の driver は lean6q8.sh が records.jsonl へ追記する仕様を見落として自前追記していた
  ため record が二重化していたが、全二重行は byte-identical であり出版前に機械排除した
  （fail-closed）。2回目の driver2.sh は読み取り専用で全 record 単一化を確認済み。

## 解釈規約（不変）

- 各幅の UNSAT はその幅の非存在の完全証明。掃引外の幅109..370には何も主張しない。
  M_{6,8}=19 の確定には残帯の全幅 UNSAT または上界改善が必要。上界 371 は変更しない。
- conflicts/sec は決定性アンカーであって勝敗ではない。SAT witness は本案では発生せず、
  発生時の decode+dual verify プロトコルは lean6q8.sh に組込み済み。
- 本実験は行の閉鎖簿計ではなく、固定幅盤の極大安全配置の全称的性質（各幅）の有限証明。
  標準 11×11 空盤勝敗には影響しない。

## レジューム（次回・着手前に必ず最新main再取得）

- 単一オーナー宣言 `7bc633a6` は m=60..370 全帯に対するものであるため、
  次回実行は宣言済み状態で **m=109 から再開**すればよい（新宣言は不要・
  driver2.sh 方式〔records grep skip込み〕を scripts/sweep_driver_6q8_band3.sh として出版）。
- 難所の出現は m=79..87（conflicts 0.8..1.05M）で第二山になる見込みだが、230s cap の
  十分余裕（max 79s）。帯全域 262幅 × 平均 ~60s ≈ 4.4h であり、1実行ではm=109..160前後が
  現実的な刻み。INDET 幅が出たら leanrow6q8.sh の rowY∈{0,1,2} 分割（K0829/K0848 被覆論）
  と --lex=H,V,HV 交差符号化に分割してから INDET 記録する。
- 並走レーン（n11 fold/extract・two-token y=8〔宣言済 4e0d920567〕・K1058 有限体）との
  経路不競合を維持すること。

## 観測: K1133 ID重複（出版監査・要対応）

2026-11-20T08:21Z の fold23 レーン出版（n11 residual29 WIN8 receipt fold）
`items/K1133-n11-residual29-win8-receipt-fold-root208090020004.md` に対し、
08:29Z の y=8 two-token レーン出版
`items/K1133-two-token-y8-parametric-allz-universal-proof.md` が**同一ID K1133**
のまま publish された（8分差・後着側が取り直し漏れ）。本log時点で repo に id: K1133 の
K項目が2つ存在し `tools/knowledge/check.py` の一意性検査は失敗するはずである。
本案（K1134・60..108帯）はこの重複と無関係の新しいIDを採番したため影響しないが、
**後着のy=8項目をK1135へ改番する修繕**が必要（K1134は本案が使用・frontmatter・
ファイル名・knowledge README bullet・研究log・実験report内の参照一式の更新が伴う）。
y=8レーンが活動中のため、他レーン（本案）は改修に着手せず、次回実行または
y=8レーン自身の確認を待つ（単一オーナー規約・押し進め禁止）。

## 確定時の後続手続き

- M_{6,8} の全体確定時（109..370 全 UNSAT）には
  新K項目で「M_{6,8}=19 exact（w=6で初の真の安定化長の完全確定）」を出版し、
  K1134 と K0848 を refuted-superseded ではなく proved-chain として更新する。
