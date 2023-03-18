#include <stdio.h>
#include <stdlib.h>
#include <likwid.h>
#include <string.h>

void matmul(int N, int *A, int *B, int *C, int *tileSizes) {
    LIKWID_MARKER_START("matrix_multiplication");
    int num_tiles_i = (N + tileSizes[0] - 1) / tileSizes[0];
    int num_tiles_j = (N + tileSizes[1] - 1) / tileSizes[1];
    int num_tiles_k = (N + tileSizes[2] - 1) / tileSizes[2];
    int total_tiles = num_tiles_i * num_tiles_j * num_tiles_k;
    int tile_counter = 0;

	//#pragma omp parallel for schedule(static) collapse(2)
    for (int i = 0; i < N; i += tileSizes[0]) {
        for (int j = 0; j < N; j += tileSizes[1]) {
            for (int k = 0; k < N; k += tileSizes[2]) {
                int ii_end = i + tileSizes[0] < N ? i + tileSizes[0] : N;
                int jj_end = j + tileSizes[1] < N ? j + tileSizes[1] : N;
                int kk_end = k + tileSizes[2] < N ? k + tileSizes[2] : N;
                for (int ii = i; ii < ii_end; ii++) {
                    for (int jj = j; jj < jj_end; jj++) {
                        int c = 0;
                        for (int kk = k; kk < kk_end; kk++) {
                            c += A[ii * N + kk] * B[kk * N + jj];
                        }
                        C[ii * N + jj] += c;
                    }
                }
                tile_counter++;
                // printf("\rProgress: %d/%d (%d%%)", tile_counter, total_tiles, tile_counter * 100 / total_tiles);
                // fflush(stdout);
            }
        }
    }
    printf("\n");
    LIKWID_MARKER_STOP("matrix_multiplication");
}

int main(int argc, char **argv) {
    LIKWID_MARKER_INIT;

    int N = atoi(argv[1]);
    int tileSize[3] = {atoi(argv[2]), atoi(argv[3]), atoi(argv[4])};

    int *A = (int*)malloc(N * N * sizeof(int));
    int *B = (int*)malloc(N * N * sizeof(int));
    int *C = (int*)calloc(N * N, sizeof(int));

    // Initialize matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i * N + j] = (int)rand() / RAND_MAX;
            printf("%d ", A[i * N + j]);
            B[i * N + j] = (int)rand() / RAND_MAX;
            printf("%d ", B[i * N + j]);
        }
    }

    // Perform matrix multiplication with loop transformation and tile size optimization
    //matmul(N, A, B, C, tileSize);

    // Print result
    printf("C[0][0] = %d\n", C[0]);

    free(A);
    free(B);
    free(C);

    LIKWID_MARKER_CLOSE;

    return 0;
}

