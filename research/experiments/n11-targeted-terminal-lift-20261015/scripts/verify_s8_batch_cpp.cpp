// Independent C++ geometry and cache-free terminal solver.
// Reuses the stand-alone S10 integer-geometry solver, not Python's implementation.
#define main s10_solver_command_main
#include "solve_s10_candidates.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc!=2)throw runtime_error("usage: verify_s8_batch_cpp certificate");
  ifstream f(argv[1]);if(!f)throw runtime_error("cannot open certificate");
  string line;
  if(!getline(f,line)||line!="# n11-S8-WIN-batch-terminal-v1")throw runtime_error("bad magic");
  if(!getline(f,line)||line!="BOARD 11")throw runtime_error("bad board");
  if(!getline(f,line)||line.substr(0,6)!="ROOTS ")throw runtime_error("bad count");
  int expected=stoi(line.substr(6));if(expected<1||expected>10000)throw runtime_error("bad count");
  set<U128> roots,witnesses,leaves;
  uint64_t states=0;
  bool ended=false;
  while(getline(f,line)){
   if(line=="END"){
    if(getline(f,line))throw runtime_error("trailing content");
    ended=true;break;
   }
   istringstream ss(line);string tag,a,b,extra;
   if(!(ss>>tag>>a>>b)||ss>>extra||tag!="EDGE")throw runtime_error("bad EDGE");
   U128 s8=parse128(a),s9=parse128(b);
   if(countbits(s8)!=8||canonical(s8)!=s8||!safe(s8))throw runtime_error("bad S8");
   if(countbits(s9)!=9||canonical(s9)!=s9||!safe(s9))throw runtime_error("bad S9");
   if(!roots.insert(s8).second)throw runtime_error("duplicate S8");
   bool child=false;for(int p:legal(s8))if(canonical(s8|((U128)1<<p))==s9){child=true;break;}
   if(!child)throw runtime_error("S9 is not legal child of S8");
   witnesses.insert(s9);
  }
  if(!ended||roots.size()!=(size_t)expected||witnesses.empty())throw runtime_error("incomplete proof");
  for(U128 s9:witnesses){
   auto moves=legal(s9);if(moves.empty())throw runtime_error("no S10 children");
   for(int p:moves){U128 leaf=canonical(s9|((U128)1<<p));
    if(leaves.insert(leaf).second){Terminal r=solve10(leaf);
     if(r.loss)throw runtime_error("S10 LOSS witness: "+hex128(leaf));
     states+=r.states;
    }
   }
  }
  cout<<"PASS S8 WIN "<<roots.size()<<" S9 witnesses "<<witnesses.size()<<" S10 WIN "<<leaves.size()<<" states "<<states<<"\n";
 }catch(const exception&e){cerr<<"FAIL "<<e.what()<<"\n";return 1;}
}
