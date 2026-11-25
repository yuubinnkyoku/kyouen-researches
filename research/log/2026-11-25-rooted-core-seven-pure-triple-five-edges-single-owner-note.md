# 単一オーナー宣言: 7点純三点辺・高々5本の完全族に対する K0684 全長34周期認証（same-K evidence update・publish-then-execute）

- 作成: 2026-11-25（Vibe 高速レーン・定時自律実行・宣言時刻は commit 日時による）
- 観測 HEAD at declaration: `7e4113461b3fab56633f6008ed1853b91c438e6f`
  （2026-11-25T17:08:42+09:00・出版直前の再取得による）。
- 対抗宣言確認（出版直前の再確認済み）: 直近 commit 列は K1316 z=12 strip キット
  （`strip-z12-min7-20261125`）・Part EE/EF 11×11 系・belowband 梯子・REMO cap 系のみで、
  rooted-core 系の 7点以上の純三点辺族への着手宣言・実験dir・ノートは存在しない。
  6点二点辺 slices レーン（`rooted-core` 6点 two-edge 系）とも非接触
  （本宣言は 6 点の値を 1 状態も再計算せず、既出版 513 型表・出版済み監査の
  byte 照合でのみ参照する）。本宣言 path は採番非依存の
  `2026-11-25-rooted-core-seven-pure-triple-five-edges-single-owner-note.md` とする。
- 採番方針: **新規 K 番号を採番しない**（採番レース回避）。本成果は K0684
  （fixed core + 長道の 34 周期予想）への same-K evidence update として
  artifacts 追記・evidence/限界節更新により反映する。
