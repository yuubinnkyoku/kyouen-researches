# 単一オーナー宣言ノート: fold24 receipt fold（K1140）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold24（K1140・残余29行 WIN8-D10 receipt fold root `00000000000000043800000008180010`）
出版成果一式に対する**外部第二検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T18:12:30Z
- 宣言時点の main HEAD: `9d708fa430d38fb535894a2494b88bf2d1ea44d0`
  （fold24外部第二検証の先行宣言なし・fold25外部第二検証は別工程として宣言済み `aad3b71ca3`）
- 対象出版物: `research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/`
  （単一コミット出版 `fc4c18fdddb4072667ad019d3218a066e313ff4e`:
  実験dir 8ファイル＋K1140 item＋研究log＋knowledge README bullet 一式）
- 対象正本:
  - fold24 receipt正本 `output/win8-root438000000818-receipt-fold-20261120.json`
    SHA-256 `c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7`
  - fold24 出版機 `scripts/fold_win8_root438000000818.py`
    SHA-256 `f462733dbaa6a958680ce49ff85e056adf8756cc946fa5ac612442f2c47b4fc8`
  - 出版同梱の独立監査正本 `output/independent-audit.json`
    SHA-256 `49f330c6e0f73c0a58fdd9b21c215c38fc3a594d35f1d617b1324468c4a3387b`
  - 出版再現log `output/reproduction.log`
    SHA-256 `cb01749a9b52e7ed4392dc2d25cf008e805b0ca17b40a25537680e9d1df0e5b2`
  - 直前のfold23 receipt正本 SHA-256 `04f334ff0f6aa995375283e94afc0e83ced6bebfeefea47359a5090a338fad59`

## 位置づけ

fold24の出版は出版社レーン自身の5回実行・生成器からの機械再生成byte一致・
同梱独立監査（46/46 checks）までを含んでいるが、出版社以外の実行主体による
第二検証はまだない。fold24後のfrontier（target 86/112・残余26行）は、
fold25（K1142・外部第二検証は宣言済み `aad3b71ca3` が対象を所有）から
fold26 receipt fold（先行レーン `23bffdd4e4`）に至るreceipt連鎖の共通前提である。
本検証は fold24 receipt の値単位の独立確認を目的とし、fold25・fold26・
round-5 refsolve（`ace38772d9`）・新WIN8-D10候補 `00000000010000809002000040002001`
の証明書抽出（`63877ffd2e`）のいずれにも着手しない（fold25外部第二検証レーンの
検証対象はfold25 receipt deltaであり、fold24 receiptはその入力に留まる）。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、上記4正本のSHA-256 pinを照合する。
2. 出版済み `research/experiments/n11-residual29-win8-receipt-fold-root438000000818-20261120/scripts/reconstruct_inputs.py`
   （SHA-256 `f4e1fa8e69b10c07d9eec7f0b798458b0e73a97308bd418b622d1e9542873591`・
   既定の固定Git参照 `b91e85a99f0480f084835bdff51533d0cf5feaa8`）で
   61入力pin（12 Git blob pin + 49 SHA-256 pin）をfail-closedで再構成する。
3. 出版機をpristine再実行する（計4回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   PYTHONHASHSEED=random 1回を含む）。出力receipt JSONは全実行でbyte-identical かつ
   出版正本 SHA-256 `c4ab76d3…` と一致すること（fold23機の隔離pristine rerun gate込み）。
4. 出版同梱の独立監査（`verify_fold24_independent.py`）を再実行し、その出力監査JSONが
   出版監査正本 SHA-256 `49f330c6…` とbyte-identicalであることを確認する。
5. 本レーンが新規に書く**別実装**の外部検証機（stdlibのみ・fold機械の幾何補助関数を流用しない）で、
   worklist・census・fold1..23 receipt記録・K1136証明書・K1136監査・K1091掃引記録から:
   - 五親target 112行の再導入とfold1..23の閉鎖行を用いた残余29行・
     open frontier 6,126/485,438 の再構成、
   - K1136 rootのC(8,6)部分幾何28 subsetのD4正準行の再導出（2方法:
     C(8,2) 2石除去×8 D4像の完全合成と、部分集合のD4正準化の各々）と
     cover conventionに基づく閉鎖候補行（主張3行・余剰0行）の再決定、
   - 親行incidence・cost・needed・S5 orbit数を含む全frontier_after統計の再計算、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
6. tamper検査: 1 byte XOR改変（pin入力2件、出版社検査済みoffsetとは別位置）が
   fail-closed（returncode 1・正本未書込）で捕捉されること。
7. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋PYTHONHASHSEED=random
   の3実行でbyte-identicalであること。

## やらないこと・非主張

- fold25 receipt foldの外部第二検証（`aad3b71ca3`所有）・fold26 receipt fold・
  round-5 refsolve・新WIN8-D10候補の証明書抽出は他レーン宣言済みで着手しない。
  新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証はreceipt簿記の再検査であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
