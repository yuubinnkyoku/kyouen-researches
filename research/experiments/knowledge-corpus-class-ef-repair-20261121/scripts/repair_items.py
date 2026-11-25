#!/usr/bin/env python3
"""Knowledge corpus class-E/F/D repair (validate 509 -> 1 deferred error).

Formalized reproduction script for the repair executed on 2026-11-21
(research/experiments/knowledge-corpus-class-ef-repair-20261121/).

Usage:
  python3 repair_items.py <mirror_root> <fix_table_out.json>

<mirror_root> must contain:
  research/knowledge/items/*.md        (pre-repair items, base commit
                                        49ad0dbc0a13b77995913584d48986fc14163ae4,
                                        with items/K1183 already at HEAD
                                        d173632fc19a3d9f9abf8e66d0595f4629748bf0)
  research/knowledge/VOCABULARY.yaml  (base commit 49ad0dbc)
  research/knowledge/SCHEMA.md        (base commit 49ad0dbc)
  tools/knowledge/common.py           (base commit 49ad0dbc)

Everything this script writes (items + VOCABULARY.yaml + SCHEMA.md +
tools/knowledge/common.py + the fix table) is a deterministic function of
those inputs; no timestamps, no environment values, no network.

Edits all item fronts in place per the tables below and records every
transform in the fix table JSON (raw_edits / rewrites / role_rewrites /
config_edits).
"""
import glob
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from yamlmin import parse_frontmatter

FENCE_RE = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", re.S)

log = {"raw_edits": [], "role_rewrites": 0, "rewrites": [], "asserts": [],
       "config_edits": []}


def apply_config_edit(path, old, new, expected_count, ident):
    raw = path.read_text(encoding="utf-8")
    n = raw.count(old)
    if n != expected_count:
        raise SystemExit(f"{ident}: pattern count {n} != {expected_count} for {old[:60]!r}")
    path.write_text(raw.replace(old, new), encoding="utf-8")
    log["config_edits"].append({"id": ident, "file": path.name,
                                "old": old, "new": new, "count": n})
    return n


CONFIG_EDITS = [
    # VOCABULARY.yaml: relations += related (class F relation-type vocabulary)
    ("VOCABULARY", "relations: [depends_on, supports, proves, refutes, verifies,"
     " generalizes, supersedes, extends]",
     "relations: [depends_on, supports, proves, refutes, verifies,"
     " generalizes, supersedes, extends, related]"),
    # VOCABULARY.yaml: topics += frontier-bookkeeping (unknown-topic class E)
    ("VOCABULARY", "statistics, search-methods, provenance, migration, multiplayer]",
     "statistics, search-methods, provenance, migration, multiplayer, frontier-bookkeeping]"),
    # VOCABULARY.yaml: verification_methods += machine-audit (solution.verification class E)
    ("VOCABULARY", "lean-soundness, reported-streaming-dp]",
     "lean-soundness, reported-streaming-dp, machine-audit]"),
    # SCHEMA.md: date/created/tags are optional metadata fields
    ("SCHEMA", "本文には命題・対象範囲・現在の根拠・限界を記す。`scope` と `evidence` は任意の文字列。",
     "本文には命題・対象範囲・現在の根拠・限界を記す。`scope` と `evidence` は任意の文字列。"
     "作成日の `date`/`created` と自由形式ラベルの `tags` も任意のメタ資料として許容する"
     "（検査は通すが生成表には使わない）。"),
    # SCHEMA.md: relation table rows for extends (in-corpus usage) and related (new vocabulary)
    ("SCHEMA", "| supersedes | 置き換える知識 → 置き換えられる異なる旧知識 |",
     "| supersedes | 置き換える知識 → 置き換えられる異なる旧知識 |\n"
     "| extends | 拡張する知識 → 拡張される先行知識 |\n"
     "| related | 非依存的な関連・対照（依存・支持・検証を意味せず、noteで関係内容を説明する） |"),
    # tools/knowledge/common.py: allowed front-matter fields += date/created/tags
    ("common", '"scope", "evidence", "solution", "_path", "_body"}',
     '"scope", "evidence", "solution", "date", "created", "tags", "_path", "_body"}'),
]


def config_edits(root):
    targets = {
        "VOCABULARY": root / "research/knowledge/VOCABULARY.yaml",
        "SCHEMA": root / "research/knowledge/SCHEMA.md",
        "common": root / "tools/knowledge/common.py",
    }
    for ident, old, new in CONFIG_EDITS:
        apply_config_edit(targets[ident], old, new, 1, ident)

# ---------------------------------------------------------------- role map
ROLE_MAP = {
    "record": "log",
    "audit": "data",
    "document": "source",
    "declaration": "log",
    "generator": "source",
    "reconstruction": "source",
    "verifier-output": "data",
    "note": "log",
    "evidence": "source",
    "code": "source",
    "machine": "verifier",
    "census": "data",
    "erratum": "log",
}

