# Exercise 1 — CMOS inverter chain

A 7-stage CMOS inverter chain was simulated using Spectre with the 22-nm PTM HP model.

For the initial smoke test:

- `k = 2`
- `L = 22 nm`
- `Wn = 44 nm`
- `Wp = 88 nm`
- `VDD = 1 V`

Propagation delays were measured graphically at the 50% VDD crossing.

### Results for initial smoke test with k=2

| Parameter | Graphical value |
|---|---:|
| `tPHL` | ≈ 1.9286 ps |
| `tPLH` | ≈ 2.668 ps |

Thus, for the initial `k = 2`:

\[
t_{PLH} > t_{PHL}
\]

### Graphical Measurements

| `tPHL` | `tPLH` |
|---|---|
| ![tPHL](./TPHL_INVERTER_CHAIN_K_IS_2.png) | ![tPLH](./TPLH_INVERTER_CHAIN_K_IS_2.png) |
