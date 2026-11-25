# WIN8-D10 certificate extraction root 9840004: single-owner declaration

- **担当レーン（単一オーナー）**: 2026-11-20 長期レーン（fold12/K1107 出版の同一実行継続）。K1097「次の一手」残項「残りWIN8候補の証明書抽出」のうち、K1086 per_root 上の最安価（最小nodes）未抽出根 root `00000000000000003800000009840004`（主張被覆3行 `00000000000000003800000009000004`・`00000000000000003800000009040000`・`00000000000000003800000009800000`・K1097 win16 footprint で intrinsic == claimed を確認済み）の着手権を確定する。
- **目的**: K1086 addtwo-greedy23掃引が両AND順序 uncapped（andclose1 nodes 1,143,198・andclose0 nodes 1,528,656・loss=true・terminal石数 [14,18]）で WIN8-D10 候補確定済みの当該 8石root の完全勝利戦略証明書（n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS）を K1096/K1106 と同一プロトコル（probe再現 → 盲抽出 A1/A2/B 3実行 → BigInt 3×3・Bareiss 4×4・python第三方法の三重検証 → root定数差し替え監査機械）で抽出・検証する。
- **管轄の区別**: 並走が宣言済みの root `…8180000`（commit 4496c888）・`…0810000a` とは別根。K1096（fold11/K1105 で fold 済み）・K1106（fold12/K1107 で fold 済み）とも独立の抽出であり、複数 root 抽出の独立導出の体。**本証明書は当該8石rootのゲーム木のみを証明する**。S6親行の被覆幾何・fold（fold13候補）は別工程であり本抽出では確定しない。行の閉鎖claimは本ノートでは行わない。
- **並走への依頼**: 他の n11 レーンは本根の抽出を重複実行しないこと。fold 完了後の refsolve（残余65行）・他のWIN8候補根の抽出はそれぞれ着手時に宣言すること。
- 解釈規約は不変: REFUTED-D10 は LOSS 証明ではない。nodes 数・solved 数を勝敗として読まない。**標準 11×11 空盤・二石 root {49,60}/{59,60}・S2 {59,60}・class 1/2/4 はすべて UNKNOWN のまま。**
