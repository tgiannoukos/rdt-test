#!/bin/bash

core_list="
1
1,2
" # will run cores in this list, 1 loop per line.

operation="-R" # MLC operation, can be change to “W6” or “W7“

function start()
{
        for i in $core_list
        do
                for mba in $(seq 10 10 100)
                do
                        pqos -I -R
                        pqos -I -a core:1=$i   # bound COS1 for cores
                        pqos -I -e mba:1=$mba  # bound MBA policy to COS1

                        echo -n "COS1 cpus_list:"
                        cat /sys/fs/resctrl/COS1/cpus_list
                        echo -n "COS1 schemata:"
                        cat /sys/fs/resctrl/COS1/schemata

                        mkdir -p $i

                        pqos -I -r -m all:[$i] > $i/pqos_$mba.txt & # pqos as monitor

                        echo "/Users/akis/Linux/mlc --loaded_latency -d0 $operation -t300 -T -k$i > $i/$mba.txt" # run 5min
                        /Users/akis/Linux/mlc --loaded_latency -d0 $operation -t300 -T -k$i > $i/$mba.txt # run 5min
                        pkill -9 pqos # close pqos
                        pqos -I -R # reset all RDT  settings.

                done
        done
}

start # begin test.`
