#!/usr/bin/env python3
"""Compact independent certificate: 18 S8 LOSS, minimum 184 S10 leaves.

Only the 184 selected LOSS leaves and 672 potentially dangerous WIN
positions need terminal verification; every other boundary position is
excluded from the lower-bound proof by geometry alone.
WIN/LOSS is from the original first player's fixed perspective.
No external verdict cache, ILP solver, or C++ compiler is needed.
"""
import base64
import zlib
from functools import lru_cache
from itertools import combinations
N=11
def check(condition,message='invalid certificate'):
    if not condition: raise ValueError(message)
def points(m): return [i for i in range(121) if m>>i&1]
def circle(a,b,c,d):
    def vec(p):
        x,y=p%N,p//N
        return (x,y,x*x+y*y)
    z=vec(d)
    u=[x-y for x,y in zip(vec(a),z)]
    v=[x-y for x,y in zip(vec(b),z)]
    w=[x-y for x,y in zip(vec(c),z)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0]))==0
def safe(m): return all(not circle(*q) for q in combinations(points(m),4))
def legal(m):
    p=points(m); triples=list(combinations(p,3))
    return [x for x in range(121) if not (m>>x&1) and all(not circle(a,b,c,x) for a,b,c in triples)]
# Precomputed D4 maps preserve the original exact integer geometry.
_D4_BITS = []
for t in range(8):
    row = []
    for p in range(121):
        x, y = p % N, p // N
        xx, yy = ((x,y),(10-y,x),(10-x,10-y),(y,10-x),(10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]
        row.append(1 << (11*yy+xx))
    _D4_BITS.append(tuple(row))

@lru_cache(maxsize=131072)
def canonical(m):
    pp = points(m)
    return min(sum(row[p] for p in pp) for row in _D4_BITS)
def children(m): return {canonical(m|(1<<p)) for p in legal(m)}
def next_player_wins_at_s10(m):
    check(m.bit_count() in (10,11) and safe(m))
    base=points(m); moves=legal(m); n=len(moves)
    check(n<=31,f'terminal bitmask width exceeded: {n}')
    bad=set()
    for i,j in combinations(range(n),2):
        if any(circle(a,b,moves[i],moves[j]) for a,b in combinations(base,2)):
            bad.add((1<<i)|(1<<j))
    for i,j,k in combinations(range(n),3):
        e=(1<<i)|(1<<j)|(1<<k)
        if any(e&b==b for b in bad):continue
        if any(circle(a,moves[i],moves[j],moves[k]) for a in base):bad.add(e)
    for ids in combinations(range(n),4):
        e=sum(1<<i for i in ids)
        if any(e&b==b for b in bad):continue
        if circle(*(moves[i] for i in ids)):bad.add(e)
    ban_by=[[] for _ in range(n)]
    for e in bad:
        for i in range(n):
            if e>>i&1:ban_by[i].append(e^(1<<i))
    @lru_cache(None)
    def win(state):
        for i in range(n):
            bit=1<<i
            if state&bit or any(state&b==b for b in ban_by[i]):continue
            if not win(state|bit):return True
        return False
    return win(0),win.cache_info().currsize




def decode(s):
    return zlib.decompress(base64.b85decode(s))

def decode_positions(s):
    b=decode(s)
    check(len(b)%16==0, 'corrupt packed positions')
    return [int.from_bytes(b[i:i+16], 'big') for i in range(0,len(b),16)]

ROOTS_B85 = 'c-mFX(G7qg5ChOc{5by_;sCk{8VAF~0T{zE^-e^%@bl7=0(v}&1db?Y_H>P9#?UwjelIJmE3S0{isKatLZ6=h_Dam8M)mRhqkAwJ1%2NfQ1_!c|4x11*(^63&%O7Whc}O}{nwWpO^p%X'
LEAVES_B85 = 'c-mc-y>3%66vvN^D>)H^Z<HaUK^-clsNw+(WQY($N5&3JOgw_qcIcQ&JU~ZA9)U;0=hJqg>MFmU<Kw^2hjRh&lb#Y(pROu^@hhYic;!t52=318n<KI}-V$fyU2gH5Ancz~ylHm9cb|Z4&n}Fd<7%{5I67sF^#CAT{*(j>;1^7s+uy*k{VOVOVGp<jKc3Iq&R0jqJ$&agq^0|RM}OHqp*<tl&Nu!1sp5KojpT>9I$Mw2Ts3}r{Ss5*Nch>^)siSPnVzS1?&R9yt&hT)ID|a$mh~I|;P@xFqV;|&oHZVB{KEd8s{xO?-$&sn9N6KpDAV~vt6EtCil_dFp!r?uz^$LIpz}@Ceqb(?U$4Ar;li74-%x%#-(h`>_s!q>F+$7lEp&gWujW6dUT@-p{Yn0$cMY?hnfhOg)FOnRn2cil_CsJT$V;;mJ7V0C*z<bn@5=owj7w=AkXdUrJ8Ox=Tk@ygA<i}rJMMO#*R1C!KDRH|E)7g}ulzSd_jg#|?ApKu;}tkxM$XO;{)+?j_r~b2TzP+~XVLkPdVeN8#r8k;d{cXW<$f@GwfZarXX_tjtvB<%&2L3LyFSm)+OK=zqW$YQ$E5Xhd#(>NXLuRdryNH6L!#U&V{yL0#J)AL@CM_7zu@aK^NkxhK&%6|?=g1XRT%c)()x0q`QVjrnN8pM!k^e5M?2<vw0jx^;orPo_m8AMs2<Px1I?fE;lh556MKKbsz*4NI`Mne!(8or!XEs{Pc*;AzSVcM<M}3gg&v>l1OFz@;6@J6&%Yr(6MGoqaXoCm!1}%FkJ5i}<}leQ8N#AZ&J$68?e&gX>LK-9OMX>f((^mz^VBaJ^{>j?QGexm2^znG#`DUoFBWC#Ke1bXz{tVYYyN}TWq*ms`2*EoC0}A+cwVcXf9dsPyY0{C+Zl5`j(Q&iSSg=r-l?9c&o7-XS-p6D*83#!{@L!6!A|+W<;13EeZj|>X&yRzs)uopFa6H>$z31m&(;r|-`wlL@fMi4q@IuSz*z69JmjNveH6d+c_K-*-?s;2wy!Uk?wi^k($DyUGV&8JN7d)Jr{wo&h5Oxu{$3_}pE&jVp6<gF%}?)-6Tbv-ypyurcV78y^YsE<57hsfaLnK'
WEIGHTS_B85 = 'c-o6fRR|DKWl3xd2n`Gk3k?kwb(tEXnz=};LnAUZG$bS>G}KiyG}JRNRKzhfG$cS&G;v~N<irpb2cZ?2N*t3EMMF7NxLi9kGF+9W3WSJ+q;!U<ih0gxSQy!)q&0OZ2LOzx9fb'
WIN_MOVES_B85 = 'c-jrk-%p!B003Z4Ixfd44InmNNPsNH2Ws}@mb(RUWqoL%S$qPc(I7vXQ_H2K?C#IszJK6bM$2#y=3uUpsh+mBJbh%-?PY@KU-9+gy$N^eG^yl;?W6PeVgK1Hx&E<Me3Z>$I_zar@7+d(p*;ZVIA}P3kb+8~q#C}BZa5C%61Z|~#-EYcclQ_Q{^afc<YNBk_Y^-b?c>>WP|x+SJsj$!dXeFT;!=Tg&W0`i6$hg_MM}MW5#Jm8R5hbY>RQzw6OaJC9LvX>qcdL~mq%9~!*K}?N37#ar)(WZlrdlIJgGxUJW&Q4&*2*boB3;A8655+Z|%AcTuYfT7I4uPW&X<WYbJJaV74$zt6ua%_Jlczc|Pr`K6omFp0E78pn5K`hjd<1P;~)HEJAe6vVv9;%RuG~wh%#}V~ez1zRFExTbgg^Mq;+e&^4cWmNboPD`j{^R;%jTL#WkgF49g<T{C9bhg@4=qOqvQHia6t7PR#f`Ty}cysC_fZZ<{MQEw;3ZrwARz&rtEZfatIWxBXph!Z)pipU7^g4-Bdxkn7!&^L%gMOI;(u!_mT)-}TXS)`d33?K)Ul)hC;ZU&qKpA*IrhcnH0vh0jQC>I$tKng2Ngn5_JD}CWXEI;0XEMB{3zbJjXD9S<J){~U(A&R2y<$T`VZE5pxnRc{^9=W<vHr1k-q<*g<^aS;F_L;lchv#H5oN-fkx0wg7{sCh1mJt'

def run():
    roots=decode_positions(ROOTS_B85)
    leaves=decode_positions(LEAVES_B85)
    check(len(roots)==18 and len(set(roots))==18, 'bad root count')
    check(len(leaves)==184 and len(set(leaves))==184, 'bad leaf count')
    for p in roots:
        check(p.bit_count()==8 and safe(p) and canonical(p)==p, 'bad root')
    for p in leaves:
        check(p.bit_count()==10 and safe(p) and canonical(p)==p, 'bad leaf')

    obligations=set().union(*(children(r) for r in roots))
    check(len(obligations)==387, 'wrong S9 boundary')
    sorted_obs=sorted(obligations)
    packed=decode(WEIGHTS_B85)
    check(len(packed)==(len(sorted_obs)+3)//4, 'bad weight size')
    weights={p:(packed[i//4]>>(2*(i%4)))&3 for i,p in enumerate(sorted_obs)}
    check(set(weights.values())<=set((0,1,2)), 'bad weight')
    check((sum(v==2 for v in weights.values()),sum(v==1 for v in weights.values()),sum(v==0 for v in weights.values()))==(81,203,103),'bad weight counts')
    check(packed[-1]>>6==0,'nonzero padding')
    halves={p for p,w in weights.items() if w==1}

    boundary=set().union(*(children(o) for o in obligations))
    check(len(boundary)==3044,'wrong S10 boundary')
    selected=set(leaves)
    check(selected<=boundary,'selected leaves not in boundary')
    coverage={p:{canonical(p^(1<<i)) for i in points(p)}&obligations for p in boundary}
    check(set().union(*(coverage[p] for p in selected))==obligations,'incomplete selected cover')

    # Prove a lower bound without classifying all 3,044 boundary positions.
    # For each candidate of dual weight > 1, verify it is WIN at S10.
    # Every other candidate satisfies the dual bound regardless of outcome.
    high=[]
    graph={p:set() for p in halves}
    for p in sorted(boundary):
        cs=coverage[p]
        w=sum(weights[q] for q in cs)
        if w>2:
            high.append(p)
            continue
        pair=list(cs&halves)
        if len(pair)==2:
            a,b=pair
            graph[a].add(b)
            graph[b].add(a)
    check(len(high)==672,'unexpected high-weight boundary')
    seen=set()
    sizes=[]
    for p in halves:
        if p in seen:continue
        todo=[p]
        seen.add(p)
        n=0
        while todo:
            v=todo.pop();n+=1
            for q in graph[v]-seen:
                seen.add(q);todo.append(q)
        sizes.append(n)
    check(sorted(sizes)==[13,19,46,125], 'half-weight component structure changed')
    lower=81+sum((n+1)//2 for n in sizes)
    check(lower==len(selected)==184,'global lower bound invalid')

    moves=decode(WIN_MOVES_B85)
    check(len(moves)==len(high),'bad WIN witness count')
    witness_states=0
    seen_s11=set()
    for p,q in zip(high,moves):
        check(q in legal(p),f'illegal WIN witness: {p:032x} {q}')
        child=canonical(p|(1<<q))
        if child in seen_s11:
            continue  # D4-symmetric S11 terminal position was already checked
        seen_s11.add(child)
        is_win,states=next_player_wins_at_s10(child)
        check(not is_win,f'bad WIN witness: {p:032x}')
        witness_states+=states
    check(len(seen_s11)==342,'unexpected S11 witness sharing')
    loss_states=0
    for p in selected:
        is_win,states=next_player_wins_at_s10(p)
        check(not is_win,f'bad LOSS leaf: {p:032x}')
        loss_states+=states
    check(loss_states==15290, 'terminal state cost changed')
    check(witness_states==7779, 'WIN witness terminal state cost changed')
    print(f'PASS: 18 S8 LOSS roots, 387 S9 obligations, 3044 S10 boundary positions')
    print(f'PASS: 672 high-weight S10 candidates are WIN (verified terminal witnesses)')
    print(f'PASS: 184 selected S10 LOSS leaves (terminal states={loss_states})')
    print(f'PASS: dual weights and components {sorted(sizes)} imply at least {lower} leaves')
    print(f'PASS: GLOBAL MINIMUM 184; terminal-checked positions {len(high)+len(selected)}/3044')
    print(f'PASS: unique S11 WIN-witness states={len(seen_s11)}, terminal states={witness_states}')

if __name__=='__main__':run()
