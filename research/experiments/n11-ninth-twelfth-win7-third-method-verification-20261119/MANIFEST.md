# n11-ninth-twelfth-win7-third-method-verification-20261119

標準11×11空盤レーン（head-1410系）の K1057 出版成果に対する第三方法（third-method）
独立検証の実験一式。repoの出版ファイルのみを入力とし、python3標準ライブラルのみの
第三実装で (1) 第9〜第12 WIN7-D10証明書4枚の戦略木再生、(2) sweep43/censusの静的
構造監査、(3) 4-receipt foldとresolve5の交差監査を行う。探索の新規実行は含まない。

## 主結果（2026-11-19時点）

- 証明書4枚（各39 gate・全合格）: 第9 72/72 subroot・84,928行・visited 171,066・
  terminal 27,410、第10 56/56・45,450・96,862・15,936、第11 47/47・24,375・
  56,207・8,516、第12 51/51・26,756・61,065・9,191。出版BigInt流量・Bareiss
  per-subroot・extractionサマリと全件一致、union差分0/0、終局石数[13,17]。
- sweep43/census静的監査（17 gate・全合格）: 43 pair witnessの86行完全1回被覆・
  43根の構造（7石・D4正準・safe・RAW maxbit child・8-D4像−1石被覆）の第三再導出・
  分類（WIN 4/REFUTED 39/CAPPED 0/矛盾0）とnodes総計173,165,148のraw記録再導出。
- fold/resolve5交差監査（62 gate・全合格）: 9 S6行閉鎖（8 target＋extra
  `00000000000000801082080400000000` cost 80）・closed_edge_cost 667・S6保存則・
  frontier 6,222/492,688→6,213/492,021・5親target 26→34/112・残余78行の
  universe 7,969再列挙・39 witnessの78行完全1回被覆と不交性・verdict pool 379/168。
- 再現性: `scripts/run_third_method_verification_20261119.sh <repoRoot>` 1本で
  6成果物が約19秒（逐次1プロセス）で再生。2回実行で wall_s 以外byte一致。
  全gate 235（39×4+17+62）が合格。

## レイアウト

    README.md                                   # 目的・方法・結果・再生手順
    scripts/verify_third_method.py              # 証明書1枚の第三方法検証器
    scripts/audit_sweep43_census.py             # sweep43/census静的監査
    scripts/audit_fold_resolve5.py              # fold/resolve5交差監査
    scripts/run_third_method_verification_20261119.sh
                                                # repo出版入力のみから全成果物を再生するwrapper
    output/win7-root-<rootHex>-third-method-verification-20261119.json  # ×4
    output/sweep43-census-third-method-static-audit-20261119.json
    output/fold-resolve5-third-method-cross-check-20261119.json

## 出力SHA-256（出版bytesのpin。wall_s以外は決定的）

- output/fold-resolve5-third-method-cross-check-20261119.json
  b741bf657020fb0466d8a3fec73fb6dd0e9781266a28a51b28fb1ca38690a099
- output/sweep43-census-third-method-static-audit-20261119.json
  ea665605caca8b5afa43dedbd810b69bb89d296f0cb558d573908302201195a9
- output/win7-root-00000000000000801202000001040200-third-method-verification-20261119.json
  cc6980bf8a11b0e8707fbec2b03c69c3c1788c454e09df9f94ea13abd09a2091
- output/win7-root-00000000000000821082040200000000-third-method-verification-20261119.json
  3a92ea9e1acf02d4ae90a3fb8426161aa13e893ca7cb844c255b096484fb198e
- output/win7-root-00000000000000821092200000000000-third-method-verification-20261119.json
  9b119ee08e8c91980d610736264f36d7bf95806f20f3974059a46a42bb2d6beb
- output/win7-root-00000000000001020003800000048000000-third-method-verification-20261119.json
  6e8ae2d3f27db3778133faf3578daf3c53c619a4ffccc5c8d756df774ab14aae

## 入力（repo出版正本・実行時に読んだcopyのSHA-256）

- 証明書正本（SHA-256はK1057 MANIFEST pinと一致。第9は .n11.gz.b64 復元後）:
  第9 503ff9dadc7a0d52cba8d75fa185273c798811e2ca1a897eee98cbd2b6cce631（.gz.b64 は
  226f2b0317f38c54b9c0aff1da65ef9ecd7b147b8b1549ceb6ef7b35851095b8）・
  第10 6ba50576f3f9500d0b11ffa4a47231255e9968af40e6dcb0330c09a58fc6d426・
  第11 c68e63752392d17002e4d2447b23f0f98da55348400b952c0f8dbff269a6b566・
  第12 6513b7d57ace489764b7c863025487b2d14313e134153a1460a039578287e37a
- extraction-summary: 第9 95802606fd2dd2c8fbf8e717ca887f142d462fe9966787bd512916521c8331d9・
  第10 e2e012abb5fb0c53f43b3b832197d3285ffa84cc211c51ddc5e7718f865f09ad・
  第11 1a40620f26b431c2b65835b551a690c8daa7cdd5e5686ca4d8f50a56c994e2cd・
  第12 a64a2aeb446464a6911f85b1665cac97a93c4f7ec7047c1b438a0621939d5223
- independent-verification（BigInt）: 第9 6147ce0e152180be0930410c30ef976042df8a4d4ffd8012f11bf80d30b9d36b・
  第10 fbddf88b42cebeb0fd1db27d9a6ca722d4eeea50773f2c7817856b606025d914・
  第11 2a32945a97b799d0740b1f371c6e36b46497b68477211dd0df0e0ce45591c15d・
  第12 94e90cd7f7a514cbb82f43bc952eb436975a1f01b314c05c4a663d2ef81b4e17
- bareiss-subroots: 第9 774e48fa6eefe3f1543ab3f4366be4400e8cb5abb8049e7f595129552a2fe82c・
  第10 bbfd75c0c289dda33794f7715b6efdd23e0c9266d2ae02101e03fd5439340fa3・
  第11 87ce62072db649973b4400a61c1c0fb9c96c504d1ba9af6e7149bea1c1a717ec・
  第12 2c5b05d242925162dd2b94d3e35811e9220212977ab3abb4fd218e6347c45438
- sweep43配下: witness-43-root-depth10-sweep-20261119.json 7940638f67af49aaf5acb0359fbf56418d52bc4cd60e028b94255cbdf5b1613b・
  probe-records-w0.jsonl 822be9d8fd3f2467f8603c7301227b956fe7299341ff206aa3a8b7e0cf120706・
  probe-records-w1.jsonl c2c8d775982a3ca153fe58b815a8d183428271389cfde6242b8204712480e647・
  roots.json cdd9110722ba714a80013557518392a5fc4294c45eae7b496bd2e69e89ebe325
- fold/resolve4/resolve5: ninth-twelfth-win7-receipt-fold-20261119.json ee002d792345cf3e2f90fda43a0d6a3d4bf6ed29d3280653491b3dd83f42e67a・
  post-eighth-receipt-cover-resolve4-20261119.json 2ad70afba4236375925dfd13230bb599b2d38f93631d6ded266fd77d34432e09（=K1057のresolve4 pinと一致）・
  post-twelfth-receipt-cover-resolve5-20261119.json 5a2f4815c1d5fbbf40a76f839425a6e3750673bb37a60b64aca8ff03e5aeef9e

## 解釈規約

- 本検証はK1057出版事実の検証強化であり、勝敗の進展ではない。
- REFUTED-D10はLOSS証明ではなく、foldは行被覆の簿記、resolve5の39 witnessは
  条件付き計画である。
- 標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべてUNKNOWN。
