# 単一オーナー宣言ノート: fold24外部第二検証（K1164）のpristine再実行第三検証（2026-11-20）

本ノートは、検証可能な小証明を積み上げる11×11長期レーンの衝突防止のため、
fold24 receipt fold（K1140）の**外部第二検証**として出版されたK1164実験一式に対する
**pristine再実行第三検証**の単一オーナーを宣言する先行出版物である。
AGENTS.md の first-published-priority 規則に従い、同一作業の先行宣言が確認された
場合は本宣言を無効とする。

- 宣言日時 (UTC): 2026-11-20T19:15:00Z
- 宣言時点の main HEAD: `118e1b3d23`（K1164第三検証の先行宣言なし。
  fold23外部第二検証は `90ac8eed`・fold25外部第二検験は `aad3b71ca3`・
  WIN8証明書行共有監査は `c403614f` が宣言済みで、いずれも本宣言の対象外）
- 対象出版物: `research/experiments/n11-fold24-external-second-verification-root438000000818-20261120/`
  （part1 `12b49de902`・part2 item/log `309d140861`・part3 README bullet/log訂正 `afd5046663`）
- 対象正本（SHA-256）:
  - K1164 検証機 `scripts/verify_fold24_external_20261120.py`
    `9bc24e3806724cf7dd3db7e23ec26fb4598ea1952bd92c2974c5626a561d8a52`（55,555 bytes）
  - K1164 監査正本 `output/external-audit.json`
    `c7e10332df04a4f1e5af7b1cbc5ec487a5c15ca7851edba102b7b3679feb7c24`（36,605 bytes・gate 800）
  - K1164 実行記録 `output/reproduction.log`
    `16b7678e062d65e29e459846feff879a77293e53cefad9357c7375cbfe9950e2`（3,970 bytes）
  - K1164 実験README `README.md`
    `ff42947934d7d9df70f549e9547b42bd56f6b566749770c20b697c9850cc6994`（6,232 bytes）
  - K1140 上流出版byte 5点（receipt `c4ab76d3…`・出版機 `f462733d…`・
    同梱監査正本 `49f330c6…`・再現log `cb01749a…`・reconstruct_inputs.py `f4e1fa8e…`）は
    K1164検証機自身のP-gate pinが検証対象とする入力である。

## 位置づけ

K1164（fold24外部第二検証）は出版社（外部第二検証レーン）が2回の外部実行と
第三実装の検証機による全再導出までを出版済みだが、出版後の第三者が出版byteだけから
検証機の監査正本をbyte再生できること（pristine再実行第三検証）はまだない。
本検証で確定するのは、K1164の実験dir・W再構成・検証機・監査正本が輸送・転写・
ローカル記憶に依存せず再現可能であることである。

## 作業範囲（受入条件）

1. K1164出版byte 4点とK1140上流出版byte 5点をGitHub（pinned commit）から再取得し、
   SHA-256 pin照合をfail-closedで行う。
2. 出版済み `reconstruct_inputs.py`（`f4e1fa8e…`・固定Git参照 `b91e85a99f0480f084835bdff51533d0cf5feaa8`）
   でW入力tree（61 pin: 12 Git blob + 49 SHA-256）を**2回**独立に再構成し、
   2回のW全入力がbyte一致することを確認する。
3. K1164検証機（`9bc24e38…`）をpristine再実行する（計4回: 同一cwd 2回＋
   隔離HOME/cwd＋`PYTHONHASHSEED=random` 1回を含む）。全実行の監査JSONが
   出版監査正本 `c7e10332…` とbyte-identicalであること（各実行はfold24機4回・
   fold23隔離rerun chain・同梱監査・tamper 2件の内訳を含む）。
4. tamper検査: 出版社T-gateが検査済みのoffset（worklist 777・K1136証明書 12345）と
   **異なる**位置で1 byte XOR 0x01を入力に施した検証機実行が、fail-closed
   （returncode 1・監査未書込）で捕捉されることを2件以上確認する。
5. 本レーンharnessの監査正本JSON（時刻を含まない決定論的出力）は、
   同一cwd 2回＋隔離＋`PYTHONHASHSEED=random` の3実行でbyte-identicalであること。
6. 監査正本に解釈ガード文言（行を1行も閉じない・UNKNOWNのまま）を同梱すること。

## やらないこと・非主張

- fold23外部第二検証（`90ac8eed`・訂正 `839057fb`）・fold25外部第二検証（`aad3b71c`）・
  WIN8証明書行共有監査（`c403614f`）・fold26 receipt fold（`23bffdd4e4`）・
  round-5 refsolve（`ace38772d9`）・WIN8-D10候補 `00000000010000809002000040002001`
  の証明書抽出（`63877ffd2e`）は他レーン宣言済みで着手しない。
  新規depth-10 probe・新規証明書抽出・行の閉鎖claimは一切行わない。
- K番号はpush時に3点確認で空きを取得する（現時点では仮番号も確定しない）。
- 本検証は検証の検証（第三検証）であり、閉じた行のゲーム理論的勝敗を主張しない。
  WIN8-D10証明書は当該8石rootのゲーム木に限られる。REFUTED-D10はLOSS証明ではない。
  nodes数・solved数を勝敗として読まない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class 1/2/4は
  すべてUNKNOWNのまま。** 行は1行も閉じない。

失敗・timeout・入力取得失敗は実験事実として記録し、部分的な数値を成果として扱わない。
重要証拠は再現可能なrepo成果物として出版する。
