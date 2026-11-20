#!/usr/bin/env python3
"""assemble_win8_audit_root208090020004.py — fail-closed audit machine for the WIN8 root
00000000000020809002000480100000 certificate extraction (residual-48 lane, 2026-11-20).

Role. This machine is the THIRD independent exact verification of the published
certificate (after the TS BigInt 3x3-cofactor verifier and the TS Bareiss 4x4
verifier, both published in this experiment directory), plus the bookkeeping gates
that tie the certificate to its published inputs. It imports no engine, no solver
and no verifier from this repository: the only imports are Python stdlib.

Third method. A full-tree traversal from the root (loser to move): every legal
first move m of the root player is a sub-root (9 stones, winner to move); from
each sub-root, every winner state must find its strategy row, the recorded move
must be legal, every loser state expands ALL legal replies, terminals must be
loser-stuck positions (no legal move at a loser-to-move depth), loser states must
not carry strategy rows, and the union of consumed winner states must equal the
certificate row set exactly (both directions). All geometry uses an exact integer
4x4 Bareiss determinant on the lifted rows [x^2+y^2, x, y, 1] (stdlib ints only).

Determinism. No randomness, no clock in the output, no network. The audit JSON is
written with sort_keys=True and no wall-clock fields, so repeated runs in any cwd
must produce byte-identical output.

Inputs (all inside the experiment directory unless overridden by env):
  certs/win8-root-00000000000020809002000480100000-20261120.n11   certificate
  output/.input-k1119-log.md      K1119 published research log (the sole published
                                  probe record carrier for this fresh-probe root;
                                  SHA-256 and git blob pinned)
  output/.input-k1097.json        K1097 refsolve master (SHA-256 pinned; footprint)
  output/.input-fold18.json       fold18 receipt-fold master (SHA-256 pinned; the
                                  residual_row_hex_after list = residual 45 rows)
  output/probe-repro-both-orderings.jsonl  runner v17 fresh-probe records (4 probes)
  output/root-legal-moves.txt     root loser first-move list (comma CSV, one line)
  output/ext-summary-a1.jsonl     extraction run A1 per-move summaries (chunked, cwd A)
  output/ext-summary-a2.jsonl     extraction run A2 per-move summaries (repeat of A1)
  output/ext-summary-b.jsonl      extraction run B summary (single process, cwd B)
  runner_v17.ts                   runner v17 fixed copy (git blob pinned)
  output/bigint-verification.json 1st independent verifier result
  output/bareiss-root-check.json  2nd independent verifier root check
  output/bareiss-stats.txt        2nd independent verifier batch stats lines
Environment overrides: K1119_LOG, K1097_JSON, FOLD18_JSON, CERT, PROBE_REPRO,
MOVES, SUMMARY_A1, SUMMARY_A2, SUMMARY_B, RUNNER, BIGINT_JSON, BAREISS_RC,
BAREISS_STATS.

Fresh-probe protocol (THIS ROOT ONLY). The published K1091/K1095 sweep
masters carry no per-root probe record for this root (it is a K1089
replacement16 candidate), so the probe pins are the values published in the
K1119 research log (total 793,616, uncapped loss=true in both AND orderings)
and reproduced here node-exact by runner v17 (cap 4,000,000, pilot_d6 control
3,402, four probes: two per AND ordering). This is the first WIN8-D10
certificate extraction executed on the fresh-probe basis.

Interpretation guard (fail-closed into the audit JSON):
  this certificate proves only the game tree of the named 8-stone root; the
  coverage/fold semantics for the S6 parent rows are a separate undertaking;
  REFUTED-D10 facts and node counts are not win/loss readings; and the standard
  11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes
  1/2/4 all remain UNKNOWN.
"""
import hashlib
import json
import os
import re
import sys

