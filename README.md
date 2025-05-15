# MQSS Qiskit Adapter

[![Documentation](https://img.shields.io/badge/Documentation-Read%20the%20Docs-blue)](https://munich-quantum-software-stack.github.io/MQSS-Interfaces/qiskit/index.html)
![PyPI - Version](https://img.shields.io/pypi/v/mqss-qiskit)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mqss-qiskit)

This repository implements a Qiskit Adapter, which is able to send quantum jobs to LRZ's
infrastructure.

## Installation

To install the package, simply run

```bash
pip install mqss-qiskit
```

## Usage

MQSS Qiskit Adapter has support for most of the basic features that a Qiskit provider implement. For
all available features, see the detailed
[documentation](https://munich-quantum-software-stack.github.io/MQSS-Interfaces/qiskit/index.html).

```python
from mqss.qiskit_adapter import MQSSQiskitAdapter
from qiskit.circuit import QuantumCircuit

#Create a quantum circuit
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()

# Get the right backend
mqss_adapter = MQSSQiskitAdapter(token="<TOKEN>")
[backend] = mqss_adapter.backends(name="<BACKEND_NAME>")

# Submit the jobs
job = backend.run(qc, shots=100)

# Get the results
print(job.result().get_counts())

```

## Contributing

Feel free to open issues or submit pull requests to improve this project!
