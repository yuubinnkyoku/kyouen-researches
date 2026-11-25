---
id: K0426
title: 11盤のS6 LOSSと3件のS8 LOSSの終局証明を独立検証し、固定計画の要求S5和集合を31,774から31,771へ縮小
kind: verification
status: verified
topics: [square-outcomes, certificates, verification, search-methods, provenance]
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 元先手固定視点の通常プレイにおける偶奇層の勝敗伝播
- type: depends_on
  target: K0424
  note: 監査基準とした凍結update6共同計画（選択S4・要求S5和集合31,774）
- type: supports
  target: K0417
  note: 検証済みS6 LOSSの3個のS5親が選択S4クラス16397に一致し、要求S5和集合を31,771へ縮小
artifacts:
- path: research/experiments/n11-targeted-terminal-lift-20261015/README.md
  role: source
  note: 407件のS10追加検査、終局証明、上位への伝播と信頼境界
- path: research/experiments/n11-targeted-terminal-lift-20261015/SHA256SUMS
  role: manifest
  note: パッケージ内50ファイルのSHA-256一覧（reproduce.shが照合）
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_loss_three_terminal.cert
  role: certificate
  note: 3個のS8 LOSS、104個のS9義務と63個の終局S10 LOSS葉
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_171_terminal.cert
  role: certificate
  note: 171個のS8 WIN終局証明
- path: research/experiments/n11-targeted-terminal-lift-20261015/certificates/new_s8_win_sixteen_terminal.cert
  role: certificate
  note: 追加16個のS8 WIN終局証明
- path: research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_loss_batch_cpp.cpp
  role: verifier
  note: キャッシュなしで終局まで再計算する独立C++検査器
- path: research/experiments/n11-targeted-terminal-lift-20261015/scripts/verify_s8_loss_batch_python.py
  role: verifier
  note: キャッシュなしで終局まで再計算する独立Python検査器
- path: research/experiments/n11-targeted-terminal-lift-20261015/REPRODUCTION_RECEIPT.txt
  role: log
  note: パッケージ再現の実行記録。2026-10-15に本repoで全手順を再実行しPASS
- path: research/experiments/n11-s6-terminal-loss-20261015/s6-loss-optimized.cert
  role: certificate
  note: 一つのS6 LOSSを29個のS8 LOSS証人と483個の終局S10葉で証明する証明書
- path: research/experiments/n11-s6-terminal-loss-20261015/verify_s6_terminal.py
  role: verifier
  note: S6証明境界と全S10葉をキャッシュなしで検査（1,028,621状態）
- path: research/experiments/n11-s6-terminal-loss-20261015/verify_s8_loss_cpp.cpp
  role: verifier
  note: 同一証明書を独立C++で終局再計算する検査器
- path: research/experiments/n11-s6-terminal-loss-20261015/audit_joint_plan.py
  role: verifier
  note: 六つのS5 LOSS親と凍結update6計画の重なり・要求S5和集合31,771の再計算
scope: 標準11×11・q=4・完全指摘・通常プレイ。勝敗ラベルは元先手固定視点。添付終局証明と派生するS5親のみに限定し、空盤面や二石rootは対象外。
evidence: 添付2パッケージを2026-10-15に本repoのWSL2環境で再実行し全PASS。S6証明書は非圧縮SHA-256 cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6照合のうえ、キャッシュ非依存のPython/C++検査器が29根・1,046 S8→S9義務・483終局S10葉・1,028,621状態で一致。S8 WIN 171+16とS8 LOSS 3の各証明書も両実装で一致し（152,566・5,929・85,676状態）、407件の未知S10もC++/Python一致（WIN 364・LOSS 43・378,648状態、衝突0）。原子mergeは51,164+407=51,571で重複0、差分監査は+187 S8 WIN・+19 S7 LOSS（新規19・重複4・衝突0）・偽近LOSS 120件の除外・高被覆475件の全分類（未知0）、改変拒否の負例対照も通過した。凍結update6計画に対する監査は、6個のS5 LOSS親のうち3個が選択S4クラス16397の8第三手群（初手24に3群・26に2群・48に3群）に現れ、S4選択を固定したまま楽観的要求S5和集合が31,774から31,771へ縮むことを再計算で確認した。
---

両パッケージの検査器を本repoで実行し、キャッシュ非依存の終局再計算の一致を確認した検証項目。独立実行で確認したのは以下の範囲であり、添付READMEの全主張を再導出したものではない。

