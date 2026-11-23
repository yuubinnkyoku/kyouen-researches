# Part CK (2026-11-23): batch-28 (class 5343) drive-4 (WIN-CONTINUE) — aa010..aa031の22キー完走 (WIN 12 / LOSS 6 / EXHAUSTED 4)・残23キーfileless UNPROBEDの誠実打ち切り

単一オーナー: n11中央応答レーン (本セッション・Part CJ継続)。宣言:
`research/log/2026-11-23-part-ck-batch28-drive4-declaration.md` (commit `ad269701…`・
publish-then-execute・fetch-back byte一致)。

## 0. 要約

- **drive-4 (WIN-CONTINUE事前登録・wave反復8 invocation・2 worker・timeout 285) で
  aa010..aa031の22キーが完走**。honest label内訳: **WIN 12行** (aa010 8,882,182 /
  aa011 12,424,953 / aa012 4,994,213 / aa013 8,317,071 / aa014 7,263,370 / aa016
  2,621,847 / aa019 7,967,030 / aa020 8,432,253 / aa022 14,044,375 / aa025 3,056,950 /
  aa026 11,019,409 / aa027 4,860,191 nodes)・**LOSS 6行** (aa015 6,152,494 / aa017
  11,446,358 / aa018 214,968 / aa023 5,000,770 / aa024 5,003,631 / aa029 10,010,789
  nodes・result 2・2-pass node-exact・**adoption候補のみ**)・**EXHAUSTED 4行**
  (aa021/aa028/aa030/aa031・nodes==budget 15M・honest UNKNOWN)。MISMATCH 0。
- **18:18:30Zにsession時間制約で誠実打ち切り**。残23キー (aa032..aa054) はfileless
  UNPROBEDのまま (宣言§1(c)どおり・将来drive-5+で継続可能)。
- 行解釈は**route bookkeepingのみ**。WIN 12行はunconsumed closure WIN候補 (34/35
  番目=aa008/aa009〔Part CJ〕に続く36..47番目に相当)。verdict不消費・WIN採用は
  scrutiny owner C++第二実装 gate `9193f5b6…` のみ・ LOSS 6行のcanonical採用は別
  adoption宣言 (pinned merger `90711961…`) 経由のみ (本Partでは一切書込なし)。
- batch-28全体の現在地 (row-audit-winhalt機械導出・pinned `96867282…`): **probed 31
  = WIN 18・LOSS 7 (aa003 + drive-4の6行)・EXHAUSTED 6・fragment 0・fileless 23・
  mismatch 0** (audit x3 byte同一・json SHA-256 `dcf078aa…`)。
- val-gate fresh 4/4 node-exact (Part CK宣言後に再実行・`.ck-host.out`)。
- tamper battery 4/4検出 (実効性assert込み) + post-battery pristine 155ファイル
  sha不変。full-variant併走 (宣言§3): `row_audit_batch28.py` はaa001のWIN 2行
  ペイロードでGATE FAILED (単行想定の既知設計・batch-26 Part BT例の再現・部分終了+
  WIN行ではwinhalt版が適用外正常挙動として記録)。
- 実験dir 151ファイル main出版済み・**最終commit `f3e87330` pinnedでfetch-back
  150/150 sha OK + MANIFEST byte同一**。
- **標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
  class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて) は本Partの実行・
  出版のどの時点でもUNKNOWNのまま。** nodes数はbookkeepingであり勝敗ではない。

## 1. 出版commit一覧 (fetch-back検証)

| Part | commit | 内容 |
| --- | --- | --- |
| 宣言 | `ad269701` | `research/log/2026-11-23-part-ck-batch28-drive4-declaration.md` (WIN-CONTINUE事前登録・対抗宣言なしgrep) |
| A | `ba45347d` | scaffold 79: scripts 8 (7 pinned byte-clone + session-local `drive4_local_step.sh` `ea0db83e…`) + input 55 + val-gate 16 (published 12 + fresh `.ck-host.out` 4) |
| B | `75538c26` | outputs 70: raw 68 (aa001..aa031 p1/p2 + sidecars 6) + status.log (21行seed + drive-4追記 = 61行) + row-audit-winhalt.json (`dcf078aa…`) |
| C | `f3e87330` | README + MANIFEST-sha256 (150行pin) |

実験dir: `research/experiments/n11-centralreply-closure-class5343-batch28-drive4-20261123/`。
fetch-back: commit `f3e87330` で全150内容ファイルsha256 OK + MANIFEST byte同一。