# ---------------------------------------------------------------- raw edits
RAW_EDITS = [
    # status
    ("K0568", "status: closed", "status: proved", 1),
    # kind: experiment -> verification (28 items, all status verified)
    *[(k, "kind: experiment", "kind: verification", 1) for k in [
        "K1105", "K1106", "K1107", "K1108", "K1109", "K1110", "K1111", "K1113",
        "K1114", "K1115", "K1116", "K1117", "K1118", "K1119", "K1120", "K1121",
        "K1122", "K1123", "K1124", "K1125", "K1128", "K1129", "K1130", "K1132",
        "K1133", "K1136", "K1137", "K1139"]],
    # topics singles
    ("K1072", "topics: [residual-coverage]",
     "topics: [frontier-bookkeeping, verification, certificates]", 1),
    ("K1073", "topics: [coverage, receipts, verification]",
     "topics: [frontier-bookkeeping, certificates, verification]", 1),
    ("K1088", "topics: [search-methods, certificates, geometry, planning]",
     "topics: [search-methods, certificates, geometry]", 1),
    ("K1196", "topics: [rectangles, variants, counting]",
     "topics: [rectangles, variants, maximal-safe]", 1),
    # relation types
    ("K1081", "- type: uses", "- type: depends_on", 1),
    ("K1196", "- type: uses", "- type: related", 1),
    ("K1096", "- type: see_also", "- type: related", 1),
    ("K1106", "- type: relates_to", "- type: related", 1),
    ("K0954", "- type: connects", "- type: related", 1),
    ("K0956", "- type: connects", "- type: related", 1),
    ("K0958", "- type: connects", "- type: related", 1),
    ("K0959", "- type: connects", "- type: related", 2),
    # K1181 path repoint (script lives at experiment root, not scripts/)
    ("K1181",
     "path: research/experiments/n11-win8-receipt-source-record-census-20261121/scripts/win8_receipt_source_record_census.py",
     "path: research/experiments/n11-win8-receipt-source-record-census-20261121/win8_receipt_source_record_census.py", 1),
]

# K1033: expand the scripts/ directory artifact into its 5 concrete drivers.
K1033_OLD = """- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/
  role: source
  note: extract/verify/fold/sweep-audit/cover-re-solve の5 driver。入力は Git blob SHA-1 で pin"""
K1033_NEW = """- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/extract_resid_win7_root_20261119.mjs
  role: source
  note: "WIN7証明書抽出driver（入力は Git blob SHA-1 で pin）"
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/verify_resid_win7_root_20261119.mjs
  role: source
  note: "抽出証明書検証driver（入力は Git blob SHA-1 で pin）"
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/fold_second_third_win7_receipts_20261119.mjs
  role: source
  note: "第2・第3WIN7 receipt fold driver（入力は Git blob SHA-1 で pin）"
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/audit_residual_48root_sweep_20261119.mjs
  role: source
  note: "48root depth-10 sweep監査driver（入力は Git blob SHA-1 で pin）"
- path: research/experiments/n11-head1410-residual-48-root-sweep-two-win-receipts-20261119/scripts/audit_refuted_excluded_cover_resolve_20261119.mjs
  role: source
  note: "REFUTED除外後cover再解決監査driver（入力は Git blob SHA-1 で pin）\""""

# K1160: expand fresh-runs/ directory artifact into its 4 concrete JSONLs.
K1160_OLD = """- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/
  role: data
  note: "第三検証者のfresh再実行4本（runA same-cwd・runB isolated-cwd-home・runC hashseed-random・runD hashseed-0・各132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）\""""
K1160_NEW = """- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/runA-same-cwd/probe-records-reexec-passA.jsonl
  role: data
  note: "第三検証者fresh再実行runA（same-cwd・132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/runB-isolated-cwd-home/probe-records-reexec-passB.jsonl
  role: data
  note: "第三検証者fresh再実行runB（隔離cwd/HOME・132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/runC-same-cwd-hashseed-random/probe-records-reexec-passA.jsonl
  role: data
  note: "第三検証者fresh再実行runC（PYTHONHASHSEED=random・132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）"
- path: research/experiments/n11-residual72-verdict-sweeps-reexec-third-verification-20261120/fresh-runs/runD-same-cwd-hashseed-0/probe-records-reexec-passA.jsonl
  role: data
  note: "第三検証者fresh再実行runD（PYTHONHASHSEED=0・132 probe）のrun JSONL（wall_s含む・byteはタイミング依存で正本はassemble監査）\""""

