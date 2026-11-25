// Search two additions after one deletion, using open candidates from two_add.cpp.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using I=__int128_t;
I det(const std::array<int,4>&q,int p){
 I x[3],y[3],z[3],x0=q[3],y0=(x0*x0)%p,z0=x0*x0+y0*y0;
 for(int k=0;k<3;k++){I a=q[k],b=(a*a)%p;x[k]=a-x0;y[k]=b-y0;z[k]=a*a+b*b-z0;}
 return x[0]*(y[1]*z[2]-z[1]*y[2])-y[0]*(x[1]*z[2]-z[1]*x[2])+z[0]*(x[1]*y[2]-y[1]*x[2]);
}
int main(int argc,char**argv){
 if(argc!=4)return 2;std::ifstream c(argv[1]),f(argv[2]);std::ofstream proof(argv[3]);int p,n;if(!proof||!(c>>p>>n)||p!=2647||n!=1303)return 2;
 std::vector<int>s(n);std::vector<bool>selected(p);for(int&x:s){if(!(c>>x)||x<0||x>=p||selected[x])return 2;selected[x]=true;}
 std::string line;std::getline(f,line);std::map<int,std::vector<int>> groups;
 while(std::getline(f,line)){std::istringstream in(line);int point;std::string state;if(!(in>>point>>state))return 2;
  if(state!="OPEN")continue;int remove;while(in>>remove){if(!selected[remove]||selected[point])return 2;groups[remove].push_back(point);}}
 long long pairs=0,detchecks=0;
 for(auto &[remove,v]:groups){std::sort(v.begin(),v.end());v.erase(std::unique(v.begin(),v.end()),v.end());
  for(size_t i=0;i<v.size();i++)for(size_t j=i+1;j<v.size();j++){
   ++pairs;int a=v[i],b=v[j];bool forbidden=false;
   for(int t:s){if(t==remove)continue;int u=(p-(a+b+t)%p)%p;
    if(u<=t||u==remove||!selected[u])continue;
    ++detchecks;if(det({a,b,t,u},p)==0){forbidden=true;proof<<remove<<' '<<a<<' '<<b<<' '<<t<<' '<<u<<'\n';break;}
   }
   if(!forbidden){std::set<int>out(s.begin(),s.end());out.erase(remove);out.insert(a);out.insert(b);
    if(out.size()!=1304)return 3;std::cerr<<"candidate remove="<<remove<<" add="<<a<<","<<b<<" tested_pairs="<<pairs<<" determinants="<<detchecks<<'\n';
    std::cout<<p<<' '<<out.size()<<'\n';bool first=true;for(int x:out){if(!first)std::cout<<' ';first=false;std::cout<<x;}std::cout<<'\n';return 0;}
  }
 }
 proof.close();if(!proof)return 3;
 std::cerr<<"no two-add candidate; tested_pairs="<<pairs<<" determinants="<<detchecks<<'\n';return 0;
}
