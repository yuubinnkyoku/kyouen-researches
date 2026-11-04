---
id: K0671
title: 3×3の空盤AND/OR証明書（KYOENC3）を再生成し、全証明DAGノードの局所条件を独立実装で再検証
kind: verification
status: verified
topics: [square-outcomes, certificates, verification]
aliases: []
relations:
- type: verifies
  target: K0013
  note: 3x3は先手必勝（ranked-and-or certificateの空盤勝敗部分）を独立実装で再検証
- type: supports
  target: K0103
  note: 3x3/2x2/1x1の小盤証明書がLeanなしでも独立Pythonで検査できることの確認
artifacts:
- path: research/experiments/n3-certificate-20261104/kyouen-3x3.cert
  role: certificate
  note: 決定的生成（KYOENC3、28ノード、forbidden=14、SHA-256 569c18efa58d…）
- path: research/experiments/n3-certificate-20261104/inspect_cert.py
  role: verifier
  note: ヘッダと全エントリを表示するデコーダ（標準ライブラリのみ）
- path: research/experiments/n3-certificate-20261104/validate_cert.py
  role: verifier
  note: D4軌道展開175ノードすべての局所条件を独立実装で検査 PASS
- path: research/experiments/n3-certificate-20261104/README.md
  role: log
  note: 手法・再現手順・証拠の意味と限界
scope: 3×3に限定。証明書のノード局所条件の検証であり、3×3全局面分類やLean形式化（K0103相当・K0102）は対象外。
evidence: KYOENC3 形式の 3×3 空盤証明書（28エントリ、winning 18 / losing 10、forbidden=14、SHA-256 569c18efa58d71b7d9e08bcac3b66e0ea9593a76b2765f1f872e3e7e6f557dfc は results/certificates.csv と一致）を決定的に再生成し、D4 対称軌道175ノードすべてで、winning は小ランクのlosing子の存在、losing は全合法子が小ランクのwinningであることを、標準ライブラリのみの独立Python実装で確認した（PASS）。lean・C++証明器には依存しない。
---

# 3×3証明書の決定的再生成と独立検証

K0013の証拠は ranked-and-or certificate＋独立C++検査だったが、本作業はその証明書ファイル自体を決定的に再生成し、標準ライブラリのみの独立Python実装で全ノードの局所条件を再検証した。ファイルSHA-256は `results/certificates.csv` の3×3エントリと一致した。

- 決定的生成: `cmake -B build-n3 --target kyouen-certgen-1-to-8 && build-n3/kyouen-certgen-1-to-8 3 kyouen-3x3.cert`
- 再検証: D4 対称軌道の全175ノードの局所条件をPASSと確認した。

## 証拠の意味と限界

これは「証明書が正しいこと」の検証であり、3×3弱解決そのものを新たに証明した
わけではなく、新しい局面の分類も行っていない。証明書が「空盤→先手必勝」を結論
できる範囲の局所的整合性である。Lean 形式化は別作業（K0103/K0102）で、本項目
は Lean なしでの独立検証可能性の確認にとどまる。
