# 2トークン残余ゲーム y=14族 全称証明: 正本検証器12機械チェック part1（K1233 fit の正本監査・昇格判定はpart2）

- 実験名: vertical-fiber-two-token-y14-parametric-allz-proof-20261122
- 対象族: H(R; (x,14); z), z >= 0, x >= 14, R >= 0（標準 11×11 とは無関係の数学的残余ゲーム族）
- 対象item: [K1233](../../knowledge/items/K1233-two-token-y14-parametric-closed-form-fit.md)（fit出版時 observed・part1 である本実験の出版後も **observed のまま**。observed→proved の昇格判定はpart2）
- 単一オーナー宣言: [2026-11-22-y14-universal-verifier-single-owner-note.md](../../log/2026-11-22-y14-universal-verifier-single-owner-note.md)（commit 24e418a9・2026-11-22T19:08:21Z・観測HEAD cd2c1095・push直前に対抗宣言なしの確認済み・part1 12チェック+part2昇格を保持範囲と宣言）
- 実行環境: Python 3.12.14 標準ライブラリのみ・cgroup RAM 上限 1,090,519,040 bytes（約1.0 GiB）・2コア・x86_64（y=12/y=13 part1 と同一ホスト同一制約）

## 機械構成（verify_y14_universal.py・SHA-256 4ecdec11bb4b5d2c7047114228c8482eff2b09db1eb7251c37c5787dda91c34e・37,439 bytes）

y=13 part1 正本機械（K1232・commit ee3b6f73・verify_y13_universal.py part1 出版byte
SHA-256 b73d9aaa94f04f1f4922d84808ac7afe6f5bfb55631b4c990cae29734279141f）と出版 cand14.py
（K1233 fit・commit b6f74dfc・SHA-256 61782b6e0a6dde7717dff9ac672299c918e6400bf18dad47ea419a9f081b961e）から
機械的に組み立て（`scripts/build_verify_y14.py`・SHA-256 24246a5d7e36a90277a29ca65a989a6b197ab309802a4fe6d589fd650dfa89bc・
全置換に count-assert・再生成物は実行物と byte 一致を本出版前に再確認）:

1. 生 2エンジン（H_ordered/H_canonical）+ K0832 単一トークン表 single_token + mex: y13 part1 機械から
   verbatim（同領域は y11 正本の 77 行 verbatim と y12/y13 出版時に確定済みの byte）。
2. cand13 ブロック（B子・y=13 出版族の逐語ブロック）: y13 part1 機械の cand13 セクションをブロック内
   Y→Y13 改名のみで転写（改名 39 行の count-assert・改名以外の差 0 行・Y13 = 13 併置で cand14 ブロックの
   Y = 14 と共存。B子 = cand13(z,x,R-1) 全域〔x>=13・全z・全R〕が K1231 全称域内。
   隣接前族（y=13）をB子に逐語転写するのは y11 機械（B子=cand10）・y12 機械（cand11）・
   y13 機械（cand12）に続き 4 連）。
3. cand14 ブロック: 出版 cand14.py（K1233・実 byte 再計算一致 61782b6e…）から fit driver（main）と
   docstring を除き verbatim（差 0 行）。ブロック内 q_odd/single_token_val/_bk の重複定義は y10..y13 検証器と
   同じくブロック毎に併置（最終定義が呼び出し時に勝つ・出版 y10..y13 検証器と同一慣行）。
4. これ以外（docstring・imports・opts14・型機械・12チェック・census runner・main）は本実験のために
   書かれた y=14 機械本体（y13 part1 機械構造の 1:1 写し・族定数のみ差し替え）。x=14 合流子:
   opts14 で A子 = cand13(z,14,R-1)（(13,14)≡(14,13) の多重集合同値・x>=15 は cand14(z,x-1,R-1)）、
   B子 = cand13(z,x,R-1)、C子 = 1 xor cand14(z-1,x,R-1)。
5. 型機械: clip 窓 2y+2 = 30・番兵 31（10族連続 tight 候補・y=5..13: 12/14/16/18/20/22/24/26/28 に続く）、
   tail x+z+15・merge x<=z-15 は corollary として機械照合。census box は z=0..79・x=14..70・R<=x+z+15、
   C12 深格子は z=0..120・x=14..120・R<=x+z+17。
6. 組み立て時の健全性 spot 4 種はすべて不一致 0: cand14 vs 独立第二検証レーン cand14 55,692 点・
   cand14 vs 生エンジン 2,268 点・cand13 vs 生エンジン 1,533 点・x=14 merger 行 970 点
   （第二検証〔V1-V4 PASS・判定等価 2,241,162 点〕との整合は cand14 ブロックの追加位置づけ）。

