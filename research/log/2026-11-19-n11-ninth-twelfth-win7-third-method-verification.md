# 2026-11-19 n11 長期レーン: 第9〜第12 WIN7-D10証明書の第三方法独立検証とsweep43/census・fold/resolve5の静的交差監査

## 経緯

- 前回実行で K1057 出版（commits 9c09329e・ed3b1930）とreplica検証記録
  （071b4498・union gate形式バグ修正 df19f965）まで完了していた。
- 今回は依頼の優先事項(4)「証明書を独立検証可能に保つ」に従い、既存の
  BigInt 3×3余因子展開・4×4 Bareissの二検証器とreplica再現（同じpipelineの
  byte再現）に加えて、第三の実装・第三の代数経路による独立検証と、
  sweep43/census・fold/resolve5の静的交差監査を実施した。検証器は
  python3標準ライブラリのみでrepoコードを読まない。
- K番号について: 有限体レーンの項目がAGENTS.md規約に従いK1057からK1058へ
  再採番済み（commit 0e0ced63）だったため、本項は当初仮番号K1059で準備したが、
  出版直前のpush前チェックで並走のn11レーンが K1059（残余78行の39-witness
  depth-10掃引・WIN 0/REFUTED 39・候補供給枯渇の確定）を先に出版したのを検出し、
  AGENTS.md規約（mainに既に存在するK番号は変更しない・衝突する新規項目を再採番）
  に従い **K1060** に再採番した。実験dir自体はK番号を含まないため実体は不変。
  なお同時刻の実験コミット1（dbd27c11）のコミットメッセージには仮番号K1059が
  含まれており、正しくはK1060（本項）を指す。

## 今回の成果（K1060として出版）

1. **第三方法検証器（verify_third_method.py）**: 3点を通る円のCramer厳密解を
   分母で交差乗算した整数判定式 `W*(s_d-s_1)+DD*(x_d-x_1)+EE*(y_d-y_1)==0`
   （共線組は直線外積式）で第4石のbanned判定を行い、証明書の戦略木を全subroot
   再生する。除算・浮動小数点なし。512サンプル三つ組のlifted-cofactor法との
   等価照合（不一致0）をラン内gateに持つ。replay規約は出版検証器と同一
   （偶数深さは証明書行厳密追随・奇数深さは全合法応手・loser詰み>=13石で終端・
   winner詰みなし）。
2. **証明書4枚の第三方法検証（各39 gate、全合格）**:
   - 第9 `00000000000000801202000001040200`: 72 subroot・84,928行・visited
     171,066・winner 110,087/loser 33,569・edge 153,450・terminal 27,410。
     入力は出版 `.n11.gz.b64` をbase64 -d|gunzipで復元、SHA-256 503ff9da…の
     出版pinと一致。
   - 第10 `00000000000000821082040200000000`: 56・45,450・96,862・15,936。
   - 第11 `00000000000000821092200000000000`: 47・24,375・56,207・8,516。
   - 第12 `00000000001020003800000048000000`: 51・26,756・61,065・9,191。
   出版BigInt流量・Bareiss per-subroot統計（72/56/47/51）・extractionサマリと
   全件一致、strategy/visited union差分0/0、終局石数[13,17]。
3. **sweep43/census静的監査（audit_sweep43_census.py、17 gate、全合格）**:
   43 pair witnessが86行を各行ちょうど1回被覆、43根の7石・D4正準・safe・RAW
   maxbit child・被覆関係（8-D4像−1石の正準形）を全件第三再導出し完全一致、
   probe 86件のnodes・cap・loss・pilot_d6制御が出版記録と全件一致、分類
   （WIN 4・REFUTED 39・CAPPED 0・矛盾0）とnodes総計173,165,148をraw probe
   記録から再導出一致、WIN 4根は第9〜第12証明書rootと完全一致。
4. **fold/resolve5交差監査（audit_fold_resolve5.py、62 gate、全合格）**:
   fold閉鎖の9 S6行（8 target行＋第10のextra行
   `00000000000000801082080400000000` cost 80）の被覆関係を第三再導出で確認、
   closed_edge_cost総計667==163+227+133+144、S6保存則（solved 1,626→1,635）・
   frontier 6,222/492,688→6,213/492,021・5親target 26→34/112（残余78行）と
   出版fold記録全一致。resolve5残余78行==86行−閉鎖8行の再計算一致、
   universe 7,969の再列挙一致（in_pool 93・既知REFUTED 46・fresh 7,830 =
   safe 4,728 + unsafe 3,102）、39 witnessの7石・D4正準・safe・78行完全
   1回被覆・43 sweep根・4 receipt根との不交、verdict pool 379/168・
   matched 78/stranded 0/matching 39の再構築一致。
5. **再現性**: wrapper `run_third_method_verification_20261119.sh` 1本で、
   repo出版ファイルのみから6成果物を約19秒（逐次1プロセス・python3 stdlib）
   で再生する。2回実行で wall_s 以外byte一致（cert_pathは出版ファイル名のみ
   記録しスクラッチ位置に依存しない）。全gate 235（39×4+17+62）が合格。

## 解釈規約（既存レーンと同一）

- 本検証はK1057出版事実の検証強化であり、**勝敗の進展ではない**。
- REFUTED-D10はLOSS証明ではなく、foldは行被覆の簿記、resolve5の39 witnessは
  条件付き計画のままである。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4はすべて
  UNKNOWNのまま。**

## 次の一手（着手前に必ず最新mainを取り直す）

1. **39-witness掃引は並走n11レーンが同時刻に完了・出版済み**（K1059・WIN 0 /
   REFUTED 39 / CAPPED 0・総nodes 115,940,695・残余78行へのadd-one-stone・
   depth-10レーンのfresh候補供給はこのスコープで枯渇確定）。したがって本レーンの
   次回は (a) 第13以降の証明書が出た場合の第三方法検証、(b) depth>10探索コスト
   測定、(c) add-two-stones拡張census、(d) 残余78行の幾何構造解析のいずれかを
   最新mainの状況（stranded状況・他レーンの進出）から選ぶ。
2. 監査の自動化: 本実験の3検証器は出版物のみを入力とするため、以後の証明書
   （第13以降）にも `verify_third_method.py` を同等の第三方法検査として
   併用できる。
3. K番号運用: 本項はpush前チェックでK1059の重複を検出しK1060へ再採番した。
   同様に、新規項目のK番号は発行直前に最新mainで重複を再確認する
   （/generated/index.md は更新遅延するため番号判定に使えない）。
