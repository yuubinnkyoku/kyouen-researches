#!/bin/sh
# Third-method verification of the K1057 ninth..twelfth WIN7-D10 certificates
# plus the sweep43/census and fold/resolve5 static audits, run against
# PUBLISHED repo files only (no local scratch state needed).
#
# Usage: sh scripts/run_third_method_verification_20261119.sh [repoRoot]
#   repoRoot defaults to "." (run from the repository root).
# Writes the six JSON outputs into output/ . Deterministic except wall_s.
set -e
REPO=${1:-.}
E="$REPO/research/experiments/n11-ninth-twelfth-win7-third-method-verification-20261119"
K117="$REPO/research/experiments/n11-117pool-d10-sweep-7th8th-win7-certs-20261119"
K86="$REPO/research/experiments/n11-stranded86-add-one-stone-expansion-d10-sweep-20261119"
OUT="$E/output"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$OUT"

# audit workdir (the file names the audit scripts expect)
ln -s "$K117/foldv2/output/post-eighth-receipt-cover-resolve4-20261119.json" "$WORK/resolve4.json"
ln -s "$K86/sweep43/output/witness-43-root-depth10-sweep-20261119.json"      "$WORK/sweep43.json"
ln -s "$K86/sweep43/output/probe-records-w0.jsonl"                            "$WORK/probe-records-w0.jsonl"
ln -s "$K86/sweep43/output/probe-records-w1.jsonl"                            "$WORK/probe-records-w1.jsonl"
ln -s "$K86/sweep43/roots.json"                                              "$WORK/roots.json"
ln -s "$K86/fold/output/ninth-twelfth-win7-receipt-fold-20261119.json"       "$WORK/fold912.json"
ln -s "$K86/fold/output/post-twelfth-receipt-cover-resolve5-20261119.json"   "$WORK/resolve5.json"

# cert-9th: restore the certificate text from the published gzip+base64 form
R9=00000000000000801202000001040200
base64 -d "$K86/cert-9th/win7-root-$R9-20261119.n11.gz.b64" \
  | gunzip > "$WORK/win7-root-$R9-20261119.n11"

for spec in "10th:00000000000000821082040200000000" "11th:00000000000000821092200000000000" "12th:00000000001020003800000048000000"; do
  d=${spec%%:*}; r=${spec#*:}
  ln -s "$K86/cert-$d/win7-root-$r-20261119.n11" "$WORK/win7-root-$r-20261119.n11"
done

# per-certificate third-method verification (cert text + published summaries)
for spec in "9th:00000000000000801202000001040200" "10th:00000000000000821082040200000000" "11th:00000000000000821092200000000000" "12th:00000000001020003800000048000000"; do
  d=${spec%%:*}; r=${spec#*:}
  python3 "$E/scripts/verify_third_method.py" \
    "$WORK/win7-root-$r-20261119.n11" \
    "$K86/cert-$d/win7-root-$r-extraction-summary-20261119.json" \
    "$K86/cert-$d/win7-root-$r-independent-verification-20261119.json" \
    "$K86/cert-$d/win7-root-$r-bareiss-subroots-20261119.jsonl" \
    "$OUT/win7-root-$r-third-method-verification-20261119.json" > /dev/null
  echo "verify_third_method: $d PASS"
done

python3 "$E/scripts/audit_sweep43_census.py" "$WORK" \
  "$OUT/sweep43-census-third-method-static-audit-20261119.json" > /dev/null
echo "audit_sweep43_census: PASS"
python3 "$E/scripts/audit_fold_resolve5.py" "$WORK" \
  "$OUT/fold-resolve5-third-method-cross-check-20261119.json" > /dev/null
echo "audit_fold_resolve5: PASS"
