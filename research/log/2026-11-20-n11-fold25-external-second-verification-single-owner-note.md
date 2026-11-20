# 単一オーナー宣言ノート: fold25 receipt fold（K1142）の外部第二検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold25（K1142・残余26行 WIN8-D10 receipt fold root `00000000000200003800200008180000`）
出版成果一式に対する**外部第二検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T17:35:00Z
- 宣言時点の main HEAD: `c0ab6a37`（remo survivor宣言追跡済み・fold25外部第二検証の先行宣言なし）
- 対象出版物: `research/experiments/n11-residual26-win8-receipt-fold-root200003800200-20261120/`
  （part1 `493becee3a`・part2 `2bdaa5ed07`・part3 `48ff216e95`）
- 対象正本:
  - fold25 receipt正本 `output/win8-root200003800200-receipt-fold-20261120.json`
    SHA-256 `5780f3875ed13554c6f58f269cdb587b792e0c9f930aba11c551a89e17a1074d`
  - fold25 出版機 `scripts/fold_win8_root200003800200.py`
    SHA-256 `e871b6f9faa899878ef9b67bd3ba2883eed0a3bd6f9a1c3a42d8f89fe849ac8e`
  - 出版同梱の独立監査正本 `output/independent-audit.json`
    SHA-256 `7747afdc2f26bb6b6a8bd794f098dd6c41c73a7c3eadfcfdf8fb475d3930715c`
  - 直前のfold24 receipt正本 SHA-256 `c4ab76d3cb7eba5c1ab8e1830c43d17bf9a771f511b66e7e8573864f3f2402c7`

## 位置づけ

fold25の出版は出版社レーン自身の三重実行・end-to-end再現・同梱独立監査
（49/49 checks）までを含んでいるが、出版社以外の実行主体による第二検証はまだない。
fold25後のfrontier（target 88/112・残余24行）は、宣言済みのfold26 receipt fold
（先行レーン `23bffdd4e4`）の直接の前提であり、round-5 refsolve
（`ace38772d9`）・新WIN8-D10候補 `00000000010000809002000040002001` の証明書抽出
（`63877ffd2e`）と並ぶ前進連鎖の共通基盤である。本検証はこの基盤の独立確認を
目的とし、三つの宣言済み工程のすべてに着手しない。

## 作業範囲（受入条件）

1. 出版byteをGitHub（pinned commit）から再取得し、実験dir正本のSHA-256 pinを照合する。
2. 出版済み `reconstruct_inputs.py`（既定の固定Git参照 `60e5109efad…`）で
   63入力pinをfail-closedで再構成する。
3. 出版機をpristine再実行する（3回: 同一cwd 2回＋隔離tree/cwd/HOME＋
   PYTHONHASHSEED=random 1回）。出力receipt JSONは3実行とも byte-identical かつ
   出版正本 SHA-256 `5780f387…` と一致すること。
4. 本レーンが新規に書く**別実装**の検証機（stdlibのみ）で、worklist・census・
   全fold receipt記録（fold1..fold24）・K1137証明書・K1137監査・K1097 refsolve記録から:
   - 五親target 112行の再導入とfold1..24の閉鎖行を用いた残余26行・open frontier 6,123/485,213 の再構成、
   - K1137 rootのC(8,6)部分幾何28 subsetのD4正準行の再導出とcover conventionに基づく
     閉鎖候補行（主張2行＋余剰1行）の再決定、
   - 親行incidence・cost・needed・S5 orbit数を含む全frontier_after統計の再計算、
   を独立に導出し、出版receipt正本の全該当fieldと値単位で一致することを確認する。
5. tamper検査: 1 byte XOR改変（pin入力2件、出版社検査済みoffsetとは別位置）が
   fail-closed（returncode 1・正本未書込）で捕捉されること。
6. 本レーン検証機の監査正本JSONは、同一cwd 2回＋隔離cwd/HOME＋PYTHONHASHSEED=random
   の3実行でbyte-identicalであること。

## やらないこと・非主張

- fold26 receipt fold・round-5 refsolve・新WIN8-D10候補の証明書抽出は他レーン宣言済みで
  着手しない。新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- 本検証はreceipt簿記の再検査であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
