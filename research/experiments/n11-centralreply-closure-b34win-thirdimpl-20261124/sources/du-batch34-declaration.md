# Part DU å®£è¨ (2026-11-24): batch-34 â closureè¡¨ rank 1/2 small-pocket classes 23101ã»1849 ã®æçµæªç¢ºå®costå­ 2ã­ã¼ probe (publish-then-executeã»åä¸ãªã¼ãã¼)

åä¸ãªã¼ãã¼: n11ä¸­å¤®å¿ç­ é·æã¬ã¼ã³ (æ¬ã»ãã·ã§ã³ã»Part DTç´æ¥ã®å¾ç¶)ã
å¯¾æå®£è¨ãªã: pushç´åã«ææ°mainãååå¾ããæè¿ã³ããããæ©æ¢°grepãã¦
batch-34 / Part DU / class 23101 / class 1849 / small-pocket ãä¸»å¼µãã
commitã»å®£è¨ããªããã¨ãç¢ºèªãã¦ããçæãã (å¾è¿°ã®è¦³æ¸¬HEADåç§)ã

## 1. ã¬ã¸ã¥ã¼ã çµç·¯ã¨é¸å®æ ¹æ 

Part DTå®äº (commit `305d1590`) ã®ã¬ã¸ã¥ã¼ã åè£ (a)ãclosureè¡¨ rankä¸ä½
small-pocket batché¸å®ããæ¡ããPart DT kit reaudit 3åºå
(refresh-summary `38fc4e19â¦`ã»closure-classes `6cc33dd7â¦`ã»per-root-coverage
`c5a2721dâ¦`) ã«ããã°ãclosureè¡¨ (807è¡) ã®ä¸ä½ã¯:

- rank 1: **class 23101** (`[1152921504892059648, 16]`) â unknown_now **1**
- rank 2: **class 1849** (`[1152922672972169216, 0]`) â unknown_now **1**
- rank 3: class 2251 (unknown 1 = æªæ¡ç¨WIN ab028ã»Part CZ thirdimpl corroborationæ¸ã¿)
- rank 4: class 5804 (unknown 4 = æªæ¡ç¨WIN 3 + EXHAUSTED 1 ad043)
- rank 5: class 34908 (unknown 9 = æªæ¡ç¨WIN 4 + EXHAUSTED 5)

rank 3ä»¥ä¸ã®æ®ä½ã¯æ¡ç¨å¾ã¡ (scrutiny owner C++ gate) ã¾ãã¯é«budgetåprobe
(å¥å®£è¨å¿é ) ã§ããã**æ¬ãããã§probeå¯è½ãªæªç¥å­ã¯rank 1ã¨rank 2ã®å1ã­ã¼
ã®ã¿**ããã®2ã­ã¼ãbatch-34ã¨ããã2ã­ã¼ã®å¯¾è±¡ãã¼ã¿ã¯refresh-summaryã®
`worklist_first` probe_order 1, 2 ( Ð¿ÑÐ±Ð»Ð¸ÐºÐ°ÑÐ¸Ð¸ç±æ¥ã»æè»¢åã¼ã­):

- **ag001**: serving class 23101ã»lo=1152921505747697664ã»hi=1032ã»
  legal=85ã»s5_index=745184ã»membership_class_count=4
- **ag002**: serving class 1849ã»lo=1153485622925590528ã»hi=0ã»
  legal=88ã»s5_index=81011ã»membership_class_count=3

ä¸¡ã­ã¼ã¨ã canonical chain cache (`973bcd19â¦`ã»6,547è¡) ã« exact-pairä¸å¨
(æ©æ¢°ç¢ºèªã»G4 gate)ã»quarantineç»é²ãªã (G5 gate)ã»legal ã¯ Boardåè¨ç®å¤ã
inputã«åºå® (jsreplayã¯å®è¡æã«ãlegalãåå°åºãã¦ä¸ä¸è´ãªãä¾å¤åæ­¢)ã

