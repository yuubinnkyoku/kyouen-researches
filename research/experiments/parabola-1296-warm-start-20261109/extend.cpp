// Find direct integer-geometry blockers for single-point extensions of Q_p.
// Completeness uses the necessary parameter-sum condition (K0334).
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using I = __int128_t;
I determinant(const std::array<int,4>& q, int p) {
    I a[4][4];
    for(int i=0;i<4;i++) {
        I x=q[i], y=(x*x)%p;
        a[i][0]=1; a[i][1]=x; a[i][2]=y; a[i][3]=x*x+y*y;
    }
    std::array<int,4> perm={0,1,2,3}; I sum=0;
    do {
        int inv=0; I prod=1;
        for(int i=0;i<4;i++) {
            prod*=a[i][perm[i]];
            for(int j=i+1;j<4;j++) inv+=perm[i]>perm[j];
        }
        sum+=(inv%2?-prod:prod);
    } while(std::next_permutation(perm.begin(),perm.end()));
    return sum;
}
bool prime(int p) { if(p<2)return false; for(int d=2;1LL*d*d<=p;d++)if(p%d==0)return false;return true; }
int main(){
    int p,n;if(!(std::cin>>p>>n)||!prime(p)||p>100000||n<0||n>p)return 2;
    std::vector<int>s(n);for(int&x:s)if(!(std::cin>>x))return 2;
    if(!std::is_sorted(s.begin(),s.end())||std::adjacent_find(s.begin(),s.end())!=s.end())return 3;
    std::vector<bool> selected(p),blocked(p);
    for(int x:s){if(x<0||x>=p)return 3;selected[x]=true;}
    int missing=p-n,found=0;std::uint64_t triples=0,checked=0;
    std::vector<std::array<int,3>> witness(p);
    for(int i=0;i<n && found<missing;i++)for(int j=i+1;j<n && found<missing;j++)for(int k=j+1;k<n && found<missing;k++){
        ++triples;int d=(p-(s[i]+s[j]+s[k])%p)%p;
        if(selected[d]||blocked[d])continue;
        ++checked;
        if(determinant({s[i],s[j],s[k],d},p)==0){blocked[d]=true;witness[d]={s[i],s[j],s[k]};++found;}
    }
    std::cout<<"p "<<p<<" n "<<n<<" missing "<<missing<<" blocked "<<found<<" triples "<<triples<<" checked "<<checked<<'\n';
    for(int d=0;d<p;d++)if(!selected[d]){
        if(blocked[d])std::cout<<d<<' '<<witness[d][0]<<' '<<witness[d][1]<<' '<<witness[d][2]<<'\n';
        else std::cout<<d<<" OPEN\n";
    }
}
