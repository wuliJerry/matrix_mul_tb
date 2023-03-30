import torch
import matplotlib.pyplot as plt

def benchmark_memory(fn, *inputs, desc='', verbose=True, **kwinputs):
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.synchronize()
    fn(*inputs, **kwinputs)
    torch.cuda.synchronize()
    mem = torch.cuda.max_memory_allocated() / ((2 ** 20) * 1000)
    if verbose:
        print(f'{desc} max memory: {mem}GB')
    torch.cuda.empty_cache()
    return mem

def matmul_tiled(N, A, B, C, tileSizes):
    for i in range(0, N, tileSizes[0]):
        for j in range(0, N, tileSizes[1]):
            for k in range(0, N, tileSizes[2]):
                ii_end = min(i + tileSizes[0], N)
                jj_end = min(j + tileSizes[1], N)
                kk_end = min(k + tileSizes[2], N)

                A_tile = A[i:ii_end, k:kk_end].float().to('cuda')
                B_tile = B[k:kk_end, j:jj_end].float().to('cuda')
                C_tile = C[i:ii_end, j:jj_end].float().to('cuda')

                C_tile += torch.matmul(A_tile, B_tile)
                C[i:ii_end, j:jj_end] = C_tile.cpu().int()



# def main():
#     # Read parameters from a text file
#     with open('params.txt', 'r') as f:
#         params = [list(map(int, line.strip().split())) for line in f.readlines()]
# 
#     # Prepare the output CSV file
#     with open('results.csv', 'w', newline='') as csvfile:
#         result_writer = csv.writer(csvfile, delimiter=',')
#         result_writer.writerow(['Parameters', 'Memory Usage (GB)'])
# 
#         # Process each parameter set
#         for param_set in params:
#             N, tile_size_i, tile_size_j, tile_size_k = param_set
#             tileSizes = (tile_size_i, tile_size_j, tile_size_k)
# 
#             A = torch.randint(1, 11, (N, N), dtype=torch.int)
#             B = torch.randint(1, 11, (N, N), dtype=torch.int)
#             C = torch.zeros((N, N), dtype=torch.int)
# 
#             # Perform matrix multiplication with loop transformation and tile size optimization
#             mem_usage = benchmark_memory(matmul_tiled, N, A, B, C, tileSizes, verbose=False)
# 
#             # Write the results to the CSV file
#             result_writer.writerow([f'{N} {tile_size_i} {tile_size_j} {tile_size_k}', mem_usage])
# 
#             print(f"Parameters: {N} {tile_size_i} {tile_size_j} {tile_size_k} - Memory Usage: {mem_usage} GB")

import csv


def main():
    # Read parameters from a text file
    with open('params.txt', 'r') as f:
        params = [list(map(int, line.strip().split())) for line in f.readlines() if line.strip()]

    # Store memory usage and reciprocal sum of tile sizes
    mem_usage_list = []
    reciprocal_sum_list = []

    with open('results.csv', 'w', newline='') as csvfile:
        result_writer = csv.writer(csvfile, delimiter=',')
        result_writer.writerow(['Parameters', 'Memory Usage (GB)'])

        # Process each parameter set
        for param_set in params:
            N, tile_size_i, tile_size_j, tile_size_k = param_set
            tileSizes = (tile_size_i, tile_size_j, tile_size_k)

            A = torch.randint(1, 11, (N, N), dtype=torch.int)
            B = torch.randint(1, 11, (N, N), dtype=torch.int)
            C = torch.zeros((N, N), dtype=torch.int)

            # Perform matrix multiplication with loop transformation and tile size optimization
            mem_usage = benchmark_memory(matmul_tiled, N, A, B, C, tileSizes, verbose=False)

            result_writer.writerow([f'{N} {tile_size_i} {tile_size_j} {tile_size_k}', mem_usage])

            print(f"Parameters: {N} {tile_size_i} {tile_size_j} {tile_size_k} - Memory Usage: {mem_usage} GB")

            mem_usage_list.append(mem_usage)
            reciprocal_sum_list.append(1 / tile_size_i + 1 / tile_size_j)

    # Plot the relationship between memory usage and the reciprocal sum of tile sizes
    plt.scatter(reciprocal_sum_list, mem_usage_list)
    plt.xlabel("1/tile_size_i + 1/tile_size_j")
    plt.ylabel("Memory Usage (GB)")
    plt.title("Memory Usage vs Reciprocal Sum of Tile Sizes")
    plt.show()

if __name__ == "__main__":
    main()
