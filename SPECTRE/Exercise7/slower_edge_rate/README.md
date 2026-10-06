# SLOW-EDGE TRANSMISSION-LINE ANALYSIS — PROJECT CONTEXT

I am extending Exercise 7 (“Transmission Lines”) to study the SLOW INPUT-EDGE regime.

IMPORTANT:
- The earlier 0.76 VDD analysis has been intentionally DROPPED and deleted from the repository.
- Do NOT reintroduce 0.76 VDD.
- The final project uses only:
  1. 0.5 VDD threshold
  2. 0.632 VDD threshold
- Both π and T distributed RC models are being compared.
- For this slow-edge experiment, the input rise/fall times are:
    tr = tf = 400 ps

## CIRCUIT PARAMETERS
- VDD = 0.8 V
- Rtot = 100 Ω
- Ctot = 1 pF
- RC = 100 ps
- Elmore delay ≈ RC/2 = 50 ps
- Input rise time = 400 ps
- Input fall time = 400 ps
- Therefore:
    tr = 400 ps >> RC/2 = 50 ps
  so this is the SLOW-INPUT-EDGE regime.

## SIMULATION SETUP
Use the same setup as the fast-edge simulations except:
    rise=400p
    fall=400p

Pulse source:
Vin (in 0) vsource type=pulse val0=0 val1=VDD delay=0 rise=400p fall=400p width=500p period=1n

Transient:
tran1 tran stop=1n maxstep=0.1p

Measurement:
.measure tran tpd
+ trig v(in) val=VTH rise=1
+ targ v(out) val=VTH rise=1

## THRESHOLDS
1. 0.5 VDD:
   VTH = 0.5 × 0.8 = 0.4 V

2. 0.632 VDD:
   VTH = 0.632 × 0.8 = 0.5056 V

## π MODEL
For N sections:
- Each series resistor = Rtot/N
- Endpoint capacitor = Ctot/(2N)
- Internal capacitor = Ctot/N

## T MODEL
For N sections:
- End resistor = Rtot/(2N)
- Internal series resistor = Rtot/N
- Each capacitor = Ctot/N

Both models preserve total R = 100 Ω and total C = 1 pF.

## SPECTRE SWEEP WORKFLOW
Do NOT use an internal Spectre sweep with conditional topology because it previously caused:

FATAL (SFE-406): Alter causes topology change (conditional instantiation) in top-level circuit.

Instead:
- Keep one N value in the base netlist.
- Generate independent N=1...10 netlists using Bash/sed.
- Run Spectre separately for each N.

Example:
```bash
for N in {1..10}
do
    sed "s/parameters N=1/parameters N=$N/" \
        base_netlist.scs > N_N${N}.scs
    spectre N_N${N}.scs > N_N${N}.log
done
```

## IMPORTANT DEBUGGING HISTORY
An earlier T-model run produced tpd = NaN because the pulse source did not actually switch. Spectre reported:
    Maximum V(in) ≈ 141.6 pV
The fix was adding:
    delay=0
to the pulse source.
All current simulations use delay=0.

## SLOW-EDGE RESULTS — 0.5 VDD
π model:
N=1   49.6608 ps
N=2   49.8523 ps
N=3   49.8754 ps
N=4   49.8827 ps
N=5   49.8860 ps
N=6   49.8878 ps
N=7   49.8888 ps
N=8   49.8895 ps
N=9   49.8899 ps
N=10  49.8903 ps

T model:
N=1   49.6608 ps
N=2   49.8523 ps
N=3   49.8754 ps
N=4   49.8827 ps
N=5   49.8860 ps
N=6   49.8878 ps
N=7   49.8888 ps
N=8   49.8895 ps
N=9   49.8899 ps
N=10  49.8903 ps

The uploaded π results are in:
`pi_based_slower_edge_50vdd_400ps_tr.txt`

The uploaded T results are in:
`T_based_slower_edge_50vdd_400ps_tr.txt`

The files show the same values to the reported precision for every N. 