# K1088: add role+note to its 4 bare artifact entries.
K1088_OLD = """artifacts:
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/README.md
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/scripts/safe8_refuted16_refsolve_20261120.py
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json
- path: research/log/2026-11-20-n11-residual72-safe8-refuted16-refsolve.md"""
K1088_NEW = """artifacts:
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/README.md
  role: source
  note: "実験README（目的・K1085 census正本5fdd342d…とK1086掃引正本3045e152…のfail-closed SHA-256 pin入力・手法の独立再導入・結果・解釈規約。probe・証明書抽出・receipt foldは行わず計画簿記のみの記録と明記）"
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/scripts/safe8_refuted16_refsolve_20261120.py
  role: verifier
  note: "REFUTED-D10 16根除外後の代替被覆根再選定機（stdlibのみ・universe82/coverage/demand/greedy計画のK1085実験機と独立な再導入・全16 gate fail-closed）"
- path: research/experiments/n11-residual72-safe8-refuted16-refsolve-20261120/output/safe8-refuted16-refsolve-20261120.json
  role: data
  note: "再解決正本（除外16根リスト・pool_P_size 120,458・代替被覆根選定の計画簿記）"
- path: research/log/2026-11-20-n11-residual72-safe8-refuted16-refsolve.md
  role: log
  note: "実行記録（宣言ノートcommit 9cf2f8d5の下の幾何・組合せ計画簿記・行の閉鎖claimなし・11×11空盤等はUNKNOWNのままの明記）\""""

BLOCK_EDITS = [("K1033", K1033_OLD, K1033_NEW, 1),
               ("K1160", K1160_OLD, K1160_NEW, 1),
               ("K1088", K1088_OLD, K1088_NEW, 1)]

# ---------------------------------------------------------------- helpers
ROOT = None  # set in main()


def find_item(ident):
    hits = sorted(glob.glob(str(ROOT / "research/knowledge/items" / f"{ident}-*.md")))
    if len(hits) != 1:
        raise SystemExit(f"item {ident}: expected 1 file, got {hits}")
    return Path(hits[0])

