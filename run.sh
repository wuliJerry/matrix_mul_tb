#!/bin/bash

# Compile the matrix multiplication code with LIKWID_PERFMON flag
gcc -O3 -DLIKWID_PERFMON -fopenmp -llikwid matmul.c -o matmul

# Loop over different tile sizes
mkdir output

export OMP_NUM_THREADS=14

for ((i=256; i<=1024; i+=256)); do
    for ((j=256; j<=1024; j+=256)); do
        for ((k=256; k<=1024; k+=256)); do
            # Run the matrix multiplication code with transformed loops and measure L1 data movements
            likwid-perfctr -C 0-13 -g L2 -m ./matmul 8192 "$i" "$j" "$k" > output/output_${i}_${j}_${k}.txt
        done
    done
done