## SLOW-EDGE RESULTS — 0.632 VDD
π model:
N=1   49.8825 ps
N=2   49.9572 ps
N=3   49.9652 ps
N=4   49.9677 ps
N=5   49.9688 ps
N=6   49.9693 ps
N=7   49.9697 ps
N=8   49.9699 ps
N=9   49.9700 ps
N=10  49.9702 ps

T model:
N=1   49.8825 ps
N=2   49.9572 ps
N=3   49.9652 ps
N=4   49.9677 ps
N=5   49.9688 ps
N=6   49.9693 ps
N=7   49.9697 ps
N=8   49.9699 ps
N=9   49.9700 ps
N=10  49.9702 ps

The uploaded π results are in:
`pi_based_slower_edge_63_2vdd_400ps_tr.txt`

The uploaded T results are in:
`T_based_slower_edge_63_2vdd_400ps_tr.txt`

Again, π and T match to the reported precision for every N.

## KEY INTERPRETATION
This is the main purpose of the slow-edge experiment.

Since:
    tr = 400 ps
    RC/2 = 50 ps

we have:
    tr >> RC/2

Therefore the input is a slow ramp compared with the line's characteristic delay.

In this regime, the output behaves approximately like a delayed version of the input. Therefore the threshold-crossing delay becomes approximately independent of the threshold chosen and approaches the Elmore delay:

    tdelay ≈ tElmore ≈ RC/2 ≈ 50 ps

This is exactly what the simulations show.

For 0.5 VDD:
    N=10 ≈ 49.890 ps

For 0.632 VDD:
    N=10 ≈ 49.970 ps

Both are very close to:
    50 ps

The difference between the two thresholds at N=10 is only about:
    49.9702 - 49.8903 ≈ 0.08 ps

which demonstrates near threshold-independence for the slow input.

π vs T:
- They are numerically identical to the displayed precision in the slow-edge simulations.
- This supports the report's statement that T and π models behave very similarly.

## FAST-EDGE RESULTS ALREADY COMPLETED
For comparison, fast-edge simulations used:
    tr = tf = 5.65 ps

Since:
    5.65 ps << 50 ps

that was the FAST-EDGE / near-step regime.

Approximate N=10 results already obtained:

Fast edge, 0.5 VDD:
    T ≈ 37.9004 ps

Fast edge, 0.632 VDD:
    T ≈ 49.6116 ps
    π ≈ 49.6115 ps

Thus the overall comparison is:

Fast edge:
- 0.5 VDD → ~37.9 ps
- 0.632 VDD → ~49.6 ps
Strong threshold dependence.

Slow edge:
- 0.5 VDD → ~49.89 ps
- 0.632 VDD → ~49.97 ps
Very weak threshold dependence.

## THEORETICAL RC STEP-RESPONSE CONTEXT
For an ideal first-order RC step:
    Vout(t) = VDD (1 - exp(-t/τ))

and:
    t = -τ ln(1 - Vout/VDD)

For the transmission-line approximation:
    τ ≈ RC/2 = 50 ps

Therefore, in the FAST-EDGE / step-like case:
- At 0.632 VDD:
      t ≈ τ = RC/2 = 50 ps
- At 0.5 VDD:
      t ≈ 0.693τ = 0.693 RC/2 ≈ 34.66 ps

However, in the SLOW-EDGE case we should NOT interpret the measured delay simply using those step-response threshold equations, because the input is no longer an instantaneous step. Instead, the line approximately delays the slowly changing input waveform, producing a threshold-independent delay ≈ Elmore delay.

## REPORT CONCLUSION TO AIM FOR
The experiment should establish:

1. Elmore delay for this distributed RC line is approximately:
       RC/2 = 50 ps

2. With a FAST input edge (5.65 ps), threshold-based measured delay depends strongly on the chosen threshold.

3. With a SLOW input edge (400 ps >> RC/2), measured delay becomes approximately threshold-independent and approaches RC/2.

4. π and T distributed models give essentially identical propagation-delay results.

5. Increasing N from 1 to 10 makes the distributed representation converge toward the same ~50 ps behavior.

The report itself discusses the slow-edge case and states that for the 400 ps rise/fall simulation the delay is approximately RC/2, and that the delay is symmetric for 0.5 VDD and 0.63 VDD thresholds.
