---
id: K0528
title: 標準11×11の未分類7石局面を12個の終局LOSS葉で独立証明
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: depends_on
  target: K0002
  note: 元先手固定視点の奇数AND・偶数OR伝播
- type: depends_on
  target: K0371
  note: LOSSからの誤った上位WIN伝播を排除
- type: depends_on
  target: K0516
  note: 既存68個の9石WIN根の終局証明
artifacts:
- path: research/experiments/n11-s7-terminal-loss12-20261024/certificate.json
  role: certificate
  note: 18新規9石WIN・3個の8石LOSS・39葉被覆・12葉最小被覆・双対重み
- path: research/experiments/n11-s7-terminal-loss12-20261024/verify.py
  role: verifier
  note: 全合法境界、固定先手極性、双対下界、C++/Python照合
- path: research/experiments/n11-s7-terminal-loss12-20261024/verify_s10_cpp.cpp
  role: verifier
  note: 独立4×4整数行列式による終局minimax
- path: research/experiments/n11-s7-terminal-loss12-20261024/README.md
  role: source
  note: 再現手順と信頼境界
scope: 標準11×11・q=4・完全指摘・通常プレイ・元先手固定視点。指定7石局面のみ。空盤は含まない。
evidence: 指定7石の全36合法8石子は独立終局証明でWIN33・LOSS3。18個の新規9石WIN根が23個の新規8石WIN子を支え、3個の8石LOSSの全74相異なる9石義務を39個の10石LOSS葉が被覆。1個の8石LOSSは22義務を12葉で被覆し、181候補の終局再計算と半整数双対下界11.5で同形式の最小性を独立検証。C++4×4とPython3点整数円方程式で1,963個の10石葉の勝敗・合法手数・個別状態数が一致（WIN1,887/LOSS76、合計396,636状態）。元先手固定7石ANDはLOSS。6石WINや二石root、空盤勝敗は導出しない。
---

# 7石局面 `00000000100000021081000020000020` はLOSS

全36個の合法8石子の勝敗を、元先手固定視点でWIN33件・LOSS3件と独立終局まで検証した。奇数石AND局面である7石にはLOSS子が存在するため、7石も**LOSS**。

最短の局所証明は、8石LOSS `00000000100000021081004020000020` と、その22個の9石子を覆う12個の10石LOSS葉。全181個の候補を分類し、半整数双対で11葉以下を排除した。最小性はこの局所的な葉形式に限る。

再現は `research/experiments/n11-s7-terminal-loss12-20261024/reproduce.sh`。旧cache勝敗を前提としない。**標準11×11空盤の勝敗はUNKNOWN**。

## 2026-10-24: 7石LOSSの三つの8石応手を横断する12葉最小性

既存の12葉最小性は、指定した一つの8石LOSS子についての下界だった。対象7石の全36合法8石子のうち、LOSSは独立証明済みの3件だけなので、7石LOSSを「8石LOSS子を1件選び、その全9石子に10石LOSS応手を与える」形式で示す際には、この3件のいずれかを選ぶ必要がある。

各8石LOSS子の全9石義務と全10石候補を整数幾何・D4正準化で再列挙すると、義務数/候補数は **22/181、23/198、31/346**。いずれの10石候補も、同じ8石根からの相異なる9石義務を高々2件しか被覆しないことを全候補で検査した。したがって後二者はWIN候補まで使えると仮定しても、それぞれ **12葉以上、16葉以上** が必要。第一根は従来の181候補の終局分類（WIN132/LOSS49）と双対重み合計23/2により **12葉以上**。実際に第一根の12個の終局LOSS葉が全22義務を覆う。

ゆえに、**対象7石のどの8石LOSS子を選んでも、この固定4層・10石LOSS葉被覆形式では12葉未満の証明は不可能**。これは単一8石子だけでなく3候補すべてを比較した最小性である。ただし任意深さ・任意表現の証明全体の最小性は主張しない。独立再検査用: `research/experiments/n11-s7-terminal-loss12-20261024/verify_three_root_minimality.py`。空盤は **UNKNOWN**。

## 2026-10-24: 三つの8石LOSS根から7石LOSS 22件へ逆向き拡張

既に終局証明した3個の8石LOSS根について、各根の8個の7石親を
D4正準化・合法手・整数幾何で独立再検査した。相異なる7石親は**22件**、
7石→8石の証人辺は**24本**。奇数7石ANDでは8石LOSS子が一つあれば
7石LOSSなので、元の対象根を含む22件のLOSSが成立する。
凍結7石LOSS2,232件との重複1件、差分21件。その21件には既存の
本K項目で証明した7石根を含むため、今回の逆向き拡張で**さらに20件**の
7石LOSSを明示的な終局証明由来の証人付きで得た。
既存35個の8石LOSS終局証明根由来の7石親246件との重複0、
凍結7石WIN17件・別途終局証明済み7石WIN5件との矛盾0。

22件の7石LOSSを一手戻すと、6石親70件への154本の合法辺が得られる。
凍結7石LOSS2,232件＋既存35根由来246件との比較では、
70件の6石候補に**147本の被覆辺が増加**する。ただしこの比較集合は
cache由来のラベルを含む。70候補の最小未被覆数は51、全子被覆0。
この逆向き伝播から6石LOSS/WINや二石rootの勝敗は導出しない。

別実装の共線退化を考慮した整数行列式・全合法辺・D4検証器と
改変拒否試験を `research/experiments/n11-s7-terminal-loss12-20261024/verify_s7_reverse_closure.py`
に追加し、`reproduce.sh` に統合した。新検証器は既存の三つの8石LOSSの
終局証明を前提とする構造検証であり、単独では終局再計算を行わない。
新規件数は指定した比較集合に限る。**標準11×11空盤はUNKNOWN**。
