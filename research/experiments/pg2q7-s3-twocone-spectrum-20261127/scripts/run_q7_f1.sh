#!/bin/bash
cd /home/user/work/pg2q7s3
D=/tmp/q7f1; rm -rf $D; mkdir -p $D
node --expose-gc spectrum.js enum nc 1 $D/nc 7 3 >$D/enum_nc.log 2>&1 || exit 1
node --expose-gc spectrum.js enum c 1 $D/c 7 3 >$D/enum_c.log 2>&1 || exit 1
node --expose-gc spectrum.js dp nc 1 $D/nc 7 3 >$D/dp_nc.json 2>$D/dp_nc.log || exit 1
node --expose-gc spectrum.js dp c 1 $D/c 7 3 >$D/dp_c.json 2>$D/dp_c.log || exit 1
node combine.js $D/nc/dp_result.json $D/c/dp_result.json 7 3 > $D/combined.json 2>/dev/null
# determinism: rerun fset=0 nc dp on fresh enum and diff dp_result.json
D2=/tmp/q7det; rm -rf $D2; mkdir -p $D2
node --expose-gc spectrum.js enum nc 0 $D2/nc 7 3 >/dev/null 2>&1
node --expose-gc spectrum.js dp nc 0 $D2/nc 7 3 >$D2/dp_nc.json 2>$D2/dp_nc.log
if cmp -s $D2/nc/dp_result.json /tmp/q7/nc/dp_result.json; then echo "DETERMINISM-NC-IDENTICAL" > $D2/verdict; else echo "DETERMINISM-FAIL" > $D2/verdict; fi
echo DONE > $D/STATUS
