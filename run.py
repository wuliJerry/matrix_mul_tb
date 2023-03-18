#!/usr/bin/python3

import subprocess as sp

arg1 = "4096"
command_base = "likwid-perfctr -C 0,2,4,6,8,10,12,14 -g L2"
command_thread = f" : ./matmul {arg1} "
command = command_base
out_prefix = "output_"

sp.run("gcc -O3 -DLIKWID_PERFMON -fopenmp -llikwid matmul.c -o matmul", shell=True)

with open("para.txt", "r") as file:
    args = []
    counter = 0
    
    for line in file:

        args.append(line.strip())

        if len(args) == 8:

            for tile in args:
                command = command + command_thread + tile
            command += f" > output/report_{counter}.txt"

            sp.run(command, shell=True)

            args = []
            command = command_base  
            counter += 1

    if len(args) > 0: 
        pass

