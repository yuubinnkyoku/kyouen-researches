// For each missing point, find forbidden triples with empty common intersection.
// Such a certificate proves that deleting any one selected point cannot admit it.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using I=__int128_t;
I det(const std::array<int,4>&q,int p){
 I x[3],y[3],z[3],x0=q[3],y0=(x0*x0)%p,z0=x0*x0+y0*y0;
 for(int k=0;k<3;k++){I a=q[k],b=(a*a)%p;x[k]=a-x0;y[k]=b-y0;z[k]=a*a+b*b-z0;}
 return x[0]*(y[1]*z[2]-z[1]*y[2])-y[0]*(x[1]*z[2]-z[1]*x[2])+z[0]*(x[1]*y[2]-y[1]*x[2]);
}
bool prime(int p){if(p<2)return false;for(int d=2;1LL*d*d<=p;d++)if(p%d==0)return false;return true;}
int main(){
 int p,n;if(!(std::cin>>p>>n)||!prime(p)||p>100000||n<0||n>p)return 2;
 std::vector<int>s(n);for(int&x:s)if(!(std::cin>>x))return 2;
 if(!std::is_sorted(s.begin(),s.end())||std::adjacent_find(s.begin(),s.end())!=s.end())return 3;
 std::vector<bool>selected(p),done(p);for(int x:s){if(x<0||x>=p)return 3;selected[x]=true;}
 std::vector<std::vector<int>> common(p);std::vector<std::vector<std::array<int,3>>> witnesses(p);
 int missing=p-n,finished=0;std::uint64_t triples=0,checked=0;
 for(int i=0;i<n&&finished<missing;i++)for(int j=i+1;j<n&&finished<missing;j++)for(int k=j+1;k<n&&finished<missing;k++){
  ++triples;int d=(p-(s[i]+s[j]+s[k])%p)%p;if(selected[d]||done[d])continue;
  ++checked;if(det({s[i],s[j],s[k],d},p)!=0)continue;
  std::array<int,3> tri={s[i],s[j],s[k]};
  if(witnesses[d].empty()){common[d]={tri.begin(),tri.end()};witnesses[d].push_back(tri);}
  else{
   auto prior=common[d];common[d].erase(std::remove_if(common[d].begin(),common[d].end(),[&](int x){return x!=tri[0]&&x!=tri[1]&&x!=tri[2];}),common[d].end());
   if(common[d]!=prior)witnesses[d].push_back(tri);
  }
  if(common[d].empty()){done[d]=true;++finished;}
 }
 std::cout<<"p "<<p<<" n "<<n<<" missing "<<missing<<" blocked_after_one_deletion "<<finished<<" triples "<<triples<<" checked "<<checked<<'\n';
 for(int d=0;d<p;d++)if(!selected[d]){
  if(!done[d]){std::cout<<d<<" OPEN";for(int x:common[d])std::cout<<' '<<x;std::cout<<" |";for(auto t:witnesses[d])std::cout<<' '<<t[0]<<' '<<t[1]<<' '<<t[2];std::cout<<'\n';}
  else{std::cout<<d;for(auto t:witnesses[d])std::cout<<' '<<t[0]<<' '<<t[1]<<' '<<t[2];std::cout<<'\n';}
 }
}
