#!/bin/bash
cd /home/user/work/pg2q7s3
D=/tmp/q7; rm -rf $D; mkdir -p $D
node --expose-gc spectrum.js enum nc 0 $D/nc 7 3 > $D/enum_nc.log 2>&1 || exit 1
node --expose-gc spectrum.js enum c 0 $D/c 7 3 > $D/enum_c.log 2>&1 || exit 1
node --expose-gc spectrum.js dp nc 0 $D/nc 7 3 > $D/dp_nc.json 2> $D/dp_nc.log || exit 1
node --expose-gc spectrum.js dp c 0 $D/c 7 3 > $D/dp_c.json 2> $D/dp_c.log || exit 1
node combine.js $D/nc/dp_result.json $D/c/dp_result.json 7 3 > $D/combined.json 2> $D/combine.log
echo DONE > $D/STATUS
