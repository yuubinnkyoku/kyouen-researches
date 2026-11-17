cost76c bit61 WIN7-D10 certificate

S6 child 00000000010000809002000001000000; bit 61; seven-stone root 0000000001000080b002000001000000.
55 legal replies; 1,325,278 extraction nodes; 30,042 strategy rows; zero FBT drops.
Certificate bytes 1083833; MD5 6a38f91cb3ec26e5bb7dd4fa937c5e42; SHA-256 91c69354d5f300a367756ca2dd430bc2f093dea8c0a188e7ee5d8b0b749c0f06.
Bareiss and BigInt verifiers pass all 55 sub-roots; exact union 0 missing / 0 extra.
Fresh-process re-extraction is byte-identical. The certificate is stored whole.

Reproduction from this directory, Node v22.16.0 or later:
ROOT=0000000001000080b002000001000000
CHILD=00000000010000809002000001000000
MOVES=$(python3 ../../scripts/legal_candidates.py "$ROOT" | tail -1)
printf '%s\n' "$MOVES" | node --experimental-strip-types ../../scripts/cert_driver76c.ts "$CHILD" 61 /tmp/bit61.cert
node ../../scripts/verify_win7_certificate_bigint_independent.mjs /tmp/bit61.cert 55
node --experimental-strip-types ../../scripts/verify_bit7_win7_cert.ts --cert /tmp/bit61.cert --root "$ROOT" --root-check --subroots "$MOVES" --consumed-out /tmp/bit61-consumed.txt

This receipt fold closes one S6 manifest row only. The standard 11x11 empty board and all smaller target roots/classes remain UNKNOWN.