ROOT_HEX = "00000000000020809002000480100000"
CERT_RELPATH = "certs/win8-root-00000000000020809002000480100000-20261120.n11"
HEADER = "n11-terminal-strategy-v1 original_first_WIN8 second_to_move_LOSS"
K1119_LOG_SHA256 = "4d11ca896815b73e4e0616a07c81f7abc582d4f5401174462d63e3abd27a4472"
K1119_LOG_BLOB = "51bad3fac4c36fcd1cbf6aeec01b7e153d9adb89"
K1119_TOTAL = 793616
RUNNER_BLOB = "c132cc6425eee3feaeef1d697dd74f968cfedb59"
K1097_SHA256 = "2896deb0c5e820904d0e2463e3fd9ebd1613b540a66a97f88d86c75bffa71f40"
FOLD18_SHA256 = "18b543c45c98c22297fd31b8060971aa90e92826f494acb27ad94ce869250026"
FRESH_PROBE_NODES = {"andclose1": 350792, "andclose0": 442824}
ROOT_BIT = 20
PILOT_NODES = 3402
EXPERIMENT_NAME = "n11-residual48-win8-cert-extract-root208090020004-20261120"
GUARD = [
    "this certificate proves only the game tree of the named 8-stone root",
    "the 8-stone receipt cover/fold semantics for the S6 parent rows are a separate undertaking",
    "loss=false (uncapped) is a REFUTED-D10 probe fact and NOT a LOSS proof of any earlier position",
    "node counts and solved counts are not win/loss readings",
    "the standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN",
]

gates = []