## 2. ã¹ã³ã¼ãã»ææ³

å®é¨dir: `research/experiments/n11-centralreply-closure-smallpockets-batch34-20261124/`ã

- ææ³: pinned runner `runbatch.sh` (sha256 `f591f8c2â¦`ã»batch-33 kitã¨byte-clone)
  + pinned replica `jsreplay.js` (sha256 `84585617â¦`ã»byte-clone)ã
  2-pass fresh-cold replayã»budget 15,000,000ã»1 solver / 1 row / 1 processã
  å®è¡åã«published val-gate 4è¡ (batch-33 kitã®2 target Ã 2M/15M) ãæ¬ç°å¢ã§
  freshåç¾ã node-exact (resultã»nodes) ä¸è´ãå¿é  (freshå®è¡ã¯å®£è¨å¾)ã
- maker `make_batch34_keys.py` (æ¬kitæ°è¦): fail-closed gates G1âG6
  (source sha pinsã»worklist_firstå¨fieldç§åã»closureè¡¨rank anchorã»
  canonical cache exact-pairä¸å¨ã»quarantineä¸å¨ã»legalåºæåºå®)ã
  å®£è¨åã­ã¼ã«ã«å®è¡ã§ gates PASS 3åbyte-identicalã»tamper battery
  pinå±¤5/5 + semanticå±¤2/2 (pinåæ¨çåããæ»æã¢ãã«ã§G2 legal driftã¨
  G4 cache hitãæ¤åº)ã»å¾©æ§å¾pristine greenãç¢ºèªæ¸ã¿ãkitåºçå¾ã¯
  published bytesããåä¸æé ãåå®è¡ããã
- **åæ­¢è¦å (äºåç»é²)**:
  1. determinism mismatch â å³æHARD-STOP (rc=42)ãä»¥å¾ã®ã­ã¼çæä¸å¯ã
  2. budgetæ¯æ¸ (result 0) â honest UNKNOWNã15Måæ¡ä»¶ã®åæ¢ç´¢ã¯ç¦æ­¢ã
     æ¬¡ã©ãã¼ (budgetææ ¼) ã¯å°æ¥ã®æ°è¦å®£è¨ãå¿è¦ã
  3. **WIN-CONTINUE (äºåç»é²ã»Part CKåä¾)**: WIN (result 1) ã¯honest label
     ã¨ãã¦status.logã»rawã«è¨é²ããããdriveã¯ç¶ç¶ãããbatch-34ã¯2ã­ã¼ã§
     ãããããä¸¡ã¯ã©ã¹ã®æçµæªç¢ºå®å­ã WIN/LOSS/EXHAUSTED ãããã§ã
     honest label ãå®èµ°ããããWINæ¡ç¨ã¯æ¬ã¬ã¼ã³ã§ã¯è¡ããªã
     (verdictä¸æ¶è²»ã»scrutiny owner C++ç¬¬äºå®è£ gate `9193f5b6â¦` å¾ã¡)ã
- æ¶è²»è¦å: æ¬Partã¯probeã®å®èµ°ã¨honest labelã®åºçã®ã¿ãcanonical cache
  ã¸ã®æ¸è¾¼ãªã (adoptionã¯å¥adoption Partã»pinned merger `90711961â¦` å°æ¨©)ã
  ã¯ã©ã¹ééã»rootè¢«è¦ã»securedã®ä¸»å¼µã¯ããªã (å¤å®ã¯å¾ç¶ã®
  refreshåå®è¡+ç¬ç«ç£æ»ãè¡ã)ã

## 3. æå¾æ©æ¢°ç°¿è¨ (äºåç»é²)

- probed total: 0 â 2 (ag001, ag002)ã**çµæéäºå** â WIN/LOSS/EXHAUSTEDã®
  åå¸ã¯å®è¡å¾ã®honest labelã
