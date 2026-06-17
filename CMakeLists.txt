cmake_minimum_required(VERSION 3.18)
project(beamng_perf_sim)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE pybind11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(beamng_perf_core src/core/engine_sim.cpp)
set_target_properties(beamng_perf_core PROPERTIES INTERPROCEDURAL_OPTIMIZATION FALSE)
