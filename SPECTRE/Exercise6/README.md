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
| Circuit D | PMOS HVT header + NMOS HVT footer |

## Leakage Results

Leakage current is obtained from the VDD supply current in Spectre.

Values below are in **nA**.

| Input State | Circuit A | Circuit B | Circuit C | Circuit D |
|---|---:|---:|---:|---:|
| 00 | **0.061** | **0.00817** | **0.01271** | **0.000960** |
| 01 | **1.027** | **0.00765** | **0.00999** | **0.000642** |
| 10 | **4.144** | **0.00781** | **0.01115** | **0.000466** |
| 11 | **12.122** | **0.00282** | **0.01131** | **0.000102** |

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

## Circuit D — Obtained Values

| Input State | Leakage |
|---|---:|
| 00 | 0.000960 nA |
| 01 | 0.000642 nA |
| 10 | 0.000466 nA |
| 11 | 0.000102 nA |

## Circuit D — Implementation

Circuit D combines the **PMOS HVT header** and **NMOS HVT footer**.

The NAND core is therefore connected between two virtual supply nodes:

\[
V_{DD} \rightarrow \text{PMOS HVT} \rightarrow vdd\_int
\]

and

\[
vss\_int \rightarrow \text{NMOS HVT} \rightarrow V_{SS}.
\]

In sleep mode, both devices are OFF:

\[
V_G(\text{PMOS header})=0.8\text{ V}
\]

and

\[
V_G(\text{NMOS footer})=0\text{ V}.
\]

The virtual nodes \(vdd\_int\) and \(vss\_int\) therefore float to values determined by the leakage paths within the circuit.

### Numerical Convergence Adjustment for Circuit D

The leakage currents in Circuit D were in the **pA range**, making them much smaller than the leakage currents observed in Circuits A–C.

To ensure that the extracted pA-level leakage was not significantly affected by the default DC convergence settings, tighter simulation options were used:

```spectre
options gmindc=1e-15 iabstol=1e-15 reltol=1e-4