S6 LOSS `00000000040004001004000004010000` は49個のS7子・29個のS8 LOSS証人・1,046個のS8→S9義務・483個の終局S10 LOSS葉で証明され、六石から各石を除いた6個のS5 LOSS親を与える。この6親は凍結計画の基準cacheと既知終局S5（層別13）のいずれにも現れない新規源である。

うち3個は選択S4クラス16397の8第三手群の要求S5和集合に含まれていたため、S4選択を固定したまま楽観的要求和集合が31,774から31,771へ縮む（K0417へ反映済み）。残る3親はこの固定計画のどの選択S4配下にも現れない。

3つのS8 LOSSからは合法な7石親23件が再生成され、既知2,213件との重複4件を除く19件の新規7石LOSSが導かれる（既知7石WINとの衝突0）。C++のみで計算されたS10 LOSS候補2,229件は今回も統合cacheに含めない。S10統合cache51,571件のうち既存51,164件は以前の監査来歴を保持し、本検証で各項目の終局再計算は行っていない。

両パッケージとも新しい二石rootを閉じていない。標準11×11空盤面の勝者は引き続きUNKNOWN。S10既存51,164件の全独立再検査や、C++のみの2,229候補の昇格も主張しない。


## 2026-10-25：既存29個の八石LOSS根を終局証明限定の被覆集合へ統合

上記の六石LOSS証明書に含まれる29個の八石LOSS根は、2026-10-24時点の
終局証明限定八石LOSS44根とは**重複0**だった。483個の十石LOSS葉を
証明済みとして再利用し、八石→九石の延べ1,046辺・相異なる1,035義務の
全被覆をJavaScriptの独立整数幾何で再生成した。483葉の終局勝敗は
今回再計算しておらず、2026-10-15のC++/Python独立証明を継承する。

統合後の終局証明限定八石LOSSは**73根**、逆向きに導く七石LOSSは
**311→534類（+223）**、六石被覆対象は**944→1,653類（+709）**、
証明済み六石→七石類辺は**2,177→3,738本（+1,561）**。
全1,653六石親の合法子は128,009類辺。全子被覆済み六石は
**既知の本項目の六石LOSS1件のみ**で、新規六石勝敗確定は0。
追加223個の七石LOSSは凍結七石LOSS2,232件にすべて含まれる。
独立証明済み八石WIN1,326件・凍結八石WIN13,501件・七石WIN17件と
極性衝突0。旧凍結一覧は比較・矛盾検出にのみ使用した。

再現可能な監査器・固定鍵一覧・検証境界：
`research/experiments/n11-s6-legacy29-union-20261025/README.md`。
今回の監査器の局所実行と構造数値は確認したが、
全体CI・knowledge生成検査は未確認。
新しい二石rootの閉鎖はなく、**標準11×11空盤はUNKNOWN**。


## 2026-10-25：既存3件の八石LOSS終局証明を統合集合へ接続

2026-10-15に本項目で独立C++/Python終局検証した
`new_s8_loss_three_terminal.cert` の3個の八石LOSS根は、
2026-10-25の終局証明限定八石LOSS73根に含まれていなかった。
既存73根との重複0、追加後は**76根**。
証明書の104個の相異なる九石義務（八石→九石105辺）は、
63個の終局LOSS葉ですべて被覆されることを整数幾何・D4で再監査した。
63葉の勝敗は既存の独立終局検証を継承し、今回再計算していない。

逆向きに導いた七石LOSSは**534→554類（+20）**、
六石被覆対象は**1,653→1,710類（+57）**、
証明済み六石→七石類別辺は**3,738→3,878本（+140）**。
全六石親の合法子類別辺は132,573本。
全子被覆済み六石は以前から証明済みの1類のみで、新規閉鎖0。
未閉鎖六石候補の最小不足は37対称類。
追加した七石20類はすべて凍結七石LOSS2,232類に含まれ、
独立証明済み八石WIN1,513類・凍結八石WIN13,501類・
既知七石WIN17類との極性衝突0。
凍結表は比較・衝突検出のみで証明根拠には用いていない。

再現監査：
`research/experiments/n11-s6-legacy3-loss-union-20261025/README.md`。
別実装による構造数値は照合済み。新しいNode一括監査器、
全体CI・knowledge生成検査の完了は未確認。
新規二石root閉鎖0、**標準11×11空盤UNKNOWN**。
