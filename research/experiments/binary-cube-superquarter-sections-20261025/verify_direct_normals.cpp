// Independent finite audit: enumerate primitive signed normal vectors with
// entries in [-2,2], canonicalize sign, and count every intercept by integer DP.
// The all-dimension theorem is independent of this bounded-coefficient audit.
#include <algorithm>
#include <cassert>
#include <iostream>
#include <map>
#include <numeric>
#include <vector>
using namespace std;

void run(int d) {
  const int total = 1 << d;
  const int bound = 2;
  int choices = 1;
  for (int i = 0; i < d; ++i) choices *= 2 * bound + 1;
  map<int, long long> sections;
  long long vectors = 0;
  for (int code = 0; code < choices; ++code) {
    int t = code, g = 0, first = 0;
    vector<int> a(d);
    for (int i = 0; i < d; ++i) {
      a[i] = t % (2 * bound + 1) - bound;
      t /= (2 * bound + 1);
      if (a[i] && !first) first = a[i];
      g = std::gcd(g, abs(a[i]));
    }
    if (first < 0 || g != 1) continue;
    ++vectors;
    int lo = 0, hi = 0;
    for (int x : a) {
      lo += min(x, 0);
      hi += max(x, 0);
    }
    vector<int> count(hi - lo + 1, 0);
    count[-lo] = 1;
    for (int x : a) {
      vector<int> next(count.size(), 0);
      for (int b = lo; b <= hi; ++b) {
        int c = count[b - lo];
        if (!c) continue;
        next[b - lo] += c;
        if (b + x >= lo && b + x <= hi) next[b + x - lo] += c;
      }
      count.swap(next);
    }
    assert(accumulate(count.begin(), count.end(), 0) == total);
    for (int n : count)
      if (4 * n > total) sections[n]++;
  }
  cout << "d=" << d << " primitive signed normals=" << vectors
       << " superquarter cuts:";
  for (auto [n, c] : sections) cout << " (" << n << ":" << c << ")";
  cout << '\n';
  const int m = 1 << (d - 7);
  assert(sections[35 * m] == (d == 7 ? 128 : 1152));
  assert(sections[40 * m] == (d == 7 ? 896 : 2688));
  assert(sections[48 * m] == (d == 7 ? 560 : 1008));
  assert(sections[64 * m] == d * (d + 1));
  assert(sections.size() == 4);
}

int main() {
  run(7);
  run(8);
}
