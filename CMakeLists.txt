cmake_minimum_required(VERSION 3.18)
project(vector_add)

find_package(pybind11 REQUIRED)
find_package(CUDAToolkit REQUIRED)

add_library(vector_add MODULE vector_add.cc vector_add.cu)
target_link_libraries(vector_add PRIVATE pybind11::module CUDA::cudart)
target_compile_features(vector_add PRIVATE cxx_std_17)
set_target_properties(vector_add PROPERTIES PREFIX "" SUFFIX ".so")

