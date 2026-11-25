// Exhaustive 6-vertex binary-cube section census, dimensions 4..7.
// Two enumeration schemes and independent integer / prime-field arithmetic.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>

using i64 = std::int64_t;
using u64 = std::uint64_t;
constexpr int P = 1009;
int inverse[P];

// Rank over F_1009 is exact: every 6x6 minor of a 0/1 matrix has
// absolute value <= 6^3 = 216 < 1009 (Hadamard bound).
template <bool Modular>
bool isolated(const std::array<int, 5>& v, int d, int& rank_out) {
  i64 a[5][8] = {};
  int pivot_col[5] = {};
  for (int i = 0; i < 5; ++i)
    for (int j = 0; j < d; ++j) a[i][j] = (v[i] >> j) & 1;
  int r = 0;
  for (int col = 0; col < d && r < 5; ++col) {
    int row = r;
    while (row < 5 && a[row][col] == 0) ++row;
    if (row == 5) continue;
    if (row != r)
      for (int j = col; j < d; ++j) std::swap(a[row][j], a[r][j]);
    i64 p = a[r][col];
    if constexpr (Modular) {
      i64 ip = inverse[p];
      for (int j = col; j < d; ++j) a[r][j] = a[r][j] * ip % P;
      p = 1;
    }
    for (int k = r + 1; k < 5; ++k) {
      i64 mul = a[k][col];
      if (!mul) continue;
      for (int j = col; j < d; ++j) {
        i64 x = p * a[k][j] - mul * a[r][j];
        if constexpr (Modular) x = (x % P + P) % P;
        a[k][j] = x;
      }
      if constexpr (!Modular) {
        i64 g = 0;
        for (int j = col + 1; j < d; ++j) g = std::gcd(g, std::abs(a[k][j]));
        if (g > 1)
          for (int j = col + 1; j < d; ++j) a[k][j] /= g;
      }
    }
    pivot_col[r++] = col;
  }
  rank_out = r;
  if (r == d) return false;

  i64 normal[8][8] = {};
  int free_count = 0;
  for (int f = 0; f < d; ++f) {
    bool pivot = false;
    for (int i = 0; i < r; ++i) pivot |= pivot_col[i] == f;
    if (pivot) continue;
    i64* n = normal[free_count++];
    if constexpr (Modular) {
      n[f] = 1;
      for (int i = r - 1; i >= 0; --i) {
        i64 s = 0;
        for (int j = pivot_col[i] + 1; j < d; ++j) s += a[i][j] * n[j];
        n[pivot_col[i]] = (P - s % P) % P;
      }
    } else {
      i64 product = 1;
      for (int i = 0; i < r; ++i) product *= a[i][pivot_col[i]];
      n[f] = product;
      for (int i = r - 1; i >= 0; --i) {
        i64 s = 0;
        for (int j = pivot_col[i] + 1; j < d; ++j) s += a[i][j] * n[j];
        assert(s % a[i][pivot_col[i]] == 0);
        n[pivot_col[i]] = -s / a[i][pivot_col[i]];
      }
    }
  }

  i64 sums[8][256] = {};
  for (int i = 0; i < free_count; ++i)
    for (int x = 1; x < (1 << d); ++x) {
      int bit = __builtin_ctz(static_cast<unsigned>(x));
      i64 s = sums[i][x & (x - 1)] + normal[i][bit];
      if constexpr (Modular) s %= P;
      sums[i][x] = s;
    }
  int count = 0;
  for (int x = 0; x < (1 << d); ++x) {
    bool in_span = true;
    for (int i = 0; i < free_count; ++i) in_span &= sums[i][x] == 0;
    count += in_span;
    if (count > 6) return false;
  }
  return count == 6;
}

struct Census {
  u64 visited = 0, candidates = 0, valid = 0;
  std::array<u64, 8> rank_valid = {};
};

template <bool Modular>
Census direct(int d) {
  Census c;
  const int end = 1 << d;
  for (int a = 1; a < end - 4; ++a)
    for (int b = a + 1; b < end - 3; ++b)
      for (int e = b + 1; e < end - 2; ++e)
        for (int f = e + 1; f < end - 1; ++f)
          for (int g = f + 1; g < end; ++g) {
            std::array<int, 5> v = {a, b, e, f, g};
            ++c.visited;
            ++c.candidates;
            int rank = 0;
            if (isolated<Modular>(v, d, rank)) {
              ++c.valid;
              ++c.rank_valid[rank];
            }
          }
  return c;
}

template <bool Modular>
Census patterns(int d) {
  Census c;
  std::array<int, 8> cols = {};
  int fact[9] = {1};
  for (int i = 1; i <= d; ++i) fact[i] = i * fact[i - 1];
  auto visit = [&]() {
    ++c.visited;
    std::array<int, 5> v = {};
    for (int j = 0; j < d; ++j)
      for (int i = 0; i < 5; ++i) v[i] |= ((cols[j] >> i) & 1) << j;
    for (int i = 0; i < 5; ++i) {
      if (!v[i]) return;
      for (int j = 0; j < i; ++j)
        if (v[i] == v[j]) return;
    }
    int weight = fact[d];
    for (int j = 0; j < d;) {
      int k = j + 1;
      while (k < d && cols[k] == cols[j]) ++k;
      weight /= fact[k - j];
      j = k;
    }
    c.candidates += weight;
    int rank = 0;
    if (isolated<Modular>(v, d, rank)) {
      c.valid += weight;
      c.rank_valid[rank] += weight;
    }
  };
  auto recurse = [&](auto&& self, int pos, int low) -> void {
    if (pos == d) { visit(); return; }
    for (int v = low; v < 32; ++v) {
      cols[pos] = v;
      self(self, pos + 1, v);
    }
  };
  recurse(recurse, 0, 0);
  assert(c.candidates % 120 == 0 && c.valid % 120 == 0);
  c.candidates /= 120;
  c.valid /= 120;
  for (auto& x : c.rank_valid) { assert(x % 120 == 0); x /= 120; }
  return c;
}

int main(int argc, char** argv) {
  if (argc != 4) {
    std::cerr << "usage: q6_census <d:4..7> <direct|patterns> <integer|prime>\n";
    return 2;
  }
  int d = std::atoi(argv[1]);
  std::string enumeration = argv[2], arithmetic = argv[3];
  if (d < 4 || d > 7 || (enumeration != "direct" && enumeration != "patterns") ||
      (arithmetic != "integer" && arithmetic != "prime")) return 2;
  inverse[1] = 1;
  for (int i = 2; i < P; ++i) inverse[i] = P - (P / i) * inverse[P % i] % P;
  Census c = enumeration == "direct"
      ? (arithmetic == "prime" ? direct<true>(d) : direct<false>(d))
      : (arithmetic == "prime" ? patterns<true>(d) : patterns<false>(d));
  assert((c.valid * (1ULL << d)) % 6 == 0);
  std::cout << "d=" << d << " enumeration=" << enumeration << " arithmetic=" << arithmetic
            << " visited=" << c.visited << " candidates=" << c.candidates
            << " rooted=" << c.valid << " E_d6=" << c.valid * (1ULL << d) / 6 << '\n';
  for (int r = 0; r <= d; ++r)
    if (c.rank_valid[r]) std::cout << "rank=" << r << " rooted=" << c.rank_valid[r] << '\n';
}
