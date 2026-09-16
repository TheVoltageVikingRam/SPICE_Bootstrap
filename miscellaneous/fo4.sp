* fo4.sp
*-----------------------------------------------------------------------------
* Parameters and models
*-----------------------------------------------------------------------------

.param SUPPLY=1.0
.param H=4

.option scale=25n
.include '../models/ibm065/models.sp'
.temp 70
.option post

*------------------------------------------------------------------------------
* Subcircuits
*------------------------------------------------------------------------------

.global vdd gnd
.subckt inv a y N=4 P=8
M1 y a gnd gnd NMOS W='N' L=2 AS='N*5' PS='2*N+10' AD='N*5' PD='2*N+10'
M2 y a vdd vdd PMOS W='P' L=2 AS='P*5' PS='2*P+10' AD='P*5' PD='2*P+10'

.ends

*-------------------------------------------------------------------------
* Simulation netlist
*-------------------------------------------------------------------------

Vdd vdd gnd 'SUPPLY'
Vin a gnd PULSE 0 'SUPPLY' 0ps 20ps 20ps 120ps 280ps
X1 a b inv * Shape input waveform
X2 b c inv M='H' * reshape input waveform
X3 c d inv M='H**2' * device under test
X4 d e inv M='H**3' *load
X5 e f inv M='H**4' *load on load


*-------------------------------------------------------------------
* Stimulus
*-------------------------------------------------------------------

.tran 0.1ps 200ps
.measure tpdr                       *rising propagation delay
+  TRIG v(c) VAL='SUPPLY/2' FALL=1
+  TARG v(d) VAL='SUPPLY/2' RISE=1

.measure tpdf                        * falling propagation delay
+  TRIG v(c) VAL='SUPPLY/2' FALL=1
+  TARG v(d) VAL='SUPPLY/2' RISE=1


.measure tpd param='(tpdr+tpdf)/2'   *average propagation delay

.measure trise                       *rise time
+  TRIG v(d) VAL='0.2*SUPPLY' RISE=1
+  TARG v(d) VAL='0.8*SUPPLY' RISE=1

.measure tfall                       * Fall time
+  TRIG v(d) VAL='0.8*SUPPLY' FALL=1
+  TARF v(d) VAL='0.2*SUPPLY' FALL=1
.end






