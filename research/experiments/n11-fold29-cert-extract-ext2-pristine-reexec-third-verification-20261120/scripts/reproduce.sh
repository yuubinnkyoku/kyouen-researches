#!/bin/sh
# Reproduction of the K1166 (fold29 certificate-extraction external second
# verification) pristine re-execution third verification.
#
# The published K1166 experiment dir bytes are fetched at the pinned main
# commit PIN_COMMIT. The UNMODIFIED published harness is then run
# twice as two independent batteries:
#   battery 1: working cwd/HOME, default hash seed
#   battery 2: isolated cwd, isolated HOME, PYTHONHASHSEED=random
# Each battery: fetch_master.py (61-file master reconstruction + git blob
# pins) -> harness stages pin / root k1136 / k1137 / k1139 / tampers /
# finalize, each in a separate command well under 300 s.
# Finally the deterministic record assembler re-checks every gate and writes
# output/third-verification.json (byte-deterministic, no timing fields).
#
# Environment used here: python3.12, node v22.20.0 (--experimental-strip-types),
# 2 cores, harness-internal parallelism fixed at 2.

set -e

PIN_COMMIT=1c42dcf25c78540033c5ec08c00952e4a939a8ee
RAW="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/$PIN_COMMIT"
EXT2="research/experiments/n11-fold29-win8-cert-extract-ext-second-verification-20261120"

# 0) published bytes (also byte-pinned by assemble_third_record.py)
mkdir -p published
curl -sL "$RAW/$EXT2/README.md"                                   -o published/README.md
curl -sL "$RAW/$EXT2/fetch_master.py"                              -o published/fetch_master.py
curl -sL "$RAW/$EXT2/pin-manifest.json"                            -o published/pin-manifest.json
curl -sL "$RAW/$EXT2/verify_cert_extract_ext_second_20261120.py"   -o published/verify_cert_extract_ext_second_20261120.py
curl -sL "$RAW/$EXT2/output/harness-audit.json"                    -o published/harness-audit.json
# expected: 6605abff.. / c3c4c9ff.. / 949868e2.. / ca662e57.. / cf6a26ab..
sha256sum published/*

# battery 1
mkdir -p b1 && cd b1
cp ../published/fetch_master.py ../published/pin-manifest.json \
   ../published/verify_cert_extract_ext_second_20261120.py .
python3 fetch_master.py
python3 verify_cert_extract_ext_second_20261120.py --stage pin
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1136
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1137
python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1139
python3 verify_cert_extract_ext_second_20261120.py --stage tampers
python3 verify_cert_extract_ext_second_20261120.py --stage finalize
sha256sum run/harness-audit.json   # -> cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f
cd ..

# battery 2 (isolated cwd/HOME + random hash seed)
mkdir -p b2/home && cd b2
cp ../published/fetch_master.py ../published/pin-manifest.json \
   ../published/verify_cert_extract_ext_second_20261120.py .
HOME="$PWD/home" PYTHONHASHSEED=random python3 fetch_master.py
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage pin
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1136
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1137
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage root --root k1139
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage tampers
HOME="$PWD/home" PYTHONHASHSEED=random python3 verify_cert_extract_ext_second_20261120.py --stage finalize
sha256sum run/harness-audit.json   # -> cf6a26abf0a459bcfb42bbb2d649ace5d3d1f1a5aee63a01af1de8b79d6a145f
cd ..

# deterministic record
python3 scripts/assemble_third_record.py b1/run b2/run
sha256sum output/third-verification.json
python3 -m unittest discover -s tests -p 'test_part_gate_completeness.py'
python3 scripts/verify_part_gate_completeness.py b1/run b2/run
sha256sum output/part-gate-completeness.json
