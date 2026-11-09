# 2026-11-09 p=2647のサイズ1323全4形状を検査し上界1322へ

AGENTS、knowledge README、K0693/K0702/K0706/K0711/K0713/K0714と最新log・experimentを読んだ。
git fetch origin main、status、実行中プロセスを確認。mainは8972b198、他者の未追跡shape出力2件を保持。
前回のPID30328は新しい探索ではなく、native監査後の2.7GB LRATをlevel-9 gzip化していた。
同じ探索・監査・圧縮は重複起動しない。

## 圧縮を待たずにLRAT自身を検査

native drat-trimの出力は完了しておりraw LRATが読めたため、別段階のhint検査を進めた。
新しいreplay_lrat_stream.pyは8MBずつ読んでhashを計算し、preflightを先に保存する。
証明全体を一括bufferへ読む旧driverは変更せず、実行とsource hashの対応を保持した。
原CNFのhashは修正後の112入力、全節schema receipt、保存solver入力と一致する。
実行する局所修正版のsource hashも、K0714の5制御例で検査したものと一致した。

raw LRATの終了後の自動cleanupに備え、生成ディレクトリ外に同じ内容のhard linkを保持した。
これは同一volumeでのリンクであり、2.7GBの複製計算を起動したものではない。
raw SHA-256は3f2789475cea38cb8edd7ea43e5042cac4a6702a4c1ab04e367987155dad7ca1、
2711546166 bytes、943588行。

局所修正版LRATは241.9秒で終了コード0・c VERIFIED。追加699109節は元の85619節を含む実装上の集計。
原版LRATの偽空節受理は使わず、空節が実際のRUP矛盾を持つことを要求した検査の受理を採用する。

## 上界1322への論理

サイズh=1323ではe=x+c、完全対は高々一つなので、000/011/101/112の4形状が全てを尽くす。
各CNFは、独立したprefix閾値counter・全節schema・提供辺の整数幾何で安全集合からの拡張可能性を確認済み。
000/011/101の削除無視・RAT禁止のRUP受理と、新しい112のLRAT受理を集約した。
qualify_upper.pyは入力・証明・検査器・回帰・receipt・manifestのhashを照合し、全4件受理を確認した。
最初の集約は絶対pathを含んだため保持し、repo相対pathに揃えたportable版を新しい出力として保存した。

従って1323点の安全集合はなく、より大きい集合から1323点部分集合を取ることもできないため上界は1322。
既存K0711を1296<=A(2647)<=1322へ更新し、K0706の参照とK0713の保留記述も更新した。
下界1296や正確値の未確定は変わらない。有限計算の監査であり、検査器全体の形式的健全性は主張しない。

## 証拠保存と後処理

LRAT受理後、raw pin・DRAT core・原証明が保持されていることを確認し、重い旧gzip後処理のPID30328だけを中断。
packing-interruption.jsonへ対象と理由を保存した。元native DRAT-trimのverdictは未永続化なので根拠へ加えない。
新しいcompress_lrat_stream.pyでlevel-1・8MB blockの圧縮とraw hash照合を行い、新しいmanifestを保存する。
大きいraw/coreはGitから除外する。採用した反駁はローカルに保持し、Gitにはhash・所在・受理receiptを保存する。
別checkoutで証明を再生するには、その本体の復元が必要である。

次は1296と1322の幅を狭める探索、または別素数の未完了監査を選ぶ。
今回閉じた1323点4形状のSAT再実行は不要。より強い1322点排除は量化範囲が異なる新課題として扱う。

## 最終検証

stream level-1保存は101.1秒、gzip880640417 bytes。
圧縮SHA-256は773482937558f0e8a90692760da74d8dc5eaa87f5a4e3593c9dfc4d69f730ca0。
往復展開も36.3秒で成功し、943588行・2711546166 bytes・raw hashが受理済みLRATと一致した。
raw pinとgzipの両方を保持している。最終qualificationは保存manifestのreceipt hashにも結び付けたpreserved版。

uv sync --locked、knowledge check（696項目、error 0 / warning 0）、共通unittest33件（319.371秒）は全て成功。
生成物をbuild.pyで再生成し、stage後に生成物差分0を確認する。
研究計算・圧縮の自分のプロセスは終了し、同じ対象の長時間jobは残していない。
他者の未追跡shape出力2件と、全raw evidenceを保持する。
