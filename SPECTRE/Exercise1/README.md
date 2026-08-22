# Exercise 1 — CMOS Inverter Chain

A 7-stage CMOS inverter chain was simulated using Spectre with the 22-nm PTM HP model.

For the initial smoke test:

- `k = 2`
- `L = 22 nm`
- `Wn = 44 nm`
- `Wp = 88 nm`
- `VDD = 1 V`

Propagation delays were measured graphically at the 50% `VDD` crossing.

## Initial Smoke Test — k = 2

| Parameter | Graphical value |
|---|---:|
| `tPHL` | ≈ 1.9286 ps |
| `tPLH` | ≈ 2.668 ps |

Thus:

$$
t_{PLH} > t_{PHL}
$$

### Graphical Measurements

| `tPHL` | `tPLH` |
|---|---|
| <img src="./TPHL_INVERTER_CHAIN_K_IS_2.png" width="500"> | <img src="./TPLH_INVERTER_CHAIN_K_IS_2.png" width="500"> |

## Part A — Sweep of k

`k` was swept from `1` to `2` in steps of `0.1`, and `tPHL` and `tPLH` were measured for each value.

The two curves intersect at approximately:

$$
k \approx 1.293
$$

At this value:

$$
t_{PHL} \approx t_{PLH} \approx 2.13\ \text{ps}
$$

### Sweep Result

<img src="./tplh_vs_tphl_as_a_function_of_k.png" width="800">
