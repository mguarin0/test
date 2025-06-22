cmake_minimum_required(VERSION 3.18)
project(vector_add LANGUAGES C CXX CUDA)

find_package(pybind11 REQUIRED)
find_package(CUDAToolkit REQUIRED)

add_library(_vector_add MODULE vector_add.cc vector_add.cu)
set_target_properties(_vector_add PROPERTIES PREFIX "" SUFFIX ".so")

target_compile_features(_vector_add PRIVATE cxx_std_17)
target_link_libraries(_vector_add PRIVATE pybind11::module CUDA::cudart)
