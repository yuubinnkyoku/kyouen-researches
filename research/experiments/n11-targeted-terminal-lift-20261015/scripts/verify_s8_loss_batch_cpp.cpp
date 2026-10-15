// Independent C++ integer geometry and terminal minimax. No verdict cache.
#define main s10_solver_command_main
#include "solve_s10_candidates.cpp"
#undef main

int main(int argc,char**argv){try{
 if(argc!=2)throw runtime_error("usage: verify_s8_loss_batch_cpp certificate");
 ifstream f(argv[1]);if(!f)throw runtime_error("cannot open certificate");
 string line;
 if(!getline(f,line)||line!="# n11-S8-LOSS-batch-terminal-v1")throw runtime_error("bad magic");
 if(!getline(f,line)||line!="BOARD 11")throw runtime_error("bad board");
 if(!getline(f,line)||line!="ROOTS 3")throw runtime_error("bad count");
 set<U128> roots;map<U128,U128> edges;
 bool ended=false;
 while(getline(f,line)){
  if(line=="END"){
   if(getline(f,line))throw runtime_error("trailing content");ended=true;break;
  }
  istringstream ss(line);string tag,a,b,extra;
  if(!(ss>>tag>>a))throw runtime_error("bad line");
  if(tag=="ROOT"){
   if(ss>>extra)throw runtime_error("bad ROOT");
   U128 s8=parse128(a);
   if(countbits(s8)!=8||canonical(s8)!=s8||!safe(s8))throw runtime_error("bad S8");
   if(!roots.insert(s8).second)throw runtime_error("duplicate S8");
  }else if(tag=="WITNESS"){
   if(!(ss>>b)||ss>>extra)throw runtime_error("bad WITNESS");
   U128 s9=parse128(a),s10=parse128(b);
   if(countbits(s9)!=9||canonical(s9)!=s9||!safe(s9))throw runtime_error("bad S9");
   if(countbits(s10)!=10||canonical(s10)!=s10||!safe(s10))throw runtime_error("bad S10");
   if(!edges.emplace(s9,s10).second)throw runtime_error("duplicate S9");
  }else throw runtime_error("bad tag");
 }
 if(!ended||roots.size()!=3)throw runtime_error("incomplete proof");
 set<U128> required;
 for(U128 s8:roots)for(int p:legal(s8))required.insert(canonical(s8|((U128)1<<p)));
 if(required.size()!=edges.size())throw runtime_error("missing or extra S9 obligation");
 set<U128> leaves;uint64_t states=0;
 for(auto [s9,s10]:edges){
  if(!required.count(s9))throw runtime_error("extra S9");
  bool child=false;
  for(int p:legal(s9))if(canonical(s9|((U128)1<<p))==s10){child=true;break;}
  if(!child)throw runtime_error("not a legal S10 child");
  if(leaves.insert(s10).second){auto v=solve10(s10);if(!v.loss)throw runtime_error("S10 WIN "+hex128(s10));states+=v.states;}
 }
 cout<<"PASS S8 LOSS "<<roots.size()<<" S9 obligations "<<edges.size()<<" S10 LOSS "<<leaves.size()<<" states "<<states<<"\n";
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