# ---------------------------------------------------------------- compact rewrites
PIN_CORE = "K0937 committed 版と byte 同一（監査PIN照合用）"
D = {  # per-item artifact notes: path-suffix -> (role, note)
 "K0926": {
   "report.md": ("proof", "K0919実験E6の有限観察「プラトー S(C,r) は r>=C で一定」を補題CAS（零石カスケード）と正準状態K_C合流により全称証明する実験レポート（定理E6U）"),
   "verify_plateau_universality.py": ("verifier", "補題CASと定理E6Uの機械検証器（stdlibのみ・決定的・--no-cacheで全再計算・r=2..40×C=1..r-1全数で違反0）"),
   "plateau_universality_audit.json": ("data", "監査正本（sha256 ef83446f…・4,748 bytes・pure ASCII・二重実行でbyte同一）"),
 },
 "K0928": {
   "report.md": ("proof", "補題P（pot定式化）・s+pot=C不変量・補題E/O・定理PAR（パリティ）・定理RED（U/V縮約）の全称証明レポート（K0859計数再帰・一様盤・零リセット）"),
   "verify_pc_twin_laws.py": ("verifier", "10チェック（PIN/REF/TWIN/STRE/STRO/RED/RECON/LAW等）の機械照合器（stdlibのみ・決定的）"),
   "pc_twin_laws_audit.json": ("data", "監査正本（全チェックOK・コールド実行間でbyte同一・sha256 6bc2ee08…）"),
   "pc_p8000.json": ("data", "P(C) C=1..8000 の完全センサス（sha256 58a414bc…）"),
   "pc_uv8000.json": ("data", "U(m)/V(m) m=1..8000 の完全センサス（sha256 8a3b318b…）"),
   "pc_fast.js": ("solver", "閉形式フェーズによる直接評価エンジン（2実装交差の一方）"),
   "pc_reduced.js": ("solver", "縮約ゲーム上の独立実装エンジン（別データ構造による交差の他方）"),
 },
 "K0929": {
   "report.md": ("proof", "LAW1/LAW2・V予想/U予想の特徴付けレポート（実験時点は予想として記述・K0939により全称定理化、本文冒頭に昇格記録あり）"),
   "verify_pc_twin_laws.py": ("verifier", "twin lawsの有限機械照合器（PIN/REF/TWIN/STRE/STRO/RED/RECON/LAW等10チェック・stdlibのみ・決定的）"),
   "pc_twin_laws_audit.json": ("data", "監査正本（全チェックOK・コールド実行間でbyte同一・sha256 6bc2ee08…）"),
   "pc_p8000.json": ("data", "LAW1照合用の P(C) C=1..8000 完全センサス（sha256 58a414bc…）"),
   "pc_uv8000.json": ("data", "V予想/U予想照合用の U(m)/V(m) m=1..8000 完全センサス（sha256 8a3b318b…）"),
   "pc_fast.js": ("solver", "閉形式フェーズによる直接評価エンジン（LAW1/LAW2掃引に使用）"),
   "pc_reduced.js": ("solver", "縮約ゲーム上の独立実装エンジン（twin law評価の交差对照）"),
 },
 "K0931": {
   "report.md": ("proof", "STR2-V/U（U/Vのstretch-2構造定理）・SIEVE3-V/U・LAW1/2のmod-6解決・LAD-h0（h=0ラダー）の全称証明レポート"),
   "sieve_test.py": ("verifier", "SIEVE構造の有限機械テスト（m<=8000・監視ラベルの死亡時点が理論と一致することのpins mode照合）"),
   "theorem_verify.py": ("verifier", "STR2定理の機械アンカー（m=4..1000・敗者系列・保持石数の完全一致照合）"),
   "ladder_verify.py": ("verifier", "LAD-h0ラダーの機械アンカー（w=2,h=0,n<=1000 と w=3,4,5列・終circle・pot・生存者整合の厳密照合）"),
   "w3_explore.py": ("verifier", "W3/H3/G3 stretch-3終状態形状の決定的探索器"),
   "audit_build.py": ("verifier", "3検証器を再実行して監査を組み立てるアセンブラ（SIEVE/STR2/LADDER/W3EXPLOREの4チェック）"),
   "uv_stretch_ladder_audit.json": ("data", "監査正本（4チェック all_ok true・2回コールド実行でbyte同一）"),
   "w3_explore.json": ("data", "stretch-3終状態形状の決定的探索データ（n mod 4分類）"),
 },
 "K0933": {
   "report.md": ("proof", "U/V縮約ゲームのstretch-3構造・重量4ファミリーのstretch-4構造・SIEVE5-U/V・spf∈{3,5}类のmod-30双子法則解決の全称証明レポート"),
   "sieve5_verify.py": ("verifier", "SIEVE5・stretch構造定理の機械検証器（stdlib Python・決定的・タイムスタンプなし）"),
   "audit_build.py": ("verifier", "検証器再実行と監査アセンブラ（2回コールド実行でbyte同一）"),
   "sieve5_uv_audit.json": ("data", "監査正本（sha256 2c1917e0…・2回コールド実行byte同一）"),
 },
 "K0934": {
   "report.md": ("proof", "LAD-GEN（制限ラダーF(w,h;n)の第一stretch-w完全法則）の全称証明レポート（K0931のopen class h>=2・1<=r<hを含む全クラス）"),
   "ladder_gen_verify.py": ("verifier", "K0928フェーズ規則シミュレータ上のLAD-GEN機械検証器"),
   "audit_build.py": ("verifier", "監査アセンブラ（2実行一致で監査正本を生成）"),
   "ladder_gen_audit.json": ("data", "決定性監査正本（all_ok true・タイムスタンプなし・ソート済みキー）"),
 },
 "K0935": {
   "report.md": ("proof", "WATCH-MAP（生存監視位置の次ラダー状態への写像の事例分類 (a)-(e)）の全称証明レポート"),
   "watchmap_verify.py": ("verifier", "LAD-GEN core（シミュレータ+閉形式）をverbatimコピーしたWATCH-MAP機械検証器"),
   "audit_build.py": ("verifier", "監査アセンブラ"),
   "watchmap_audit.json": ("data", "決定性監査正本（all_ok true・fail_count 0・実行同一）"),
 },
 "K0936": {
   "report.md": ("proof", "SIEVE7-U/V（stretch-5/6監視追跡の組成・spf=7）の全称証明レポート（32行クラステーブル・双子法則のmod 210全解決）"),
   "sieve7_verify.py": ("verifier", "LAD-GEN core verbatimコピー上のSIEVE7機械検証器（32行クラステーブル全照合）"),
   "audit_build.py": ("verifier", "監査アセンブラ"),
   "sieve7_uv_audit.json": ("data", "決定性監査正本（32行テーブル全文同梱・sha256つき）"),
 },
 "K0937": {
   "report.md": ("proof", "INV-TRACK（監視距離不変量）・死亡合同式・t=1へのWATCH-MAP拡張と限界特定・SIEVE-COMPOSITE-GEN・双子法則のmod 210制限除去の全称証明レポート"),
   "sievegen_core.py": ("solver", "track_gen/play_full等の共有コア（K0934-K0936検証器からverbatim・以降の実験群でpinned byte同一コピーとして参照される）"),
   "sievegen_verify.py": ("verifier", "12チェックの機械アンカー（全前提を検証）"),
   "audit_build.py": ("verifier", "監査アセンブラ（2回in-process実行一致・2回コールド実行でbyte同一）"),
   "sievegen_audit.json": ("data", "監査正本（file sha256 5281e92e…・12チェック表）"),
 },
 "K0939": {
   "report.md": ("proof", "END-SIEVE（t=0エンドゲームの約数篩）とSIEVE-PRIME全称証明・双子法則の全称完結レポート"),
   "sievegen_core.py": ("solver", "K0937実験ディレクトリ committed版のbyte同一コピー（track_gen・play_full・ピン読み込みをそのまま使用）"),
   "sieveprime_verify.py": ("verifier", "7チェックの機械検証器（すべてstdlib・決定的・PIN検査を含む）"),
   "audit_build.py": ("verifier", "監査アセンブラ（2回コールド実行でbyte同一）"),
   "sieveprime_audit.json": ("data", "監査正本（監査sha256 07d844c6…）"),
 },
 "K0941": {
   "report.md": ("proof", "合成NのV(m)/U(m)完全決定（LADDER-ONLY・死の二分法・E-game閉包・ラベル合成）の全称証明レポート"),
   "sievegen_core.py": ("solver", "K0937のbyte同一コピー（sha256 a69f916c…）"),
   "composite_core.py": ("solver", "定理C/Dのσ再帰コア実装（以降のK0943-K0951実験群でpinned byte同一コピーとして使用される）"),
   "composite_verify.py": ("verifier", "本文全定理の機械的証拠の検証器"),
   "audit_build.py": ("verifier", "監査アセンブラ"),
   "composite_values_audit.json": ("data", "監査正本（sha256 97e854f7…）"),
 },
 "K0943": {
   "report.md": ("proof", "STATE-CF/DS-CF（ladder監視状態と死亡状態のO(1)閉形式）・p^2崩壊定理P2の全称証明レポート（K0941レジューム(i)の完成）"),
   "sievegen_core.py": ("solver", "K0937 committed版のbyte同一コピー（sha256 a69f916c…）"),
   "deathstate_verify.py": ("verifier", "閉形式定理の機械検証器"),
   "audit_build.py": ("verifier", "監査アセンブラ"),
   "deathstate_audit.json": ("data", "監査正本（sha256 9bc8c2f4…・7,514 bytes）"),
 },
 "K0945": {
   "report.md": ("proof", "σ_Z(3,K)のfold分解（RUN-3/FOLD三分法Φ_K）・ONE-CHAR（値1位置特徴付け）・A2-NEVER（K≡2 mod 4 の全称的不存在）の全称証明レポート"),
   "sievegen_core.py": ("solver", "K0937 committed版byte同一コピー（監査PIN照合用）"),
   "composite_core.py": ("solver", "K0941定理C/D σ再帰のpinned byte同一コピー（sha256 3990d67f…）"),
   "sigmaz3_core.py": ("solver", "fold4実装としてのσ_Z(3,K)高速評価コア（K<=4,000でpinned σ_Zと0不一致・予備的にK<=20,000でも0不一致）"),
   "sigmaz3_verify.py": ("verifier", "RUN-3/FOLD/ONE-CHAR/A2-NEVERの機械検証器"),
   "deep_census.py": ("solver", "深いセンサス掃引機（2回実行byte-identical・値1位置台帳の決定的再生成）"),
   "audit_build.py": ("verifier", "監査アセンブラ（PIN/FASTEQ等の監査を出力）"),
   "sigmaz3_audit.json": ("data", "監査正本（2回コールド実行でbyte同一）"),
   "deep_census.json": ("data", "深いセンサスの値1位置台帳（K<=10^5で1,146個すべてK≡0 mod 4・ONE-CHARと91<->91双方向一致）"),
 },
 "K0946": {
   "report.md": ("proof", "σ_Z(M,·)値1軌跡の一般構造（ONE-CHAR全M一般化・除外定理・素数M法則）の全称証明レポート"),
   "sigma_locus_core.js": ("solver", "σ_Z(M,K)分割掃引エンジン（M=1..40,K<=10^5・M∈{2,3,5,7},K<=10^6等のスペクトラム表生成）"),
   "audit_build.py": ("verifier", "監査アセンブラ（COREPIN等の監査群）"),
   "sievegen_core.py": ("solver", "pinned byte同一コピー（sha256 a69f916c…）"),
   "composite_core.py": ("solver", "K0941 pinned coreのbyte同一コピー（sha256 3990d67f…）"),
   "sigma_locus_audit.json": ("data", "監査正本（COREPIN等・all_ok true）"),
 },
 "K0948": {
   "report.md": ("proof", "E(P;n,0)零点の完全分類U0-CLASSIFYとU0-NEVER解決・系群の全称証明レポート"),
   "audit_build.py": ("verifier", "監査アセンブラ（all_ok true・cold 2回実行byte同一）"),
   "composite_core.py": ("solver", "pinned byte同一コピー（sha256 3990d67f…）"),
   "sievegen_core.py": ("solver", "pinned byte同一コピー（sha256 a69f916c…）"),
   "u0_audit.json": ("data", "監査正本（監査sha256 d1a83169…）"),
 },
 "K0949": {
   "report.md": ("proof", "RELAY-REDUCE（E状態リレー還元）・σ_Z値1軌跡の純算術還元（約数・spf）・PRIME-M/PARITYの全称証明レポート"),
   "audit_build.py": ("verifier", "監査アセンブラ（all_ok true・cold 2回実行byte同一）"),
   "composite_core.py": ("solver", "pinned byte同一コピー（sha256 3990d67f…）"),
   "sievegen_core.py": ("solver", "pinned byte同一コピー（sha256 a69f916c…）"),
   "relay_audit.json": ("data", "監査正本（監査sha256 c92cb52f…）"),
 },
 "K0950": {
   "report.md": ("proof", "HIT-ARITH/PAIR-2/PAIR-3（σ_Z値1軌跡の素数対への完全還元）とP-KILL剰余法則の全称証明レポート"),
   "hitpair_core.py": ("solver", "HIT-ARITH直接実装コア（素数対軌跡の評価）"),
   "audit_build.py": ("verifier", "監査アセンブラ（pinned coresの入力ピン照合を含む・all_ok true）"),
   "composite_core.py": ("solver", "pinned byte同一コピー（sha256 3990d67f…・入力ピン: K0949 relay_audit / K0945 deep_census）"),
   "sievegen_core.py": ("solver", "pinned byte同一コピー（sha256 a69f916c…）"),
   "hitpair_audit.json": ("data", "監査正本（all_ok true）"),
   "pkill_tight_sweep.py": ("solver", "κクラスtight掃引スイープ（tier1..5の掃引台帳生成器）"),
   "pkill_tight_deep.py": ("solver", "深域tight掃引機（打ち切り2クラスdeep probe）"),
   "kappa_density.py": ("solver", "κ密度スイープの生成器"),
   "pkill_class_probe.py": ("solver", "単一クラス深部プローブ（HIT-ARITH直接実装・(1367,682)/(1741,648)の初回ヒット特定）"),
   "pkill_tight_tier1_slim.json": ("data", "tight掃引tier1台帳（F(M)確定に使用・決定的再生成可能）"),
   "pkill_tight_tier2.json": ("data", "tight掃引tier2台帳"),
   "pkill_tight_tier3.json": ("data", "tight掃引tier3台帳"),
   "pkill_tight_tier4_slim.json": ("data", "tight掃引tier4台帳（slim）"),
   "pkill_tight_tier5_slim.json": ("data", "tight掃引tier5台帳（slim）"),
   "kappa_density_slim.json": ("data", "κ密度スイープ台帳（slim）"),
   "sparse_classes_le2.json": ("data", "初回ヒット<=2×10^5のsparse κクラス台帳"),
   "pkill_probe_deep.json": ("data", "打ち切り2クラスの深部プローブ台帳（初回ヒットK=215,458/220,140）"),
   "firsthit_growth.py": ("solver", "FIRSTHIT-GROWTH（初回ヒット増大則）定量評価スイープの生成器"),
   "firsthit_growth.json": ("data", "初回ヒット増大則の定量評価台帳"),
 },
 "K0951": {
   "report.md": ("proof", "FOLD-GEN（一般bump-foldフレーム(1,c,k,kTop)のO(1)三分法）・RUNG-1/2・EXCL-U-MOD5・Uのmod-5 fold力学的篩の全称証明レポート"),
   "foldgen_core.js": ("solver", "CommonJS foldエンジン（純JSサンドボックス転写実行・出版pin検証済みsha256Hex）"),
   "foldgen_verify.js": ("verifier", "純JS検証器（クロスラン再現性はチャンクリストsha ピンE/F/G/H 4本が保証）"),
   "census_extend.js": ("solver", "Uセンサスの2×10^5拡張掃引機"),
   "composite_core.py": ("solver", "K0941定理C/D σ再帰のpinned byte同一コピー"),
   "sievegen_core.py": ("solver", "K0937 committed版byte同一コピー"),
   "fast_census.json": ("data", "U(1..200000)=6,531件のセンサス正本（出版3,658+新規2,873・mod5全体ヒストグラム[2143,1,2216,2171,0]）"),
   "foldgen_audit.json": ("data", "機械的証拠監査バッテリー表（foldgen_grid 428,220事象等）"),
 },
}

