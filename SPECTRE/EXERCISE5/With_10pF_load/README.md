# 10 pF CMOS Inverter Chain Delay Study

22 nm PTM HP BSIM4 model, \(V_{DD}=0.8\) V, \(C_L=10\) pF.

Fine multi-finger (`nf`) partitioning is used with a maximum finger width of 220 nm.

\[
t_{pd}=\frac{t_{PHL}+t_{PLH}}{2}
\]

| n | Stages | \(t_{pd}\) (ps) |
| -: | -----: | --------------: |
| 3 | 4 | 111.84 |
| 4 | 5 | 83.53 |
| 5 | 6 | 72.02 |
| 6 | 7 | 66.88 |
| 7 | 8 | 64.86 |
| **8** | **9** | **64.45** |
| 9 | 10 | 65.00 |
| 10 | 11 | 66.17 |

Minimum measured delay:

\[
\boxed{t_{pd}=64.45\text{ ps at }n=8}
\]

Thus, the minimum delay occurs for a **9-stage inverter chain**.
