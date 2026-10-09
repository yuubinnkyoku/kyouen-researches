# reply27 strategy redesign, 2026-10-10

開始時にorigin/mainをfetchし、HEADと `52239697a6a65b11889669725f8599604d53656f` が一致することを確認した。tracked worktreeはcleanだった。.localと過去の未追跡一次資料を保持し、branch/PRは作成していない。

最初にAGENTS、knowledge README、K0105、K0355、resume logとboundary experiment、DFPN exact replay、S5/S6/S7 generator/verifierを確認。最新checkpointは5700 S5 cache、117/119、S4 `(1333065489702715392,0)` の104 LOSS / 2 UNKNOWN、6 UNKNOWN S6、512 S7。条件付き4 S7証人、245 S8、122 S9、3734 S10遷移の保存物も確認した。

固定プレイヤー極性をコードと照合して、旧S7 helperにnegamax式の誤反転を発見。旧derived S5 WIN2件は直接15M UNKNOWNしか支持がなく根拠撤回。旧raw/cache/logは変更せず、registryと主要cache loaderを訂正した。有限三値境界のBoolean completionテストでS4..S10全パターンを検査した。

studyの最初のraw scanはbudget0のderived cache projectionに遭遇して停止した。これはsolver rawではないため別物として除外し、raw positive-budgetのhash/geometry監査を完了した。UNKNOWNをcacheへ採用せず、原データを改変していない。baselineの正しいcacheは5698行。全6871 edges / 3384 classes / 119 verticesを再構成し、残り100/108を覆う115候補、44 WIN除外、71 UNKNOWNを得た。

2M / 1 worker / memo22 / count / same binaryでA4 S7とB4 S5を比較。Aは4 LOSS（290045 nodes）、Bは1 LOSS / 3 UNKNOWN（7289601 nodes）。Aの4証人はWIN側の条件付きcoverであり、その選択をLOSS側の証明と読めない。

Cとして6 S6を15Mへ増額。計20056308 nodes、5 WIN / 1 LOSS。完全境界によるA二つのS5は1 LOSS / 1 WINで、S4 classはWIN。第二S5は完全51子中50既知WIN・UNKNOWN1だったので、そのS6の2214318-node WINだけでclassを棄却できた。残るS6も固定pilotとして回収し、一つのLOSSからreverse propagationで5新S5 LOSSを得た。将来のrunnerでは上位の決着を各完了時に伝播して、より早く止めるべきである。

B最初の候補 `(1297036692700528640,0)` の2M UNKNOWNを15Mへ増額すると、最初の子が7541821 nodesでWIN。残る7件は停止。記述的WIN頻度/打切りcost/共有を使う8 S5 probeは4 WIN / 4 LOSS、44544197 nodes。経験frequencyは選択バイアスを含み、確率校正も勝敗証明もしていない。

次候補 `(1297036692952186880,0)` は8/8 LOSS pilot（27200838 nodes）で有望と判断し、残る91子へ15M / 4 workersで拡大。12 replay（62024329 nodes、11 LOSS / 1 WIN）でWINを得て79未dispatchを停止、activeをdrain。class全106子はLOSS26 / WIN1 / UNKNOWN79。少数のLOSS標本はclass LOSSを保証しない。

全探索168947139 nodes。direct exact40（S5 6 WIN / 24 LOSS、S6 5 WIN / 1 LOSS、S7 4 LOSS）、UNKNOWN S5 raw3。S6伝播から6新S5（1 WIN / 5 LOSS）。旧2無根拠WINを除外して36新行を加えたexact cacheは5734（WIN156 / LOSS5578、conflict0）。S4 LOSS31 / WIN268 / UNKNOWN3085。secured117/119、remaining100/108、minimum1 = rational dual1。reply27とemptyはUNKNOWN、第一目標のLOSS certificateは未完成。

新raw input/output/logを保存し、再利用したS6 raw140キーをbyte-identical保全。独立determinant/D4 verifierは完全上位certificate146 S6 leaves、全6871 edges・全3384 S4/S5境界、canonicality、coverageを再構成した。geometry監査と上位論理を独立に確認したが、exact葉の再帰的minimaxはC++ solver信頼のまま。全探索木の独立certificateとは区別する。

次の未dispatch scheduleは `(1297036692683751424,16)`、108子中9 LOSS / 99 UNKNOWN、coverage26/28/100/108。打切り加算proxy約549.79M nodesは完了上界ではない。再開時に最新main/cache/raw/registry/S6/S7を更新監査する。

統合検証: polarity/geometry/quarantine regression5件、boundary regression58件、frontier recovery6件が成功。knowledge checks、最終artifact inventory、main再fetchとpushはこの記録に続けて確認する。

統合確認を完了した。`uv sync --locked`、knowledge check（367 items、0 errors/warnings）、knowledge unittest33件、knowledge build、生成物をstage後の再buildと `git diff --exit-code -- README.md research/knowledge/generated` が成功。既知空盤n4 LOSS / n5 WIN回帰も成功。最初のknowledge checkはinventory内のrepo-relative verifierパス表記で停止し、正しいroot-relativeパスへ訂正して再実行した。373-file inventoryはmissing/mismatch0で、Git indexのblob SHA-256も全件一致することを確認した。outputの -text属性で原raw bytesを保持する。既存のoriginal-claimsのinvalid escape SyntaxWarningは表示されたが、check/test/buildは成功。最後のfetchでもorigin/mainは52239697で一致した。直接mainへのcommit/pushとremote照合は、この完成済み検証結果の後に実施する。
