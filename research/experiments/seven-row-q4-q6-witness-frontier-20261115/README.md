# seven-row-q4-q6-witness-frontier-20261115

高速レーン（(7,9)帯閉包 2026-11-15 と同一実行の後続バッチ）。K0827 の3ファミリー
（q=4,5,6 ≤ w=7・genfast 系不適用）の witness 前線を SAT 側で再確認・前進させた。

## 主張

1. **(7,4) m=22..27: SAT witness 6 幅（すべて 0 conflicts・2系統検証 PASS）**。
   - m=22: 18石 rows [3,3,3,3,3,2,1]（K0827 構成的延伸の free empty-column
     extension と同一構造）、
   - m=23..27: 20石 rows [3,3,3,3,3,3,2]（構成的延伸 config CA と同一行構造）。
   - これは seven-row-q4-extension-band-20261114 の構成的 witness のうち
     m=22..27（tsVerify のみで jsVerify/pyVerify 再検証 pending とされていた幅）の
     **SAT + sat.js verifyConfig + Python Fraction による再検証**である。
     より正確に: 構成的 witness とは独立に sat2.js 完全符号化 + kissat で
     witness を発見し、行構造が構成的 config と一致することを確認した。
   - M_{7,4} ≥ 28。K0827 の構成的延伸 m=28..35 を合わせると M_{7,4} ≥ 36
     （前線 7×36・本実験の上界影響なし）。
2. **(7,5) 7×32: def-mode kissat 200s INDET（329,844 conflicts）** —
   前線幅の初記録。不在主張ではない。
3. **(7,6) 7×27: def-mode kissat 200s INDET（744,027 conflicts）** —
   前線幅の初記録。不在主張ではない。
4. **sat2.js census 壁の定量的記録**: 7×28 (q=4) の全三つ組census生成が
   node heap 2560MB で OOM（rc 137・コンテナメモリ上限）。
   SAT による (7,4) 帯の直接延長は m=28 で停止。q ≤ w 向けのメモリ有界
   census（genfast の q < w 版）が今後の実装課題。

## 手法

- 符号化: seven-row-inband-families-20261114/scripts/sat2.js verbatim
  （q ≤ w のため全三つ組census・def 単一節は行欠損存在の完全符号化）。
- ソルバ: kissat 4.0.4 official linux-amd64（200s cap・変更なし）。
- 検証: decode_verify.js（census 不使用 sat.js verifyConfig）+
  verify_witness.py（Python Fraction・独立実装）の 2 系統で
  safe+maximal+行欠損 すべて PASS（records.jsonl の jsVerify/pyVerify すべて true）。
- 較正: (7,5) m=23 の再実行が 1,200 conflicts で K0827 公開 record と bit-exact
  （同一インスタンス性の確認）。

## スコープ

有限機械検証。m=22..27 の SAT witness はこれらの幅の行欠損極大存在の完全証明。
7×32 (q5)・7×27 (q6) の INDET は不在主張ではない（正直な負記録）。
(7,4) m=28 以降の SAT 探索は census メモリ壁のため未実施（不在主張ではない）。
