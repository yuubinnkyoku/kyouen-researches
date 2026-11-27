# Addendum: publication integrity note for the ultra-cheap legal-precheck kit

During fetch-back verification of
`research/experiments/n11-ultra-cheap-legal-precheck-20261127/`, the
kit's `in/shared-s5-tasks.csv` (552,371B) was initially published
TRUNCATED at 63,922B: the publishing path read the file in a single
non-chunked pass and the read boundary cut the file (same failure
class as the 2026-11-27 `sweep-anomalies-raw.txt` 344B-short incident
repaired in commit b874536e8b by a parallel lane). Detected by the
byte-compare fetch-back gate.

Repair: republished the complete file in a second commit with the
read performed in offset-continuation chunks (all 552,371 chars
pushed). Verification of the repaired remote copy, since the raw CDN
edge serving this lane kept returning the stale truncated copy even
after cache-busting attempts: the GitHub contents API reports the
remote git blob sha `98866f47fd9cbd0d243dd88db8e509b1dd9c55b4`, which
is exactly the git blob sha of the local complete file
(sha256 `31f0d29b...`, 4,562 data rows), so the remote copy is
byte-exact and consistent with the kit MANIFEST.

All other 13 kit files and the completion log verified byte-identical
by raw CDN fetch-back on the first pass. No output, script, or gate
content was affected; the census run json and all PASS evidence are
untouched. Verdict NOT consumed, no key probed: standard 11x11 empty
board UNKNOWN, all 19 central-reply roots UNKNOWN, two-stone root
{60,27} and third moves 100/108 UNKNOWN.
