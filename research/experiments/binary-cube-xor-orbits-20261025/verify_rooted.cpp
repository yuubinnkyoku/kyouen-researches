#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <utility>

namespace {
constexpr int P = 101;
int rank_mod101(const std::array<int, 5>& vertices, int rows, int d) {
  int a[5][6] = {};
  for (int i = 0; i < rows; ++i)
    for (int j = 0; j < d; ++j)
      a[i][j] = (vertices[i] >> j) & 1;
  int rank = 0;
  for (int col = 0; col < d && rank < rows; ++col) {
    int pivot = rank;
    while (pivot < rows && a[pivot][col] == 0) ++pivot;
    if (pivot == rows) continue;
    for (int j = col; j < d; ++j) std::swap(a[rank][j], a[pivot][j]);
    int inverse = 1;
    while ((a[rank][col] * inverse) % P != 1) ++inverse;
    for (int j = col; j < d; ++j)
      a[rank][j] = (a[rank][j] * inverse) % P;
    for (int i = rank + 1; i < rows; ++i) {
      const int multiple = a[i][col];
      for (int j = col; j < d; ++j)
        a[i][j] = (a[i][j] - multiple * a[rank][j] + P * P) % P;
    }
    ++rank;
  }
  return rank;
}

void verify(int d, std::uint64_t expected_rooted, std::uint64_t expected_total) {
  const int n = 1 << d;
  std::uint64_t rooted = 0, total = 0;
  std::array<int, 5> v = {};
  for (int a = 1; a < n; ++a)
    for (int b = a + 1; b < n; ++b)
      for (int c = b + 1; c < n; ++c)
        for (int e = c + 1; e < n; ++e) {
          v[0] = a; v[1] = b; v[2] = c; v[3] = e;
          const int rank = rank_mod101(v, 4, d);
          bool good = true;
          for (int x = 1; x < n; ++x) {
            if (x == a || x == b || x == c || x == e) continue;
            v[4] = x;
            if (rank_mod101(v, 5, d) == rank) {
              good = false;
              break;
            }
          }
          rooted += good;
          ++total;
        }
  if (rooted != expected_rooted || total != expected_total ||
      (rooted * static_cast<std::uint64_t>(n)) % 5 != 0)
    throw std::runtime_error("rooted-section count mismatch");
  std::cout << "d=" << d << " candidates=" << total
            << " rooted=" << rooted
            << " E_d5=" << rooted * n / 5 << '\n';
}
}  // namespace

int main() {
  verify(5, 405, 31465);
  verify(6, 20055, 595665);
}
