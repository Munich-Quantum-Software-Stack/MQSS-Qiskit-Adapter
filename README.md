# mqp-qiskit-provider

## Installation

```shell
pip install mqp-qiskit-provider
```

## Usage

```python
from qiskit import QuantumCircuit
from mqp.qiskit_provider import MQPProvider

# instantiate the MQP provider with your api token
provider = MQPProvider(token="<api-token>")
# get a list of all backends you have access to
all_backends = provider.backends()
# get a specific backend by its name
backend = provider.get_backend("<resource-name>")

# create a circuit
circuit = QuantumCircuit(2, 2)
circuit.h(0)
# .....
# create a job and get the results
# (currently one one circuit per job)
job = backend.run(circuit, shots=1000)
# query the status of the job
status = job.status()
# cancel the job
job.cancel()
# get the result of the job
result = job.result()
# get the job's resulting counts
counts = result.get_counts()
```

## Changelog

See the [CHANGELOG](CHANGELOG.md) for details on changes in each version.
