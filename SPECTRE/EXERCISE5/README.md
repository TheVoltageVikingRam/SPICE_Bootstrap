# 1 pF CMOS Inverter Chain Delay Study

22 nm PTM HP BSIM4 model, \(V_{DD}=0.8\) V, \(C_L=1\) pF.

The inverter widths are geometrically tapered using the calculated \(\alpha\) for each \(n\). Propagation delay is

$$
t_{pd}=\frac{t_{PHL}+t_{PLH}}{2}.
$$

## Case 1 — `rgatemod = 0`

Gate-resistance effects are disabled. The same transistor sizing is used for every \(n\).

|  n | Stages | \(\alpha\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | --------------: |
|  3 |      4 |  10.810515 |           66.36 |
|  4 |      5 |   6.715481 |           56.11 |
|  5 |      6 |   4.889123 |           52.50 |
|  6 |      7 |   3.897350 |       **51.66** |
|  7 |      8 |   3.287935 |           52.18 |
|  8 |      9 |   2.880629 |           53.51 |
|  9 |     10 |   2.591424 |           55.32 |
| 10 |     11 |   2.376535 |           57.45 |

Minimum measured delay:

$$
\boxed{t_{pd}=51.66\text{ ps at }n=6}
$$

## Case 2 — `rgatemod = 1`

Gate-resistance effects are enabled, while the large transistors are still represented as single devices.

|  n | Stages | \(\alpha\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | --------------: |
|  3 |      4 |  10.810515 |           86.36 |
|  4 |      5 |   6.715481 |          113.60 |
|  5 |      6 |   4.889123 |          165.54 |
|  6 |      7 |   3.897350 |          235.95 |
|  7 |      8 |   3.287935 |          320.61 |
|  8 |      9 |   2.880629 |          416.20 |
|  9 |     10 |   2.591424 |          520.41 |
| 10 |     11 |   2.376535 |          631.53 |

The delay increases strongly with \(n\), unlike the `rgatemod=0` case.

## Next

Introduce realistic **multi-finger devices with `rgatemod = 1`** while preserving the same total transistor widths, and compare the resulting \(t_{pd}\) against the two cases above.
