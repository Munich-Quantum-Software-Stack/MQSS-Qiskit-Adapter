# Getting Started

## Installation

To install the MQP Qiskit provider, use the following command:

```shell
pip install mqp-qiskit-provider
```

## Overview

The Qiskit provider for MQP allows users to access MQP backends through Qiskit. The main components are:

- [`MQPProvider`](../api/mqp_provider.md): This is the main entry point for accessing MQP backends.
- [`MQPBackend`](../api/mqp_backend.md): It interfaces with the MQP backends.
- [`MQPJob`](../api/mqp_job.md): It handles job submission, cancellation, status checking, and result retrieval.

## Usage

### Import Required Modules

Import the necessary components from [Qiskit](https://qiskit.org) and the MQP provider package.

```python
from qiskit import QuantumCircuit
from mqp.qiskit_provider import MQPProvider
```

### Initialize the MQP Provider

Create an instance of `MQPProvider` by supplying your token from [MQP](https://portal.quantum.lrz.de).

```python
provider = MQPProvider(token="<api-token>")
```

### List Available Backends

Retrieve and inspect the list of backends accessible to your account.

```python
all_backends = provider.backends()
print("Available backends:", all_backends)
```

### List Online Backends

Retrieve and inspect the list of backends that are online and accessible to your account.

```python
all_backends = provider.backends(online=True)
print("Available backends:", all_backends)
```

### Select a Specific Backend

Choose a backend by its identifier. Replace `<resource-name>` with the actual name of the backend.

```python
backend = provider.get_backend("<resource-name>")
# OR
[backend] = provider.backends(name="<resource-name>")
```

### Design Your Quantum Circuit

Construct your quantum circuit using Qiskit's [`QuantumCircuit`](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html). For example, create a circuit with 2 qubits and 2 classical bits.

```python
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])
```

### Submit Your Job

Submit the circuit for execution on the chosen backend. Specify the number of shots as required. Note that the circuit is transpiled automatically at server before it is submitted to the backend.

```python
job = backend.run(circuit, shots=1000)
```

### Transpile Circuit and Submit Job

If you want to transpile the circuit yourself you can do it as follows and then submit it as a job with `no_modify=True` flag to skip transpilation at server side and submit the circuit as it is to the backend.

!!! Note "The transpilation at user end may not be supported for some backends."

```python
from qiskit import QuantumCircuit, compiler
transpiled_circuit = compiler.transpile(circuit, backend, optimization_level=3)
job = backend.run(transpiled_circuit, shots=1000, no_modify=True)
```

### Monitor Job Status

You can check the status of your job as follows. The status indicates the current stage (e.g., QUEUED, INITIALIZING, DONE).

```python
status = job.status()
print("Job status:", status)
```

### Cancel the Job

If necessary, you cancel the job before it completes.

```python
job.cancel()
```

### Retrieve and Display Results

Once the job is completed, fetch the results and display the measurement counts.

```python
result = job.result()
counts = result.get_counts()
print("Measurement counts:", counts)
```

### Timestamps for Job Execution

```python
result_dict = job.result().to_dict()
print(result_dict["timestamps"]["submitted"])
print(result_dict["timestamps"]["scheduled"])
print(result_dict["timestamps"]["completed"])
```
