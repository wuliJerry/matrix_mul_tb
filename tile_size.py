factors = [factor for factor in range(1, 8193) if 8192 % factor == 0]

for i in factors:
    for j in factors:
        if i*j <= 512*1024:
            for k in factors:
                if i*k + j*k + i*j <= 512*1024 and 2*i*k + 2*j*k + i*j >= 512*1024:
                    print(f"{i}, {j}, {k}")

