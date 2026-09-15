* inv.sp
*----------------------------------------------------
* Parameters and Models
*----------------------------------------------------

.param SUPPLY=1.0
.option scale=25n
.include '../models/ibm065/models.sp'
.temp 70
.option post

*--------------------------------------------------------
* Simulation Netlist
*--------------------------------------------------------

Vdd vdd gnd 'SUPPLY'
Vin a gnd PULSE 0 'SUPPLY' 25ps 0ps 0ps 35ps 80ps
M1 y a gnd gnd NMOS W=4 L=2 AS=20 PS=18 AD=20 PD=18
M2 y a vdd vdd PMOS W=8 L=2 AS=40 PS=26 AD=40 PD=26

*---------------------------------------------------------
* Stimulus
*---------------------------------------------------------

.tran 0.1ps 80ps
.end

