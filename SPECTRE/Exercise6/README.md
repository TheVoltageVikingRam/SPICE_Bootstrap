# Exercise — NAND Leakage in Sleep Mode

## Objective

Simulate the static leakage current of a 2-input CMOS NAND gate in different sleep-mode circuit configurations using the 22 nm PTM model.

Use:

- \(V_{DD} = 0.8\text{ V}\)
- \(W_n = 44\text{ nm}\)
- \(L_n = L_p = 22\text{ nm}\)
- \(k = 1.30\)
- \(W_p = kW_n = 57.2\text{ nm}\)

### HVT Device Assumption

For the newly introduced HVT devices, the threshold voltage is taken as **1.5 times the nominal threshold voltage**, as specified by the professor.

For the PMOS, this corresponds to increasing the **magnitude** of \(V_T\) by a factor of 1.5.

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
| Circuit B | PMOS HVT header only |
| Circuit C | NMOS HVT footer only |
| Circuit D | __________ |

## Leakage Results

Leakage current is obtained from the VDD supply current in Spectre.

Values below are in **nA**.

| Input State | Circuit A | Circuit B | Circuit C | Circuit D |
|---|---:|---:|---:|---:|
| 00 | **0.061** | **0.00817** | **0.01271** | ___ |
| 01 | **1.027** | **0.00765** | **0.00999** | ___ |
| 10 | **4.144** | **0.00781** | **0.01115** | ___ |
| 11 | **12.122** | **0.00282** | **0.01131** | ___ |

### Circuit A — Obtained Values

| Input State | Leakage |
|---|---:|
| 00 | 0.061 nA |
| 01 | 1.027 nA |
| 10 | 4.144 nA |
| 11 | 12.122 nA |

### Circuit B — Obtained Values

| Input State | Leakage |
|---|---:|
| 00 | 0.00817 nA |
| 01 | 0.00765 nA |
| 10 | 0.00781 nA |
| 11 | 0.00282 nA |

## Circuit B — Implementation

Circuit B adds a **PMOS HVT header** between the supply \(V_{DD}\) and the NAND core.

In sleep mode:

\[
S=1 \quad\Rightarrow\quad V_S=0.8\text{ V}
\]

so the PMOS header is OFF.

The NAND core is connected to the resulting virtual supply node \(vdd\_int\).

## Circuit C — Obtained Values

| Input State | Leakage |
|---|---:|
| 00 | 0.01271 nA |
| 01 | 0.00999 nA |
| 10 | 0.01115 nA |
| 11 | 0.01131 nA |

## Circuit C — Implementation

Circuit C adds an **NMOS HVT footer** between the NAND core and ground.

The NAND core is connected to the virtual ground node \(vss\_int\).

In sleep mode, the footer gate is held at 0 V:

\[
V_G=0\text{ V}
\]

so the NMOS HVT footer is OFF.

## Spectre Measurement

The leakage current is extracted using:

```spectre
save VDD_SRC:p