## 12チェック構成と実行結果（overall PASS・total_points 6,377,860・total_bad 0）

| check | 内容 | points | bad |
|---|---|---|---|
| C1 | 両生エンジン vs cand14・z=0..14・x=14..32・R<=x+z+47 | 22,230 | 0 |
| C1b | K0832 単一トークン raw anchor・出版 cand13（y=13族=B子）raw anchor・x=14 合流子 (13,14)≡(14,13) raw anchor | 42,447 | 0 |
| C2 | 閉形式恒等式格子 z=0..48・x=14..58・R<=x+z+41（merge/tail 併合） | 222,705 | 0 |
| C2b | 深tail行 z∈{60,72,84,96,108,120,240,400}・x=14..64(step5)・R<=x+z+31 で (x+14) mod 2 | 19,140 | 0 |
| C3 | 選択肢分解の生エンジン子列挙照合 z=0..5・x=14..18 | 1,185 | 0 |
| C4 | 型機械 box ±60（clip 30/番兵31）・(value, sorted子) 完全収束 | 606,427 | 0（C4時点 248,232 型・identity/confluence とも 0） |
| C4t | tightness probe clip 29/番兵30: 2,480 収束違反・最初 (60,92,92) → clip 2y+2=30 が tight | 606,427 | （bad 総計外・情報提示） |
| C7 | シード 20261142・200k 点・z,x<=3000 | 200,000 | 0 |
| C8 | 境界多様体 z<=3000・dx∈[-30,17]・tail 窓 [x+z+15, x+z+17] | 993,021 | 0 |
| C9 | v空間シェル [61,64]/[89,92]/[117,120] | 910,710 | 0 |
| C11 | 生 census アンカー z=0..79・x=14..70・R<=x+z+15・両エンジン（後述） | 889,200 | 0 |
| C12 | 深格子 z=0..120・x=14..120・R<=x+z+17 | 1,864,368 | 0 |

- corollary merge（x<=z-15 → single_token(x+14,z,R)）: 1,370,848 点・不一致 0
- corollary tail（R>=x+z+15 → (x+14) mod 2）: 212,713 点・不一致 0
- 型総数（全チェック終了時）: 281,912
- **C4t で clip 29（2y+1）では 2,480 点の収束違反（最初の違反 (60,92,92)）があり、clip 2y+2=30 が tight。
  2y+2 clip tight は 10 族連続（y=5..14: 12/14/16/18/20/22/24/26/28/30）**

## C11 census の bounded-memoization twin（y12/y13 part1 と同一設計・本ホストの 1 GiB cgroup 制約）

census box（z=0..79・x=14..70・R<=x+z+15・444,600 点/エンジン）を無制限 memo の生エンジンで
1 プロセス実行すると再帰キャッシュが cgroup 上限（約1.0 GiB）を超えて OOM kill する
（y12 前身試行で exit 137・maxrss 996MB・行ごと cache-clear 版が 300 秒コマンド上限超過を
y12 part1 published_run.txt が実測記録・y=13/y=14 は同一ホスト同一制約）。そこで:

1. **bounded-memoization twin**: 出版生エンジンの code object を module globals の浅い複写に再束縛し、
   再帰参照（H_ordered/H_canonical 名）を LRU 上限 1,600,000 のキャップ付きキャッシュへ張り替えた双生機。
   再帰定義の byte は正本と同一（types.FunctionType + globals 複写）で、決定的純関数の memo化は透過・
   LRU 追い出しは固定訪問順の下で決定的。したがって値は出版エンジンと厳密一致し、上限は residency のみ制限。
2. **engine 別コマンド分割**: `C11ordered` / `C11canonical` 各コマンドが census 一式（444,600 点・twin cache・
   merge/tail corollary 併合）を実行し `output/census-<engine>.json` を書く。実測（run1）: ordered 14.8秒・
   canonical 16.6秒・cgroup 上限内で OOM なし。
3. **fail-closed merge**: `C11` モードは両 part ファイルを読み、engine 名・box 表記・cache 上限・
   点数（= census 幾何公式からの再計算期待値 444,600/merge 144,534/tail 4,560 を再計算して照合）・
   bad==0 を検証した上で merge し audit の C11 に記録。part ファイル欠落・1 点改ざん・
   corollary 改ざんは全て fail-closed（SystemExit・監査不成立）で捕捉。
