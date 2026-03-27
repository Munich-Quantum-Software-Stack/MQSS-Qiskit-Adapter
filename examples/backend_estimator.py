import math
import sys
from qiskit import QuantumCircuit
from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.primitives import BackendEstimatorV2

adapter = MQSSQiskitAdapter(token="<api-token>")
[backend] = adapter.backends(name="<resource-name>")


def estimate_required_shots(precision, variance=1.0):
    if precision <= 0:
        raise ValueError("precision must be > 0")
    return math.ceil(variance / (precision**2))


# State-preparation circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Define a simple Hamiltonian
H = SparsePauliOp.from_list(
    [
        ("ZI", 1.0),
        ("IZ", 1.0),
        ("ZZ", 1.0),
    ]
)

# Compute the ideal expectation for comparisons
sv_logical = Statevector.from_instruction(qc)
ev_ideal = sv_logical.expectation_value(H)
ev_ideal_val = float(ev_ideal.real)

# Run the Estimator grouping commuting observables
estimator = BackendEstimatorV2(backend=backend)
estimator.options.abelian_grouping = True
precision = 0.01

estimated_num_shots = estimate_required_shots(precision=precision, variance=1.0)
print(f"Requested precision = {precision}")
print(f"Estimated shots (placeholder worst-case) ≈ {estimated_num_shots}")

if estimated_num_shots > 20000:
    print("Error: estimated shot count is too high.")
    print("Consider using a looser precision (e.g. precision=0.05).")
    sys.exit(1)

job = estimator.run([(qc, H)], precision=precision)
result = job.result()
pub_result = result[0]

ev_backend_val = float(pub_result.data.evs)
print("Ideal Estimator expectation value   =", ev_ideal_val)
print("Backend Estimator expectation value =", ev_backend_val)
print("Absolute error |backend - ideal|   =", abs(ev_backend_val - ev_ideal_val))
