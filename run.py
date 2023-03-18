#!/usr/bin/python3

import subprocess as sp

matSize = "4096"
command_base = "likwid-perfctr -g L2 "
command_thread = f" -m ./matmul {matSize} "
command = ""
out_prefix = "output_"

sp.run("gcc -O3 -DLIKWID_PERFMON -fopenmp -llikwid matmul.c -o matmul", shell=True)

with open("para.txt", "r") as file:
    args = []
    
    for line in file:

        args.append(line.strip())

        if len(args) == 8:
            counter = 0
            for tile in args:
                i, j, k = tile.split()
                command += command_base + f"-C {counter}" + command_thread + tile
                command += f" > output/report_{i}_{j}_{k}.txt &"
                counter += 2

            # sp.run(command, shell=True)
            print(command)

            args = []
            command = ""
            counter = 0

    if len(args) > 0: 
        pass