4. 無制限 verbatim エンジンは引き続き C1・C1b・C3 の生アンカーを担う。

## 決定性（3回実行 byte-identical）

- audit.json: run1（同一cwd）→ run2（同一cwd再実行・census parts 含む全再生成）→ run3
  （隔離 tree/cwd/HOME + PYTHONHASHSEED=random・census parts も隔離側で再生成）の 3 実行とも
  byte-identical（SHA-256 f8f7180f958ebda39cc0e2efdb64b00416d8e01ea901ef2970201e870d6b7d76・3,105 bytes）。
- census-ordered.json: 3 実行とも byte-identical
  （SHA-256 6bb64b3c96dec85059005b19a84546cae54f0896a318f84824e6152a47f6e431・486 bytes）。
- census-canonical.json: 同様に byte-identical
  （SHA-256 f31a990ee1b3da2a8adcaf49768345198f6e046226e7cfa0240cf2a03946259c・488 bytes）。
- 監査は時刻・実行時間・パスを含まない。seed 固定・sorted keys。
- 機械組み立てスクリプト（scripts/build_verify_y14.py）の再生成物は実行物と byte 一致
  （sha256 一致を本出版前に再確認）。

## fail-closed 検査（census part 経路・出版前に実施・3/3 捕捉）

1. census-ordered.json の points を 444,600→444,601 に改ざん → `FAIL-CLOSED: census points 444601 != 444600`。
2. merge corollary 点数を改ざん → `FAIL-CLOSED: census merge corollary mismatch`。
3. census-ordered.json を一時退避（欠落）→ `FAIL-CLOSED: census part file for engine 'ordered' is missing...`。
   （いずれも監査不成立で PASS 出力なし。改ざん後は正本を復元し、フル12チェックを再実行して正本監査を
   再確定・byte-identical を確認。なお audit.json は最後に実行したモードの監査を同じパスに書くため、
   単体 C11 モードや default モードは部分監査で正本 audit.json を上書きする。本実験の出版 byte は
   チェック名明示のフル12チェック実行で確定したもの。）

## 再現コマンド

```sh
python3 verify_y14_universal.py                  # 12チェックのうち C11 以外
python3 verify_y14_universal.py C11ordered       # census part1（約15秒）
python3 verify_y14_universal.py C11canonical     # census part2（約17秒）
python3 verify_y14_universal.py C1 C1b C2 C2b C3 C4 C4t C7 C8 C9 C11 C12  # フル12チェック（正本監査・最後に実行）
sha256sum verify_y14_universal.py scripts/build_verify_y14.py output/audit.json output/census-ordered.json output/census-canonical.json
```

- 再生成: `scripts/build_verify_y14.py` は本実験で実際に実行した機械組み立てスクリプトの出版 byte。
  ソース定数は組み立て実行時の作業tree配置を指す（SRC13 = `verify_y13_part1.py` は y13 part1 出版byte
  〔commit ee3b6f73・SHA-256 b73d9aaa…〕・SRC14PUB = `../their/cand14.py` は出版 cand14.py
  〔commit b6f74dfc・SHA-256 61782b6e…〕）。この 2 byte を同じ相対配置に置いて（または同 sha の
 出版byte 2 ファイルを指すよう定数だけ差し替えて）実行すると、`verify_y14_universal.py` を
  byte-identical に再生成する（4ecdec11…）。
- 実行細部（run1 transcript・run2/3・fail-closed 3 種・builder 再生成・注記）は
  [published_run.txt](output/published_run.txt) の記録の通り。

## 解釈規約

- K1233 の status は本 part1 出版の時点では **observed** のまま。昇格判定は part2（C1d 出版固定z切片
  アンカーの y=14 特殊化 + census_rows.py 第三実装 + 3回 byte-identical）で行う
  （K1152/y=12・K1231/y=13 と同一手続き・同一K項目・新規採番なし）。part1 の position は
  「正本検証器と 12チェック監査の出版」であり、全称主張の確定主張は part2 まで行わない。
- 有限照合は有限観察の機械的証拠であって、trust 境界（選択肢分解の健全性・mex 恒等式・有限型空間の完全性）は
  y=5..13 系列と同一の機械分類に依存する。
- 標準 11×11 の空盤勝敗・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて **UNKNOWN** のまま。
  本実験は残余ゲーム族 H(R;(x,14);z) の数学的構造の機械検証であり、標準盤の勝敗には一切言及しない。
- 3トークン以上・y>=15 族・固定幅・q点版安定化長は範囲外。
