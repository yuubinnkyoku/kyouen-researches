// Exact Node Kayles census of connected split graphs with independent-side degree 1 or 2.
// Usage: c++ -std=c++17 -O3 verify_census.cpp -o /tmp/split_census
//        /tmp/split_census [--dump-g4] > /tmp/g4.txt
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct Solver {
  int k, limit;
  vector<int> types, multiplicity, grundy, active_parity, degree_parity;
  Solver(int clique) : k(clique), limit(1 << k), multiplicity(limit),
                       grundy(limit), active_parity(limit), degree_parity(k) {
    for (int i=0; i<k; ++i) types.push_back(1 << i);
    for (int i=0; i<k; ++i)
      for (int j=i+1; j<k; ++j) types.push_back((1 << i) | (1 << j));
  }
  int evaluate() {
    int present[128], odd[128], np=0, no=0;
    for (int s : types) if (multiplicity[s] != 0) {
      present[np++] = s;
      if (multiplicity[s] & 1) odd[no++] = s;
    }
    fill(degree_parity.begin(), degree_parity.end(), 0);
    for (int j=0; j<no; ++j)
      for (int i=0; i<k; ++i) if (odd[j] & (1 << i)) degree_parity[i] ^= 1;
    active_parity[0] = 0;
    for (int C=1; C<limit; ++C) {
      int parity = 0;
      for (int j=0; j<no; ++j) if (odd[j] & C) parity ^= 1;
      active_parity[C] = parity;
    }
    grundy[0] = 0;
    for (int C=1; C<limit; ++C) {
      uint32_t seen = 0;
      for (int i=0; i<k; ++i)
        if (C & (1 << i))
          seen |= uint32_t(1) << (active_parity[C] ^ degree_parity[i]);
      for (int j=0; j<np; ++j) if (present[j] & C) {
        const int next = C & ~present[j];
        const int child = grundy[next] ^ active_parity[C] ^ active_parity[next] ^ 1;
        if (child >= 31) { cerr << "Grundy overflow\n"; abort(); }
        seen |= uint32_t(1) << child;
      }
      grundy[C] = __builtin_ctz(~seen);
    }
    return grundy[limit - 1];
  }
};

int main(int argc, char **argv) {
  const bool dump = argc > 1 && string(argv[1]) == "--dump-g4";
  const int only_k = getenv("ONLY_K") ? atoi(getenv("ONLY_K")) : -1;
  const int only_n = getenv("ONLY_N") ? atoi(getenv("ONLY_N")) : -1;
  for (int n : {13,14}) {
    if (only_n >= 0 && n != only_n) continue;
    uint64_t total = 0;
    int maximum = 0;
    for (int k=5; k<=n; ++k) {
      if (only_k >= 0 && k != only_k) continue;
      const int m = n-k;
      Solver solver(k);
      array<uint64_t,16> histogram{};
      vector<int> current(m);
      function<void(int,int)> dfs = [&](int index, int lower) {
        if (index == m) {
          int g = solver.evaluate();
          if (g >= 16) abort();
          ++histogram[g];
          maximum = max(maximum,g);
          if (dump && g==4) {
            cout << "g4 " << k << ' ' << m;
            for (int s : current) cout << ' ' << s;
            cout << '\n';
          }
          return;
        }
        for (int j=lower; j<(int)solver.types.size(); ++j) {
          const int s = solver.types[j];
          ++solver.multiplicity[s];
          current[index]=s;
          dfs(index+1,j);
          --solver.multiplicity[s];
        }
      };
      dfs(0,0);
      uint64_t subtotal = 0;
      for (uint64_t count : histogram) subtotal += count;
      total += subtotal;
      cerr << "n=" << n << " k=" << k << " independent=" << m
           << " total=" << subtotal << " max=";
      for (int j=15; j>=0; --j) if (histogram[j]) { cerr << j; break; }
      cerr << " g4=" << histogram[4] << '\n';
    }
    cerr << "n=" << n << " grand_total=" << total << " maximum=" << maximum << '\n';
  }
}
