# 第17 WIN7-D10証明書の知識項目化（2026-11-20）

## 作業開始時点

- 作業開始時のmain head: `ca8d7010f978e0ade579b473b78a128b00fbb5d4`。
- `AGENTS.md`、`research/knowledge/README.md`、`SCHEMA.md`、`VOCABULARY.yaml`を確認。
- `research/log/2026-11-20-n11-fold10-single-owner-note.md`を確認。第17 receiptのfold10は既存の単一オーナーが担当中であり、重複実行しない。
- 並走可能な作業として、既に出版済みの第17証明書実験を独立したknowledge itemへ索引化する。

## 確認した既存正本

実験 `n11-residual78-seventeenth-win7-cert-extract-20261120` のREADME、証明書、builder、機械可読な38 gate検証記録をmainから取得した。検証記録の要点は次の通り。

- root: `00004000000000821082000000000100`（7石・D4正準形）、child `4000000000821082000000000000` + bit 8。
- 証明書: 49,591戦略行、1,791,541 bytes、SHA-256 `21dd2f0e9f0b8ec22e917fce5a732835098baf37570a227bebacacb4c13807c8`。
- blind抽出: 4,250,297 nodes、second moverの合法初手60通り、fbt_drops=0。2回の出力はbyte-identical。
- TS Bareiss 4×4: 60/60 subroot、seen 103,152、terminal 17,157、opponent edges 90,499、union差分0/0。
- Python exact Bareiss: 60/60、visited winner states 150,963、terminal石数{13,15,17}、union差分0/0。
- BigInt 3×3 cofactor: 60/60、winner states 66,212、loser states 19,783、loser reply edges 90,499、terminal 17,157、union差分0/0。
- fail-closed builderの全38 gateがPASS。発見元の39-root掃引は78/78 probeで別実行とnode-exact一致。

上記は既存の出版済み検証記録からの転記・照合であり、この作業で証明書本体を再抽出したり三検証器を再実行したものではない。

## 反映

- 新規knowledge item: [K1070](../knowledge/items/K1070-n11-residual78-seventeenth-win7-certificate.md)。
- `research/knowledge/README.md`へK1070の要約を追加。
- 証明書と38 gate正本は既存experimentのまま保持。生成領域は直接編集しない。
- branch / PRなし。mainへ直接反映。

## 閉鎖計上と未解決範囲

第17証明書が幾何学的に覆う候補行は
`00000000000000821082000000000001` と
`00000000000000821082000000000004`。
ただし証明書だけでは残余行を閉じない。fold10側で8 D4像から1石を除くjoinを再導出し、receiptとして計上するまで、fold9後の残余74行のままとする。本作業は単一オーナーのfold10を実行していない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。REFUTED-D10、pn/dn、solved数を勝敗と解釈しない。
