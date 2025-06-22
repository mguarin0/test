// vector_add.cc
#include <cuda_runtime.h>
#include <pybind11/pybind11.h>
#include "xla/ffi/api/c_api.h"
#include "xla/ffi/api/ffi.h"

__global__ void vector_add_kernel(const float* a, const float* b, float* out, int size);

void VectorAddImpl(const float* a, const float* b, float* out, int size, cudaStream_t stream) {
    int threads = 256;
    int blocks = (size + threads - 1) / threads;
    vector_add_kernel<<<blocks, threads, 0, stream>>>(a, b, out, size);
}

XLA_FFI_DEFINE_HANDLER(
    VectorAddHandler,
    std::tuple<const float*, const float*, float*, int>,
    {
        const float* a = std::get<0>(args);
        const float* b = std::get<1>(args);
        float* out = std::get<2>(args);
        int size = std::get<3>(args);
        VectorAddImpl(a, b, out, size, stream);
    }
)

namespace py = pybind11;

PYBIND11_MODULE(vector_add, m) {
    xla::ffi::RegisterHandler("my.vector_add", VectorAddHandler);
}

