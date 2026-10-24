// Independent finite enumeration of all five-point subsets in V_d (d=4,5,6).
// Prime 101 is larger than the absolute value of every relevant 4x4 minor
// (Hadamard bound 16), so modular ranks equal rational ranks.
#include <cstdint>
#include <cstdio>
#include <cstdlib>
using namespace std;

static int inv101[101];
static inline int norm(int x) {
    x %= 101;
    return x < 0 ? x + 101 : x;
}

int main(int argc, char** argv) {
    int d = argc > 1 ? atoi(argv[1]) : 5;
    if (d < 4 || d > 6) return 2;
    for (int x = 1; x < 101; ++x)
        for (int y = 1; y < 101; ++y)
            if (x * y % 101 == 1) { inv101[x] = y; break; }

    const int n = 1 << d;
    int64_t five_sets = 0, hist[9] = {};
    for (int a = 0; a < n; ++a)
    for (int b = a + 1; b < n; ++b)
    for (int c = b + 1; c < n; ++c)
    for (int e = c + 1; e < n; ++e)
    for (int f = e + 1; f < n; ++f) {
        int pts[5] = {a, b, c, e, f};
        int mat[4][6] = {};
        for (int i = 0; i < 4; ++i)
            for (int j = 0; j < d; ++j)
                mat[i][j] = ((pts[i + 1] >> j) & 1) - ((a >> j) & 1);
        int piv[4], rank = 0;
        for (int j = 0; j < d && rank < 4; ++j) {
            int sel = -1;
            for (int k = rank; k < 4; ++k)
                if (mat[k][j]) { sel = k; break; }
            if (sel < 0) continue;
            for (int l = 0; l < d; ++l) {
                int tmp = mat[rank][l];
                mat[rank][l] = mat[sel][l];
                mat[sel][l] = tmp;
            }
            int factor = inv101[norm(mat[rank][j])];
            for (int l = 0; l < d; ++l)
                mat[rank][l] = norm(mat[rank][l] * factor);
            for (int k = 0; k < 4; ++k)
                if (k != rank) {
                    int v = mat[k][j];
                    if (v)
                        for (int l = 0; l < d; ++l)
                            mat[k][l] = norm(mat[k][l] - v * mat[rank][l]);
                }
            piv[rank] = j;
            ++rank;
        }
        if (rank != 3) continue;
        ++five_sets;

        // The three pivot coordinates uniquely determine a point of the flat.
        // Try their eight binary assignments and reconstruct all coordinates.
        int size = 0;
        for (int mask = 0; mask < 8; ++mask) {
            bool valid = true;
            for (int j = 0; j < d; ++j) {
                int x = (a >> j) & 1;
                for (int k = 0; k < 3; ++k)
                    x += (((mask >> k) & 1) - ((a >> piv[k]) & 1))
                         * mat[k][j];
                x = norm(x);
                if (x != 0 && x != 1) { valid = false; break; }
            }
            size += valid;
        }
        if (size < 5 || size > 8) {
            fprintf(stderr, "unexpected section size %d\n", size);
            return 3;
        }
        ++hist[size];
    }
    const int64_t multiplicity[9] = {0, 0, 0, 0, 0, 1, 6, 21, 56};
    for (int s = 5; s <= 8; ++s)
        if (hist[s] % multiplicity[s]) return 4;
    if (hist[7] != 0) return 5;
    printf("d=%d rank3_five_subsets=%lld H5=%lld H6=%lld H8=%lld\n",
           d, (long long)five_sets, (long long)hist[5],
           (long long)(hist[6] / 6), (long long)(hist[8] / 56));
    const int64_t expected[3][4] = {
        {1360, 0, 40, 20},
        {22240, 480, 1200, 260},
        {311360, 20160, 22400, 2800}
    };
    const int64_t* e = expected[d - 4];
    return (five_sets == e[0] && hist[5] == e[1] &&
            hist[6] / 6 == e[2] && hist[8] / 56 == e[3]) ? 0 : 6;
}