REMO_ITEMS = ["K0926", "K0928", "K0929", "K0931", "K0933", "K0934", "K0935", "K0936",
              "K0937", "K0939", "K0941", "K0943", "K0945", "K0946", "K0948", "K0949",
              "K0950", "K0951"]
REMO_TOPICS = ["variants", "multiplayer", "strategy-length"]

K098X = {
 "K0980": {
   "title": "K0980-two-token-z7-y4-boundary",
   "artifacts": [
     ("research/experiments/vertical-fiber-two-token-z7-y4-boundary-20261118/report.md", "proof",
      "固定z=7,y=4・全x>=4,R>=0のGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明"),
     ("research/experiments/vertical-fiber-two-token-z7-y4-boundary-20261118/verify_z7_y4.py", "verifier",
      "直接多重集合再帰とA/B/C再構成（B=K0979・C=K0880アンカー）の照合・署名帯表・K0832 tail定理照合・Theorem T偶奇検査を行う独立有限監査器（2回実行byte-identical必須）"),
   ],
   "relations": [
     ("depends_on", "K0832", "残余ゲームHの定義・A/B/C再帰・Theorem T・単一トークン閉形式・高さだけの縮約・高R tail定理（R>=x+12）を使用する"),
     ("depends_on", "K0979", "B子の評価にz=7,y=3境界切片の全Grundy公式を使用する"),
     ("depends_on", "K0880", "C子の評価にz=6,y=4境界切片の全Grundy公式を使用する"),
     ("supports", "K0976", "z=7のy>=4候補式の全称証明（S=x+y強帰納）に必要な境界切片のうちy=4を供給する"),
   ],
   "topics": ["grundy", "residual-games"],
 },
 "K0981": {
   "title": "K0981-two-token-z7-y5-boundary",
   "artifacts": [
     ("research/experiments/vertical-fiber-two-token-z7-y5-boundary-20261118/report.md", "proof",
      "固定z=7,y=5・全x>=5,R>=0のGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明"),
     ("research/experiments/vertical-fiber-two-token-z7-y5-boundary-20261118/verify_z7_y5.py", "verifier",
      "直接多重集合再帰とA/B/C再構成（B=K0980・C=K0884アンカー）の照合・署名帯表・K0832 tail定理照合・Theorem T偶奇検査を行う独立有限監査器（2回実行byte-identical必須）"),
   ],
   "relations": [
     ("depends_on", "K0832", "残余ゲームHの定義・A/B/C再帰・Theorem T・単一トークン閉形式・高さだけの縮約・高R tail定理（R>=x+13）を使用する"),
     ("depends_on", "K0980", "B子の評価にz=7,y=4境界切片の全Grundy公式を使用する"),
     ("depends_on", "K0884", "C子の評価にz=6,y=5境界切片の全Grundy公式を使用する"),
     ("supports", "K0976", "z=7のy>=4候補式の全称証明に必要な境界切片のうちy=5を供給する"),
   ],
   "topics": ["grundy", "residual-games"],
 },
 "K0982": {
   "title": "K0982-two-token-z7-y6-boundary",
   "artifacts": [
     ("research/experiments/vertical-fiber-two-token-z7-y6-boundary-20261118/report.md", "proof",
      "固定z=7,y=6・全x>=6,R>=0のGrundy値0/1/2をA/B/C選択肢署名表とR強帰納で分類する全称証明"),
     ("research/experiments/vertical-fiber-two-token-z7-y6-boundary-20261118/verify_z7_y6.py", "verifier",
      "直接多重集合再帰とA/B/C再構成（B=K0981・C=K0885アンカー）の照合・署名帯表・K0832 tail定理照合・Theorem T偶奇検査を行う独立有限監査器（2回実行byte-identical必須）"),
   ],
   "relations": [
     ("depends_on", "K0832", "残余ゲームHの定義・A/B/C再帰・Theorem T・単一トークン閉形式・高さだけの縮約・高R tail定理（R>=x+14）を使用する"),
     ("depends_on", "K0981", "B子の評価にz=7,y=5境界切片の全Grundy公式を使用する"),
     ("depends_on", "K0885", "C子の評価にz=6,y=6境界切片の全Grundy公式を使用する"),
     ("supports", "K0976", "z=7のy>=4候補式の全称証明に必要な境界切片のうちy=6を供給する"),
   ],
   "topics": ["grundy", "residual-games"],
 },
}

