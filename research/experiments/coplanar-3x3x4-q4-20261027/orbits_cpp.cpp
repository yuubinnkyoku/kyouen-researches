// Fast C++ port of orbits_top.py: top-layer orbit census for the 3x3xm
// coplanar board under D4 (square cross-section) x Z2 (length flip),
// order 16. Same point labelling (itertools.product order: index
// (x*3+y)*m+z), same canonical-representative convention (minimum image),
// same JSON output format. Validated by reproducing orbits_m9.json
// byte-for-byte from the enum3 m=9 top-layer dump.
// Usage: orbits_cpp <m> <dumpfile>  (JSON on stdout)
#include <bits/stdc++.h>
using namespace std;
int main(int argc,char**argv){
    int m=atoi(argv[1]); int N=9*m;
    // square maps, same list/order as orbits_top.py
    function<pair<int,int>(int,int)> sq[8]={
        [](int x,int y){return make_pair(x,y);},
        [](int x,int y){return make_pair(x,2-y);},
        [](int x,int y){return make_pair(2-x,y);},
        [](int x,int y){return make_pair(2-x,2-y);},
        [](int x,int y){return make_pair(y,x);},
        [](int x,int y){return make_pair(y,2-x);},
        [](int x,int y){return make_pair(2-y,x);},
        [](int x,int y){return make_pair(2-y,2-x);}};
    int trans[16][99];
    int ti=0;
    for(int f=0;f<8;f++)for(int zf=0;zf<2;zf++,ti++){
        for(int x=0;x<3;x++)for(int y=0;y<3;y++)for(int z=0;z<m;z++){
            auto [nx,ny]=sq[f](x,y); int nz=zf?(m-1-z):z;
            trans[ti][(x*3+y)*m+z]=(nx*3+ny)*m+nz;
        }
    }
    vector<unsigned __int128> masks; masks.reserve(1<<20);
    FILE*fp=fopen(argv[2],"r"); if(!fp){perror("open");return 1;}
    unsigned long long hi,lo;
    while(fscanf(fp,"%llu %llu",&hi,&lo)==2)  // enum3 dumps are decimal pairs
        masks.push_back(((unsigned __int128)hi<<64)|(unsigned __int128)lo);
    fclose(fp);
    auto image2=[&](unsigned __int128 s,const int*t){
        unsigned __int128 r=0;
        for(int i=0;i<N;i++) if(s>>i&1) r|=(unsigned __int128)1<<t[i];
        return r;};
    vector<unsigned __int128> can(masks.size());
    for(size_t j=0;j<masks.size();j++){
        unsigned __int128 best=~ (unsigned __int128)0;
        for(int t=0;t<16;t++){unsigned __int128 im=image2(masks[j],trans[t]); if(im<best)best=im;}
        can[j]=best;
    }
    sort(can.begin(),can.end());
    vector<unsigned __int128> reps; vector<int> sizes;
    for(size_t j=0;j<can.size();){
        size_t e=j+1; while(e<can.size()&&can[e]==can[j])e++;
        // orbit size = number of distinct images of the representative
        unsigned __int128 imgs[16]; int ni=0;
        for(int t=0;t<16;t++){unsigned __int128 im=image2(can[j],trans[t]);
            bool dup=false; for(int q=0;q<ni;q++) if(imgs[q]==im){dup=true;break;}
            if(!dup)imgs[ni++]=im;}
        reps.push_back(can[j]); sizes.push_back(ni);
        j=e;
    }
    sort(sizes.begin(),sizes.end());
    // reps are already ascending (can sorted); emit JSON like json.dumps(sort_keys=True)
    auto hex=[&](unsigned __int128 v){
        if(!v)return string("0");
        string s; while(v){int d=(int)(v&15); s.push_back(d<10?'0'+d:'a'+d-10); v>>=4;}
        reverse(s.begin(),s.end()); return s;};
    printf("{\"K\": 9, \"m\": %d, \"num_orbits\": %zu, \"orbit_reps\": [",m,reps.size());
    for(size_t j=0;j<reps.size();j++) printf("%s\"%s\"",j?", ":"",hex(reps[j]).c_str());
    printf("], \"orbit_sizes\": [");
    for(size_t j=0;j<sizes.size();j++) printf("%s%d",j?", ":"",sizes[j]);
    printf("], \"top_layer\": %zu}\n",masks.size());
    return 0;
}
