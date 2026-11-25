---
date: 2026-11-24
kind: incident-amendment
scope: research/knowledge/README.md restoration (K1286 publish chain, commit 9305b278)
status: repaired-and-verified
---

# K1286 README push 切断 incident と修復記録（honest）

## 何が起きたか

K1286 出版 chain の最終 commit 9305b278（knowledge README 末尾 bullet append）で、
push 側の本文読み出しがページネーション付き read の**最初の 1 ページのみ**
（37,571 文字 = 63,749 bytes・was_truncated を確認せず）を push していたことが、
publish 後の fetch-back 照合で判明した。

- 意図した本文: 1,028,444 bytes（9336611a 時点の README 1,023,527 bytes +
  K1286 bullet 4,917 bytes・sha256 1811a75c2967d179010857c308ff0754eb9bff27b170317319f89695ae95a0f7）
- 実際に 9305b278 に commit された本文: その**先頭 63,749 bytes だけ**
  （git blob sha1 f5b215ccedd4a480bfd0b7a89ff85126c077d1a8）
- 結果: main の research/knowledge/README.md が約 96% 欠損した状態で公開された
  （K0881 以降の全 bullet・末尾の K items 群が欠落）。

## 検出方法（独立二経路）

1. GitHub connector get_file_contents の first-element SHA（= git blob sha1）
   f5b215cc… が、ローカル正本の git blob sha1 147839af… と不一致。
2. repo が public であることを利用し raw.githubusercontent.com で本文を直接取得:
   63,749 bytes・sha256 585f8c49… = 正本の先頭 63,749 bytes と byte 一致 → 切断確定。
   9305b278 の直前 commit 9336611a の README は 1,023,527 bytes で
   ローカルの K1285 時代正本（sha256 0d7fd00e…）と byte 一致
   （ベースの取得は「fresh fetch」ではなく K1285 時代のローカル copy の再利用だったが、
   事後照合で 9336611a の repo 状態と byte 一致していたため内容被害は切断のみ。
   push 元に「fresh fetch」と記した点も本 note で訂正する）。

## 修復

- ページネーション read を next_offset で完走（17 chunks・総 641,464 chars）し
  サンドボックス内で連結、write_file で roundtrip ファイルを生成して
  sha256 1811a75c… の byte 完全一致を確認後、同一の連結文字列を push。
- 修復 commit の README blob は 1,028,444 bytes・git blob sha1
  147839afdea110f6079e41f7400cae78b8990b40・sha256 1811a75c…
  （= 9336611a 正文 + K1286 bullet・意図した最終状態）。
- raw.githubusercontent.com による修復後の直接 byte 照合も実施（下記検証行参照）。

## 影響範囲と訂正

- K1286 の他の全出版物（宣言ノート f6db3f33・機体 13 files ccf48d10・
  公式監査 22 files a92dcc12・K item + run log 9336611a）は影響なし
  （fetch-back sha256 照合済み・K item 15,430 bytes・run log 10,253 bytes byte 一致）。
- run log（2026-11-24-border-slices-prediag.md）の「README bullet push 完了」
  記述は本 note で訂正: 実際は切断 commit であり、本 repair commit で完了。
- 11×11 verdict・他レーン（Part DF/DG/DL/DJ 等）との非接触は不変。
- 今後の運用 lesson（他レーンにも適用）: >64KB のファイル push は
  read pagination 完走 + 連結 + roundtrip sha 照合を必須とし、
  push 後は first-element blob sha で本文完全性を検証する。

## 検証行（修復 commit 後に記入）

- 修復 commit sha: （この note と同一 commit）
- README restored blob sha1: 147839afdea110f6079e41f7400cae78b8990b40
- README restored sha256: 1811a75c2967d179010857c308ff0754eb9bff27b170317319f89695ae95a0f7
- 意図 byte size: 1,028,444（63,749→復元）

