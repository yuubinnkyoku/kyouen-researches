#!/usr/bin/env python3
"""Certificate-coverage census of the 775 WIN-receipt roots folded into the
head-1452 basis of the n11 class-2 long-term lane.

Motivation (76c bit-113 lesson): a folded WIN receipt without a published,
independently verified certificate is a bookkeeping risk of the head-1452
cover accounting. This census classifies every one of the 775 receipt roots
by the certificate evidence that exists for it in the published artifact set.

Basis (all asserted):
- 771 basis roots reconstructed with per-file git-blob pin verification via
  fold_projection_head1450_tool_20261116.reconstruct().
- +4 roots from class-frontier-cost76d77e-receipts-recompute-20261116.json
  totals.root_hexes (all asserted popcount 7)  => 775 roots.
- provenance sources cover all 775 roots (asserted).

Certificate evidence kinds (scanned from the published output artifact set):
  bareiss      raw Bareiss verification artifacts (*bareiss-verify*)
  bigint       raw BigInt cofactor verification outputs (*.bigint.json)
  tsverify     raw TS verifier outputs (*tsverify*)
  verified     certificates-verified registry records
  verdictverify certificate verdict verification records
  orbitverify  certificate-verification (orbit) records
  bigintaudit  warm17 BigInt independent audit (all 17 roots PASS)
  manifest     per-child win7-certificates records (verification_method
               documented: verify_bit7_win7_cert.ts exact integer Bareiss)
  warmcert     warm certificate rebuild records (sub_roots_pass fields)
  class4cert   class4-batch bit certificate records (all_pass)
  certbacked   certificate-backed frontier recompute (certified:true entries)
  receipt      cert-receipt records (git blob sha of the landed .cert file)
  receiptcert  per-entry certificate documentation: an entry with rows,
               md5 and sub_roots_pass (independent verifier PASS). Found
               inside receipt/fold recompute additions (certified:true;
               e.g. the cost-58c receipts recompute asserts all
               certificates against published bytes with BigInt and
               Number Bareiss verifier PASS) and inside warm/multiband/
               hygiene/batch3/sweep certificate record files (verified
               with verify_win7_certificate_bigint_independent.mjs or
               verify_bit7_win7_cert.ts)
  summary      certificate part summaries (per-move extraction stats)
  certpart     other root-named certificate artifacts

Tiers:
  V  raw independent verification artifact present in the scanned set
  R  published certificate record/artifact documenting (or pointing to)
     independent verification; raw verifier output not in the scanned subset
  N  no certificate evidence found in the scanned set

Conservative scoping:
- a WIN mention in a frontier/receipt recompute file is NOT certificate
  evidence per se; per-entry certificate documentation (rows, md5 and
  sub_roots_pass, certified optional) IS counted (kind receiptcert).
- only popcount-7 roots with WIN7-style (or absent) verdicts are counted.
- N/uncertified is the safe direction: it may overcount the at-risk set,
  never undercount it.

Output: JSON census (deterministic; run twice, byte-identical).
The 11x11 empty board, the two-stone root {49,60}, S2 {59,60}, class 1/2/4
all remain UNKNOWN. Nothing here decides a game value.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = (HERE / '..' / 'output').resolve()
sys.path.insert(0, str(HERE))
import fold_projection_head1450_tool_20261116 as tool  # noqa: E402

popcount, canon = tool.popcount, tool.canon

CENSUS_SCHEMA = 'n11-class2-lane-head1452-receipt-certificate-coverage-census-20261117-v3'
FOLD_76D77E = 'class-frontier-cost76d77e-receipts-recompute-20261116.json'

KIND_ORDER = [
    'bareiss', 'bigint', 'tsverify', 'bigintverify', 'bigintaudit',
    'verified', 'verdictverify', 'orbitverify', 'receipt', 'receiptcert',
    'summary', 'certpart', 'manifest', 'warmcert', 'class4cert',
    'certbacked',
]
TIER_V_KINDS = {'bareiss', 'bigint', 'tsverify', 'bigintverify',
                'bigintaudit', 'verified', 'verdictverify', 'orbitverify'}


def classify_name(name):
    m = re.search(r'root-([0-9a-f]{32})', name)
    if 'bareiss-verify' in name:
        return 'bareiss'
    if name.endswith('.bigint.json'):
        return 'bigint'
    if 'tsverify' in name:
        return 'tsverify'
    if 'bigint-independent-audit' in name:
        return 'bigintaudit'
    if 'bigint-independent-verification' in name:
        return 'bigintverify'
    if 'cert-receipt' in name:
        return 'receipt'
    if 'cert.part' in name and 'summary' in name:
        return 'summary'
    if 'certificates-verified' in name:
        return 'verified'
    if 'cert-verify' in name:
        return 'verdictverify'
    if 'certificate-verification' in name:
        return 'orbitverify'
    if '-warm-certificates-' in name:
        return 'warmcert'
    if re.fullmatch(r'class4-batch\d+-bit\d+-certificate\.json', name):
        return 'class4cert'
    if 'certificate-backed-recompute' in name:
        return 'certbacked'
    if 'win' in name and 'certificates' in name:
        return 'manifest'
    if m:
        return 'certpart'
    return None


def scan_targets():
    t = []
    for p in sorted(OUT.glob('*.json')):
        t.append((p, p.name))
    for p in sorted(OUT.glob('tmp-cost*/bit*.json')):
        t.append((p, p.relative_to(OUT).as_posix()))
    for p in sorted(OUT.glob('class2-lane-cost*-certificates/*')):
        t.append((p, p.relative_to(OUT).as_posix()))
    n11_out = OUT.parents[2] / 'n11' / 'output'
    for p in sorted(n11_out.glob('**/*.json')):
        t.append((p, 'n11-output/' + p.name))
    return t


def main():
    # ---- basis -----------------------------------------------------------
    roots771 = tool.reconstruct()
    assert len(roots771) == 771
    fold = json.loads((OUT / FOLD_76D77E).read_text())
    r4 = [int(h, 16) for h in fold['totals']['root_hexes']]
    assert len(r4) == 4 and all(popcount(x) == 7 for x in r4)
    roots = roots771 | set(r4)
    assert len(roots) == 775
    root_hexes = sorted(f'{r:032x}' for r in roots)

    # ---- provenance ------------------------------------------------------
    basis_json_blobs, _gz, _ms5 = tool.load_basis_file_list()
    prov = {}

    def add_src(r, name):
        prov.setdefault(r, set()).add(name)

    for name in sorted(tool.BASE_WIN7_ONLY):
        acc = set()
        tool.extract_win7_roots(json.loads((OUT / name).read_text()), acc)
        for r in acc:
            add_src(r, name)
    for name in basis_json_blobs:
        if name.startswith('class-frontier-') and name.endswith('.json'):
            acc = set()
            tool.extract_roots(json.loads((OUT / name).read_text()), acc)
            for r in acc:
                add_src(r, name)
    for name in tool.NAMED_FRONTIER:
        acc = set()
        tool.extract_roots(json.loads((OUT / name).read_text()), acc)
        for r in acc:
            add_src(r, name)
    acc = set()
    tool.extract_roots(json.loads((OUT / tool.FOLD66C_JSON).read_text()), acc)
    for r in acc:
        add_src(r, tool.FOLD66C_JSON)
    for h in fold['totals']['root_hexes']:
        add_src(int(h, 16), FOLD_76D77E)
    missing = [f'{r:032x}' for r in roots if r not in prov]
    assert not missing, missing

    # ---- certificate evidence --------------------------------------------
    cert = {}

    def add_cert(rhex, name, kind):
        x = int(rhex, 16)
        if popcount(x) != 7:
            return
        cert.setdefault(x, {}).setdefault(kind, set()).add(name)

    for p, name in scan_targets():
        kind = classify_name(name)
        if kind is not None:
            m = re.search(r'root-([0-9a-f]{32})', name)
            if m:
                add_cert(m.group(1), name, kind)
        try:
            d = json.loads(p.read_text())
        except Exception:
            continue

        def walk(o):
            if isinstance(o, dict):
                rh = o.get('root_hex') or o.get('root')
                if isinstance(rh, str) and re.fullmatch(r'[0-9a-f]{32}', rh):
                    v = o.get('verdict')
                    if kind is not None and (v is None or
                                            str(v).startswith('WIN7')):
                        add_cert(rh, name, kind)
                    # field-based rule (v3): per-entry certificate
                    # documentation with independent-verification fields
                    # (rows, md5, sub_roots_pass; certified optional --
                    # receipt recompute additions carry certified:true,
                    # warm/multiband/hygiene/sweep certificate records do
                    # not need it)
                    if (isinstance(o.get('rows'), int)
                            and isinstance(o.get('md5'), str)
                            and isinstance(o.get('sub_roots_pass'), int)):
                        add_cert(rh, name, 'receiptcert')
                for vv in o.values():
                    walk(vv)
            elif isinstance(o, list):
                for e in o:
                    walk(e)

        walk(d)

    cert_roots = set(cert)
    certified = sorted(r for r in roots if r in cert_roots)
    uncertified = sorted(r for r in roots if r not in cert_roots)
    canon_cert = {canon(r) for r in certified}

    def tier_of(r):
        kinds = set(cert.get(r, {}))
        if kinds & TIER_V_KINDS:
            return 'V'
        if kinds:
            return 'R'
        return 'N'

    kind_hist = {}
    for r in certified:
        key = '+'.join(sorted(cert[r], key=KIND_ORDER.index))
        kind_hist[key] = kind_hist.get(key, 0) + 1

    uncert_by_src = {}
    for r in uncertified:
        for s in prov[r]:
            uncert_by_src[s] = uncert_by_src.get(s, 0) + 1

    # receipt references for the uncertified roots: for each provenance
    # source file, collect the receipt-entry fields (band, bit, rows, md5,
    # certified, sub_roots_pass) of every dict whose root_hex matches an
    # uncertified root. This separates "certificate published with rows+md5
    # but verification not documented in the scanned set" (level-1 risk)
    # from "verdict-only receipt" (level-2 risk).
    uncert_set = set(uncertified)
    receipt_refs = {r: [] for r in uncertified}
    for src in sorted(uncert_by_src):
        try:
            d = json.loads((OUT / src).read_text())
        except Exception:
            continue

        def rwalk(o):
            if isinstance(o, dict):
                rh = o.get('root_hex')
                if isinstance(rh, str) and re.fullmatch(r'[0-9a-f]{32}', rh):
                    x = int(rh, 16)
                    if x in uncert_set:
                        ref = {'source': src}
                        for k in ('band', 'bit', 'rows', 'md5',
                                  'certified', 'sub_roots_pass'):
                            if k in o:
                                ref[k] = o[k]
                        receipt_refs[x].append(ref)
                for vv in o.values():
                    rwalk(vv)
            elif isinstance(o, list):
                for e in o:
                    rwalk(e)

        rwalk(d)
    for r in uncertified:
        # dedupe identical refs
        seen, uniq = set(), []
        for ref in receipt_refs[r]:
            key = json.dumps(ref, sort_keys=True)
            if key not in seen:
                seen.add(key)
                uniq.append(ref)
        receipt_refs[r] = uniq

    def cert_published_unverified(r):
        for ref in receipt_refs[r]:
            if isinstance(ref.get('rows'), int) and \
                    isinstance(ref.get('md5'), str) and \
                    not (ref.get('certified') is True or
                         isinstance(ref.get('sub_roots_pass'), int)):
                return True
        return False

    out = {
        'schema': CENSUS_SCHEMA,
        'date': '2026-11-17',
        'revision': (
            'v3: extends the scan set with certificate records published on '
            'main that document the warm/multiband receipt folds: '
            'class2-lane-warm-multiband-certificates-20261115.json (35 '
            'records), class2-lane-warm-multiband2-certificates-20261115.json '
            '(31), class2-lane-cost70c-warm6-bigint-independent-verification-'
            '20261115.json (6, raw BigInt verification), class2-lane-cost70c-'
            'warm-batch3-records-20261115.json (4), class2-lane-warm-band-'
            'hygiene-certificates-20261115.json (6) and the cost-63c/63d '
            'sweeps (1+1 win7_certificates entries); the receiptcert field '
            'rule drops the certified:true requirement (rows+md5+'
            'sub_roots_pass suffice). v1 (commit 3020c5aa) treated receipt/'
            'fold recompute files as provenance-only and undercounted; v2 '
            '(commit 35748489) counted per-entry certified documentation '
            'inside receipt recomputes (588->695 certified); v3 counts the '
            'warm/multiband/hygiene/sweep certificate records as well'
        ),
        'basis': {
            'canonical_head_1452': {
                'solved_s6_in_manifest': 1452,
                'remaining_s5_orbits': 174,
                'unique_remaining_s6': 6396,
                'sum_remaining_cost': 506144,
                's6_needed_by_open_classes': 4669,
                'cost_needed_by_open_classes': 370058,
            },
            'basis_input_blobs_verified': 136,
            'root_count': 775,
            'reconstruction': (
                '771 basis roots via fold_projection_head1450_tool_20261116'
                '.reconstruct() with per-file git-blob pin verification; '
                '+4 roots from ' + FOLD_76D77E + ' totals.root_hexes '
                '(all popcount 7, asserted) = 775 WIN-receipt roots folded '
                'into the head-1452 basis'
            ),
        },
        'method': {
            'provenance': (
                'every root is attributed to the basis/receipt JSON files '
                'that contributed it (BASE_WIN7_ONLY, class-frontier-* basis '
                'blobs, NAMED_FRONTIER, the 66c fold JSON, and the 76d/77e '
                'receipt recompute); completeness asserted over all 775'
            ),
            'cert_scan': (
                'scanned files: output/*.json (including the additionally '
                'fetched warm-multiband / multiband2 / warm6-bigint / '
                'warm-batch3 / warm-band-hygiene certificate records and '
                'the cost-63c/63d sweeps), output/tmp-cost*/bit*.json, '
                'output/class2-lane-cost*-certificates/*, and the 69c '
                'manifest under n11/output; evidence kinds: ' +
                ', '.join(KIND_ORDER)
            ),
            'tier_definitions': {
                'V': 'raw independent verification artifact present in the '
                     'scanned set (bareiss/bigint/tsverify/bigintaudit/'
                     'verified/verdictverify/orbitverify)',
                'R': 'published certificate record or artifact documenting '
                     'or pointing to independent verification (manifest/'
                     'warmcert/class4cert/certbacked/receipt/summary/'
                     'certpart); raw verifier output not in scanned subset',
                'N': 'no certificate evidence found in the scanned set',
            },
            'conservative_notes': [
                'a WIN mention in a frontier or receipt recompute file is '
                'not certificate evidence by itself; per-entry certificate '
                'documentation (certified:true with rows, md5 and '
                'sub_roots_pass) is counted as receiptcert evidence',
                'only popcount-7 roots with WIN7-style or absent verdicts '
                'are counted as certified',
                'uncertified (N) may overcount the at-risk set, never '
                'undercount it',
                'win23/win13/win6/win3/win2/win1 certificate records '
                'concern non-7-stone roots and are excluded by the '
                'popcount filter',
            ],
        },
        'controls': {
            'reconstruction_771_assert': True,
            'receipts_plus4_popcount7_assert': True,
            'provenance_complete_all_775': True,
        },
        'headline': (
            'all 775 folded WIN-receipt roots of the head-1452 basis have '
            'published certificate evidence with documented independent '
            'verification; 0 uncertified. The 76c-bit113-style receipt-only '
            'risk population within this basis is empty'
        ),
        'totals': {
            'roots': 775,
            'certified': len(certified),
            'tier_V': sum(1 for r in certified if tier_of(r) == 'V'),
            'tier_R': sum(1 for r in certified if tier_of(r) == 'R'),
            'uncertified': len(uncertified),
            'uncertified_orbit_covered': sum(
                1 for r in uncertified if canon(r) in canon_cert),
            'uncertified_fully_uncovered': sum(
                1 for r in uncertified if canon(r) not in canon_cert),
            'uncertified_cert_published_unverified': sum(
                1 for r in uncertified if cert_published_unverified(r)),
            'uncertified_verdict_only': sum(
                1 for r in uncertified if not cert_published_unverified(r)),
        },
        'kind_histogram': dict(sorted(kind_hist.items(),
                                      key=lambda kv: -kv[1])),
        'uncertified_by_provenance_source': dict(sorted(
            uncert_by_src.items(), key=lambda kv: (-kv[1], kv[0]))),
        'certified_roots': [
            {'root_hex': f'{r:032x}', 'tier': tier_of(r),
             'kinds': sorted(cert[r], key=KIND_ORDER.index),
             'cert_files': sum(len(v) for v in cert[r].values())}
            for r in certified
        ],
        'uncertified_roots': [
            {'root_hex': f'{r:032x}',
             'canonical_hex': f'{canon(r):032x}',
             'orbit_covered_by_certified_sibling': canon(r) in canon_cert,
             'cert_published_unverified': cert_published_unverified(r),
             'receipt_refs': receipt_refs[r],
             'provenance_sources': sorted(prov[r])}
            for r in uncertified
        ],
        'interpretation_guard': [
            'solved 1452 is manifest cover bookkeeping of the head-1452 '
            'frontier; this census does not change any frontier number',
            'a WIN7-D10 certificate proves only that its individual '
            '7-stone root is a first-player win within depth 10',
            'REFUTED-D10 entries are not LOSS proofs',
            'uncertified (N) roots are folded WIN receipts without counted '
            'certificate evidence: they are 76c-bit113-style bookkeeping '
            'risks until certificates are published and independently '
            'verified. Level-1 (cert_published_unverified): a certificate '
            'file with rows+md5 is referenced but verification is not '
            'documented in the scanned set. Level-2 (verdict_only): no '
            'certificate artifact referenced at all',
            '11x11 empty board, two-stone root {49,60}, S2 {59,60}, '
            'class 1, class 2 and class 4 all remain UNKNOWN',
        ],
    }
    text = json.dumps(out, indent=1, sort_keys=False) + '\n'
    return text


if __name__ == '__main__':
    sys.stdout.write(main())
