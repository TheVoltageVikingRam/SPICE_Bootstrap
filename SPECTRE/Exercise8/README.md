# Exercise 8: Drain Diffusion Capacitance of NMOS and PMOS (22 nm PTM HP)

Spectre AC simulations that extract the capacitance seen at the drain node of a minimum-size NMOS and PMOS as a function of drain bias, using the 22 nm High-Performance PTM BSIM4 model card.

## Files

| File | Description |
|---|---|
| `nmos_diffusion_cap.scs` | Spectre netlist for the NMOS (W = 44 nm, L = 22 nm) |
| `pmos_diffusion_cap.scs` | Spectre netlist for the PMOS (W = 1.3 x 44 = 57.2 nm, L = 22 nm) |
| `nmos_diffusion_cap_vd_sweep.csv` | NMOS capacitance vs. frequency for each drain bias |
| `pmos_diffusion_cap_vd_sweep.csv` | PMOS capacitance vs. frequency for each drain bias |

The netlists `include "22nm_HP.pm"` (PTM 22 nm HP, BSIM4 level 54, nominal VDD = 0.8 V). The model card is not part of this folder; place it next to the netlists before running (it is available from the PTM website).

## Setup

- Drain is driven by an AC voltage source (`PORT0`, `mag = 1m`) on top of a DC level `VD_VAL`.
- Gate, source and bulk are tied to the same rail, so they are AC grounds:
  - NMOS: gate, source and bulk at 0 V
  - PMOS: gate, source and bulk at VDD = 0.8 V
- DC sweep of `VD_VAL` = 0, 0.2, 0.4, 0.6, 0.8 V.
- AC analysis from 100 Hz to 10 MHz in 1 kHz steps (10,001 points).
- Diffusion geometry (set in the netlists):
  - `AD = AS = W x 1.5L`
  - `PD = PS = 2W + 3L`

`PD`/`PS` use `2W + 3L` because the model card sets `permod = 1`, which makes BSIM4 expect the perimeter to include the gate-side edge. With `W + 3L` the isolation sidewall is under-counted and the capacitance comes out about 25% low.

## Extraction

The capacitance is taken from the imaginary part of the drain current:

```
C = Im( I(PORT0:p) ) / ( 2*pi*f * 1 mV )
```

The CSV columns are `freq` followed by one column per `VD_VAL` (0, 0.2, 0.4, 0.6, 0.8 V).

- **Sign:** `PORT0:p` is the current into the source, so the CSV values are negative. Take the magnitude (or multiply by -1).
- **Frequency:** the values are flat from 100 Hz to 10 MHz, so a single frequency point is enough.
- **Units:** values are per device, in farads.

## Results

Magnitude of the drain capacitance, in aF, per device (flat over frequency, read at 1 MHz).

| VD_VAL (V) | NMOS (reverse bias = VD) | PMOS (reverse bias = 0.8 - VD) |
|---|---|---|
| 0.0 | 90.2 | 85.8 |
| 0.2 | 83.1 | 89.2 |
| 0.4 | 78.2 | 93.5 |
| 0.6 | 74.6 | 99.6 |
| 0.8 | 71.8 | 108.4 |

- The NMOS capacitance falls as VD_VAL rises, because its reverse bias increases.
- The PMOS capacitance rises as VD_VAL rises, because its bulk is at VDD and its reverse bias is 0.8 - VD_VAL. Plot it against reverse bias to see the same trend as the NMOS.
- Normalised to width at zero bias, the NMOS is about 2.05 fF/um.

## Hand-calculation check

BSIM4 junction capacitance with `permod = 1`, using the model card values (all `pb` = 1 V):

```
Cj(Vr) = cjd   * AD       / (1+Vr)^0.5
       + cjswd * (PD - W) / (1+Vr)^0.33
       + cjswgd * W       / (1+Vr)^0.33
```

NMOS at zero bias: 0.73 aF (area) + 55 aF (isolation sidewall) + 22 aF (gate-edge sidewall), about 78 aF. Adding the gate-drain overlap and fringe term, `(cgdo + cgdl) x W` = 14.5 aF, gives about 92.5 aF against 90.2 aF simulated.

PMOS at zero reverse bias (VD = 0.8 V): 91.1 aF junction + 18.9 aF overlap and fringe = 110.0 aF against 108.4 aF simulated.

The hand estimate treats the gate-drain term as constant. In BSIM4 `cgdl` is bias dependent, so the estimate runs higher than the simulation by a few aF at high reverse bias (about 6-8 aF at the extremes). Intrinsic gate-drain capacitance and Weff/Leff corrections are also ignored.

## Notes

- The measurement is the total capacitance at the drain node. It includes gate-drain overlap and fringe capacitance, not only the junction capacitance. For junction capacitance alone, use the equation above or the model's operating-point values.
- `type=sine ampl=1m` in the source has no effect in AC analysis; only `mag` matters.
- The CSV expressions use `2*3.14` rather than `2*pi`, an error of about 0.05%.
