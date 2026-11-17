#!/usr/bin/env bash
# Independent byte-level re-fetch audit for the 13 cost71e WIN7-D10 certificates.
# Expected values are pinned from manifest blob a9ddec439e1931614679c2575e4adeb5fe770d2b.
# Source snapshot: a8ff1d814a64565491a8527a7489b97952ec9514.
set -euo pipefail

PIN="a8ff1d814a64565491a8527a7489b97952ec9514"
BASE="https://raw.githubusercontent.com/yuubinnkyoku/kyouen-researches/${PIN}/research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71e-certificates"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

command -v sha256sum >/dev/null
command -v md5sum >/dev/null
if command -v curl >/dev/null; then
  fetch() { curl -fsSL --retry 2 --connect-timeout 10 "$1" -o "$2"; }
else
  command -v wget >/dev/null
  fetch() { wget -q --timeout=30 --tries=2 -O "$2" "$1"; }
fi

total=0
count=0
check_one() {
  local bit="$1" file="$2" whole_bytes="$3" want_sha="$4" want_md5="$5"
  local mode="$6" p1_bytes="${7:-0}" p2_bytes="${8:-0}"
  local joined="$TMP/$file" actual_bytes actual_sha actual_md5
  if [ "$mode" = split ]; then
    fetch "$BASE/$file.part1of2" "$TMP/$file.part1of2"
    fetch "$BASE/$file.part2of2" "$TMP/$file.part2of2"
    [ "$(wc -c < "$TMP/$file.part1of2" | tr -d '[:space:]')" = "$p1_bytes" ]
    [ "$(wc -c < "$TMP/$file.part2of2" | tr -d '[:space:]')" = "$p2_bytes" ]
    cat "$TMP/$file.part1of2" "$TMP/$file.part2of2" > "$joined"
  else
    fetch "$BASE/$file" "$joined"
  fi
  actual_bytes="$(wc -c < "$joined" | tr -d '[:space:]')"
  actual_sha="$(sha256sum "$joined" | awk '{print $1}')"
  actual_md5="$(md5sum "$joined" | awk '{print $1}')"
  [ "$actual_bytes" = "$whole_bytes" ]
  [ "$actual_sha" = "$want_sha" ]
  [ "$actual_md5" = "$want_md5" ]
  total=$((total + actual_bytes))
  count=$((count + 1))
  printf 'bit=%s bytes=%s sha256=%s md5=%s PASS\n' "$bit" "$actual_bytes" "$actual_sha" "$actual_md5"
}

check_one 3 n11_s7_00000000000000c09002000000002008.cert 1299200 e8d5764a7b5dac30ddd434f6615e8248126f59095793a1c7e6040b7acbca533d cf094e2df7b17d94a05b436eab8de09a split 649608 649592
check_one 4 n11_s7_00000000000000c09002000000002010.cert 1838885 717320b77193475c1020f1fde02f58d591b924c7390a2aedd4e8979737c840d8 8ea573a6d99c071b09df39bb4045a2c6 split 919446 919439
check_one 8 n11_s7_00000000000000c09002000000002100.cert 1488731 533531415df54d2bbe095c5d26848ad979c11239c5c1b8339d5256bd5a51cf3e f498610883fde98a44607fec37ff9966 split 744382 744349
check_one 41 n11_s7_00000000000000c09002020000002000.cert 955669 98a3d7aec4e750d967469cf0865a29c5cba90e5fa9532cb8a956054a4800d06e ff8c708f7f1c4dc32ff42e72a75134e8 whole
check_one 54 n11_s7_00000000000000c09042000000002000.cert 1707208 d9d9201976610f5afc0607afa3ada22e4cd2fe1cd73d490ec6137cfc48306239 5341d200850a83b7f8678c9260a825df split 853607 853601
check_one 58 n11_s7_00000000000000c09402000000002000.cert 1178240 8dfefa4c9fe29db845088850927757c7a05327077fa48f25472384c6bb1ce9ba 1e09f18f16cacf480ee7a5408ea2d268 whole
check_one 76 n11_s7_00000000000010c09002000000002000.cert 1533901 398d909296b930bd5f9bf44a10eee8e8f46beff8f89a62a9ba34ab9d278891ba 9a9ea6239a5e9d0b4ec52757970c583b split 766956 766945
check_one 79 n11_s7_00000000000080c09002000000002000.cert 936287 a92d11a9054b9adf5f7ffca5a5f69e3ea5b5c9939c1a1eaf90ae43b59175b4e0 aa06ba70bd3f70bd7e4b876dcb476bcc whole
check_one 94 n11_s7_00000000400000c09002000000002000.cert 1629102 ff9811c101f76edf00849d04bf5f53292dcc566ee26402e6c117b01905195687 0a37cea9cd538660fb4b3acff8a9cb91 split 814565 814537
check_one 96 n11_s7_00000001000000c09002000000002000.cert 1709180 1510b5455095727e038f14989d7b30935eb8da172897f67af0910184977ec8f5 77cffa20d368c58a010001baaec931d3 split 854599 854581
check_one 100 n11_s7_00000010000000c09002000000002000.cert 1221794 976d23ed96375820ef6831fe5e5b5e4381a47f8037be35c05668910154a216da e44613fa7a471ddf2e0890f16ef2561a split 610900 610894
check_one 116 n11_s7_00100000000000c09002000000002000.cert 2016154 a73e0070f221360812454a2aafc7d61e22b0c6f98f0cc8152e6a957825059d3d 6421c42c66c563bad61ee7494de147f3 split 1008085 1008069
check_one 119 n11_s7_00800000000000c09002000000002000.cert 1785754 1ecd6fbab037ca13c1b29f6b5666c2a975456cfd5c2199bb6e3c73080d3700a4 557844e8e329cfabd0e0d41755d2ee66 split 892908 892846

[ "$count" = 13 ]
[ "$total" = 19300105 ]
printf 'TOTAL certificates=%s bytes=%s PASS\n' "$count" "$total"