- closureè¡¨ã»free_nowã»excluded_nowã»unknownã»update8ã»greedyç­ã®å¤åã¯
  æ¬Partã§ã¯ derive ããªã (adoptionå¾ã®reauditãæ©æ¢°å°åºãã)ã
- nodesæ°ã»wallç§æ°ã¯bookkeepingã§ããåæã§ã¯ãªãã

## 4. scrutiny owner C++ gate (Part DT ã¬ã¸ã¥ã¼ã (d)) ã®ç¾ç¶

Part DT ã¬ã¸ã¥ã¼ã â¤(d)ãWIN 4è¡ scrutiny-owner C++ gate `9193f5b6â¦` å®æ½ãã
æ¬ã»ãã·ã§ã³åé ­ã«æ¤è¨ãããæ¡ç¨ã²ã¼ãã¯C++ç¬¬äºå®è£
`cpp/solvers/kyouen_dfpn_root.cpp` (pin `9193f5b6â¦`) ã ããæ¬å®è¡ç°å¢ã«ã¯
C++ã³ã³ãã¤ã©ãå­å¨ãããããã±ã¼ã¸å°å¥ãç¦æ­¢ããã¦ãã
(2026-11-22 Part Gå½åã®éå®³ã¨åä¸)ããã£ã¦æ¬ã¬ã¼ã³ã¯C++ gateãå¼ãç¶ã
å®è¡ã§ãããWINè¡æ¡ç¨ã®å°æ¨©ã¯scrutiny ownerã®ã¾ã¾ä¸å¤ããã®æå ±ãå®é¨äºå®
ã¨ãã¦å®äºlogã«è¨é²ããã

## 5. åºçå½¢æ (å®£è¨å¾ã«é æ¬¡)

A) å®£è¨ (æ¬note) â B) kit (scripts 3 + input 3 + val-gate 8) â
C) outputs (status.logã»raw 4ã»val-gate fresh .b34-host.out 4) â
D) README + MANIFEST-sha256 + å®äºlogãå¨files commit-pinned
fetch-back byteç§åã»branch path URL (CDN stale) ã¯ä½¿ããªãã

## 6. ä¸¦èµ°ã¨ã®ä¸æ¥è§¦

- fast lane (K1302åºçæ¸ã¿ã»K1303 general-w inductionå®£è¨/kitã¯å¥ã¬ã¼ã³ææ)ã»
  cap-games lane (PG(2,9) orbitç³»)ã»moment/s-parameterç³»ã¬ã¼ã³: å¯¾è±¡ã­ã¼ã»
  classã»æä»¶ãå¨ãå¥ã§éæ¥è§¦ã
- batch-33 (Part DQ/DR/DS)ã»adoption Part DT ã®published dirs (ä¸å¤)ã
- unconsumed WINåè£ (class 5343 46è¡ã»2251 ab028ã»5804 3è¡ã»34269 11è¡ã»
  34908 4è¡) ã®æ¡ç¨ç¶æã»scrutiny owner gateãEXHAUSTED 5è¡ (34908) ã®
  é«budgetåprobe (å¥å®£è¨å¿é )ã

## 7. UNKNOWNæä¿

**æ¨æº11Ã11ç©ºç¤ã»19 central-reply rootsã»äºç³root {49,60}/{59,60}ã»S2 {59,60}ã»
class 1/2/4ã»class 23101ã»class 1849 (æ¬batchã®2ã­ã¼ãå«ãå¨ã¡ã³ãã¼) ã¯
æ¬Partã®å®è¡ã»åºçã®ã©ã®æç¹ã§ãUNKNOWNã®ã¾ã¾ã** nodesæ°ãåæãè·é¢ã¨ãã¦
èª­ã¾ãªããWIN/LOSSæ¡ç¨ã¯scrutiny owner C++ gate ééå¾ã®å¥adoption Part
(pinned merger `90711961â¦`) ã®ã¿ãclosureè¡¨ã»worklistã¯scheduling bookkeeping
ã§ããclass statusãéã°ãªãã
