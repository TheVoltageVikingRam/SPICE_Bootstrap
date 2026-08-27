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

### Sweep Result

| Spectre Result | Python Generated Result |
|---|---|
| <img src="./tplh_vs_tphl_as_a_function_of_k.png" width="500"> | <img src="./tplh_vs_tphl_python_generated.png" width="500"> |

The intersection of the two curves gives approximately:

$$
k \approx 1.293
$$

At this point:

$$
t_{PHL} \approx t_{PLH} \approx 2.13\ \text{ps}
$$

### Calculator Utility Result

The intersection was also obtained using the Spectre calculator:

<img src="./k_value_for_tplh_equal_tphl_from_calc_utility.png" width="600">

The calculator gives:

$$
\boxed{k \approx 1.293}
$$

with the corresponding delay of approximately:

$$
\boxed{2.13\ \text{ps}}
$$

The sweep data is also provided as a CSV file:

[`tplh_vs_tphl_as_func_of_k.csv`](./tplh_vs_tphl_as_func_of_k.csv)

### Rise and Fall Time Analysis

Similarly, `t_rise` and `t_fall` were measured as `k` was swept.

| Spectre Result | Python Generated Result |
|---|---|
| <img src="./trise_vs_tfall_values_as_k_is_swept_at_x_of10p.png" width="500"> | <img src="./trise_vs_tfall_python_generated.png" width="500"> |

The intersection of the two curves gives approximately:

$$
k \approx 1.82
$$

At this point:

$$
t_{rise} \approx t_{fall} \approx 4.55\ \text{ps}
$$

The sweep data for rise and fall times is also provided as a CSV file:

[`trise_tfall_at_x_equal_to10p.csv`](./trise_tfall_at_x_equal_to10p.csv)

## Part B
