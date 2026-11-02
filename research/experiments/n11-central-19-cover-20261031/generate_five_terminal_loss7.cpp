// Deterministic strategy generator for five selected 11x11 S7 positions.
// The independent verifier uses a separate 4x4 integer determinant.
// All generated strategy files must be audited before being called proofs.
#include <bits/stdc++.h>
using namespace std;
using U = unsigned __int128;
const int N = 121;
const U FULL = (U(1) << 121) - 1;
U forbidden[121 * 121 * 121];
int tx[8][121];
struct Entry { uint8_t result; uint8_t move; };
struct Hash {
    size_t operator()(U x) const noexcept {
        uint64_t lo = (uint64_t)x, hi = (uint64_t)(x >> 64);
        uint64_t z = lo ^ (hi * 0x9e3779b97f4a7c15ULL);
        z ^= z >> 30; z *= 0xbf58476d1ce4e5b9ULL;
        z ^= z >> 27; z *= 0x94d049bb133111ebULL;
        return z ^ (z >> 31);
    }
};
unordered_map<U, Entry, Hash> tt;
long long calls = 0, hits = 0;
chrono::steady_clock::time_point start_clock;
int secs = 30;
size_t maxstates = 1000000;
inline int id(int a, int b, int c) { return (a * 121 + b) * 121 + c; }
inline int det(int a, int b, int c, int d) {
    int ax = a % 11, ay = a / 11, bx = b % 11, by = b / 11;
    int cx = c % 11, cy = c / 11, dx = d % 11, dy = d / 11;
    int x1 = bx-ax, y1 = by-ay, z1 = bx*bx+by*by-ax*ax-ay*ay;
    int x2 = cx-ax, y2 = cy-ay, z2 = cx*cx+cy*cy-ax*ax-ay*ay;
    int x3 = dx-ax, y3 = dy-ay, z3 = dx*dx+dy*dy-ax*ax-ay*ay;
    return x1*(y2*z3-z2*y3) - y1*(x2*z3-z2*x3) + z1*(x2*y3-y2*x3);
}
void init() {
    for (int a=0;a<121;a++) for(int b=a+1;b<121;b++)
        for(int c=b+1;c<121;c++) {
            U mask=0;
            for(int d=0;d<121;d++)
                if(d!=a && d!=b && d!=c && det(a,b,c,d)==0)
                    mask |= U(1)<<d;
            forbidden[id(a,b,c)]=mask;
        }
    for(int p=0;p<121;p++) {
        int x=p%11,y=p/11;
        int xx[8]={x,10-y,10-x,y,10-x,10-y,x,y};
        int yy[8]={y,x,10-y,10-x,y,10-x,10-y,x};
        for(int t=0;t<8;t++) tx[t][p]=yy[t]*11+xx[t];
    }
}
inline int pts(U mask,int p[]) {
    int n=0;
    while(mask) {
        int i=((uint64_t)mask) ? __builtin_ctzll((uint64_t)mask)
             : 64+__builtin_ctzll((uint64_t)(mask>>64));
        p[n++]=i; mask&=mask-1;
    }
    return n;
}
inline U legal(U mask) {
    int p[121],n=pts(mask,p);
    U bad=mask;
    for(int i=0;i<n;i++) for(int j=i+1;j<n;j++)
        for(int k=j+1;k<n;k++) bad |= forbidden[id(p[i],p[j],p[k])];
    return FULL & ~bad;
}
inline U canon(U mask) {
    int p[121],n=pts(mask,p); U best=mask;
    for(int t=1;t<8;t++) {
        U q=0;
        for(int i=0;i<n;i++) q |= U(1)<<tx[t][p[i]];
        if(q<best) best=q;
    }
    return best;
}
int dfs(U mask) {
    calls++;
    if((calls & 65535)==0 &&
       (tt.size()>maxstates ||
        chrono::duration_cast<chrono::seconds>(
            chrono::steady_clock::now()-start_clock).count()>secs))
        throw runtime_error("budget exceeded");
    U cm=canon(mask);
    auto it=tt.find(cm);
    if(it!=tt.end()) { hits++; return it->second.result; }
    U moves=legal(mask);
    if(!moves) { tt.emplace(cm,Entry{0,255}); return 0; }
    vector<pair<int,int>> opts;
    while(moves) {
        int m=((uint64_t)moves) ? __builtin_ctzll((uint64_t)moves)
             : 64+__builtin_ctzll((uint64_t)(moves>>64));
        moves&=moves-1;
        U child=mask|(U(1)<<m), c=canon(child);
        auto z=tt.find(c);
        U lm=legal(child);
        int score=(z!=tt.end() ? (z->second.result==0?-100000:100000)
                  : __builtin_popcountll((uint64_t)lm)
                    +__builtin_popcountll((uint64_t)(lm>>64)));
        opts.push_back({score,m});
    }
    sort(opts.begin(),opts.end());
    for(auto [score,m]:opts) {
        if(dfs(mask|(U(1)<<m))==0) {
            tt.emplace(cm,Entry{1,(uint8_t)m});
            return 1;
        }
    }
    tt.emplace(cm,Entry{0,255});
    return 0;
}
string hex32(U x) {
    string s(32,'0');
    for(int i=31;i>=0;i--) {
        s[i]="0123456789abcdef"[(int)(x&15)]; x>>=4;
    }
    return s;
}
unordered_set<U,Hash> reached;
map<U,int> strategy;
size_t terminals=0,allmoves=0;
int minTerminal=100,maxTerminal=0;
void emit(U mask,int depth) {
    if(!reached.insert(mask).second) return;
    U moves=legal(mask);
    if(!moves) {
        if((depth&1)==0) throw runtime_error("winner unable to move");
        terminals++;
        int n=__builtin_popcountll((uint64_t)mask)
             +__builtin_popcountll((uint64_t)(mask>>64));
        minTerminal=min(minTerminal,n);
        maxTerminal=max(maxTerminal,n);
        return;
    }
    auto it=tt.find(canon(mask));
    if(it==tt.end() || it->second.result!=(depth%2==0?1:0))
        throw runtime_error("missing or inconsistent TT outcome");
    if((depth&1)==0) {
        int chosen=-1; U rem=moves;
        while(rem) {
            int m=((uint64_t)rem) ? __builtin_ctzll((uint64_t)rem)
                 : 64+__builtin_ctzll((uint64_t)(rem>>64));
            rem&=rem-1;
            auto child=tt.find(canon(mask|(U(1)<<m)));
            if(child!=tt.end() && child->second.result==0) {
                chosen=m; break;
            }
        }
        if(chosen<0) throw runtime_error("no certified winning move");
        strategy.emplace(mask,chosen);
        emit(mask|(U(1)<<chosen),depth+1);
    } else {
        while(moves) {
            int m=((uint64_t)moves) ? __builtin_ctzll((uint64_t)moves)
                 : 64+__builtin_ctzll((uint64_t)(moves>>64));
            moves&=moves-1; allmoves++;
            emit(mask|(U(1)<<m),depth+1);
        }
    }
}
U parse(const string &s) {
    if(s.size()!=32) throw runtime_error("root must have 32 hex digits");
    U x=0;
    for(char c:s) {
        if(!isxdigit((unsigned char)c)) throw runtime_error("bad root hex");
        x=x*16+(c<='9'?c-'0':tolower(c)-'a'+10);
    }
    return x;
}
int main(int argc,char**argv) {
    if(argc!=3) { cerr<<"usage: generator ROOT_HEX CERT_OUT\n"; return 2; }
    try {
        U root=parse(argv[1]);
        int n=__builtin_popcountll((uint64_t)root)
             +__builtin_popcountll((uint64_t)(root>>64));
        if(n!=7 || root>>121) throw runtime_error("invalid seven-stone root");
        init();
        start_clock=chrono::steady_clock::now();
        int result=dfs(root);
        if(result!=1) throw runtime_error("root not proved WIN for player to move");
        emit(root,0);
        ofstream out(argv[2]);
        if(!out) throw runtime_error("cannot write certificate");
        out<<"n11-terminal-strategy-v1 original_first_LOSS7 second_to_move_WIN\n";
        out<<"root "<<hex32(root)<<"\n";
        for(auto [board,m]:strategy) out<<hex32(board)<<" "<<m<<"\n";
        out.close();
        if(!out) throw runtime_error("certificate write failure");
        cout<<"root="<<hex32(root)<<" states="<<tt.size()
            <<" winner_states="<<strategy.size()
            <<" reachable="<<reached.size()<<" terminals="<<terminals
            <<" opponent_edges="<<allmoves
            <<" terminal_stones="<<minTerminal<<"-"<<maxTerminal<<"\n";
        return 0;
    } catch(const exception &e) {
        cerr<<"UNKNOWN / GENERATION FAILED: "<<e.what()<<"\n";
        return 1;
    }
}
