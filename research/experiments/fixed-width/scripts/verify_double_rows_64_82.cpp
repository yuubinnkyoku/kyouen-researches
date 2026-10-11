// Independent transposed-residue verifier for T(64..82)=16.
// Requires C++17 and 128-bit unsigned integers. K0369 supplies T(63)=16.
#include <bits/stdc++.h>
using namespace std; using U=__uint128_t;
int bc(U x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
vector<U> maximal(vector<U> v){sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());sort(v.begin(),v.end(),[](U a,U b){int ca=bc(a),cb=bc(b);return ca!=cb?ca>cb:a<b;});vector<U> out;for(U a:v){bool dominated=false;for(U b:out)if((a&b)==a){dominated=true;break;}if(!dominated)out.push_back(a);}return out;}
vector<U> via_transpose(int len,int p){vector<U> v; vector<unsigned long long> rowAllowed(len); for(int c=0;c<p;c++){for(int k=0;k<len;k++){int z=(2*k+c)%p;z=z*z%p;unsigned long long bits=0;for(int d=0;d<p;d++)bits|=1ULL<<((z+d*d)%p);rowAllowed[k]=bits;}for(int n=0;n<p;n++){U mask=0;for(int k=0;k<len;k++)if(rowAllowed[k]&(1ULL<<n))mask|=U(1)<<k;if(bc(mask)>=17&&(mask&1)&&((mask>>(len-1))&1))v.push_back(mask);}}return maximal(v);}
vector<int> circle_rows(int w,int c,int d){vector<int> out;for(int y=0;y<w;y++){long long z=1-4LL*(y*y+c*y+d);if(z<=0)continue;long long t=sqrtl(z);while(t*t<z)t++;while(t*t>z)t--;if(t*t==z&&(t&1)){long long x1=(-1-t)/2,x2=(-1+t)/2;assert(x1!=x2);assert(x1*x1+y*y+x1+c*y+d==0);assert(x2*x2+y*y+x2+c*y+d==0);out.push_back(y);}}return out;}
int main(){vector<int> mods={9,11,7,49,19,23,31,37,41,43,47,53};for(int w=64;w<=82;w++){for(int g=1;g*16<=w-1;g++)if((w-1)%g==0){int len=(w-1)/g+1;vector<U> states={((U(1)<<len)-1)};bool ok=false;for(int p:mods){if(gcd(p,g)!=1)continue;auto local=via_transpose(len,p);vector<U> candidates;for(U a:states)for(U b:local){U v=a&b;if(bc(v)>=17)candidates.push_back(v);}states=maximal(move(candidates));cout<<"CASE "<<w<<" "<<g<<" MOD "<<p<<" LOCAL "<<local.size()<<" STATES "<<states.size()<<"\n";if(states.empty()){ok=true;break;}}if(!ok){cerr<<"FAIL "<<w<<" "<<g<<"\n";return 1;}}cout<<"PASS "<<w<<"\n";}
assert(circle_rows(63,-47,0).size()==16);
assert((circle_rows(83,-105,-6)==vector<int>{0,1,5,6,9,12,19,23,28,30,42,50,55,63,75,77,82}));
cout<<"PASS T(83)=17 via witness and T(82)+1 bound\n";
}
