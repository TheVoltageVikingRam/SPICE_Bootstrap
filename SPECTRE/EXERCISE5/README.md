# 1 pF CMOS Inverter Chain Delay Study

22 nm PTM HP BSIM4 model, \(V_{DD}=0.8\) V, \(C_L=1\) pF.

The inverter widths are geometrically tapered using the calculated \(\alpha\) for each \(n\). Propagation delay is

\[
t_{pd}=\frac{t_{PHL}+t_{PLH}}{2}.
\]

## Case 1 — `rgatemod = 0`

Gate-resistance effects are disabled. The same transistor sizing is used for every \(n\).

| n | Stages | \(\alpha\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | --------------: |
| 3 | 4 | 10.810515 | 66.36 |
| 4 | 5 | 6.715481 | 56.11 |
| 5 | 6 | 4.889123 | 52.50 |
| 6 | 7 | 3.897350 | **51.66** |
| 7 | 8 | 3.287935 | 52.18 |
| 8 | 9 | 2.880629 | 53.51 |
| 9 | 10 | 2.591424 | 55.32 |
| 10 | 11 | 2.376535 | 57.45 |

Minimum measured delay:

\[
\boxed{t_{pd}=51.66\text{ ps at }n=6}
\]

## Case 2 — `rgatemod = 1`

Gate-resistance effects are enabled, while the large transistors are represented as single devices.

| n | Stages | \(\alpha\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | --------------: |
| 3 | 4 | 10.810515 | 86.36 |
| 4 | 5 | 6.715481 | 113.60 |
| 5 | 6 | 4.889123 | 165.54 |
| 6 | 7 | 3.897350 | 235.95 |
| 7 | 8 | 3.287935 | 320.61 |
| 8 | 9 | 2.880629 | 416.20 |
| 9 | 10 | 2.591424 | 520.41 |
| 10 | 11 | 2.376535 | 631.53 |

The delay increases strongly with \(n\).

## Case 3 — `m`-based implementation, `rgatemod = 1`

The geometric scaling is implemented using the MOS `m` parameter, representing parallel device multiplicity, while keeping the base transistor width unchanged.

For stage \(i\),

\[
m_i=\alpha^i
\]

The table lists the final-stage multiplier \(m_n=\alpha^n\).

| n | Stages | \(\alpha\) | Final-stage \(m_n\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | ------------------: | --------------: |
| 3 | 4 | 10.810515 | 1263.394958 | 62.32 |
| 4 | 5 | 6.715481 | 2033.800805 | 53.11 |
| 5 | 6 | 4.889123 | 2793.538099 | 49.99 |
| 6 | 7 | 3.897350 | 3504.420068 | **49.40** |
| 7 | 8 | 3.287935 | 4153.960176 | 50.08 |
| 8 | 9 | 2.880629 | 4741.308767 | 51.51 |
| 9 | 10 | 2.591424 | 5270.441129 | 53.39 |
| 10 | 11 | 2.376535 | 5747.002426 | **55.55** |

Minimum measured delay:

\[
\boxed{t_{pd}=49.40\text{ ps at }n=6}
\]
