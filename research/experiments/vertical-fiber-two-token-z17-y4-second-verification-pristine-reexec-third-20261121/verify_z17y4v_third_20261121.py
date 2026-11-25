#!/usr/bin/env python3
"""Third verification (pristine re-execution) of the published K1079 second
verification of the K1076 two-token z=17, y=4 boundary slice.

Subject experiment (published, frozen):
  research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120/
  pin commit 2339957f76a548e75b23e9b73b3d5b4b172084f6 (single-commit publication
  of the experiment dir, the research log, and the K1079 knowledge item).

Fixed verification target of the subject: the K1076 verifier
  research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120/verify_z17_y4.py
  at commit 412d75b93d14752f528c4fa4c6b5d472a4ca5ac8, whose closed-form block
  ("def odd" .. "expected_signature" final "    return None") is spliced verbatim
  into both subject scripts.

Stages: pin / recon / rerun / tampers / finalize.
Stdlib only. Fail-closed: the audit JSON is written only if every gate passes;
any failure aborts with a non-zero exit and writes nothing.
The audit JSON is byte-deterministic: no timestamps, no absolute paths, no
volatile values. All pinned fetches use raw.githubusercontent.com commit-pinned
URLs only (no api.github.com). Declaration note (single-owner basis for this
battery): commit d6858a93679f5ce914f123505702dd4dde760731 published at
2026-11-21T07:02Z with declaration-time HEAD c1a2a333ea8a18263195ec79e111681643f9d7c4.
"""
from __future__ import annotations
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
import urllib.request

RAW = "https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches"
PIN_COMMIT = "2339957f76a548e75b23e9b73b3d5b4b172084f6"
K1076_COMMIT = "412d75b93d14752f528c4fa4c6b5d472a4ca5ac8"
REF_A = "c1a2a333ea8a18263195ec79e111681643f9d7c4"      # declaration-time HEAD
REF_B = "d6858a93679f5ce914f123505702dd4dde760731"      # declaration note commit
EXP = "research/experiments/vertical-fiber-two-token-z17-y4-second-verification-20261120"
BOUND = "research/experiments/vertical-fiber-two-token-z17-y4-boundary-20261120"
LOG = "research/log/2026-11-20-vertical-fiber-two-token-z17-y4-second-verification.md"
ITEM = "research/knowledge/items/K1079-two-token-z17-y4-second-verification.md"
DECNOTE = "research/log/2026-11-21-vertical-fiber-z17-y4-second-verification-pristine-reexec-third-single-owner-note.md"
NOTE_SHA = "e420f3fbd10777b73e4bf9e16e1d6a31f94ad5800b780559176c13979da601f4"

EXP_FILES = {
    "report.md": ("12a937dca24eef339a2fe06bc617e8971242fe8e5bf64060666dda3fe52f9159", 7326),
    "verify_z17_y4_second.py": ("83002a3b3911a86fab240d622bdff69c218d188320e801a857af7f2336d7eb9a", 19036),
    "census_z17_y4_second.py": ("5f84ccbdacae4495dc0bf46bf9be25cbfdcc6224628f60e1842a63051cdb3704", 9806),
    "output/audit.json": ("bfc2fb341d9c566afbc84bc218a3e895f7f91a3c4a744b1277ab6a24661ff043", 1183),
    "output/census.txt": ("48bde24ae8d4583da6b2dd17e9ffb638fb5c8eeab58104d3bf197ee9d2126348", 6801),
}
K1076_SHA, K1076_SIZE = "a7878b8e40d116b6e5d25a6f94562a5584b8bc0374375868a1e4555a0f205d98", 11517
K1076_BLOB = "911dc4bfb707081f4c354a32ae2bd4fbe7a79a66"
BLOCK_SHA, BLOCK_SIZE = "73435e45844749abccea98706df60146652dbb7e6d5a2a2a7a9104da505a4cf4", 6677

T1_OFF, T1_ORIG = 2257, 0x39   # verify: g17y3 "odd(r, 1, 19)" -> '9'
T2_OFF, T2_ORIG = 11908, 0x30  # verify: cand_pred x==5 "r>=10" -> '0'
T3_OFF, T3_ORIG = 3918, 0x31   # census: in_parent_P x==5 "r >= 10" -> '1'
T1_LAST = "AssertionError: (14, 19, 0)"
T2_LAST = "AssertionError: (5, 10)"
CENSUS_STDOUT_PASS = b"checks=2961 mismatch=0 status=PASS\n"

