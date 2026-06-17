#include <pybind11/pybind11.h>

namespace py = pybind11;

// This is a simple test function. Later we will put real torque math here.
float calculate_torque(float rpm, float max_torque) {
    if (rpm < 1000) return max_torque * (rpm / 1000.0f) * 0.8f;
    if (rpm < 4000) return max_torque * 0.8f + (max_torque * 0.2f) * ((rpm - 1000) / 3000.0f);
    if (rpm < 7000) return max_torque - (max_torque * 0.3f) * ((rpm - 4000) / 3000.0f);
    return max_torque * 0.1f;
}

// This binds the C++ function to Python so our server can use it
PYBIND11_MODULE(beamng_perf_core, m) {
    m.def("calculate_torque", &calculate_torque, "A function to calculate engine torque");
}
