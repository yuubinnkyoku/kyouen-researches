# K1285 実行 log — ペア対角スライス理論と pure-c1 ラダーの全称確定（T-PS0/1/2・T-L1/L2/L3・T-ALM・C-PB2/C-PC）

- 日付: 2026-11-24（Vibe 高速レーン・定時自律実行）
- 対応宣言ノート: `research/log/2026-11-24-pair-slices-pure-c1-ladders-single-owner-note.md`
  （出版 2114a771・観測 HEAD 81ae89f1・K1285 空き・対抗宣言なし）
- 対応機体: `research/experiments/pair-slices-20261124/`
  （出版 2c70a1b6・公式成果物 c4b66682）
- K item: `research/knowledge/items/K1285-pair-slices-pure-c1-ladders.md`

## 内容（成果サマリ）

1. **T-PS0/1/2（主定理）**: ペア (m, m+g)・対角座標 k := R − 2m − g
   に対し、z0 k∈{1,2,3}・z1 k∈{2,3}・z2 k∈{3,4} の全スライスで
   H(2m+g+k; (m, m+g); z) = [g odd]（∀m>=1, g>=1）。
   **z2 面は K1283/K1284 の時点で open だった領域の最初の体系的確定**。
2. **T-L1/L2/L3**: pure-c1 ラダー H(2m+d+2;(m,m+d);0) =
   H(2m+d+3;…;1) = H(2m+d+4;…;2) = [d odd]（∀d, m・再添字による
   即時系）。**d=1 の z1 行 (j, j+1)@2j+4 z1 = 1 ∀j は K1284 open
   登録 C-PC1z1-d4 の c=1 半分の全称解決**（c>=2 半分は open 継続）。
3. **T-ALM**: allm-2 族 6 床（(m,m)@2m+2 z0・2m+3 z0・2m+2 z1
   〔=公刊 T-E1 instance〕・2m+3 z1・2m+3 z2・2m+4 z2）= 0。
4. **C-PB2/C-PC**: pre-band 単層族 (x^c)@(x+2,z1)・(x+1,z0) =
   (c=1: [x odd], c>=2: [x even])。公刊 T-B1′(i)/T-B0′(i) 帯底の
   直接实例（既刊帯定理の外縁での具体値確定）。
5. 床 L-EMPTY・L-11z0・L-1s（手証明）。
6. **構造的発見（族の閉性）**: ペア局面の手がすべて
   （i）同族ペア〔fall: 行 m−1・g+1・k 不変 / upper-drop: g−1・k 不変〕、
   （ii）g=1 upper-drop による allm-2 床 (m,m)@2m+k、
   （iii）C 手子の z−1 面 k−1 スライス、
   （iv）行1 B 手子の単一トークン v(g+1, z+1, g+k+1) = [g even]
   （K0832 tail 分岐読み・全関与面で一様）
   に落ち、**予算 R−1 の子が全て既知族**。g odd は fall/B 子 = 0 を
   0-witness、g even は全子 = 1 で mex = 0・C 手子カスケード
   （1 XOR [g odd]）で 3 面が連結し、予算強帰納で全主張が同時確定
   （well-founded・宣言ノート §2.8）。K1282-K1284 の行帰納（行 m←m−1）
   に対し、本項は R 軸の帰納で閉じる独立の構文。
7. open 登録（有限観測のみ）: 境界三角形法則（z0-k0 = [2,1,0,
   [g even]]・z1-k1 = [1,2,0,[g even]]・z2-k2 = [1,0,2,[g even]]・
   z2-k1 = [g odd] clean・証明には z1-k0 → z0-k(−1) へのカスケード
   すなわち k<0 座標拡張が必要・**未来課題 F1**）・multi-c web
   （F(1,c>=2)=0・G(1,2)=0・G(1,c>=3)=2・a-ladder a>=3・
   G(d,c>=2)・Y族 spread・**spread 理論〔c 方向帰納〕が本命・
   未来課題 F2**）・C-PC1z1-d4 の c>=2 半分（**F3**）・
   z2 pre-band (x^c)@(x+3) z2（z2-band 崩壊が blocker）。

## 出版・監査の記録（publish-then-execute）

1. 最新 main 確認: HEAD 観測 0b113ef3 → push 直前再取得 81ae89f1
   （いずれも Part CP/DJ 探査レーン・非接触）。K1285 空きを
   items dir のコミット履歴で直接確認（最新 K item = K1284 =
   7abca71f・K1285 取得コミットなし）。対抗宣言なし。
2. **commit 2114a771**: 宣言ノート先行出版（証明全文・§1-§5 + honest
   記録・push 競合なし）。宣言ノートの記法正規化もこの時点で確定
   （A手 w→w−1 の向き・角予算式 2m+k・B 手子予算 g+k+1）。
