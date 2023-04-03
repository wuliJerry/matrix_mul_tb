#include <iostream>
#include <vector>
#include <fstream>
#include <cuda_runtime.h>
#include <sstream>
#include <iterator>
#include <cuda_profiler_api.h>
#include <cuda_device_runtime_api.h>

__global__ void matmul_tiled(const int N, const float *A, const float *B, float *C, int tileSizes[3]) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    int j = blockIdx.y * blockDim.y + threadIdx.y;
    int k_tile = blockIdx.z * blockDim.z + threadIdx.z;

    if (i < N && j < N && k_tile < N) {
        float sum = 0.0f;
        for (int k = k_tile; k < min(k_tile + tileSizes[2], N); k++) {
            sum += A[i * N + k] * B[k * N + j];
        }
        atomicAdd(&C[i * N + j], sum);
    }
}

void read_params(const std::string &filename, std::vector<std::vector<int>> &params) {
    std::ifstream file(filename);
    std::string line;
    while (std::getline(file, line)) {
        std::istringstream iss(line);
        std::vector<int> param_set((std::istream_iterator<int>(iss)), std::istream_iterator<int>());
        if (!param_set.empty()) {
            params.push_back(param_set);
        }
    }
}

int main() {
	// cudaProfilerStart();
    cudaDeviceSynchronize();

    std::vector<std::vector<int>> params;
    read_params("params.txt", params);

    for (const auto &param_set : params) {
        int N = param_set[0];
        int tileSizes[3] = {param_set[1], param_set[2], param_set[3]};

        float *A, *B, *C;
        cudaMallocManaged(&A, N * N * sizeof(float));
        cudaMallocManaged(&B, N * N * sizeof(float));
        cudaMallocManaged(&C, N * N * sizeof(float));

		std::cout << N << " " << tileSizes[0] << " " << tileSizes[1] << " " << tileSizes[2] << std::endl;

        for (int i = 0; i < N * N; i++) {
            A[i] = rand() % 10 + 1;
            B[i] = rand() % 10 + 1;
            C[i] = 0;
        }

        dim3 blockDim(tileSizes[0], tileSizes[1], tileSizes[2]);
        dim3 gridDim((N + blockDim.x - 1) / blockDim.x, (N + blockDim.y - 1) / blockDim.y, (N + blockDim.z - 1) / blockDim.z);
        matmul_tiled<<<gridDim, blockDim>>>(N, A, B, C, tileSizes);

        cudaDeviceSynchronize();

        // Print the result matrix C (optional)
        // for (int i = 0; i < N; i++) {
        //     for (int j = 0; j < N; j++) {
        //         std::cout << C[i * N + j] << " ";
        //     }
        //     std::cout << std::endl;
        // }

        cudaFree(A);
        cudaFree(B);
        cudaFree(C);
    }

  	// cudaProfilerStop();

	cudaDeviceSynchronize();
    return 0;
}

