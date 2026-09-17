* corner.sp
* Step response of unloaded inverter across process corners

*-------------------------------------------------------------
* Parameters and models
*-------------------------------------------------------------

.option scale=25n
.param SUP=1.0      *Must set before calling .lib
.lib '../models/ibm065./opconditions.lib' TT
.option post

*--------------------------------------------------------------
* Simulation Netlist
*--------------------------------------------------------------

Vdd vdd gnd 'SUPPLY'
Vin a gnd PULSE 0 'SUPPLY' 25ps 0ps 0ps 35ps 80ps
M1 y a gnd gnd NMOS W=4 L=2 AS=20 PS=18 AD=20 PD=18
M2 y a vdd vdd PMOS W=8 L=2 AS=40 PS=26 AD=40 PD=26

*--------------------------------------------------------------
* Stimulus
*--------------------------------------------------------------

.tran 0.1ps 80ps
.alter
.lib '../models/ibm065/opconditions.lib' FF
.alter 
.lib '../models/ibm065/opconditions.lib' SS
.end





