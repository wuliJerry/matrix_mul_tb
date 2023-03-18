#!/usr/bin/python3

import subprocess as sp

arg1 = "4096"
command_base = "likwid-perfctr -g L2 "
command_thread = f" -m ./matmul {arg1} "
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
                command = command_base + f"-C {counter}" + command_thread + tile
                command += f" > output/report_{tile}.txt"
                counter += 2

            # sp.run(command, shell=True)
            print(command)

            args = []
            command = command_base  
            counter = 0

    if len(args) > 0: 
        pass

