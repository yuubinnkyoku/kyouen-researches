// Independent integer audit of the sharpness witness; no generated input.
#include <array>
#include <cassert>
#include <iostream>
#include <set>
#include <tuple>
int main(){
 const std::array<int,5> b{-40,-32,-24,-16,0},c{-37,-35,-27,-5,13};
 std::set<std::tuple<int,int,int>> circles,through;
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)
 for(int k=0;k<5;k++)for(int l=k+1;l<5;l++){
  if(b[i]+b[j]!=c[k]+c[l])continue;
  int s=b[i]+b[j],d=c[k]*c[l]-b[i]*b[j],p=b[i]*b[j];
  circles.insert({s,d,p});
  if(23290+770*s+10*d+25*p==0)through.insert({s,d,p});
 }
 const std::set<std::tuple<int,int,int>> expected{{-72,15,1280},{-40,-209,384},{-32,135,0},{-24,-481,0}};
 assert(circles.size()==6&&through==expected);
 std::cout<<"six catalog circles; exactly four through P: PASS\n";
 const std::array<int,5> ib{-20,-10,0,5,20},ic{-15,-10,-5,0,10};
 circles.clear();through.clear();
 for(int i=0;i<5;i++)for(int j=i+1;j<5;j++)
 for(int k=0;k<5;k++)for(int l=k+1;l<5;l++){
  if(ib[i]+ib[j]!=ic[k]+ic[l])continue;
  int s=ib[i]+ib[j],d=ic[k]*ic[l]-ib[i]*ib[j],p=ib[i]*ib[j];
  circles.insert({s,d,p});
  if(200+6*d+20*s+5*p==0){
   assert((d-100)%10==0);int A=(d-100)/10,B=-s,C=p;
   assert(144+16+12*A-4*B+C==0);
   int nb=0,nc=0;
   for(int y:ib)nb+=y*y+B*y+C==0;
   for(int y:ic)nc+=100+y*y+10*A+B*y+C==0;
   assert(nb==2&&nc==2);through.insert({s,d,p});
  }
 }
 const std::set<std::tuple<int,int,int>> integer_expected{{-15,100,-100},{-10,0,0},{0,300,-400},{5,-50,0}};
 assert(circles.size()==9&&through==integer_expected);
 std::cout<<"nine catalog circles; exactly four through integer P: PASS\n";
}
