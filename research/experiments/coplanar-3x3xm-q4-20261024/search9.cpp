#include <bits/stdc++.h>
using namespace std;
struct P{int x,y,z;};P p[9];int m;long long calls=0;bool found=false;
int det(P a,P b,P c,P d){int x=b.x-a.x,y=b.y-a.y,z=b.z-a.z;int X=c.x-a.x,Y=c.y-a.y,Z=c.z-a.z;int xx=d.x-a.x,yy=d.y-a.y,zz=d.z-a.z;return x*(Y*zz-Z*yy)-y*(X*zz-Z*xx)+z*(X*yy-Y*xx);}
void dfs(int i){if(found)return;if(i==9){found=true;return;}int x=i/3,y=i%3;for(int z=0;z<m;z++){p[i]={x,y,z};bool ok=true;for(int a=0;a<i&&ok;a++)for(int b=a+1;b<i&&ok;b++)for(int c=b+1;c<i&&ok;c++)if(det(p[a],p[b],p[c],p[i])==0)ok=false;calls++;if(ok){dfs(i+1);if(found)return;}}}
int main(int argc,char**argv){if(argc!=2)return 2;m=atoi(argv[1]);dfs(0);cout<<"m="<<m<<" found="<<found<<" attempts="<<calls<<"\n";if(found)for(int i=0;i<9;i++)cout<<"("<<p[i].x<<","<<p[i].y<<","<<p[i].z<<") ";cout<<"\n";}
