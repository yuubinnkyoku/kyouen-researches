"""Verify the new bound K <= q+2 against the corrected exact series."""

INV = {3: 5, 5: 6, 7: 6, 9: 9, 11: 9, 13: 8, 17: 9, 19: 9, 23: 10, 29: 8}
AG = {3: 5, 5: 6, 7: 6, 9: 9, 11: 9, 13: 13}

print("INVERSIVE PLANE: K <= q+2 for odd q (new bound)")
print(f"{'q':>3} {'K':>4} {'q+2':>5} {'slack':>6} {'ok':>4}")
for q in sorted(INV):
    K = INV[q]
    print(f"{q:>3} {K:>4} {q+2:>5} {q+2-K:>6} {str(K <= q+2):>4}")
print()
print("all odd q satisfy K <= q+2:", all(INV[q] <= q + 2 for q in INV))
print("max slack:", max(q + 2 - INV[q] for q in INV))
print("min slack:", min(q + 2 - INV[q] for q in INV))

print()
print("AG(2,q): K <= q+2 (lambda_2 = q, so lambda_2+2 = q+2)")
print(f"{'q':>3} {'K':>4} {'q+2':>5} {'slack':>6} {'ok':>4}")
for q in sorted(AG):
    K = AG[q]
    print(f"{q:>3} {K:>4} {q+2:>5} {q+2-K:>6} {str(K <= q+2):>4}")
print()
print("all AG q satisfy K <= q+2:", all(AG[q] <= q + 2 for q in AG))
print("AG attains K = q+2 exactly at q =", [q for q in AG if AG[q] == q + 2])
