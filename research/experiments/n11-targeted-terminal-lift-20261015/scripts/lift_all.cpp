#include <sstream>
// Independent integer-geometry audit for n11 S10(WIN)->S9(WIN)->S8(WIN).
// Does not trust Python's legal-move or D4 implementation.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using U=unsigned __int128;
U parse(const std::string& s){U v=0; if(s.size()!=32)throw std::runtime_error("bad hex width"); for(char c:s){int n=(c>='0'&&c<='9')?c-'0':(c>='a'&&c<='f')?c-'a'+10:-1;if(n<0)throw std::runtime_error("bad hex");v=(v<<4)|n;}return v;}
std::string hex32(U v){const char* digits="0123456789abcdef";std::string s(32,'0');for(int i=31;i>=0;i--){s[i]=digits[int(v&15)];v>>=4;}return s;}
int pc(U s){int n=0;while(s){s&=s-1;++n;}return n;}
std::vector<int> bits(U s){std::vector<int> r;for(int p=0;p<121;p++)if((s>>p)&1)r.push_back(p);return r;}
std::array<long long,3> v(int p){int x=p%11,y=p/11;return {x,y,x*x+y*y};}
long long det(int a,int b,int c,int d){auto A=v(a),B=v(b),C=v(c),D=v(d);long long x=A[0]-D[0],y=A[1]-D[1],z=A[2]-D[2],X=B[0]-D[0],Y=B[1]-D[1],Z=B[2]-D[2],u=C[0]-D[0],w=C[1]-D[1],t=C[2]-D[2];return x*(Y*t-Z*w)-y*(X*t-Z*u)+z*(X*w-Y*u);}
bool safe(U s){auto a=bits(s);for(size_t i=0;i<a.size();i++)for(size_t j=i+1;j<a.size();j++)for(size_t k=j+1;k<a.size();k++)for(size_t l=k+1;l<a.size();l++)if(!det(a[i],a[j],a[k],a[l]))return false;return true;}
std::vector<int> legal(U s){auto a=bits(s);std::vector<int> r;for(int p=0;p<121;p++){if((s>>p)&1)continue;bool ok=true;for(size_t i=0;i<a.size()&&ok;i++)for(size_t j=i+1;j<a.size()&&ok;j++)for(size_t k=j+1;k<a.size();k++)if(!det(a[i],a[j],a[k],p)){ok=false;break;}if(ok)r.push_back(p);}return r;}
U canon(U s){U best=s;auto a=bits(s);for(int t=1;t<8;t++){U m=0;for(int p:a){int x=p%11,y=p/11;int X,Y;switch(t){case 1:X=10-y;Y=x;break;case 2:X=10-x;Y=10-y;break;case 3:X=y;Y=10-x;break;case 4:X=10-x;Y=y;break;case 5:X=10-y;Y=10-x;break;case 6:X=x;Y=10-y;break;default:X=y;Y=x;}m|=U(1)<<(11*Y+X);}if(m<best)best=m;}return best;}
std::set<U> load(const std::string& p){std::ifstream f(p);if(!f)throw std::runtime_error("cannot open "+p);std::set<U> s;std::string h;while(f>>h){U m=parse(h);if(!s.insert(m).second)throw std::runtime_error("duplicate in "+p);}return s;}


int main(int argc,char**argv){try{
 if(argc!=8)throw std::runtime_error("usage: lift_all cache prior_s8_win prior_s8_loss prior_s7_loss output_s7 output_s8");
 std::ifstream f(argv[1]);std::string h,z;std::set<U> win,loss;
 while(f>>h>>z){U m=parse(h);if(z=="WIN")win.insert(m);else if(z=="LOSS")loss.insert(m);else throw std::runtime_error("invalid verdict");}
 auto oldwin=load(argv[2]);auto oldloss=load(argv[3]);
 std::set<U> known7loss;std::ifstream l(argv[4]);std::string line;
 while(std::getline(l,line)){if(line.empty()||line[0]=='#')continue;std::istringstream ss(line);ss>>h;known7loss.insert(parse(h));}
 std::set<U> candidate9;
 for(U s:win){if(pc(s)!=10||canon(s)!=s||!safe(s))throw std::runtime_error("invalid WIN S10");for(int p:bits(s))candidate9.insert(canon(s^(U(1)<<p)));}
 std::set<U> won9;
 for(U s:candidate9){if(pc(s)!=9||!safe(s))throw std::runtime_error("bad S9");bool allwin=true;auto moves=legal(s);if(moves.empty())continue;
  for(int p:moves)if(!win.count(canon(s|(U(1)<<p)))){allwin=false;break;}
  if(allwin)won9.insert(s);
 }
 std::set<U> won8=oldwin;
 for(U s:won9)for(int p:bits(s))won8.insert(canon(s^(U(1)<<p)));
 for(U s:won8)if(oldloss.count(s))throw std::runtime_error("S8 WIN/LOSS conflict");
 std::set<U> candidate7,won7;
 for(U s:won8)for(int p:bits(s))candidate7.insert(canon(s^(U(1)<<p)));
 for(U s:candidate7){bool allwin=true;for(int p:legal(s))if(!won8.count(canon(s|(U(1)<<p)))){allwin=false;break;}
  if(allwin)won7.insert(s);
 }
 for(U s:won7)if(known7loss.count(s))throw std::runtime_error("S7 WIN/LOSS conflict");
 std::ofstream o(argv[5]);for(U s:won7)o<<hex32(s)<<"\n";
 std::ofstream o8(argv[6]);for(U s:won8)o8<<hex32(s)<<"\n";
 std::ofstream o9(argv[7]);for(U s:won9)o9<<hex32(s)<<"\n";
 std::cout<<"S10WIN="<<win.size()<<" S10LOSS="<<loss.size()<<" S9candidate="<<candidate9.size()<<" S9WIN="<<won9.size()<<" S8WIN="<<won8.size()<<" S7candidate="<<candidate7.size()<<" S7WIN="<<won7.size()<<" conflicts=0\n";
}catch(const std::exception& e){std::cerr<<"FAIL "<<e.what()<<"\n";return 1;}}
