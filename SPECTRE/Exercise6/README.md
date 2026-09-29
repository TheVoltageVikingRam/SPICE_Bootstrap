# Exercise — NAND Leakage in Sleep Mode

## Objective

Simulate the static leakage current of a 2-input CMOS NAND gate in different sleep-mode circuit configurations using the 22 nm PTM model.

Use:

- \(V_{DD} = 0.8\text{ V}\)
- \(W_n = 44\text{ nm}\)
- \(L_n = L_p = 22\text{ nm}\)
- \(k = 1.30\)
- \(W_p = kW_n = 57.2\text{ nm}\)

## Input States

The four NAND input combinations are:

| State | A | B |
|---|---:|---:|
| 00 | 0 V | 0 V |
| 01 | 0 V | 0.8 V |
| 10 | 0.8 V | 0 V |
| 11 | 0.8 V | 0.8 V |

## Circuit Configurations

| Configuration | Description |
|---|---|
| Circuit A | Baseline NAND |
| Circuit B | __________ |
| Circuit C | __________ |
| Circuit D | __________ |

## Leakage Results

Leakage current is obtained from the VDD supply current in Spectre.

Values below are in **nA**.

| Input State | Circuit A | Circuit B | Circuit C | Circuit D |
|---|---:|---:|---:|---:|
| 00 | **0.061** | ___ | ___ | ___ |
| 01 | **1.027** | ___ | ___ | ___ |
| 10 | **4.144** | ___ | ___ | ___ |
| 11 | **12.122** | ___ | ___ | ___ |

### Circuit A — Obtained Values

| Input State | Leakage |
|---|---:|
| 00 | 0.061 nA |
| 01 | 1.027 nA |
| 10 | 4.144 nA |
| 11 | 12.122 nA |

## Spectre Measurement

The leakage current is extracted using:

```spectre
save VDD_SRC:p
