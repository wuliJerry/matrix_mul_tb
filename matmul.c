#include <stdio.h>
#include <stdlib.h>
#include <likwid.h>

void matmul(int N, float *A, float *B, float *C, int tileSize) {
	LIKWID_MARKER_START("matrix_multiplication");
    for (int i = 0; i < N; i += tileSize) {
        for (int j = 0; j < N; j += tileSize) {
            for (int k = 0; k < N; k += tileSize) {
                for (int ii = i; ii < i + tileSize && ii < N; ii++) {
                    for (int jj = j; jj < j + tileSize && jj < N; jj++) {
                        float c = 0.0;
                        for (int kk = k; kk < k + tileSize && kk < N; kk++) {
                            c += A[ii * N + kk] * B[kk * N + jj];
                        }
                        C[ii * N + jj] += c;
                    }
                }
            }
        }
    }
	LIKWID_MARKER_STOP("matrix_multiplication");
}

int main(int argc, char **argv) {
	LIKWID_MARKER_INIT;
    int N = atoi(argv[1]);
    int tileSize = atoi(argv[2]);

    float *A = (float*)malloc(N * N * sizeof(float));
    float *B = (float*)malloc(N * N * sizeof(float));
    float *C = (float*)calloc(N * N, sizeof(float));

    // Initialize matrices
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i * N + j] = (float)rand() / RAND_MAX;
            B[i * N + j] = (float)rand() / RAND_MAX;
        }
    }

    // Perform matrix multiplication with loop transformation and tile size optimization
    matmul(N, A, B, C, tileSize);

    // Print result
    printf("C[0][0] = %f\n", C[0]);

    free(A);
    free(B);
    free(C);
	LIKWID_MARKER_CLOSE;

    return 0;
}