def gate(name, passed, detail=None):
    gates.append({"gate": name, "passed": bool(passed),
                  **({"detail": detail} if detail is not None else {})})
    return bool(passed)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1_file(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def exp_path(arg_default):
    env_name = arg_default[0]
    default = arg_default[1]
    return os.environ.get(env_name) or os.path.join(EXPROOT, default)


EXPROOT = os.environ.get("EXPERIMENT_ROOT", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def lifted(b):
    x, y = b % 11, b // 11
    return (x * x + y * y, x, y, 1)


def det4_bareiss(p0, p1, p2, p3):
    a = [list(lifted(q)) for q in (p0, p1, p2, p3)]
    sign, prev = 1, 1
    for k in range(3):
        if a[k][k] == 0:
            for j in range(k + 1, 4):
                if a[j][k] != 0:
                    a[k], a[j] = a[j], a[k]
                    sign = -sign
                    break
            else:
                return 0
        pivot = a[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                v = a[i][j] * pivot - a[i][k] * a[k][j]
                if v % prev != 0:
                    raise ValueError("non-integral Bareiss step")
                a[i][j] = v // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[3][3]


_triple_mask_cache = {}


def triple_mask(a, b, c):
    key = (a, b, c)
    m = _triple_mask_cache.get(key)
    if m is not None:
        return m
    # expansion coefficients of the lifted 3x3 matrix along the 4th row
    rows = [lifted(q) for q in (a, b, c)]
    coeff = []
    for col in range(4):
        minor = [[rows[r][cc] for cc in range(4) if cc != col] for r in range(3)]
        d3 = (minor[0][0] * (minor[1][1] * minor[2][2] - minor[1][2] * minor[2][1])
              - minor[0][1] * (minor[1][0] * minor[2][2] - minor[1][2] * minor[2][0])
              + minor[0][2] * (minor[1][0] * minor[2][1] - minor[1][1] * minor[2][0]))
        coeff.append(d3 if col % 2 == 0 else -d3)
    mask = 0
    for d in range(121):
        if d == a or d == b or d == c:
            continue
        r = lifted(d)
        v = coeff[0] * r[0] + coeff[1] * r[1] + coeff[2] * r[2] + coeff[3] * r[3]
        if v == 0:
            mask |= 1 << d
    _triple_mask_cache[key] = mask
    return mask


FULL = (1 << 121) - 1


def points_of(mask):
    out = []
    i = 0
    while mask:
        low = mask & -mask
        # bit index of lowest set bit
        b = low.bit_length() - 1
        out.append(b)
        mask ^= low
        i += 1
    return out


def legal_of_points(pts):
    banned = 0
    for p in pts:
        banned |= 1 << p
    n = len(pts)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                banned |= triple_mask(pts[i], pts[j], pts[k])
    return FULL & ~banned


def main():
    global EXPROOT
    argv = sys.argv[1:]
    out_path = None
    for i, a in enumerate(argv):
        if a == "--out" and i + 1 < len(argv):
            out_path = argv[i + 1]
        if a == "--experiment-root" and i + 1 < len(argv):
            EXPROOT = argv[i + 1]

    cert_path = exp_path(("CERT", CERT_RELPATH))
    k1119log_path = exp_path(("K1119_LOG", "output/.input-k1119-log.md"))
    k1097_path = exp_path(("K1097_JSON", "output/.input-k1097.json"))
    fold18_path = exp_path(("FOLD18_JSON", "output/.input-fold18.json"))
    repro_path = exp_path(("PROBE_REPRO", "output/probe-repro-both-orderings.jsonl"))
    moves_path = exp_path(("MOVES", "output/root-legal-moves.txt"))
    sa1 = exp_path(("SUMMARY_A1", "output/ext-summary-a1.jsonl"))
    sa2 = exp_path(("SUMMARY_A2", "output/ext-summary-a2.jsonl"))
    sb = exp_path(("SUMMARY_B", "output/ext-summary-b.jsonl"))
    runner_path = exp_path(("RUNNER", "runner_v17.ts"))
    bigint_path = exp_path(("BIGINT_JSON", "output/bigint-verification.json"))
    brc_path = exp_path(("BAREISS_RC", "output/bareiss-root-check.json"))
    bstats_path = exp_path(("BAREISS_STATS", "output/bareiss-stats.txt"))

    recorded = {}

    # ---------- G1: K1119 published log pin ----------
    k1119log_sha = sha256_file(k1119log_path)
    k1119log_blob = git_blob_sha1_file(k1119log_path)
    gate("g01_k1119_log_sha256_pin",
         k1119log_sha == K1119_LOG_SHA256 and k1119log_blob == K1119_LOG_BLOB,
         {"sha256": k1119log_sha, "git_blob": k1119log_blob})
    k1119log_text = open(k1119log_path, encoding="utf-8").read()
    ws = re.sub(r"\s+", "", k1119log_text)
    total_str = "{:,}".format(K1119_TOTAL)
    g02_ok = ((ROOT_HEX + "`（" + total_str + "）") in ws
              and "全7根両AND順序uncappedloss=true" in ws)
    gate("g02_k1119_log_root_probe_total_published", g02_ok,
         {"published_total": K1119_TOTAL, "root_hex_in_log": ROOT_HEX in k1119log_text,
          "uncapped_loss_true_statement_in_log": "全7根両AND順序uncappedloss=true" in ws})

    # ---------- G3: runner fixed copy blob ----------
    runner_blob = git_blob_sha1_file(runner_path)
    gate("g03_runner_v17_copy_git_blob", runner_blob == RUNNER_BLOB, runner_blob)

    # ---------- G4/G5: root shape and mobility (own arithmetic) ----------
    root = int(ROOT_HEX, 16)
    root_pts = points_of(root)
    root8 = len(root_pts) == 8
    quad_free = True
    n8 = len(root_pts)
    for i in range(n8):
        for j in range(i + 1, n8):
            for k in range(j + 1, n8):
                for q in range(k + 1, n8):
                    if det4_bareiss(root_pts[i], root_pts[j], root_pts[k], root_pts[q]) == 0:
                        quad_free = False
    root_legal_mask = legal_of_points(root_pts)
    root_moves = points_of(root_legal_mask)
    gate("g04_root_shape_safe", root8 and quad_free,
         {"stones": len(root_pts), "quadruple_free": quad_free})
    gate("g05_root_mobility_54", len(root_moves) == 54, len(root_moves))

    # K1097 per-root footprint: claimed rows (fresh-probe basis: the K1097
    # refsolve master is the only published claimed-coverage carrier for this root)
    k1097 = json.load(open(k1097_path))
    fp = k1097["win16_intrinsic_footprints"][ROOT_HEX]
    covered = fp["claimed"]
    gate("g06_fresh_probe_constants_match_k1119_total",
         sum(FRESH_PROBE_NODES.values()) == K1119_TOTAL,
         {"andclose1": FRESH_PROBE_NODES["andclose1"],
          "andclose0": FRESH_PROBE_NODES["andclose0"], "sum": K1119_TOTAL})
    gate("g07_k1097_root_claimed_coverage_3rows",
         fp["intrinsic_equals_claimed"] is True and len(covered) == 3
         and fp["intrinsic"] == covered and fp["claimed"] == covered, covered)
    recorded["k1097_claimed_coverage_rows"] = covered

    # ---------- G8: probe reproduction records ----------
    repro_lines = [json.loads(l) for l in open(repro_path) if l.strip()]
    probes_seen = {"andclose1": [], "andclose0": []}
    pilots = 0
    for r in repro_lines:
        if r.get("control") == "pilot_d6":
            pilots += 1
            if not (r["loss"] is False and r["nodes"] == PILOT_NODES and r["capped"] is False):
                pilots = -10
        elif "bit" in r:
            probes_seen["andclose1" if r["andclose"] else "andclose0"].append(r)
    # expectation: each AND ordering reproduced at least twice (node-exact), 4 pilot controls total
    repro_ok = pilots == 4
    for k, nodes in FRESH_PROBE_NODES.items():
        got = probes_seen[k]
        if len(got) < 2:
            repro_ok = False
            continue
        for r in got:
            if not (r["bit"] == ROOT_BIT and r["loss"] is True and r["capped"] is False
                    and r["nodes"] == nodes and r["terminalStoneRange"] == [14, 18]):
                repro_ok = False
    repro_ok = repro_ok and (sum(FRESH_PROBE_NODES.values()) == K1119_TOTAL)
    gate("g08_probe_reproduction_matches_k1119_total", repro_ok,
         {"pilot_d6": pilots, "reproduced": {k: len(v) for k, v in probes_seen.items()}})

    # ---------- G9: root legal move list file vs machine re-derivation ----------
    moves_file = [int(x) for x in open(moves_path).read().strip().split(",")]
    gate("g09_root_move_list_equals_rederivation", moves_file == root_moves,
         {"file": len(moves_file), "rederived": len(root_moves)})

    # ---------- G10: extraction summaries ----------
    def read_summaries(path):
        out = {}
        for l in open(path):
            if not l.strip():
                continue
            s = json.loads(l)
            mv = int(s["moves"])
            pm = s["perMove"][str(mv)]
            out[mv] = (pm["ok"], pm["capped"], pm["nodes"], tuple(pm["terminalRange"]),
                       s["fbt_drops"], s["fbt_fallbacks"], bool(s.get("fatal")),
                       bool(s.get("conflicts")))
        return out

    s1 = read_summaries(sa1)
    s2 = read_summaries(sa2)
    summ_ok = (
        sorted(s1) == root_moves and sorted(s2) == root_moves
        and all(v[0] and not v[1] and v[4] == 0 and not v[6] and not v[7] for v in s1.values())
        and all(v[0] and not v[1] and v[4] == 0 and not v[6] and not v[7] for v in s2.values()))
    gate("g10_extraction_runs_a1_a2_clean", summ_ok,
         {"a1_moves": len(s1), "a2_moves": len(s2)})
    a1_eq_a2 = all(s1[m] == s2[m] for m in s1)
    gate("g11_a1_a2_per_move_node_exact_repeat", a1_eq_a2,
         {"identical_moves": sum(1 for m in s1 if s1[m] == s2.get(m))})
    sb_obj = None
    bl = [json.loads(l) for l in open(sb) if l.strip()]
    if len(bl) == 1:
        sb_obj = bl[0]
    b_clean = (sb_obj is not None
               and all(v["ok"] is True and v["capped"] is False for v in sb_obj["perMove"].values())
               and sb_obj["fbt_drops"] == 0 and not sb_obj.get("fatal")
               and not sb_obj.get("conflicts")
               and sorted(int(m) for m in sb_obj["perMove"].keys()) == root_moves
               and sb_obj["moves"] == ",".join(str(m) for m in root_moves))
    gate("g12_extraction_run_b_single_process_clean", b_clean,
         {"b_moves": len(sb_obj["perMove"]) if sb_obj else 0})
    sum_a1_nodes = sum(v[2] for v in s1.values())
    sum_b_nodes = sb_obj["sum"] if sb_obj else -1
    gate("g13_node_accounting_chunk_vs_single",
         sum_b_nodes is not None and sum_b_nodes > 0 and sum_b_nodes <= sum_a1_nodes,
         {"a1_chunk_total_nodes": sum_a1_nodes, "b_single_process_nodes": sum_b_nodes})
    recorded["extraction_nodes"] = {"run_a1_chunked": sum_a1_nodes,
                                    "run_b_single_process": sum_b_nodes}

    # ---------- G14: certificate format ----------
    raw = open(cert_path, "rb").read()
    cert_sha = hashlib.sha256(raw).hexdigest()
    text = raw.decode("ascii")
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    fmt_ok = (lines[0] == HEADER and lines[1] == "root " + ROOT_HEX)
    prev = ""
    n_rows = 0
    strat = {}
    row_re = re.compile(r"^([0-9a-f]{32}) (\d{1,3})$")
    for ln in lines[2:]:
        m = row_re.match(ln)
        if not m:
            fmt_ok = False
            break
        k = m.group(1)
        mv = int(m.group(2))
        if k <= prev or mv >= 121 or (int(k, 16) >> mv) & 1:
            fmt_ok = False
            break
        prev = k
        strat[k] = mv
        n_rows += 1
    ends_nl = raw.endswith(b"\n")
    gate("g14_certificate_format_sorted_unique",
         fmt_ok and ends_nl and n_rows == strat.__len__(),
         {"rows": n_rows, "bytes": len(raw), "sha256": cert_sha})
    recorded["certificate"] = {"sha256": cert_sha, "bytes": len(raw), "rows": n_rows}
    gate("g15_run_b_rowcount_matches_certificate",
         sb_obj is not None and sb_obj["nRows"] == n_rows,
         {"cert": n_rows, "b_nRows": sb_obj["nRows"] if sb_obj else None})

    # ---------- G16: THIRD-METHOD full-tree traversal ----------
    consumed = set()
    visited = 0
    winner_states = 0
    loser_states = 0
    terminal_count = 0
    loser_reply_edges = 0
    seen_all = 0
    min_term, max_term = 99, 0
    traversal_fail = None
    boards_cache = {}

    for m in sorted(root_moves):
        v0 = root | (1 << m)
        stack = [(v0, 0)]
        seen = set()
        while stack:
            board, depth = stack.pop()
            hxp = format(board, "032x")
            if hxp in seen:
                continue
            seen.add(hxp)
            seen_all += 1
            pts = points_of(board)
            options = legal_of_points(pts)
            if options == 0:
                if depth % 2 != 1:
                    traversal_fail = "winner stuck at " + hxp
                    break
                if hxp in strat:
                    traversal_fail = "terminal has strategy row " + hxp
                    break
                terminal_count += 1
                if len(pts) < min_term:
                    min_term = len(pts)
                if len(pts) > max_term:
                    max_term = len(pts)
                continue
            if depth % 2 == 0:
                winner_states += 1
                if hxp not in strat:
                    traversal_fail = "missing winner strategy row " + hxp
                    break
                mv = strat[hxp]
                if not (options >> mv) & 1:
                    traversal_fail = "illegal strategy move at " + hxp
                    break
                consumed.add(hxp)
                stack.append((board | (1 << mv), depth + 1))
            else:
                loser_states += 1
                if hxp in strat:
                    traversal_fail = "strategy provided on loser turn " + hxp
                    break
                opts = options
                while opts:
                    bit = opts & -opts
                    opts ^= bit
                    loser_reply_edges += 1
                    stack.append((board | bit, depth + 1))
        if traversal_fail:
            break
    missing = [k for k in strat if k not in consumed]
    extra = [k for k in consumed if k not in strat]
    third_ok = (traversal_fail is None and not missing and not extra
                and len(consumed) == n_rows)
    gate("g16_third_method_traversal_pass", third_ok,
         {"failure": traversal_fail, "missing": len(missing), "extra": len(extra),
          "visited_states": seen_all, "winner_states": winner_states,
          "loser_states": loser_states, "loser_reply_edges": loser_reply_edges,
          "terminal_count": terminal_count,
          "terminal_range": [min_term if min_term <= 20 else 99,
                             max_term if max_term >= 12 else 0],
          "subroot_mobility": len(root_moves)})
    recorded["third_method"] = {"visited_states": seen_all,
                                "winner_states": winner_states,
                                "loser_states": loser_states,
                                "loser_reply_edges": loser_reply_edges,
                                "terminal_count": terminal_count,
                                "terminal_range": [min_term, max_term],
                                "root_first_moves": len(root_moves)}

    # ---------- G17: aggregate agreement with the two published verifiers ----------
    big = json.load(open(bigint_path))
    bare_stats = {}
    for l in open(bstats_path):
        if not l.strip():
            continue
        r = json.loads(l)
        for k, v in r["stats"].items():
            bare_stats[int(k[1:])] = v
    brc = json.loads(open(brc_path).readline().strip())
    bt_min = min(v["range"][0] for v in bare_stats.values())
    bt_max = max(v["range"][1] for v in bare_stats.values())
    agree = (
        big["strategy_rows"] == n_rows and big["consumed_winner_rows"] == n_rows
        and big["union_missing"] == 0 and big["union_extra"] == 0
        and big["root_stones"] == 8 and big["root_mobility"] == 54
        and big["root_safe"] is True and big["subroots_passed"] == 54
        and big["terminal_range"] == [min_term, max_term]
        and big["winner_states"] == winner_states
        and big["loser_states"] == loser_states
        and big["terminal_count"] == terminal_count
        and big["loser_reply_edges"] == loser_reply_edges
        and big["visited_states_across_subroots"] == seen_all
        and len(bare_stats) == 54
        and sum(v["terminals"] for v in bare_stats.values()) == terminal_count
        and sum(v["opponentEdges"] for v in bare_stats.values()) == loser_reply_edges
        and sum(v["seen"] for v in bare_stats.values()) == seen_all
        and bt_min == min_term and bt_max == max_term
        and brc == {"stones": 8, "loserMobility": 54})
    gate("g17_three_method_aggregate_agreement", agree,
         {"bigint_terminal_count": big["terminal_count"],
          "third_method_terminal_count": terminal_count,
          "bareiss_subroots": len(bare_stats)})
    gate("g18_interpretation_guard_present", len(GUARD) == 5 and GUARD[4].endswith("all remain UNKNOWN"), str(len(GUARD)) + " guard lines")

    # ---------- G19: K1097 footprint + fold18 residual openness ----------
    k1097_sha = sha256_file(k1097_path)
    fold18_sha = sha256_file(fold18_path)
    fold18 = json.load(open(fold18_path))
    residual = fold18["five_parent_target_after"]["residual_row_hex_after"]
    fp_ok = (k1097_sha == K1097_SHA256
             and fold18_sha == FOLD18_SHA256
             and len(residual) == 45
             and fp["intrinsic_equals_claimed"] is True
             and fp["claimed"] == covered
             and fp["intrinsic"] == fp["claimed"]
             and len(fp["claimed"]) == 3
             and all(row in residual for row in covered))
    gate("g19_k1097_footprint_and_fold18_residual_open", fp_ok,
         {"k1097_sha256": k1097_sha, "fold18_sha256": fold18_sha,
          "claimed": fp["claimed"], "residual_rows": len(residual),
          "claimed_rows_open_in_residual": sum(1 for row in covered if row in residual)})
    recorded["k1097_footprint_rows"] = fp["claimed"]
    recorded["fold18_residual_open_check"] = {
        "residual_row_count": len(residual),
        "claimed_rows_present": [row in residual for row in covered]}

    all_pass = all(g["passed"] for g in gates)
    audit = {
        "root": ROOT_HEX,
        "experiment": EXPERIMENT_NAME,
        "schema": "win8-cert-extract-verification-v1",
        "verdict": "WIN8 root certificate triple-verified (extraction self-check + "
                   "BigInt 3x3 cofactor + Bareiss 4x4 + python third-method); "
                   "all gates PASS" if all_pass else "GATE FAILURE",
        "all_gates_pass": all_pass,
        "gate_count": len(gates),
        "gates": gates,
        "recorded": recorded,
        "guard": GUARD,
        "pinned_inputs": {
            "k1119_log_sha256": k1119log_sha,
            "k1119_log_git_blob": k1119log_blob,
            "k1097_json_sha256": k1097_sha,
            "fold18_json_sha256": fold18_sha,
            "runner_v17_git_blob": runner_blob,
            "certificate_sha256": cert_sha,
        },
    }
    payload = json.dumps(audit, sort_keys=True, indent=1, ensure_ascii=False) + "\n"
    if out_path:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w") as f:
            f.write(payload)
    sys.stdout.write(payload if not out_path else json.dumps(
        {"all_gates_pass": all_pass, "gate_count": len(gates),
         "out": out_path}, sort_keys=True) + "\n")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
