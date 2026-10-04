* interconnect.sp
*----------------------------------------------------------------------------
* Parameters and models
*----------------------------------------------------------------------------

.param SUPPLY=1.0
.include '../models/ibm065/models.sp'
.temp 70
.option post
*---------------------------------------------------------------------
* Subcircuits
*---------------------------------------------------------------------

.global vdd gnd
.subckt inv a y N=100nm P=200nm
M1 y a gnd gnd NMOS W='N' L=50nm
+ AS='N*125nm' PS='2*N+250nm' AD='N*125nm' PD='2*N+250nm'

M2 y a vdd vdd PMOS W='P' L=50nm
+ AS='P*125nm' PS='2*P+250nm' AD='P*125nm' PD='2*P+250nm'

.ends


*---------------------------------------------------------------------------
* Compute transmission line parameters
*---------------------------------------------------------------------------
.material   oxide DIELECTRIC ER=3.55
.material   copper METAL CONDUCTIVITY=56.7meg
.layerstack chipstack LAYER=(oxide,2.5um)
.fsoptions  opt1 ACCURACY=MEDIUM PRINTDATA=YES
.shape widewire RECTANGLE WIDTH=2um HEIGHT=0.7um
.model coplanar W MODELTYPE=FieldSolver
+ LAYERSTACK=chipstack FSOPTIONS=opt1 RLGCFILE=coplanar.rlgc
+ CONDUCTOR=(SHAPE=widewire ORIGIN=(0,0.9um) MATERIAL=copper TYPE=reference)
+ CONDUCTOR=(SHAPE=widewire ORIGIN=(8um,0.9um) MATERIAL=copper)
+ CONDUCTOR=(SHAPE=widewire ORIGIN=(12um,0.9um) MATERIAL=copper)
+ CONDUCTOR=(SHAPE=widewire ORIGIN=(20um,0.9um) MATERIAL=copper TYPE=reference)

*--------------------------------------------------------------------------
* Simulation Netlist
*--------------------------------------------------------------------------

Vdd vdd gnd 'SUPPLY'
Vin n11 gnd PULSE 0 'SUPPLY' 0ps 20ps 20ps 500ps 1000ps
W1 n12 n22 gnd n13 n23 gnd FSmodel=coplanar N=2 l=6mm
X1 n11 n12 inv M=80
X2 n13 n14 inv M=40
X3 gnd n22 inv M=80
X4 n23 n24 inv M=40

*-----------------------------------------------------------------
* Stimulus
*-----------------------------------------------------------------
.tran 1ps 250ps
.end





























