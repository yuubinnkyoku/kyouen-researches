# 2026-11-18 n11 class2-lane: コーディネーターSTERILE-parent修正の検証側クロスチェック (2026-11-18)

## 背景

cost82e revalidation sweep出版（commit `beb41b19`）に続き、sweep完了後に並走が出版した
コーディネーター修正（commits `1d05b0a1`/`e3db912a`/`4ffdf3b6`/`8c04f41e`: v18
sterile-parent filter audit・cost82d claim v3化）の事実基盤を、本レーンの出版データ
（census v19・cost82e sweep監査）から独立に再導出した。**検証側の位置づけで、新規の
ゲームverdictは一切生成しない**。

## クロスチェック（`audit_sterile_parent_correction_crosscheck_20261118.py`・blob `20dc3f1f`・
出力 `class2-lane-sterile-parent-correction-crosscheck-20261118.json`・blob `1baaf4c6`・336 checks all PASS・二重実行byte-identical）

入力4ファイルは全てgit blob pin検証済み: census v19 `a0c6abaf`（本レーン・commit `122cb6c6`）・
K0865 census `9c251da3`（並走・commit `5ada304a`）・v18 sterile-parent filter audit `60233241`
（並走・commit `1d05b0a1`・audited_main `43f9e07a`）・cost82e raw-batches audit `49757780`
（本レーン・commit `beb41b19`）。

- **A. K0865 totals**: 174 open S5 / 3 unclosable / 57 partial / 114 no_sterile / 91 sterile refs /
  12,274 remaining row refs / eff 12,183がfilter auditの記載と完全一致。
- **B. unclosable parent**: class-4 S5 `00000000020000003800000080000000`（rem 18・rem_cost 1460・
  sterile_cost 1460・18 refs）がK0865のunclosable_s5[classes==4]とfilter auditのparent blockの
  両方に一致。
- **C. 18 sterile refsの構造**: 各refはparentとちょうど1 bit差（xorが2の冪）で、
  ref hex == D4 canon(parent | 1<<bit)（独立再計算）・popcount 6（S6行）・18行distinct・
  cost総和 == 1460 == rem_cost。parentはpopcount 5（S5）。
- **D. filter auditの9行pool**: 全行のparent == 上記STERILE parent・全行が18 refs内・
  costがK0865 refsと完全一致・9行distinct・STERILEフィルタ後のeligible行は0。
- **E. census v19 ranking（8行）== filter audit pool（9行）− cost82d行**: 8行全てparent一致・
  cost一致・**open_after_census_v19 == open_after_v18 − 2が全8行で成立**
  （82d verdict mapが各sibling行の対称2 bitをcanon被覆する予測通り・v19出版時の主張を
  行単位で機械確認）。
- **F. census v19 family表**: parent familyの18行が18 sterile refsと集合一致（costも全行一致）。
  swept/excluded 10行 + remaining 8行に分割され、remaining 8行 == ranking 8行と一致・sweptと
  remainingは互いに素。
- **G. cost82e revalidation整合**: 82e child `00000000020000003800000090000000`は18 refs中の
  cost 82行。census v19 selected_targetのbits（63 sweep + 19 confirmation = 82）がcost82e監査の
  82 bitと完全一致し、**全82 per-bit root canonをD4 canon(child | 1<<bit)として再導出して
  監査記録と一致**・全bit REFUTED-D10・0 WIN7-D10・0 capped・70,583,627 nodes・pilot 8/8・
  v15 crosscheck 19/19。K0865のSTERILE分類（この行の全合法候補がREFUTED-D10）と
  cross-versionで整合。

## 結論

コーディネーター修正の事実基盤を336チェックすべて独立再現した: **v18/v19残poolの全行が
単一のall_remaining_sterile parentに所属し、どの行もparentのD10 WIN7 receipt閉鎖に
寄与しない（K0863）**。したがって残pool行のD10 receipt-closure掃引は誤方向であり、
歴史的行のsweepはcross-version revalidationとしてのみ意味を持つ（cost82e revalidation
sweep・claim v2のラベリングと整合）。STERILEフィルタ付きcensus再構築は並走管轄のまま。

## 制限

- 本クロスチェックは検証側の簿記であり、engine実行・新規verdict生成を含まない。
- **REFUTED-D10はLOSS証明ではない。STERILEもLOSS証明ではない。**
- 11x11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はいずれも
  **UNKNOWN** のまま。

## 次の一手

- 並走のSTERILEフィルタ付きcensus再構築の出版を待ち、出版されたら検証側に回る
  （本クロスチェックのparent/ref構造チェックはその検証にも再利用可能）。
- 残pool 8行の再検証は「revalidation」ラベルでのみ実施。
- partial-STERILE 57 parentのcross-cover価値分析（非STERILE children経由）は未着手。
