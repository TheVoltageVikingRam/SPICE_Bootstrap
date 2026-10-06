#!/bin/bash

for N in {1..10}
do
    sed "s/parameters N=1/parameters N=$N/" \
        parameterized_T_netlist.scs > T_N${N}.scs

    spectre T_N${N}.scs > T_N${N}.log

    echo "Finished N=$N"
done
