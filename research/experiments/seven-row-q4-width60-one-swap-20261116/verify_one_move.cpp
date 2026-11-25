// Complete one-for-one relocation audit for two 7-row q=4 seed witnesses.
// Safety and blocking use exact integer cross products and 4x4 determinants.
#include <bits/stdc++.h>
using namespace std;
struct P { int x,y; };
long long cross(P a,P b,P c) {
    return 1LL*(b.x-a.x)*(c.y-a.y)-1LL*(b.y-a.y)*(c.x-a.x);
}
bool forbidden4(P a,P b,P c,P d) {
    if (cross(a,b,c)==0 && cross(a,b,d)==0) return true;
    long long ax=b.x-a.x, ay=b.y-a.y;
    long long az=1LL*b.x*b.x+1LL*b.y*b.y-1LL*a.x*a.x-1LL*a.y*a.y;
    long long bx=c.x-a.x, by=c.y-a.y;
    long long bz=1LL*c.x*c.x+1LL*c.y*c.y-1LL*a.x*a.x-1LL*a.y*a.y;
    long long cx=d.x-a.x, cy=d.y-a.y;
    long long cz=1LL*d.x*d.x+1LL*d.y*d.y-1LL*a.x*a.x-1LL*a.y*a.y;
    return ax*(by*cz-bz*cy)-ay*(bx*cz-bz*cx)+az*(bx*cy-by*cx)==0;
}
struct Counts { string name; int native_width; long long candidates=0,safe=0,safe_maximal=0; };
vector<P> base53() {
    return {{21,0},{23,0},{26,0},{18,1},{27,1},{39,1},{14,2},{28,2},{46,2},
            {25,3},{30,3},{39,3},{18,4},{36,4},{43,4},{13,5},{27,5},{35,5},
            {14,6},{42,6}};
}
vector<P> foundB() {
    return {{21,0},{23,0},{26,0},{18,1},{27,1},{39,1},{14,2},{46,2},{25,3},
            {30,3},{39,3},{18,4},{43,4},{13,5},{27,5},{35,5},{14,6},{42,6},
            {56,2},{7,4}};
}
array<int,7> row_counts(const vector<P>& s) {
    array<int,7> r{}; for (P p:s) ++r[p.y]; return r;
}
bool safe_set(const vector<P>& s) {
    for (int a=0;a<(int)s.size();++a)
      for (int b=a+1;b<(int)s.size();++b)
       for (int c=b+1;c<(int)s.size();++c)
        for (int d=c+1;d<(int)s.size();++d)
         if (forbidden4(s[a],s[b],s[c],s[d])) return false;
    return true;
}
bool maximal_row(const vector<P>& s,int width,int row) {
    for (int x=0;x<width;++x) {
        bool occupied=false; for (P p:s) if (p.x==x && p.y==row) { occupied=true; break; }
        if (occupied) continue;
        P q{x,row}; bool blocked=false;
        for (int a=0;a<(int)s.size() && !blocked;++a)
         for (int b=a+1;b<(int)s.size() && !blocked;++b)
          for (int c=b+1;c<(int)s.size();++c)
           if (forbidden4(q,s[a],s[b],s[c])) { blocked=true; break; }
        if (!blocked) return false;
    }
    return true;
}
Counts audit(const string& name,int native_width,const vector<P>& seed) {
    if (seed.size()!=20 || row_counts(seed)!=array<int,7>{3,3,3,3,3,3,2} || !safe_set(seed))
        throw runtime_error("invalid seed: "+name);
    if (!maximal_row(seed,native_width,6)) throw runtime_error("seed not maximal at native width: "+name);
    Counts out{name,native_width};
    bool occupied[7][60]={}; for(P p:seed) occupied[p.y][p.x]=true;
    for (int rem=0;rem<20;++rem) {
        auto rows=row_counts(seed); --rows[seed[rem].y];
        for (int ay=0;ay<7;++ay) for (int x=0;x<60;++x) {
            if (occupied[ay][x]) continue;
            ++rows[ay]; bool profile=(rows==array<int,7>{3,3,3,3,3,3,2}); --rows[ay];
            if (!profile) continue;
            vector<P> cand; cand.reserve(20);
            for(int i=0;i<20;++i) if(i!=rem) cand.push_back(seed[i]);
            cand.push_back({x,ay}); ++out.candidates;
            // The seed is safe, so every new forbidden quadruple must contain the added point.
            bool safe=true;
            for(int a=0;a<19 && safe;++a)
             for(int b=a+1;b<19 && safe;++b)
              for(int c=b+1;c<19;++c)
               if(forbidden4(cand[19],cand[a],cand[b],cand[c])) { safe=false; break; }
            if(!safe) continue;
            ++out.safe;
            auto cr=row_counts(cand);
            int deficient=-1; for(int y=0;y<7;++y) if(cr[y]==2) deficient=y;
            if(deficient<0) throw runtime_error("missing deficient row");
            if(maximal_row(cand,60,deficient)) ++out.safe_maximal;
        }
    }
    return out;
}
int main() {
    vector<Counts> results;
    results.push_back(audit("base53",53,base53()));
    results.push_back(audit("foundB_7x59",59,foundB()));
    cout << "{\n  \"method\": \"exact integer cross products and 4x4 determinants\",\n"
         << "  \"target_width\": 60,\n  \"required_row_profile\": [3,3,3,3,3,3,2],\n  \"results\": [\n";
    for(size_t i=0;i<results.size();++i){
        const auto&r=results[i]; if(i) cout << ",\n";
        cout << "    {\"seed\":\""<<r.name<<"\",\"native_width\":"<<r.native_width
             <<",\"candidates\":"<<r.candidates<<",\"safe\":"<<r.safe
             <<",\"safe_maximal\":"<<r.safe_maximal<<"}";
    }
    bool all_zero=all_of(results.begin(),results.end(),[](const Counts& r){return r.safe_maximal==0;});
    cout << "\n  ],\n  \"all_safe_maximal_counts_zero\": " << (all_zero?"true":"false") << "\n}\n";
}