def yq(s):
    assert '"' not in s and "\\" not in s, f"quote hazard: {s!r}"
    return '"' + s + '"'

def fmt_art(path, role, note):
    return f"- path: {path}\n  role: {role}\n  note: {yq(note)}\n"

def rel_block(entries, with_note=True):
    out = ""
    for e in entries:
        if with_note and len(e) == 3:
            t, tgt, note = e
            out += f"- type: {t}\n  target: {tgt}\n  note: {yq(note)}\n"
        else:
            t, tgt = e[:2]
            out += f"- type: {t}\n  target: {tgt}\n"
    return out

def rewrite_remo(ident):
    p = find_item(ident)
    raw = p.read_text(encoding="utf-8")
    m = FENCE_RE.fullmatch(raw)
    fm, body = m.group(1), m.group(2)
    d = parse_frontmatter(fm)
    title_line = next(l for l in fm.splitlines() if l.startswith("title:"))
    date_line = next((l for l in fm.splitlines() if l.startswith("date:")), "")
    tags_line = next((l for l in fm.splitlines() if l.startswith("tags:")), "")
    status = d["status"]
    assert status in ("proved", "mixed"), (ident, status)
    # relations expansion
    rels = d["relations"]
    assert isinstance(rels, list) and all(isinstance(r, dict) and len(r) == 1 for r in rels), ident
    entries = []
    for r in rels:
        (k, targets), = r.items()
        for tgt in targets:
            t = "depends_on" if k == "depends_on" else ("related" if k == "connects" else None)
            if t is None:
                raise SystemExit(f"{ident}: unexpected relation key {k}")
            entries.append((t, tgt))
    arts = d["artifacts"]
    notes = D[ident]
    art_fm = ""
    for a in arts:
        suffix = a.split("/")[-1]
        if suffix not in notes:
            raise SystemExit(f"{ident}: no note rule for {a}")
        role, note = notes[suffix]
        art_fm += fmt_art(a, role, note)
    new_fm = "---\n"
    new_fm += f"id: {d['id']}\n"
    new_fm += title_line + "\n"
    new_fm += f"kind: proposition\n"
    new_fm += f"status: {status if status != 'mixed' else 'proved'}\n"
    new_fm += "topics: [" + ", ".join(REMO_TOPICS) + "]\n"
    new_fm += "aliases: []\n"
    new_fm += "relations:\n" + rel_block(entries)
    new_fm += "artifacts:\n" + art_fm
    for extra in (date_line, tags_line):
        if extra:
            new_fm += extra + "\n"
    new_fm += "---\n"
    p.write_text(new_fm + body, encoding="utf-8")
    log["rewrites"].append({"id": ident, "relations": len(entries), "artifacts": len(arts),
                            "status": status, "note_rules": len(notes)})

