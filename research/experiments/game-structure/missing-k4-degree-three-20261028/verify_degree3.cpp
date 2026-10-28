#include <algorithm>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <vector>
using namespace std;

struct State {
  int k;
  vector<int> leaves, pairs;
};
int edge_index(int k, int a, int b) {
  if (a > b) swap(a, b);
  return a * (2 * k - a - 1) / 2 + b - a - 1;
}
int permuted_mask(int k, int mask, const vector<int>& perm) {
  int result = 0;
  for (int a = 0; a < k; ++a)
    for (int b = a + 1; b < k; ++b)
      if ((mask >> edge_index(k, a, b)) & 1)
        result |= 1 << edge_index(k, perm[a], perm[b]);
  return result;
}
int predicted(const State& s) {
  int u = 0;
  vector<int> z(s.k);
  for (int i = 0; i < s.k; ++i) u ^= z[i] = (s.leaves[i] & 1);
  for (int a = 0; a < s.k; ++a)
    for (int b = a + 1; b < s.k; ++b) {
      int v = s.pairs[edge_index(s.k, a, b)] & 1;
      u ^= v; z[a] ^= v; z[b] ^= v;
    }
  bool uniform = all_of(z.begin(), z.end(), [&](int x) { return x == z[0]; });
  return uniform ? (1 ^ u ^ z[0]) : (2 + u);
}
// Quotient by the surviving clique subset X. All independent vertices
// still adjacent to X are active; the others are isolated and handled
// through their parity on each move. No use of the proposed formula.
int grundy(const State& s) {
  int k = s.k, N = 1 << k;
  vector<pair<int, int>> types;
  for (int i = 0; i < k; ++i)
    if (s.leaves[i]) types.emplace_back(1 << i, s.leaves[i]);
  for (int a = 0; a < k; ++a)
    for (int b = a + 1; b < k; ++b) {
      int n = s.pairs[edge_index(k, a, b)];
      if (n) types.emplace_back((1 << a) | (1 << b), n);
    }
  vector<int> active(N), g(N);
  for (int X = 1; X < N; ++X) {
    int p = 0;
    for (auto [signature, count] : types)
      if (signature & X) p ^= count & 1;
    active[X] = p;
    uint32_t seen = 0;
    for (int i = 0; i < k; ++i) if (X & (1 << i)) {
      int isolated = 0;
      for (auto [signature, count] : types)
        if ((signature & X) && !(signature & (1 << i))) isolated ^= count & 1;
      seen |= 1u << isolated;
    }
    for (auto [signature, count] : types) if (signature & X) {
      int Y = X & ~signature;
      int child = g[Y] ^ p ^ active[Y] ^ 1;
      assert(child < 31);
      seen |= 1u << child;
    }
    while (seen & (1u << g[X])) ++g[X];
  }
  return g[N - 1];
}
struct Result {
  long long total = 0, failures = 0;
  map<int, long long> histogram, failure_histogram;
  int minimum_exception_vertices = 1000, minimum_four_vertices = 1000;
  set<int> bad_masks;
};
void check_mask(int k, int missing, Result& result) {
  int E = k * (k - 1) / 2;
  vector<int> present;
  for (int i = 0; i < E; ++i) if (!((missing >> i) & 1)) present.push_back(i);
  int leaf_choices = 1;
  for (int i = 0; i < k; ++i) leaf_choices *= 3;
  for (int leaf_code = 0; leaf_code < leaf_choices; ++leaf_code) {
    State s{k, vector<int>(k), vector<int>(E)};
    int x = leaf_code;
    for (int& v : s.leaves) { v = x % 3; x /= 3; }
    for (int bits = 0; bits < (1 << present.size()); ++bits) {
      for (int j = 0; j < (int)present.size(); ++j)
        s.pairs[present[j]] = 1 + ((bits >> j) & 1);
      int got = grundy(s), want = predicted(s);
      ++result.total;
      ++result.histogram[got];
      int vertices = k + accumulate(s.leaves.begin(), s.leaves.end(), 0)
                       + accumulate(s.pairs.begin(), s.pairs.end(), 0);
      if (got == 4) result.minimum_four_vertices = min(result.minimum_four_vertices, vertices);
      if (got != want) {
        if (k == 5 && missing == 183) {
          int positive_spokes = 0;
          for (int i = 0; i < 4; ++i) positive_spokes += (s.leaves[i] > 0);
          assert(positive_spokes <= 1);
        }
        ++result.failures;
        ++result.failure_histogram[got];
        result.bad_masks.insert(missing);
        result.minimum_exception_vertices = min(result.minimum_exception_vertices, vertices);
      }
    }
  }
}
int main() {
  // All unlabeled missing graphs on five vertices with maximum degree <= 3.
  int k = 5, E = 10;
  vector<int> perm(k);
  iota(perm.begin(), perm.end(), 0);
  vector<vector<int>> perms;
  do { perms.push_back(perm); } while (next_permutation(perm.begin(), perm.end()));
  set<int> representatives;
  for (int mask = 0; mask < (1 << E); ++mask) {
    bool allowed = true;
    for (int i = 0; i < k; ++i) {
      int degree = 0;
      for (int j = 0; j < k; ++j) if (i != j)
        degree += (mask >> edge_index(k, i, j)) & 1;
      if (degree > 3) allowed = false;
    }
    if (!allowed) continue;
    int representative = mask;
    for (const auto& p : perms)
      representative = min(representative, permuted_mask(k, mask, p));
    representatives.insert(representative);
  }
  Result five;
  for (int mask : representatives) check_mask(5, mask, five);
  cout << "k5 classes=" << representatives.size() << " checked=" << five.total
       << " failures=" << five.failures << " bad_masks=";
  for (int mask : five.bad_masks) cout << mask << ",";
  cout << " min_exception_vertices=" << five.minimum_exception_vertices
       << " min_g4_vertices=" << five.minimum_four_vertices << "\n";
  for (auto [g, count] : five.histogram)
    cout << "k5 g=" << g << " count=" << count
         << " failures=" << five.failure_histogram[g] << "\n";
  assert(representatives.size() == 23);
  assert(five.total == 756216 && five.failures == 25);
  assert(five.bad_masks == set<int>{183});
  assert(five.minimum_exception_vertices == 13 && five.minimum_four_vertices == 14);
  assert(five.histogram == (map<int, long long>{{0,23529},{1,23775},{2,354368},{3,354532},{4,12}}));
  // Six-vertex base: missing K4 on vertices 0,1,2,3; all other pairs present.
  int missing_k4 = 0;
  for (int a = 0; a < 4; ++a)
    for (int b = a + 1; b < 4; ++b)
      missing_k4 |= 1 << edge_index(6, a, b);
  Result six;
  check_mask(6, missing_k4, six);
  cout << "k6 missing_K4=" << missing_k4 << " checked=" << six.total
       << " failures=" << six.failures << "\n";
  assert(missing_k4 == 615);
  assert(six.total == 373248 && six.failures == 0);
  cout << "total_checked=" << five.total + six.total << "\n";
}
