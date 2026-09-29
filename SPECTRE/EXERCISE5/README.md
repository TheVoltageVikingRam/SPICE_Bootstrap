# 1 pF CMOS Inverter Chain Delay Study

A comparative study of propagation delay in a geometrically tapered CMOS inverter chain using a **22 nm PTM HP BSIM4 model**.

### Simulation Parameters

- Supply voltage: \(V_{DD}=0.8\text{ V}\)
- Load capacitance: \(C_L=1\text{ pF}\)
- Channel length: \(L=22\text{ nm}\)
- Base NMOS width: \(W_n=2L=44\text{ nm}\)
- PMOS/NMOS width ratio: \(k=1.3\)
- Tapering: geometric
- Measurement threshold: \(V_{DD}/2=0.4\text{ V}\)
- Propagation delay:

\[
t_{pd}=\frac{t_{PHL}+t_{PLH}}{2}
\]

For each value of \(n\), the chain contains \(n+1\) inverter stages, with stage \(i\) scaled by

\[
W_i=W_0\alpha^i.
\]

---

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

---

## Case 2 — `rgatemod = 1`

Gate-resistance effects are enabled, while the large transistors are represented as **single devices** whose width is directly scaled with the geometric multiplier.

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

The delay increases strongly with the number of stages under this single-device implementation.

---

## Case 3 — `m`-based implementation, `rgatemod = 1`

The geometric scaling is implemented using the MOS `m` parameter, representing parallel device multiplicity, while keeping the base transistor width unchanged.

For stage \(i\),

\[
m_i=\alpha^i.
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
| 10 | 11 | 2.376535 | 5747.002426 | 55.55 |

Minimum measured delay:

\[
\boxed{t_{pd}=49.40\text{ ps at }n=6}
\]

---

## Case 4 — Fine `nf` partitioning, `rgatemod = 1`

The geometric scaling is implemented using **multi-finger MOS devices**.

For each stage \(i\), the required total transistor widths are

\[
W_{n,\mathrm{tot}}=W_n\alpha^i
\]

and

\[
W_{p,\mathrm{tot}}=kW_n\alpha^i.
\]

The total widths are partitioned into fingers using a maximum finger-width constraint of

\[
W_f=220\text{ nm}.
\]

The number of fingers is calculated as

\[
NF_n=
\left\lceil
\frac{W_{n,\mathrm{tot}}}{220\text{ nm}}
\right\rceil
\]

and

\[
NF_p=
\left\lceil
\frac{W_{p,\mathrm{tot}}}{220\text{ nm}}
\right\rceil.
\]

The total transistor width is preserved while the resulting `nf` values are supplied to the BSIM4 device model.

| n | Stages | \(\alpha\) | \(t_{pd}\) (ps) |
| -: | -----: | ---------: | --------------: |
| 3 | 4 | 10.810515 | 65.42 |
| 4 | 5 | 6.715481 | 55.44 |
| 5 | 6 | 4.889123 | 51.97 |
| 6 | 7 | 3.897350 | **51.16** |
| 7 | 8 | 3.287935 | 51.73 |
| 8 | 9 | 2.880629 | 53.07 |
| 9 | 10 | 2.591424 | 54.89 |
| 10 | 11 | 2.376535 | 57.01 |

Minimum measured delay:

\[
\boxed{t_{pd}=51.16\text{ ps at }n=6}
\]

Thus, for the tested range \(n=3\) to \(10\), the fine `nf` partitioning method gives its minimum measured delay for a **7-stage inverter chain**.

---

## Summary

| Case | Implementation | `rgatemod` | Optimal \(n\) | Stages | Minimum \(t_{pd}\) |
| ----- | ----- | -----: | -----: | -----: | -----: |
| 1 | Single wide device | 0 | 6 | 7 | 51.66 ps |
| 2 | Single wide device | 1 | 3* | 4 | 86.36 ps |
| 3 | `m`-based parallel multiplicity | 1 | 6 | 7 | **49.40 ps** |
| 4 | Fine `nf` multi-finger partitioning | 1 | 6 | 7 | 51.16 ps |

\*For Case 2, the delay increased monotonically over the tested range \(n=3\)–\(10\), so \(n=3\) is simply the lowest-delay point within that range.

### Main Observation

For the geometrically tapered inverter chain driving a 1 pF load, the simulations show that the optimum number of stages depends strongly on how the very large devices are represented.

The single-wide-device implementation with `rgatemod = 1` exhibits a strong increase in delay as the number of stages increases. In contrast, both the `m`-based implementation and the fine `nf` multi-finger implementation exhibit a minimum around

\[
\boxed{n=6\quad\text{(7 inverter stages)}}
\]

with measured delays of approximately 49–51 ps.

The `nf` implementation provides an explicit multi-finger representation while maintaining the intended total transistor width.
