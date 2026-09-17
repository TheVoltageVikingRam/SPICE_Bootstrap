* fo4opt.sp
*---------------------------------------------------------------------
* Parameters and models
*---------------------------------------------------------------------

.param SUPPLY=1.0
.option scale=25n
.include '../models/ibm065/models.sp'
.temp 70
.option reset

*----------------------------------------------------------------------
* Subcircuits
*----------------------------------------------------------------------

.global vdd gnd
.subckt inv a y N=4 P=8
M1 y a gnd gnd NMOS W='N' L=2 AS='N*5' PS='2*N+10' AD='N*5' PD='2*N+10'

M2 y a vdd vdd PMOS W='P' L=2 AS='P+5' PS='2*P+10' AD='P*5' PD='2*P+10'
.ends


*----------------------------------------------------------------------
* Simulation netlist
*----------------------------------------------------------------------

Vdd vdd gnd 'SUPPLY'
Vin a gnd PULSE 0 'SUPPLY' 0ps 20ps 20ps 120ps 280ps
X1 a b inv P='P1'       *shape inpur waveform
X2 b c inv P='P1' M=4   *reshape input waveform
X3 c d inv P='P1' M=16  *device under test
X4 d e inv P='P1' M=64  *load
X5 e f inv P='P1' M=256 *load under load

*-----------------------------------------------------------------------
* Optimization setup
*-----------------------------------------------------------------------

.param P1=optrange(8,4,16)    *search from 4 to 16, guess 8
.model optmod opt itropt=30    *maximum of 30 iterations
.measure bestratio param='P1/4'  *compute best P/N ratio

*-----------------------------------------------------------------------
* Stimulus 
*-----------------------------------------------------------------------

.tran 0.1ps 280ps SWEEP OPTIMIZE=optrange RESULTS=diff MODEL=optmod
.measure tpdr                             *rising propagation delay
+ TRIG v(c) VAL='SUPPLY/2' FAIL=1
+ TARG v(d) VAL='SUPPLY/2' RISE=1

.measure tpdf                              *falling propagation delay
+ TRIG v(c) VAL='SUPPLY/2' RISE=1
+ TARG v(d) VAL='SUPPLY/2' FALL=1


.measure tpd param='(tpdr+tpdf)/2' goal=0    *average prop delay
.measure diff param='tpdr-tpdf' goal=0        *diff between delays

.end




























