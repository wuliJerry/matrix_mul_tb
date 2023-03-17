#!/bin/bash

# Compile the matrix multiplication code with LIKWID_PERFMON flag
gcc -O3 -DLIKWID_PERFMON -llikwid matmul.c -o matmul

# Loop over different tile sizes
mkdir output

for ((i=32; i<=128; i+=32)); do
    for ((j=32; j<=128; j+=32)); do
        for ((k=32; k<=128; k+=32)); do
            # Run the matrix multiplication code with transformed loops and measure L1 data movements
            likwid-perfctr -C 0-3 -g L2 -m ./matmul 1024 "$i" "$j" "$k" > output/output_${i}_${j}_${k}.txt
        done
    done
done

