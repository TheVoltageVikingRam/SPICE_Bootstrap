# Part A — MOSFET Gate Capacitance (Cgg) Extraction via AC Small-Signal Analysis

## Objective
Extract the intrinsic gate capacitance of NMOS and PMOS transistors (22 nm PTM-HP model, `Wn=44n`, `Ln=22n`, `k=1.3`, `VDD=0.8 V`) across four gate bias points, under both a standard and a cross-biased terminal configuration.

## Method
- Spectre `ac` analysis, frequency swept **100 Hz – 10 MHz**, `VG_VAL` swept over **[0.2, 0.4, 0.6, 0.8] V**
- AC stimulus amplitude: **1 mV**
- Capacitance computed from the imaginary part of the small-signal gate current:

$$C = \dfrac{\mathrm{Im}(I)}{2\pi f \cdot V_{ac}}$$

- Verified flat to 4+ significant figures across the full frequency sweep for every case, confirming purely capacitive (non-resonant) behavior.

### Bias configurations

| Netlist | Device | Drain | Source / Body | Notes |
|---|---|---|---|---|
| `nmos_cg_gnd.scs` | NMOS | GND | GND | Standard bias, Vds = 0 |
| `cgs_nmos_vdd.scs` | NMOS | GND | VDD | Cross-biased |
| `cgs_pmos_gnd.scs` | PMOS | VDD | GND | Cross-biased |
| `cgs_pmos_vdd.scs` | PMOS | VDD | VDD | Standard bias, Vds = 0 |

### Extraction formula (OCEAN calculator utility)
```lisp
imag(leafValue( i("PORTx:p" ?result "sweepVG_ac1-sweep" ?resultsDir "./<name>.raw") "VG_VAL" <val> ))
/ (2*3.14*xval(leafValue( i("PORTx:p" ?result "sweepVG_ac1-sweep" ?resultsDir "./<name>.raw") "VG_VAL" <val> ))*1m)
```

## Results

### Gate capacitance vs VG_VAL (fF)

| VG_VAL (V) | NMOS — standard (D=S=GND) | NMOS — cross (S=VDD) | PMOS — standard (D=S=VDD) | PMOS — cross (S=GND) |
|---:|---:|---:|---:|---:|
| 0.2 | 0.0314 | 0.0276 | 0.0551 | 0.0494 |
| 0.4 | 0.0329 | 0.0334 | 0.0457 | 0.0461 |
| 0.6 | 0.0399 | 0.0358 | 0.0433 | 0.0397 |
| 0.8 | 0.0418 | 0.0388 | 0.0380 | 0.0330 |

*Values are magnitudes; the raw `Im(I)` sign is negative in every file, a current-reference-direction artifact, not a physically negative capacitance.*

### Source CSV files

| File | Device | Config |
|---|---|---|
| `cgs_with_gnd_cap_value_nmos.csv` | NMOS | D = S = GND |
| `cgs_with_vdd_cap_value_nmos.csv` | NMOS | S = VDD |
| `cgs_with_gnd_cap_value_pmos.csv` | PMOS | S = GND |
| `cgs_with_vdd_cap_value_pmos.csv` | PMOS | D = S = VDD |

## Key Observations
- **NMOS Cgg rises with VG_VAL** — effective `Vgs ≈ VG_VAL` in both configs, so higher VG_VAL drives deeper inversion.
- **PMOS Cgg falls with VG_VAL** — effective `Vsg ≈ VDD − VG_VAL`, so higher VG_VAL reduces overdrive, moving the device toward cutoff.
- **Standard vs. cross-biased configs differ by only a few aF** at matched VG_VAL — this gap reflects the Vds-dependence of inversion-charge partitioning between the two channel terminals.