def rewrite_k098x(ident):
    spec = K098X[ident]
    p = find_item(ident)
    raw = p.read_text(encoding="utf-8")
    m = FENCE_RE.fullmatch(raw)
    fm, body = m.group(1), m.group(2)
    d = parse_frontmatter(fm)
    created_line = next((l for l in fm.splitlines() if l.startswith("created:")), "")
    tags_line = next((l for l in fm.splitlines() if l.startswith("tags:")), "")
    new_fm = "---\n"
    new_fm += f"id: {d['id']}\n"
    new_fm += next(l for l in fm.splitlines() if l.startswith("title:")) + "\n"
    new_fm += "kind: proposition\nstatus: proved\n"
    new_fm += "topics: [" + ", ".join(spec["topics"]) + "]\n"
    new_fm += "aliases: []\n"
    new_fm += "relations:\n" + rel_block(spec["relations"])
    new_fm += "artifacts:\n"
    for path, role, note in spec["artifacts"]:
        new_fm += fmt_art(path, role, note)
    for extra in (created_line, tags_line):
        if extra:
            new_fm += extra + "\n"
    new_fm += "---\n"
    p.write_text(new_fm + body, encoding="utf-8")
    log["rewrites"].append({"id": ident, "relations": len(spec["relations"]),
                            "artifacts": len(spec["artifacts"]), "kind": "theorem->proposition",
                            "dropped_next": True})

