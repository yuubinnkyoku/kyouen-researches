# next98 49-cover audit: canonical key precision correction

The JSON file `post-b4d9b6a9-next98-conditional-s6-cover-audit.json` was
written through a JavaScript serialization path. Its two arrays `s4_key`
and `three_parent_shared_common_s5` contain unsafe IEEE-754 numbers and
**must not be used as exact canonical keys**.

The exact decimal-string keys are:

- `s4_key = ("1152921504741065728", "68719476736")`
- `three_parent_shared_common_s5 = ("10376293541595841536", "68719476736")`

The 49-line CSV uses exact decimal text and is unaffected. Other integer
counts in the JSON are small and exactly representable.

The cover is conditional only. S6 verdicts, the two-stone root and the
11×11 empty board remain UNKNOWN.
