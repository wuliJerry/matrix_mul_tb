#!/bin/bash

# Compile the matrix multiplication code with LIKWID_PERFMON flag
gcc -O3 -DLIKWID_PERFMON -llikwid matmul.c -o matmul

# Loop over different tile sizes
mkdir output

for tileSize in 32 64 96 128; do
    # Run the matrix multiplication code with transformed loops and measure L1 data movements
    likwid-perfctr -C 0-3 -g CACHE -m ./matmul 1024 $tileSize > output/output_${tileSize}.txt
done

