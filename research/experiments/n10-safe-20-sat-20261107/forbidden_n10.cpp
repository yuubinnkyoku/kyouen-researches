// Forbidden concyclic/collinear quadruples of the 10x10 grid.
// Points are indexed p = x + 10*y (0 <= x,y <= 9).  A quadruple is forbidden
// iff the 4x4 determinant with rows (x*x+y*y, x, y, 1) vanishes.
#include <array>
#include <cstdlib>
#include <iostream>
#include <vector>
using I = long long;

static I det4(const std::array<int, 4>& q) {
    I m[4][4];
    for (int r = 0; r < 4; ++r) {
        I x = q[r] % 10, y = q[r] / 10;
        m[r][0] = x * x + y * y;
        m[r][1] = x;
        m[r][2] = y;
        m[r][3] = 1;
    }
    // 4x4 determinant via Laplace expansion along the first row.
    I total = 0;
    for (int c = 0; c < 4; ++c) {
        I sub[3][3];
        for (int r = 1; r < 4; ++r) {
            int cc = 0;
            for (int k = 0; k < 4; ++k) {
                if (k == c) continue;
                sub[r - 1][cc++] = m[r][k];
            }
        }
        I d = sub[0][0] * (sub[1][1] * sub[2][2] - sub[1][2] * sub[2][1])
            - sub[0][1] * (sub[1][0] * sub[2][2] - sub[1][2] * sub[2][0])
            + sub[0][2] * (sub[1][0] * sub[2][1] - sub[1][1] * sub[2][0]);
        total += (c % 2 ? -d : d) * m[0][c];
    }
    return total;
}

int main() {
    const int N = 100;
    long long count = 0;
    for (int a = 0; a < N; ++a)
        for (int b = a + 1; b < N; ++b)
            for (int c = b + 1; c < N; ++c)
                for (int d = c + 1; d < N; ++d)
                    if (det4({a, b, c, d}) == 0) {
                        std::cout << a << ' ' << b << ' ' << c << ' ' << d << '\n';
                        ++count;
                    }
    std::cerr << "forbidden quadruples: " << count << '\n';
    return 0;
}
