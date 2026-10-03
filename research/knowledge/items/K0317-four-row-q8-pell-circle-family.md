---
id: K0317
title: 四連続整数行を2点ずつ通る8点円には無限Pell族がある
kind: proposition
status: proved
topics: [geometry, rectangles, variants]
aliases: []
relations:
- type: supports
  target: K0077
  note: 4×m・q=8では非局所円が無限に現れても早い安定化と両立する
artifacts:
- path: research/q48-pell-circle-family.md
  role: proof
  note: Pell方程式による無限構成と最初の非局所例の証明
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/q48_pell_family.json
  role: data
  note: 最初の例と有限検算
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
- path: research/verification/scripts/q48_pell_family.py
  role: verifier
  note: Pell再帰・座標・円方程式・行列式の再現検査
  commit: 49891aaf2d402436b9581296ec91b52769e687d6
---

# 四連続整数行を2点ずつ通る8点円には無限Pell族がある

Pell方程式
`u^2-10v^2=1`
の解から、四連続整数行を各2格子点ずつ通る円を無限に構成できる。半径と必要列数は無限に増える。

この族で最初の非局所的な8点円が盤内に全て現れるのは4×74で、8点中7点を含める最小盤は4×69。これらの「最初」は弦長の有限完全分類で確認されている。

従って4行盤では、十分長くしても局所円以外が消えるわけではない。K0077の早い安定化M_{4,8}=11は、円型そのものの消滅ではなく、少数石から塞げる点数の上界によって成立する。
