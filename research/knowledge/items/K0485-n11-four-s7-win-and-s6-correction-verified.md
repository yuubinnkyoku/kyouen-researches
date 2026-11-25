---
id: K0485
title: 11盤の既知S7 WIN四件を終局から独立再検証し、S6のUNKNOWN誤記を訂正
kind: verification
status: verified
topics:
- square-outcomes
- certificates
- verification
- provenance
aliases: []
relations:
- type: depends_on
  target: K0371
  note: 勝敗は元先手固定視点。S6はOR節点。
artifacts:
- path: research/experiments/n11-s7-four-win-terminal-20261020/s7_win_four_min_certificate.json
  role: certificate
  note: 4根の終局証明
- path: research/experiments/n11-s7-four-win-terminal-20261020/verify_s7_certificate.py
  role: verifier
  note: 別幾何・全合法子・終局再帰と負例検査
- path: research/experiments/bundle-integration-20261020/n11-four-win-validation.txt
  role: log
  note: 今回のC++再生成・バイト比較・Python独立検証の実行記録
- path: research/log/2026-10-20-n11-s6-win-four-s7-correction.md
  role: log
  note: 旧logの誤分類訂正
scope: 標準11×11、q=4、完全指摘・通常プレイ。指定S6と既知S7四根のみ。
evidence: 2026-10-20にreproduce.shをWSL Ubuntuで実行し終了コード0。2670終局葉・569993状態、負例4種類拒否。
---

S6 `00000000041000001000401000100000` は元先手WIN。49個の合法S7子のうち、旧logがUNKNOWNとした次の4件は既知WINである。

- `00000000041000001000401080100000`
- `00000000041000001000501000100000`
- `00000000041000021000401000100000`
- `00000000041002001000401000100000`

今回、既存cacheを根拠にせずC++で証明書を再生成し、収録証明書とのバイト一致を確認した。Pythonは幾何・全合法子・終局勝敗を別方式で再計算し、159個のS8、129個のS9証人、2670個のS10葉・569993状態で一致。欠落子・不正辺・終局記録改変を含む負例4種類も拒否した。S6はOR節点なのでWIN子1件で十分である。

新規7石分類や新規二石root閉鎖はない。標準11×11空盤はUNKNOWN。旧experiment・logは当時の一次資料として保持し、そこにあるUNKNOWN表記を現在の結論に使わない。
