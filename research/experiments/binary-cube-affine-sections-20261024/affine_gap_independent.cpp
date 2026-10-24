// Independent finite-field RREF audit of Boolean-cube affine sections.
// For d<=5 all integer minors have |det|<=6^3=216<1009.
#include <array>
#include <cassert>
#include <functional>
#include <iostream>
#include <map>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;
constexpr int P=1009;
int power(int a,int n){int r=1;for(;n;n>>=1,a=a*a%P)if(n&1)r=r*a%P;return r;}
using Row=array<int,7>;
struct Basis {
    array<Row,7> r{};int piv[7]{},rank=0,d=0;
    explicit Basis(int dim):d(dim){}
    void add(Row a){
        for(int i=0;i<rank;i++){int c=a[piv[i]];if(c)for(int j=0;j<=d;j++)a[j]=(a[j]-c*r[i][j]%P+P)%P;}
        int p=-1;for(int j=0;j<=d;j++)if(a[j]){p=j;break;}if(p<0)return;
        int inv=power(a[p],P-2);for(int j=0;j<=d;j++)a[j]=a[j]*inv%P;
        int ins=0;while(ins<rank&&piv[ins]<p)ins++;
        for(int i=rank;i>ins;i--){r[i]=r[i-1];piv[i]=piv[i-1];}
        r[ins]=a;piv[ins]=p;rank++;
        for(int i=0;i<rank;i++)if(i!=ins){int c=r[i][p];if(c)for(int j=0;j<=d;j++)r[i][j]=(r[i][j]-c*r[ins][j]%P+P)%P;}
    }
    bool contains(Row a)const{
        for(int i=0;i<rank;i++){int c=a[piv[i]];if(c)for(int j=0;j<=d;j++)a[j]=(a[j]-c*r[i][j]%P+P)%P;}
        for(int j=0;j<=d;j++)if(a[j])return false;
        return true;
    }
    string key()const{
        string s;for(int i=0;i<rank;i++)for(int j=0;j<=d;j++){s+=char(r[i][j]&255);s+=char(r[i][j]>>8);}
        return s;
    }
};
int main(){
    for(auto [d,k]:vector<pair<int,int>>{{3,2},{4,2},{4,3},{5,2},{5,3},{5,4}}){
        int n=1<<d;vector<Row> pts(n);
        for(int v=0;v<n;v++){pts[v][0]=1;for(int j=0;j<d;j++)pts[v][j+1]=(v>>j)&1;}
        unordered_set<string> seen;map<int,long long> counts;map<string,long long> six_types;vector<int> comb(k+1);
        function<void(int,int)> dfs=[&](int pos,int start){
            if(pos==k+1){
                Basis b(d);for(int v:comb)b.add(pts[v]);
                if(b.rank!=k+1)return;
                if(!seen.insert(b.key()).second)return;
                vector<int> section;
                for(int v=0;v<n;v++)if(b.contains(pts[v]))section.push_back(v);
                int c=(int)section.size();
                if(k==3&&c==6){
                    map<int,int> mids;
                    for(int i=0;i<6;i++)for(int j=i+1;j<6;j++){
                        int code=0,scale=1;
                        for(int z=0;z<d;z++){
                            code+=(((section[i]>>z)&1)+((section[j]>>z)&1))*scale;
                            scale*=3;
                        }
                        mids[code]++;
                    }
                    int multiplicity=0;
                    for(auto [code,m]:mids)if(m>multiplicity)multiplicity=m;
                    assert(multiplicity==2||multiplicity==3);
                    six_types[multiplicity==3?"octahedron":"prism"]++;
                }
                counts[c]++;return;
            }
            for(int v=start;v<=n-(k+1-pos);v++){comb[pos]=v;dfs(pos+1,v+1);}
        };
        dfs(0,0);
        long long total=0;
        for(auto [t,count]:counts){assert(t==(1<<k)||t<=3*(1<<(k-2)));total+=count;}
        assert(total==(long long)seen.size());
        assert(counts[3*(1<<(k-2))]>0);
        if(k==3&&(d==4||d==5)){
            long long prism=d==4?32:960,octahedron=d==4?8:240;
            assert(six_types["prism"]==prism&&six_types["octahedron"]==octahedron);
            cout<<"six_point_sections d="<<d<<" prism="<<prism<<" octahedron="<<octahedron<<"\n";
        }
        if(d==5&&k==3){
            assert(counts[4]==3840&&counts[5]==480&&counts[6]==1200&&counts[8]==260);
            assert(counts[5]+6*counts[6]+56*counts[8]==22240);
        }
        cout<<"d="<<d<<" k="<<k<<" flats="<<seen.size()<<" sizes=";
        for(auto [t,count]:counts)cout<<t<<":"<<count<<" ";
        cout<<"\n";
    }
}