- ラベル規約: nodes 数・検証点数を勝敗として読まない。標準 11×11 空盤・二石 root
  {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はどの時点でも UNKNOWN のまま。
  被覆・secured・root 勝敗の主張をしない。本宣言は rooted core + 長道の Grundy 列
  （有限離散残局）のみを対象とし、verdict は一切消費しない。
- 規約: publish-then-execute。本ノート出版後に公式 solve・照合電池を実行する。
  宣言前探査として実施済みの事項は「6. 宣言前探査の全開示」に正確に記録する（隠さない）。
- 実行環境: 定時自律実行のためユーザーの PC には到達不可。全計算・全照合は
  クラウド側サンドボックス（Python 3 標準ライブラリのみ・決定論的）で実行する。

## 1. 対象と主張の体裁

K0682/K0684 と同一の設定: 7 点（根 0 含む）上の純三点辺（各辺は 3 頂点からなる
clutter 辺）を高々 5 本持つ残余核 C の根付き同型型すべてに、根に長さ L の
二点禁止道を付けた通常ゲームの Grundy 列 f_C(L) について、共同適応有限窓認証
（K0682 規則: T=34・N = max(500, 全状態の最終周期破綻+1)・needed = 2N+69・
窓 i∈[N, 2N+35] で道と全状態値が一致すれば全長 34 周期が証明される）により
**全長周期認証**を目指す。

三点辺同士は包含を持たないため、k 本 (k<=5) の三点辺族はすべて clutter であり、
C(7,3)=35 トリプルからの選択は全て合法核である（5点以下の two-edge 場合と同様の
合法性構造）。

## 2. 機械派生値（宣言前 probe・公上演算で枚挙再現する）

- 素材族（ラベル付き）: Σ_{k=0..5} C(35,k) = 1+35+595+6545+52360+324632 = **384,168**
- 根付き同型型（根 0 を固定した頂点置換の標準形）: **924 型**
- 閉包（engine.closure・合法着手による子状態の全閉包）: **2,948 状態**
- base513 既知（K0682 出版済み <=5 点表）で既カバー: **344 状態**
- 新規閉状態: **2,604**（7 頂点 924・6 頂点 1,680）

## 3. 方法

- engine.py: 出版済み `rooted-core-tail-periodicity-20261107/engine.py`
  （sha256 `e7c86bbaf93362cf5120755aa5d7bc69a796c699ae6f3b9c0829ad75cb5b38ee`）
  の `canonical/closure/play/ordinary/delete_root/mex` を import してそのまま使用。
  Grundy 並列再帰は six-edges/full 出版系と同型: 根 X で ordinary 化、根以外の
  着手は retained/detached に分類し、道の値と合成。
- 既知状態は K0682 の出版表 `output/audit.json`
  （git blob `90e28b1f`・prefix 0..1069・添字 500..533 の 34 周期ブロック拡張）から
  遅延拡張する。出版 six-edges 監査（`rooted-core-six-pure-triple-six-edges-20261107`）
  と全レコード一致を宣言前 smoke で確認済み（6. 参照）。
- 新規状態に限り再帰を長さ L で同期進行させ、L>=534 から N を更新し、
  L >= 2N+69 で窓 i∈[N, 2N+35] の一致を全状態に対し検査、全一致で certified。
- 決定論的（set のみだが列挙順は標準形辞書順）、標準ライブラリのみ。

## 4. 受入条件（acceptance）

1. 公式 solve が `jointly_certified=true` で終了し、`output/official_records.json`
   (2,604 新規状態の全値 prefix) が生成されること。
2. 同一環境での再実行（チェックポイント無し・別プロセス）が records 全 byte 一致。
3. `verify_seven_leq5.py` 電池が PASS:
   - 枚挙再現（384,168/924/2,948/2,604/344 の全一致）、
   - canonical 主張の engine 型照合（drive_slice の assert 相当: 全 924 型が
     engine.canonical の冪等固定点であること、写像の単射性は 384,168 → 924 で
     fiber 計算により検証）、
   - 窓証明の再検査（N/needed/窓一致の独立再計算）、
   - base513 既知 344 状態の値が出版表拡張と一致、
   - **6 点側交差照合**: 閉包内 6 頂点状態のうち、出版済み 6 点全型監査
     `rooted-core-six-pure-triple-full-20261108`（10,688 状態）に含まれるものは
     値が全長完全一致、
   - 独立 subset mex 照合（固定 seed・階層化 400 型 × 長さ 0..6・原始定義による
     値の独立再計算と一致）、
   - fail-closed 改変電池（records/既知表/道値の改変・窓破壊が検出されること）、
   - 公式 2 走の stdout が PYTHONHASHSEED の偏りに無関係に byte 一致
     （同一 cwd × `PYTHONHASHSEED=random/1` と 隔離 tree `env -i` × 2）。
4. 上記を満たした場合のみ K0684 item へ artifacts 追記・evidence/限界節更新と
   実験dir 出版（proof.md・records・MANIFEST-sha256）を行う。

## 5. 反例プロトコル

窓認証が maxlen 2200 までに成功しない場合、または窓検査が矛盾する場合:
- 該当状態の特定・L での周期破綻位置・観測尾部を run log に正確に記録する。
- その場合、K0684 予想（任意固定核で最終 34 周期）に対する**この族内の反例候補**
  となる。ただし有限窓の失敗だけでは非周期性の証明にならないため
  （6点 full と同じ限界規約）、発表は「窓認証失敗・周期未確定」もしくは
  「最終周期が 34 でない全称認証」までを区別して記述する。
- K0682 の有限窓定理は候補周期の認証のみを保証し、認証成功を保証しない
  （K0684 item 記載の限界と同一）。

## 6. 宣言前探査の全開示

- **宣言前 smoke（出版済み監査の完全再現）**: 同一パイプライン（solve_core.py
  + engine.py）で 6 点純三点辺 <=6 辺族（raw 60,460・根付き 732 型）を
  チェックポイント付きスライス実行で再計算し、出版済み
  `rooted-core-six-pure-triple-six-edges-20261107` 監査と照合した:
  **全 732 レコードの状態集合・prefix 値完全一致、joint start 571・needed 1211・
  jointly_certified=true・prefix 上 Grundy 最大 27・worst entry
  [6,[7,11,14,19,28,37]] · 571 も完全一致**。生成物 `output/smoke6_records.json`
  （sha256 `dd416a011862303466dc5028e6665f6a37c13de2bf4916514becaf22d6f8eebf`）
  は実験dirに残置し、verifier 電池にも組み込む。この smoke は 6 点族への
  新しい主張ではなく、既出版結果の再現検証である。
- **emit_records の事前修正**: 宣言前レビューで `solve_core.py` の
  `distinct_initial_types` 集計式に冗長誤記（`s[0]==0 or True` と `and` の畳み込みで
  実質「閉包内 n 頂点状態数」を数えていた）を発見し、真の初期型数
  （`len(initial)`）に修正した（sha256 修正後
  `35a563254da03da66c2f12a512c489c82405d2ba2c396d1a0746f5e5a25272e5`）。
  smoke 6 点族では両者は偶然同じ値 732 を与えたため smoke 成果物は無修正のまま
  正しい。engine.py・再帰・認証規則は一切変更していない。
- **予備 probe（宣言値の由来）**: `initial_types` 枚挙・閉包・既知表差し引きは
  2026-11-25 の宣言前 probe で実行済み。§2 の数値はその機械派生値であり、
  探査に限定した再現であり新規の数学的主張を含まない。

## 7. 非衝突宣言

- 6点 two-edge slices・6点全型（出版済み `rooted-core-six-pure-triple-full-20261108`）
  は再計算しない（値の照合のみ byte 照合で読む）。
- 11×11 Part E 系各レーン・K1316 z=12 strip・belowband 梯子（K1311-K1315・O-BBL3）・
  REMO cap15/16・2トークン vertical-fiber・PG(2,q)/Witt・s_n/K_n 各レーン: 非接触。
- K0684 に対応する 7 点族の実験dir `rooted-core-seven-pure-triple-five-edges-20261125`
  は本宣言の時点で存在せず（git log・tree 確認済み）、本レーンが作成・管理する。

以下、公式実行は publish-then-execute により本ノートの commit 時刻以降に開始する。