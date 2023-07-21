#!/bin/bash


operation="-R" # MLC operation, can be change to “W6” or “W7“
gcc -Ofast -fargument-noalias -mavx2 -fopenmp -DSTREAM_ARRAY_SIZE=55000000 stream.c -o stream

function start()
{
        for mba in $(seq 10 10 100)
        do
                pqos -I -R
                pqos -I -e mba:1=$mba  # bound MBA policy to COS1

                echo -n "COS1 cpus_list:"
                cat /sys/fs/resctrl/COS1/cpus_list
                echo -n "COS1 schemata:"
                cat /sys/fs/resctrl/COS1/schemata

                mkdir -p results

                pqos -I -r  > results/pqos_$mba.txt & # pqos as monitor

                echo "./stream > results/$mba.txt" # run 5min
                ./stream > results/$mba.txt # run 5min
                pkill -9 pqos # close pqos
                pqos -I -R # reset all RDT  settings.

        done
}

start # begin test.`
