// Deterministic strategy generator for one n11 S6 root.
// Solver geometry: 3x3 determinant after subtracting the first circle row.
// The independent verifier uses a direct 4x4 Laplace expansion instead.
// This generator is not itself the proof checker.
#include <bits/stdc++.h>
using namespace std;
using U = unsigned __int128;
constexpr int N = 121;
struct Hash {
  size_t operator()(U v) const noexcept {
    uint64_t a = (uint64_t)v, b = (uint64_t)(v >> 64);
    return a * 0x9e3779b97f4a7c15ULL ^
      (b + 0x9e3779b97f4a7c15ULL + (a << 6) + (a >> 2));
  }
};
vector<U> forbidden;
unordered_map<U, int8_t, Hash> memo;
unordered_map<U, uint8_t, Hash> chosen;
uint64_t visited = 0, hits = 0;
int triple_index(int a, int b, int c) { return (a*N+b)*N+c; }
int det3(int a,int b,int c,int d,int e,int f,int g,int h,int i) {
  return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g);
}
int circle_det(int a,int b,int c,int d) {
  int x1=a%11,y1=a/11,x2=b%11,y2=b/11,x3=c%11,y3=c/11,x4=d%11,y4=d/11;
  return det3(x2-x1,y2-y1,x2*x2+y2*y2-x1*x1-y1*y1,
              x3-x1,y3-y1,x3*x3+y3*y3-x1*x1-y1*y1,
              x4-x1,y4-y1,x4*x4+y4*y4-x1*x1-y1*y1);
}
vector<int> points(U b) {
  vector<int> out;
  while (b) {
    int p = (uint64_t)b ? __builtin_ctzll((uint64_t)b)
                         : 64 + __builtin_ctzll((uint64_t)(b >> 64));
    out.push_back(p);
    b &= b - 1;
  }
  return out;
}
U legal(U b) {
  auto ps = points(b);
  U bad = b;
  for (int i=0;i<(int)ps.size();i++)
    for (int j=i+1;j<(int)ps.size();j++)
      for (int k=j+1;k<(int)ps.size();k++)
        bad |= forbidden[triple_index(ps[i],ps[j],ps[k])];
  return ((((U)1)<<121)-1) & ~bad;
}
string hex32(U b) {
  char z[33];
  for (int i=31;i>=0;i--) {
    z[i] = "0123456789abcdef"[(int)(b&15)];
    b >>= 4;
  }
  z[32] = 0;
  return z;
}
U parse_hex(const string &s) {
  if (s.size()!=32) throw runtime_error("invalid root length");
  U v=0;
  for (char c:s) {
    if (c<'0'||(c>'9'&&c<'a')||c>'f') throw runtime_error("invalid root hex");
    v=(v<<4)|((c<='9')?c-'0':c-'a'+10);
  }
  return v;
}
int solve(U b) {
  auto it=memo.find(b);
  if (it!=memo.end()) { hits++; return it->second; }
  if (++visited>12000000) throw runtime_error("node budget exceeded");
  U moves=legal(b);
  if (!moves) { memo[b]=0; return 0; }
  vector<pair<int,int>> candidates;
  while (moves) {
    int p=(uint64_t)moves ? __builtin_ctzll((uint64_t)moves)
                          : 64+__builtin_ctzll((uint64_t)(moves>>64));
    moves &= moves-1;
    U child_moves=legal(b|(((U)1)<<p));
    int score=__builtin_popcountll((uint64_t)child_moves)
              +__builtin_popcountll((uint64_t)(child_moves>>64));
    candidates.push_back({score,p});
  }
  sort(candidates.begin(),candidates.end());
  for (auto [score,p]:candidates) {
    if (!solve(b|(((U)1)<<p))) {
      memo[b]=1;
      chosen[b]=p;
      return 1;
    }
  }
  memo[b]=0;
  return 0;
}
void emit(U b, unordered_set<U,Hash>&seen, ofstream&out) {
  if (!seen.insert(b).second) return;
  U moves=legal(b);
  if (!moves) return;
  if (memo.at(b)==1) {
    auto it=chosen.find(b);
    if (it==chosen.end()) throw runtime_error("missing strategy move");
    int p=it->second;
    out<<hex32(b)<<" "<<p<<"\n";
    emit(b|(((U)1)<<p),seen,out);
  } else {
    while (moves) {
      int p=(uint64_t)moves ? __builtin_ctzll((uint64_t)moves)
                            : 64+__builtin_ctzll((uint64_t)(moves>>64));
      moves &= moves-1;
      emit(b|(((U)1)<<p),seen,out);
    }
  }
}
int main(int argc,char**argv) {
  if (argc!=3) { cerr<<"usage: generator root-hex output-path\n"; return 1; }
  forbidden.resize(N*N*N);
  for (int a=0;a<N;a++)
    for (int b=a+1;b<N;b++)
      for (int c=b+1;c<N;c++) {
        U f=0;
        for (int d=0;d<N;d++)
          if (d!=a&&d!=b&&d!=c&&circle_det(a,b,c,d)==0)
            f|=((U)1)<<d;
        forbidden[triple_index(a,b,c)]=f;
      }
  U root=parse_hex(argv[1]);
  if ((hex32(root)!="00000000000200801002000081000000"
       && hex32(root)!="00000000000000203808000000000020")
      || points(root).size()!=6) throw runtime_error("unexpected root");
  if (solve(root)!=1) throw runtime_error("root was not proved winning");
  ofstream out(argv[2]);
  out<<"# n11 strategy root="<<hex32(root)
     <<" player-to-move WIN, P nodes expand all legal children\n";
  unordered_set<U,Hash> seen;
  emit(root,seen,out);
  cerr<<"nodes="<<visited<<" hits="<<hits
      <<" reached="<<seen.size()<<" strategy_rows="<<chosen.size()<<"\n";
}