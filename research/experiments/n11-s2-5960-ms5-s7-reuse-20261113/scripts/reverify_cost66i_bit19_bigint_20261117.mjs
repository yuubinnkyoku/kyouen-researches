#!/usr/bin/env node
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const HERE = dirname(fileURLToPath(import.meta.url));
const EXP = resolve(HERE, "..");
const OUT = join(EXP, "output");
const CERT_DIR = join(OUT, "class2-lane-cost66i-certificates");
const MANIFEST_PATH = join(OUT, "class2-lane-cost66i-win7-certificates-20261116.json");
const README_PATH = join(CERT_DIR, "README-split-bit19.md");
const VERIFIER_PATH = join(HERE, "verify_win7_certificate_bigint_independent.mjs");
const PINS = {
  manifest: "8a85ecef573bb6234b2ee1d9f7cb747926bd26ca",
  readme: "aa6edc6acff4234d18ee3ee6838e7852f05e4c3a",
  verifier: "62b5d9413daafb172f6e10249976ee6808f7b454",
  part1: "e8f083cd357ce03aaf177f8ee40c868450e11a37",
  part2: "53efcd57fbda21c8f5976987a23f55dbd4cad993"
};

function fail(message) { throw new Error(message); }
function check(condition, message) { if (!condition) fail(message); }
function hash(algorithm, bytes) { return createHash(algorithm).update(bytes).digest("hex"); }
function gitBlobSha(bytes) {
  return hash("sha1", Buffer.concat([Buffer.from(`blob ${bytes.length}\0`, "utf8"), bytes]));
}
function pinnedFile(path, expected, label) {
  const bytes = readFileSync(path);
  const actual = gitBlobSha(bytes);
  check(actual === expected, `${label} git blob SHA mismatch: ${actual} != ${expected}`);
  return bytes;
}

const manifestBytes = pinnedFile(MANIFEST_PATH, PINS.manifest, "manifest");
const readmeBytes = pinnedFile(README_PATH, PINS.readme, "README-split");
pinnedFile(VERIFIER_PATH, PINS.verifier, "BigInt verifier");
const manifest = JSON.parse(manifestBytes.toString("utf8"));
const entry = manifest.certificates.find((x) => x.bit === 19);
check(entry, "bit19 manifest entry missing");
check(entry.verdict === "WIN7" && entry.depth === 10, "unexpected verdict/depth");
check(entry.root === "00000000000000801226000000080000", "unexpected raw root");
check(entry.d4_canon_root === entry.root, "unexpected D4 canonical root");
check(entry.rows === 40935 && entry.loser_mobility === 52, "unexpected rows/mobility");
check(entry.subroots === 52 && entry.subroots_pass === 52, "manifest subroot count mismatch");
check(entry.fbt_drops === 0 && entry.fatal === null, "incomplete extraction metadata");
check(entry.union_missing === 0 && entry.union_extra === 0, "manifest union mismatch");

const part1Path = join(CERT_DIR, `${entry.file}.part1of2`);
const part2Path = join(CERT_DIR, `${entry.file}.part2of2`);
const part1 = pinnedFile(part1Path, PINS.part1, "certificate part1");
const part2 = pinnedFile(part2Path, PINS.part2, "certificate part2");
check(part1.length === 739395 && part2.length === 739348, "split part byte lengths mismatch");
check(part1[part1.length - 1] === 0x0a, "part1 does not end on a line boundary");
const readme = readmeBytes.toString("utf8");
check(readme.includes("739,395 bytes") && readme.includes("739,348 bytes"), "README split sizes mismatch");
const joined = Buffer.concat([part1, part2]);
check(joined.length === 1478743, "joined certificate byte length mismatch");
const joinedMd5 = hash("md5", joined);
const joinedSha256 = hash("sha256", joined);
check(joinedMd5 === entry.md5, `joined MD5 mismatch: ${joinedMd5}`);
check(joinedSha256 === entry.sha256, `joined SHA-256 mismatch: ${joinedSha256}`);

const tempDir = mkdtempSync(join(tmpdir(), "n11-cost66i-bit19-"));
let verification;
try {
  const tempCert = join(tempDir, "bit19.cert");
  writeFileSync(tempCert, joined);
  const run = spawnSync(process.execPath, [VERIFIER_PATH, tempCert, String(entry.loser_mobility)], {
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024
  });
  if (run.error) throw run.error;
  check(run.status === 0, `BigInt verifier failed (${run.status}): ${run.stderr}`);
  verification = JSON.parse(run.stdout);
} finally {
  rmSync(tempDir, { recursive: true, force: true });
}
check(verification.verdict === "WIN7 certificate independently verified", "BigInt verifier verdict mismatch");
check(verification.root_hex === entry.root && verification.root_stones === 7 && verification.root_safe === true, "BigInt root check mismatch");
check(verification.root_mobility === 52 && verification.subroots_passed === 52, "BigInt mobility/subroot mismatch");
check(verification.strategy_rows === 40935 && verification.rows_sorted_unique === true, "BigInt strategy row mismatch");
check(verification.consumed_winner_rows === 40935 && verification.union_missing === 0 && verification.union_extra === 0, "BigInt strategy union mismatch");
check(verification.terminal_range[0] >= 13 && verification.terminal_range[1] <= 17, "BigInt terminal range mismatch");

const result = {
  schema: "n11-class2-lane-cost66i-bit19-bigint-independent-reverification-20261117-v1",
  date: "2026-11-17",
  certificate: {
    bit: 19,
    root: entry.root,
    d4_canon_root: entry.d4_canon_root,
    verdict: entry.verdict,
    depth: entry.depth,
    rows: entry.rows,
    loser_mobility: entry.loser_mobility,
    extraction_nodes: entry.extraction_nodes
  },
  publication: {
    part1_bytes: part1.length,
    part1_git_blob_sha: PINS.part1,
    part2_bytes: part2.length,
    part2_git_blob_sha: PINS.part2,
    joined_bytes: joined.length,
    joined_md5: joinedMd5,
    joined_sha256: joinedSha256,
    manifest_md5_match: true,
    manifest_sha256_match: true,
    split_boundary_line_aligned: true
  },
  verifier: {
    implementation: "pinned verify_win7_certificate_bigint_independent.mjs; exact BigInt 3x3 cofactor expansion; no floating point, solver, or verdict-cache import",
    verifier_git_blob_sha: PINS.verifier,
    ...verification
  },
  interpretation_guard: "This verifies only the individual seven-stone root. It creates no new engine verdict, applies no receipt fold, and closes no S5 parent. Recompute all cost66i receipt marginals against the canonical head 1473 before folding. The standard 11x11 empty board and requested two-stone roots/classes remain UNKNOWN."
};
process.stdout.write(JSON.stringify(result, null, 2) + "\n");
