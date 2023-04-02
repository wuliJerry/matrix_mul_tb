#!/usr/bin/python3

import torch

def matmul_tiled(N, A, B, C, tileSizes):
    for i in range(0, N, tileSizes[0]):
        for j in range(0, N, tileSizes[1]):
            for k in range(0, N, tileSizes[2]):
                ii_end = min(i + tileSizes[0], N)
                jj_end = min(j + tileSizes[1], N)
                kk_end = min(k + tileSizes[2], N)

                A_tile = A[i:ii_end, k:kk_end].float()
                B_tile = B[k:kk_end, j:jj_end].float()
                C_tile = C[i:ii_end, j:jj_end].float()

                C_tile += torch.matmul(A_tile, B_tile)
                C[i:ii_end, j:jj_end] = C_tile

def main():
    # Read parameters from a text file
    with open('params.txt', 'r') as f:
        params = [list(map(int, line.strip().split())) for line in f.readlines() if line.strip()]

    # Process each parameter set
    for param_set in params:
        N, tile_size_i, tile_size_j, tile_size_k = param_set
        tileSizes = (tile_size_i, tile_size_j, tile_size_k)

        device = torch.device('cuda')

        A = torch.randint(1, 11, (N, N), dtype=torch.int, device=device)
        B = torch.randint(1, 11, (N, N), dtype=torch.int, device=device)
        C = torch.zeros((N, N), dtype=torch.int, device=device)

        # Perform matrix multiplication with loop transformation and tile size optimization
        matmul_tiled(N, A, B, C, tileSizes)

        # Transfer the final result to the host
        # C = C.cpu().int()

if __name__ == "__main__":
    main()