## 2. 正直開示

1. **val-gate freshファイル名の命名乖離**: 宣言§5では本host fresh 4ファイルを
   「`.cj-host.out`」と表記したが、実際の出版名は **`.ck-host.out`** (drive-3の
   Part CJ fresh実行と区別するため)。内容は宣言後の本host fresh再実行 (4/4
   node-exact) で宣言要件を満たす。命名のみの乖離として開示。
2. **drive-4 kitはdrive-3 published dirのbyte-cloneからdrive-3 session-local script
   (drive3_local_step.sh) と drive-3 host val-gate 4ファイル (.cj-host.out) を除外
   した構成** (宣言§5の「published 12 + fresh 4」と整合させた)。seed (status.log
   21行・raw aa001..aa009の22 files) はpublished pinsどおり。
3. **aa030/aa031のtimeout→retry**: 初回invocationは両キーともp1完走 (EXHAUSTED
   15M・wall 157/159s) 直後のp2がtimeout窓でtruncated。sidecar 2 filesはrunner
   rename・P2-TRUNCATED-RETRY bookkeeping 2行をstatus.logに記録した上で、次
   invocationのcompleteness guardがp2のみfresh-cold再実行し完走 (EXHAUSTED確定)。
   truncated passはevidenceでなくretry設計どおりの挙動。
4. **READMEのタイポを出版前に機械検出**: 「WIN-HALT」表記にキリル文字混入
   (Wро-HALT) が1箇所 → 出版前にsed修正 (キリル文字数0を機械検証)・出版後の
   事故はなし。MANIFESTは修正後のREADMEで再生成。

## 3. 運用知見 (今回new)

- (a) **15M budgetのEXHAUSTEDキーはpassあたり約160秒** (aa030/aa031・wall 157/159s):
  timeout 285窓では「p1完走+p2完走」が入らないため、大キーは2 invocation構成になる
  (guardのresume設計どおり・failではない)。WIN/LOSSの小キーはpass数十秒で終わる
  場合があり、wave内で完了する。
- (b) **WIN-CONTINUE設計 (Part CE先例) のbatch-28への導入効果**: drive-1/2/3の
  2-WIN halt設計では1 invocationで止まっていたところ (drive-1: 2キー・drive-2:
  5キー・drive-3: 2キー) に対し、本driveは8 invocationで22キー完走 (session時間
  制約まで)。class閉包の列挙効率はwave-halt設計の約4〜10倍。ただしrunner内蔵の
  rc=45 stopは不変で、**継続判定はsession-local orchestration層のみ**に置いた
  (宣言で明示)。
- (c) drive4_local_step.shはdrive3_local_step.shのpath/workerlog差のみ (二重sed
  差分で同一性機械確認・CJ (c)と同じ手続き)。

## 4. 次回候補 (Part CK以降)

1. **drive-5**: 残23キー (aa032..aa054) の完走 (同一WIN-CONTINUE設計・別宣言。
   残りはEXHAUSTED級の大キー濃度が高い可能性に注意)。
2. **drive-4 LOSS 6行 (aa015/aa017/aa018/aa023/aa024/aa029) のcanonical adoption**:
   Part CH (aa003単行) 先例のloss-only採用part・maker/merger/refresh/extractor一式。
   本レーン次回の最有力候補 (採用はadoption Partで・closure table churnはreaudit
   が機械導出)。**ただし並走が先にdrive-5/adoptionを宣言した場合は最新mainで確認
   して回避すること。**
3. aa004/aa005/aa021/aa028/aa030/aa031 (EXHAUSTED @15M) の高budget再probeは別宣言のみ。
4. batch-29 (Part CI)・batch-23 (Part CE) の並走成果回収・batch-24 fileless選定。
5. unconsumed closure WIN候補35+12キーの採用はscrutiny owner gate待ち (非代行)。

## 5. UNKNOWN担保 (最終)

**標準11×11空盤・19 central-reply roots・二石root {49,60}/{59,60}・S2 {59,60}・
class 1/2/4・class 10968・class 23964・class 5343 (54キーすべて・aa010..aa031を含む) は
2026-11-23 Part CK完了時点でUNKNOWNのまま。** class 5343はWIN 18行 unconsumed +
EXHAUSTED 6行 + fileless 23キーが残るため閉じない (canonical cache `3124461b…` は
本Partでは一切変更なし・closure tableのclass 5343行 (unknown_now 53) はadoption Part
を通らない限り不変)。閉鎖・被覆・secured・root勝敗の主張は一切しない。