def main():
    global ROOT
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        raise SystemExit(__doc__)
    ROOT = Path(sys.argv[1])
    out_table = Path(sys.argv[2]) if len(sys.argv) == 3 else Path("fix-table.json")
    # 0) config trio edits (VOCABULARY.yaml / SCHEMA.md / tools/knowledge/common.py)
    config_edits(ROOT)
    # 1) compact rewrites
    for ident in REMO_ITEMS:
        rewrite_remo(ident)
    for ident in ("K0980", "K0981", "K0982"):
        rewrite_k098x(ident)

    # 2) raw edits
    for ident, old, new, expected in RAW_EDITS:
        p = find_item(ident)
        raw = p.read_text(encoding="utf-8")
        n = raw.count(old)
        if n != expected:
            raise SystemExit(f"{ident}: pattern count {n} != {expected} for {old[:60]!r}")
        p.write_text(raw.replace(old, new), encoding="utf-8")
        log["raw_edits"].append({"id": ident, "old": old, "new": new, "count": n})

    # 3) block edits
    for ident, old, new, expected in BLOCK_EDITS:
        p = find_item(ident)
        raw = p.read_text(encoding="utf-8")
        if raw.count(old) != expected:
            raise SystemExit(f"block edit {ident}: count mismatch")
        p.write_text(raw.replace(old, new), encoding="utf-8")
        log["raw_edits"].append({"id": ident, "old": old[:80], "new": new[:80] + "…", "count": expected,
                                 "block": True})

    # 4) global invalid-role mapping
    pat = re.compile(r"^(\s*)role: (" + "|".join(ROLE_MAP) + r")\s*$", re.M)
    total = 0
    per_file = {}
    for fn in sorted(glob.glob(str(ROOT / "research/knowledge/items" / "*.md"))):
        p = Path(fn)
        raw = p.read_text(encoding="utf-8")
        new, n = pat.subn(lambda m: f"{m.group(1)}role: {ROLE_MAP[m.group(2)]}", raw)
        if n:
            p.write_text(new, encoding="utf-8")
            per_file[p.name.split("-")[0]] = n
            total += n
    log["role_rewrites"] = {"total": total, "per_file_counts": per_file}
    if total != 96:
        raise SystemExit(f"role rewrite total {total} != 96")

    out_table.write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
    print("rewrites:", len(log["rewrites"]), "raw_edits:", len(log["raw_edits"]), "role total:", total, "config_edits:", len(log["config_edits"]))

if __name__ == "__main__":
    main()
