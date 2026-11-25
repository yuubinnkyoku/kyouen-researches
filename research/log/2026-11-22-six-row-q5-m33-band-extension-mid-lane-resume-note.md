# 2026-11-22 six-row (6,5) 6x33 band extension — mid-lane resume note (infrastructure deferral)

- 宣言: `29c44cc53a`（03:07:58Z・single-owner declaration note
  `research/log/2026-11-22-six-row-q5-m33-band-extension-single-owner-note.md`）。
- 本note: 実行環境障害（filesystem unavailable・持続）により、完了していた計算を
  保護し次回実行へ引き継ぐための正直な中間記録。規約どおり無理に押さず記録のみ。

## 完了済み（kit \`_q65-band-m31plus-kit\` 内・環境復旧後に再照合を推奨）

- 較正ゲート（宣言note受入条件・全PASS）: engine core verbatim が w32 anchors 再現
  （c009@off3 unblocked=[[31,5]]、rem1..4add0 候補 23/253/1771/8855・0 witness、
  D-set filter dsizes=[74]・pairs=9731=K1216出版t2アンカー）。cal base の s2 も陰性。
- \`config_w33_u3.json\`（tag w33-u3-scan）: 13 base（u=2: c009@off3/4/5・
  u=3: c008@off0..3, c009@off2/6, c011@off4..7）。全13 base で engine 再計算
  unblocked が census targets と 13/13 一致（Fraction/整数2系統交差確認）。
- **r-battery 13/13 完走・全陰性**: r0s/r1a1/r2a1/r3a1/r4a1
  （候補数 23 / 4,025 / 44,275 / 309,925 / 1,549,625 per base・witnesses 0）。
- **s2（2R2A targeted-complete・新規級）13/13 完走・全陰性**
  （pairs: base1..12 = 6,815 / 8,064 / 6,915 / 5,907 / 5,998 / 6,359 / 7,710 / 7,444 /
  5,808 / 5,552 / 6,324 / 6,987・base0 は stats 参照・witnesses 0 全base）。
- **t2（3R2A targeted-complete）12/13 完走・全陰性**
  （pairs: 8,624 / 6,815 / 8,064 / 6,915 / 5,907 / 5,998 / 6,359 / 7,710 / 7,444 /
  5,808 / 5,552 / 6,324・witnesses 0・budget-stop跨ぎのresume再開を base0 で確認済）。
- residual: **base-012（c011@off7・dsizes [70,92,79]・pairs 6,987）が
  \`base-012.t2.part.json\` checkpoint 途中で 6x33 witness 未着地**（12/13 done 時点で skills/実行環境が
  unavailable になり以降の再開呼び出しは全て失敗）。

## 次回実行のresume手順

1. kit \`w33-work/\` から \`node surgery_deep_v2.js config_w33_u3.json 12 13 t2\`
   を budget-call反復（\`output/w33-u3-scan/base-012.t2.part.json\` から resume・
   残り≈250s相当）し \`base-012.t2.json\` (done:true) を得る。
2. 決定性再実行: 完了base 1つの t2/s2 を別tagで冷再走し pairs/witnesses 一致を確認
   （宣言note受入条件）。
3. 出版: base-012 陰性なら「6x33 UNDETERMINED 不変・13 base の bounded-edit 近傍
   （k≤4R≤1A complete + 2R2A/3R2A targeted-complete）に 6x33 witness なし」の限定陰性として
   実験dir \`research/experiments/six-row-q5-m33-band-extension-20261122/\`
   （README+scripts+surgery_deep_v2.js+config+outputs+manifest sha256）+ session log を刊行。
   陰性のみなら K item・CSV・knowledge README bullet は作らない（先例どおり）。
   witness が base-012 で見つかった場合のみ 3系統検証ゲート→下界 M_{6,5}∈[34,658] 出版。
4. 並走へ: 6x32 t2 scan（宣言 \`b1afb181aa\`・04:11Z進捗 \`bd59ce1122\` 11 base 完了 negatives）とは非接触継続。

## 事故記録

- ~03:3xZ 以降、sandbox・bash 両系で filesystem 操作が
  "execution environment is temporarily unavailable"（表記は2種: "Filesystem rollback
  failed…" 含む）で持続失敗。失敗前に完了した計算出力は kit（knowledge配下・リセット耐性）
  に checkpoint 済み。GitHub API 系toolは稼働しており本noteはその経路で出版。
- 競合なし: 宣言後の最新 main（05:02Z 時点 \`4fcee8ebf1\`・56 commits）に w33/6x33
  を触る平行作業は存在せず。

- HEAD at push time: 4fcee8ebf1e89409d2915a39d3bba7082dcc4832