3. **commit 2c70a1b6**: 機体キット出版 13 ファイル
   （README・verify_k1285.py〔sha256 a4165f68…・engine pin
   bd5f22e4… ゲート内蔵〕・engine_block.py〔582c93c1…・K1282/
   K1283/K1284 kit と同一 bytes〕・explore_k1285.py/.out〔E1-E6〕・
   output/dryrun1-4 + .info〔宣言前 dryrun・4 走 byte-identical
   確認済み〕）。**fetch-back**: 13 ファイル size 完全一致 +
   宣言ノート・verify_k1285.py・engine_block.py の全文照合（297 行
   全行・ENGINE_BLOCK/PIN/D1-D10/FAMS/P0-P2/main harness 一致）。
4. **公式実行（fetch-back 検証機体バイトから）**:
   - 4 走すべて rc=0・stdout byte-identical・sha256
     `41762e1b986d08494f4afd0ab4d8f1eb5a406e3608bc8696991b2019df735730`
     （同一 cwd PYTHONHASHSEED=random/1 ×2 + 隔離 tree
     env -i PYTHONHASHSEED=99/7 ×2・/usr/local/bin/python3 3.12・
     ~3-4s/走）。宣言ノート §4 の宣言値と完全一致。
   - counts `[1296, 864, 864, 768, 180, 400, 130, 4200, 560, 532]`・
     総計 9,794 点・bad 0・engine_gate PASS・D1-D3 スライス hist は
     g-parity のみ・D4 ラダー hist {0,1}・D8 wide census（m<=30,
     g<=20・全 7 族）・D9 cross-engine canonical vs ordered 一致。
   - 変異電池 8/8 期待どおり fail-closed・rc-exact:
     --tamper-engine → rc=2。zz0 bad=1296・zz1 864・zz2 864・
     lad 768・alm 180・fl 5・pb 130（すべて rc=1・宣言値と一致。
     fl は床消失検知 5 点）。
5. **commit c4b66682**: 公式成果物出版 18 ファイル
   （output/audit_run1-4.out+.info・tamper_engine/zz0/zz1/zz2/lad/
   alm/fl/pb 8 ファイル・detcheck.json〔verdict OFFICIAL-PASS〕・
   MANIFEST-sha256 31 entries）。
6. **publish (D)**: 本 run log・K item（items/K1285-pair-slices-
   pure-c1-ladders.md）・knowledge README 末尾 bullet
   （curl fetch-back 1,019,639B ベースに純 append・push 後
   fetch-back wc/sha 照合）。

## 受入判定

OFFICIAL-PASS。宣言した全期待値（stdout sha・counts・変異電池
8 種の挙動）が fetch-back で全文照合した機体バイトからの公式
実行で再現され、証明は宣言ノート §2 に全文収録・9,794 点の機械
照合が bad 0。K1284 open 登録 C-PC1z1-d4 の c=1 半分が全称解決、
z2 面初の体系的値域确定、ペア族の閉性という未踏の構造補題を得た。

## 規約・11×11 への接続

- verdict 不消費・11×11 空盤の UNKNOWN は不変・Part CY/CP/DH/DA/
  DJ レーン（batch-28/29/30/31 探査）と完全非接触。
- ペア対角スライスは枝刈り格子としてそのまま利用可能（ペア局面の
  子が全て既知族に落ちるため O(1) 値評価）。巨大レーンへの採用
  判断は巨大レーンオーナーに委ねる（記録のみ）。

## 次課題

1. **F1**: 境界三角形法則の全称化。z1-k0 → z0-k(−1) カスケード、
   k<0 座標系の拡張が blocker。z2-k1 = [g odd] clean 観測の証明化。
2. **F2**: multi-c web の spread 理論（c 方向の帰納）。
   F(1,c>=2)=0・G(1,c>=3)=2 の全称化が最初の目標。
3. **F3**: C-PC1z1-d4 の c>=2 半分（spread 理論待ち）。
4. z2 pre-band (x^c)@(x+3) z2（z2-band 崩壊が鍵）・z2 面の
   δ 軸拡張（T-PS2 の k>=5 側）。

## honest 記録

- 宣言 push に fast-forward 競合なし（K1284 の先例と異なり今回は
  競合なしで 1 発成功・並走レーンとの接触なし）。
- 宣言ノート執筆中の作業修正（公式実行より前・外部には未出版の
  段階での修正・宣言値への影響なし）: A手の向きの正規化
  （repo 規約 w→w−1 に修正）・角の予算式 off-by-one
  （2m+k−1 → 2m+k）・B 手子予算（g+k → g+k+1）・§2.9 表記整理。
  修正後に全 § の子の予算計算を見直して整合（機体側は最初から
  正しく dryrun 段階で 4 走 byte-identical・宣言 sha 不変）。
- dryrun1-4 は宣言前のローカル 4 走で byte-identical（sha
  41762e1b…）を確認済みで、公式 4 走と同一の stdout。
- 公式 4 走・変異電池は fetch-back 全文照合済みの機体バイトから
  実行（隔離 tree 2 走含む）。explore_k1285 の E1-E6 出力は
  seed 非依存で決定的。