ROOT = Path(__file__).resolve().parent
WORK = ROOT / "W"
GATES = []

def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def git_blob_sha1(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()

def fetch(ref: str, path: str) -> bytes:
    url = "%s/%s/%s" % (RAW, ref, path)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read()
        except Exception:
            if attempt == 2:
                raise
    raise AssertionError("unreachable")

def gate(stage: str, name: str, ok: bool, detail: str = "") -> None:
    if not ok:
        raise SystemExit("GATE FAILED [%s/%s] %s" % (stage, name, detail))
    GATES.append({"stage": stage, "gate": name})

def expect_sha(stage: str, name: str, data: bytes, sha: str, size: int) -> None:
    gate(stage, name, sha256(data) == sha and len(data) == size,
         "len=%d sha=%s" % (len(data), sha256(data)))

def short(fname: str) -> str:
    return fname.split("/")[-1].replace(".py", "").replace(".", "_")

def stage_pin() -> dict:
    out = {}
    for fname, (sha, size) in EXP_FILES.items():
        pin_b = fetch(PIN_COMMIT, "%s/%s" % (EXP, fname))
        head_b = fetch(REF_A, "%s/%s" % (EXP, fname))
        expect_sha("pin", "p_%s_pin" % short(fname), pin_b, sha, size)
        expect_sha("pin", "p_%s_head" % short(fname), head_b, sha, size)
        gate("pin", "p_%s_bytepinhead" % short(fname), pin_b == head_b)
        out[fname] = pin_b
    for label, path, sha, size in (
        ("log", LOG, "8e12b4c194b2fc07d9fc5b155dfcf00edc184a763c6c0166aebfacb2e8320fdc", 7684),
        ("item", ITEM, "bcd35800262f123476928add1baa358bcbfba3d4ee5cbf86bf92cbb1012dba37", 7368),
    ):
        pin_b = fetch(PIN_COMMIT, path)
        head_b = fetch(REF_A, path)
        decl_b = fetch(REF_B, path)
        expect_sha("pin", "p_%s_pin" % label, pin_b, sha, size)
        expect_sha("pin", "p_%s_head" % label, head_b, sha, size)
        expect_sha("pin", "p_%s_decl" % label, decl_b, sha, size)
        gate("pin", "p_%s_pinheadequal" % label, pin_b == head_b == decl_b)
    note_b = fetch(REF_B, DECNOTE)
    expect_sha("pin", "p_declnote_decl", note_b, NOTE_SHA, 7600)
    return out

def extract_k1076_block(data: bytes) -> bytes:
    text = data.decode("utf-8")
    start = text.index("def odd(r:")
    anchor = "@lru_cache(maxsize=None)\ndef raw_recursive"
    end = text.index(anchor)
    blk = text[:end][start:]
    blk = blk[:-1]  # strip the one trailing blank-newline before the anchor
    return blk.encode("utf-8")

def splice_of(data: bytes) -> bytes:
    text = data.decode("utf-8")
    a = text.index("# ============ PUBLISHED K1076 CLOSED FORMS")
    a = text.index("\n", a) + 1
    b = text.index("# ============ END PUBLISHED K1076 BLOCK")
    return text[a:b].encode("utf-8")

def stage_recon(subject: dict) -> None:
    k_fixed = fetch(K1076_COMMIT, "%s/verify_z17_y4.py" % BOUND)
    k_head = fetch(REF_A, "%s/verify_z17_y4.py" % BOUND)
    k_decl = fetch(REF_B, "%s/verify_z17_y4.py" % BOUND)
    expect_sha("recon", "r_k1076_fixedref", k_fixed, K1076_SHA, K1076_SIZE)
    gate("recon", "r_k1076_headref", k_fixed == k_head)
    gate("recon", "r_k1076_declref", k_fixed == k_decl)
    gate("recon", "r_k1076_blob", git_blob_sha1(k_fixed) == K1076_BLOB,
         "blob=%s" % git_blob_sha1(k_fixed))
    block = extract_k1076_block(k_fixed)
    expect_sha("recon", "r_k1076_block", block, BLOCK_SHA, BLOCK_SIZE)
    gate("recon", "r_splice_verify", splice_of(subject["verify_z17_y4_second.py"]) == block)
    gate("recon", "r_splice_census", splice_of(subject["census_z17_y4_second.py"]) == block)

def run_sub(script: str, cwd: Path, env: dict | None, timeout: int = 900):
    if env is None:
        return subprocess.run([sys.executable, script], cwd=str(cwd),
                              capture_output=True, timeout=timeout)
    return subprocess.run([sys.executable, script], cwd=str(cwd),
                          capture_output=True, timeout=timeout, env=env)

def stage_rerun(subject: dict) -> dict:
    if WORK.exists():
        shutil.rmtree(WORK)
    results = {}
    verify_b = subject["verify_z17_y4_second.py"]
    census_b = subject["census_z17_y4_second.py"]
    expect_sha("recon", "w_verify_assembled", verify_b, EXP_FILES["verify_z17_y4_second.py"][0],
               EXP_FILES["verify_z17_y4_second.py"][1])
    expect_sha("recon", "w_census_assembled", census_b, EXP_FILES["census_z17_y4_second.py"][0],
               EXP_FILES["census_z17_y4_second.py"][1])
    audit_sha = EXP_FILES["output/audit.json"][0]
    cen_sha = EXP_FILES["output/census.txt"][0]
    iso_env_a = {"PATH": os.environ.get("PATH", "/usr/local/bin:/usr/bin:/bin"),
                 "HOME": str(WORK / "iso_home_a"), "TMPDIR": str(WORK / "iso_tmp_a")}
    iso_env_b = dict(iso_env_a)
    iso_env_b["HOME"] = str(WORK / "iso_home_b")
    iso_env_b["TMPDIR"] = str(WORK / "iso_tmp_b")
    iso_env_b["PYTHONHASHSEED"] = "random"
    for d in ("iso_home_a", "iso_tmp_a", "iso_home_b", "iso_tmp_b"):
        (WORK / d).mkdir(parents=True, exist_ok=True)
    # --- verifier: r1/r2 same cwd (one shared dir, two runs), r3/r4 isolated ---
    shared = WORK / "runs_shared"
    shutil.rmtree(shared, ignore_errors=True)
    shared.mkdir(parents=True)
    (shared / "verify_z17_y4_second.py").write_bytes(verify_b)
    (shared / "census_z17_y4_second.py").write_bytes(census_b)
    audits = []
    for label in ("r1", "r2"):
        r = run_sub("verify_z17_y4_second.py", shared, None)
        gate("rerun", "rerun_%s_rc" % label, r.returncode == 0,
             "rc=%d stderr=%s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-200:]))
        gate("rerun", "rerun_%s_stdout_sha" % label, sha256(r.stdout) == audit_sha,
             "stdout sha=%s" % sha256(r.stdout))
        out = shared / "output" / "audit.json"
        gate("rerun", "rerun_%s_audit_written" % label, out.is_file())
        gate("rerun", "rerun_%s_audit_sha_file" % label, sha256(out.read_bytes()) == audit_sha,
             "file sha=%s" % sha256(out.read_bytes()))
        audits.append(out.read_bytes())
    for label, env in (("r3", iso_env_a), ("r4", iso_env_b)):
        d = WORK / ("iso_" + label)
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        (d / "verify_z17_y4_second.py").write_bytes(verify_b)
        (d / "census_z17_y4_second.py").write_bytes(census_b)
        r = run_sub("verify_z17_y4_second.py", d, env)
        gate("rerun", "rerun_%s_rc" % label, r.returncode == 0,
             "rc=%d stderr=%s" % (r.returncode, r.stderr.decode("utf-8", "replace")[-200:]))
        gate("rerun", "rerun_%s_stdout_sha" % label, sha256(r.stdout) == audit_sha,
             "stdout sha=%s" % sha256(r.stdout))
        out = d / "output" / "audit.json"
        gate("rerun", "rerun_%s_audit_written" % label, out.is_file())
        gate("rerun", "rerun_%s_audit_sha_file" % label, sha256(out.read_bytes()) == audit_sha,
             "file sha=%s" % sha256(out.read_bytes()))
        audits.append(out.read_bytes())
    gate("rerun", "rerun_all4_audit_identical", audits[0] == audits[1] == audits[2] == audits[3])
    # --- census: c1/c2 same cwd, c3/c4 isolated ---
    shared_c = WORK / "runs_census_shared"
    shutil.rmtree(shared_c, ignore_errors=True)
    shared_c.mkdir(parents=True)
    (shared_c / "census_z17_y4_second.py").write_bytes(census_b)
    outs = []
    for label in ("c1", "c2"):
        r = run_sub("census_z17_y4_second.py", shared_c, None)
        gate("rerun", "rerun_%s_rc" % label, r.returncode == 0, "rc=%d" % r.returncode)
        gate("rerun", "rerun_%s_stdout" % label, r.stdout == CENSUS_STDOUT_PASS,
             "stdout=%r" % r.stdout[:80])
        outf = shared_c / "output" / "census.txt"
        gate("rerun", "rerun_%s_written" % label, outf.is_file())
        gate("rerun", "rerun_%s_sha" % label, sha256(outf.read_bytes()) == cen_sha,
             "sha=%s" % sha256(outf.read_bytes()))
        outs.append(outf.read_bytes())
    for label, env in (("c3", iso_env_a), ("c4", iso_env_b)):
        d = WORK / ("iso_" + label)
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        (d / "census_z17_y4_second.py").write_bytes(census_b)
        r = run_sub("census_z17_y4_second.py", d, env)
        gate("rerun", "rerun_%s_rc" % label, r.returncode == 0, "rc=%d" % r.returncode)
        gate("rerun", "rerun_%s_stdout" % label, r.stdout == CENSUS_STDOUT_PASS,
             "stdout=%r" % r.stdout[:80])
        outf = d / "output" / "census.txt"
        gate("rerun", "rerun_%s_written" % label, outf.is_file())
        gate("rerun", "rerun_%s_sha" % label, sha256(outf.read_bytes()) == cen_sha,
             "sha=%s" % sha256(outf.read_bytes()))
        outs.append(outf.read_bytes())
    gate("rerun", "rerun_all4_census_identical", outs[0] == outs[1] == outs[2] == outs[3])
    results["verify"] = audits[0]
    results["census"] = outs[0]
    return results

def stage_tampers(subject: dict) -> None:
    verify_b = bytearray(subject["verify_z17_y4_second.py"])
    census_b = bytearray(subject["census_z17_y4_second.py"])
    gate("tampers", "t1_offset_byte", verify_b[T1_OFF] == T1_ORIG)
    gate("tampers", "t2_offset_byte", verify_b[T2_OFF] == T2_ORIG)
    gate("tampers", "t3_offset_byte", census_b[T3_OFF] == T3_ORIG)

    def probe(tag, data, off, script):
        d = WORK / ("tamper_" + tag)
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)
        probe_b = bytearray(data)
        probe_b[off] ^= 0x01
        files = {"verify_z17_y4_second.py": bytes(verify_b),
                 "census_z17_y4_second.py": bytes(census_b)}
        files[script] = bytes(probe_b)
        for name, content in files.items():
            (d / name).write_bytes(content)
        gate("tampers", "tamper_%s_output_pre_absent" % tag, not (d / "output").exists())
        r = run_sub(script, d, None, timeout=600)
        return d, r

    # t1: published-block side of verify (child anchor engine check)
    d, r = probe("t1", verify_b, T1_OFF, "verify_z17_y4_second.py")
    gate("tampers", "tamper_t1_rc", r.returncode != 0, "rc=%d" % r.returncode)
    last = r.stderr.decode("utf-8", "replace").rstrip("\n").split("\n")[-1]
    gate("tampers", "tamper_t1_stderr_last", last == T1_LAST, "last=%r" % last)
    gate("tampers", "tamper_t1_output_post_absent", not (d / "output").exists())
    # t2: first-derivation oracle side of verify
    d, r = probe("t2", verify_b, T2_OFF, "verify_z17_y4_second.py")
    gate("tampers", "tamper_t2_rc", r.returncode != 0, "rc=%d" % r.returncode)
    last = r.stderr.decode("utf-8", "replace").rstrip("\n").split("\n")[-1]
    gate("tampers", "tamper_t2_stderr_last", last == T2_LAST, "last=%r" % last)
    gate("tampers", "tamper_t2_output_post_absent", not (d / "output").exists())
    # t3: census published-block side (detect-and-record design)
    d, r = probe("t3", census_b, T3_OFF, "census_z17_y4_second.py")
    gate("tampers", "tamper_t3_rc", r.returncode == 0, "rc=%d" % r.returncode)
    out = d / "output" / "census.txt"
    gate("tampers", "tamper_t3_written", out.is_file())
    txt = out.read_text(encoding="utf-8")
    lines = {}
    for l in txt.splitlines():
        if "=" in l and not l.startswith("x="):
            lines[l.split("=")[0]] = l
        if l.startswith("status="):
            # census.txt has two status-free... keep last assignment as authority
            pass
    gate("tampers", "tamper_t3_status_fail",
         any(l == "status=FAIL" for l in txt.splitlines()),
         "status lines=%r" % [l for l in txt.splitlines() if l.startswith("status")])
    gate("tampers", "tamper_t3_mismatch_5",
         any(l == "mismatch_vs_published=5" for l in txt.splitlines()),
         "mismatch lines=%r" % [l for l in txt.splitlines() if l.startswith("mismatch")])
    gate("tampers", "tamper_t3_checks_unchanged",
         any(l == "checks=2961" for l in txt.splitlines()))
    gate("tampers", "tamper_t3_differs_published",
         sha256(out.read_bytes()) != EXP_FILES["output/census.txt"][0])
    # post-tamper pristine re-verification
    expect_sha("tampers", "w_verify_post_tampers", subject["verify_z17_y4_second.py"],
               EXP_FILES["verify_z17_y4_second.py"][0], EXP_FILES["verify_z17_y4_second.py"][1])
    expect_sha("tampers", "w_census_post_tampers", subject["census_z17_y4_second.py"],
               EXP_FILES["census_z17_y4_second.py"][0], EXP_FILES["census_z17_y4_second.py"][1])

def main() -> None:
    subject = stage_pin()
    stage_recon(subject)
    rerun = stage_rerun(subject)
    stage_tampers(subject)
    stages = ["pin", "recon", "rerun", "tampers"]
    counts = {s: sum(1 for g in GATES if g["stage"] == s) for s in stages}
    audit = {
        "schema": "vertical-fiber-z17-y4-second-verification-pristine-reexec-third-20261121-v1",
        "subject": "K1079 second verification of the K1076 z=17 y=4 boundary slice: ext2 pristine re-execution third verification",
        "pin_commit": PIN_COMMIT,
        "k1076_fixed_commit": K1076_COMMIT,
        "ref_a_declaration_head": REF_A,
        "ref_b_declaration_commit": REF_B,
        "gates_total": len(GATES),
        "gates_pin": counts["pin"],
        "gates_recon": counts["recon"],
        "gates_rerun": counts["rerun"],
        "gates_tampers": counts["tampers"],
        "all_gates_pass": True,
        "published_audit_sha256": EXP_FILES["output/audit.json"][0],
        "published_census_sha256": EXP_FILES["output/census.txt"][0],
        "rerun_audit_sha256": sha256(rerun["verify"]),
        "rerun_census_sha256": sha256(rerun["census"]),
        "byte_identical": True,
        "tamper_offsets": {"t1": T1_OFF, "t2": T2_OFF, "t3": T3_OFF},
        "tamper_detection": {
            "t1": "child_anchor_K1067 raw-engine assert, audit not written",
            "t2": "first_derivation_vs_published assert, audit not written",
            "t3": "census detect-and-records status=FAIL mismatch=5, output written",
        },
        "interpretation_guard": [
            "この監査は第三実装・第三実行環境によるK1079第二検証のpristine再実行・tamper検出・監査byte決定性の検査であり、z=17 y=4切片のGrundy分類に関する新しい数学的主張ではない。",
            "有限監査は全称証明の代わりではなく、K1076の全称性は引き続きx外帰納と全R署名帯表による（K1079の位置づけを継承する）。",
            "K1076パッケージのbyte-pin不整合（コミット済み検証器a7878b8e…とコミット済み監査pin 388e1a47…の不一致）の修正はK1076レーン管轄で本レーンの対象外。",
            "本harnessはstdlibのみで構成され、pinned fetchはraw固定commit URLのみでapi.github.comに依存せず、待機pollingは存在しない。",
            "本レーンはn11（標準11×11）の勝敗状態を一切変更しない。",
        ],
        "unknown_guard": "STANDARD 11x11 EMPTY BOARD: UNKNOWN; two-stone roots {49,60}/{59,60}: UNKNOWN; S2 {59,60}: UNKNOWN; class 1/2/4: UNKNOWN. REFUTED-D10 is not a LOSS proof; win bands and witness roots are not certificates.",
        "gate_names": [g["gate"] for g in GATES],
    }
    (Path(__file__).parent / "audit_z17y4v_third.json").write_text(
        json.dumps(audit, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(audit, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
