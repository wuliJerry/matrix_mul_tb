matrix_size = 8192
cache_size = 512*1024
factors = [factor for factor in range(1, matrix_size+1) if matrix_size % factor == 0]

for i in factors:
    for j in factors:
        if i*j <= cache_size:
            for k in factors:
                if i*k + j*k + i*j <= cache_size and 2*i*k + 2*j*k + i*j >= cache_size:
                    print(f"{i}, {j}, {k}")
