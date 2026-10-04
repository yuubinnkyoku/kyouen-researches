// Independent generic 4x4 Leibniz determinant. Search uses a translated
// 3x3 determinant; this verifier neither imports nor links the search code.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using I = __int128_t;
I determinant(const std::array<int,4>& q,int p){
    I matrix[4][4];
    for(int r=0;r<4;++r){
        I x=q[r],y=1LL*q[r]*q[r]%p;
        matrix[r][0]=1;matrix[r][1]=x;matrix[r][2]=y;
        matrix[r][3]=x*x+y*y;
    }
    std::array<int,4> perm={0,1,2,3}; I sum=0;
    do {
        int inversions=0;I product=1;
        for(int r=0;r<4;++r){
            product*=matrix[r][perm[r]];
            for(int s=r+1;s<4;++s)inversions+=perm[r]>perm[s];
        }
        sum+=(inversions%2?-product:product);
    }while(std::next_permutation(perm.begin(),perm.end()));
    return sum;
}
bool prime(int n){if(n<2)return false;for(int d=2;1LL*d*d<=n;++d)if(n%d==0)return false;return true;}
int main(int argc,char**argv){
    bool filtered=argc==2 && std::string(argv[1])=="--modular-filter";
    int p,n;
    while(std::cin>>p>>n){
        if(!prime(p) || p>100000 || n!=(p+3)/2)return 2;
        std::vector<int> ts(n);for(int&i:ts)std::cin>>i;
        if(!std::is_sorted(ts.begin(),ts.end()) || ts[0]<0 || ts.back()>=p)return 3;
        for(int i=1;i<n;++i)if(ts[i]==ts[i-1])return 3;
        std::uint64_t checked=0,covered=1ULL*n*(n-1)*(n-2)*(n-3)/24;
        if(filtered){
            // Completeness uses the proven quartic/Vandermonde condition:
            // a zero integer determinant entails sum(parameters)=0 mod p.
            // Enumerate every selected triple and its unique possible
            // fourth parameter; all untested quadruples are nonzero mod p.
            std::vector<bool> selected(p);for(int t:ts)selected[t]=true;
            for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c){
                int d=(-(ts[a]+ts[b]+ts[c])%p+p)%p;
                if(d<=ts[c] || !selected[d])continue;
                ++checked;if(determinant({ts[a],ts[b],ts[c],d},p)==0)return 4;
            }
        }else{
            for(int a=0;a<n;++a)for(int b=a+1;b<n;++b)for(int c=b+1;c<n;++c)for(int d=c+1;d<n;++d){
                ++checked;if(determinant({ts[a],ts[b],ts[c],ts[d]},p)==0)return 4;
            }
        }
        std::cout<<p<<' '<<n<<' '<<covered<<' '<<checked<<'\n';
    }
}
