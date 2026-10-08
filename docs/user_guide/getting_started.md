# Getting Started

## Installation

To install the MQSS Qiskit adapter, use the following command:

```shell
pip install mqss-qiskit
```

## Overview

The Qiskit adapter for MQSS allows users to access MQSS backends through Qiskit. The main components
are:

- [`MQSSQiskitAdapter`](../api/mqss_adapter.md): This is the main entry point for accessing MQSS
  backends.
- [`MQSSQiskitBackend`](../api/mqss_backend.md): It interfaces with the MQSS backends.
- [`MQSSQiskitJob`](../api/mqss_job.md): It handles job submission, cancellation, status checking,
  and result retrieval.

## Usage

### Import Required Modules

Import the necessary components from [Qiskit](https://qiskit.org) and the MQSS adapter package.

```python
from qiskit import QuantumCircuit
from mqss.qiskit_adapter import MQSSQiskitAdapter
```

### Initialize the MQSS Qiskit Adapter

Create an instance of `MQSSQiskitAdapter` by supplying your token from
[MQP](https://portal.quantum.lrz.de).

```python
adapter = MQSSQiskitAdapter(token="<api-token>")
```

### List Available Backends

Retrieve and inspect the list of backends accessible to your account.

```python
all_backends = adapter.backends()
print("Available backends:", all_backends)
```

### List Online Backends

Retrieve and inspect the list of backends that are online and accessible to your account.

```python
all_online_backends = adapter.backends(online=True)
print("Available backends:", all_online_backends)
```

### Select a Specific Backend

Choose a backend by its identifier. Replace `<resource-name>` with the actual name of the backend.

```python
backend = adapter.get_backend("<resource-name>")
# OR
[backend] = adapter.backends(name="<resource-name>")
```

### Design Your Quantum Circuit

Construct your quantum circuit using Qiskit's
[`QuantumCircuit`](https://qiskit.org/documentation/stubs/qiskit.circuit.QuantumCircuit.html). For
example, create a circuit with 2 qubits and 2 classical bits.

```python
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])
```

### Submit Your Job

Submit the circuit for execution on the chosen backend. Specify the number of shots as required.
Note that the circuit is transpiled automatically at server before it is submitted to the backend.

```python
job = backend.run(circuit, shots=1000)
```

### Transpile Circuit and Submit Job

If you want to transpile the circuit yourself you can do it as follows and then submit it as a job
with `no_modify=True` flag to skip transpilation at server side and submit the circuit as it is to
the backend.

!!! Note "The transpilation at user end may not be supported for some backends."

```python
from qiskit import QuantumCircuit, compiler
transpiled_circuit = compiler.transpile(circuit, backend, optimization_level=3)
job = backend.run(transpiled_circuit, shots=1000, no_modify=True)
```

### Select Physical Qubits

To choose which physical qubits execute a circuit, provide an `initial_layout` when transpiling. The
list position is the virtual circuit qubit, and the value is the physical backend qubit. For
example, this maps circuit qubit 0 to physical qubit 3 and circuit qubit 1 to physical qubit 5:

```python
from qiskit import transpile

transpiled_circuit = transpile(
  circuit,
  backend,
  initial_layout=[3, 5],
  optimization_level=1,
)
job = backend.run(transpiled_circuit, shots=1000, no_modify=True)
```

Use `no_modify=True` to prevent server-side transpilation from changing the selected mapping. If the
selected physical qubits are not directly connected in the backend topology, Qiskit may insert SWAP
operations. You can inspect the resulting mapping with `print(transpiled_circuit.layout)`.

### Checking the Number of Pending Jobs on a Backend

To determine if a backend is overloaded, you can check the number of pending jobs using the
`num_pending_jobs` property.

```python
print("Number of pending jobs:", backend.num_pending_jobs)
```

### Queuing a Job when Backend is Offline

By default, a job scheduled on a backend with an offline status will be cancelled. To queue a job on
an offline backend, use the `queued=True` flag. This will ensure that the job is enqueued and will
be executed once the backend becomes available.

!!! Note "The job is queued for limited time and cancelled if the backend is still offline."

```python
job = backend.run(circuit, shots=1000, queued=True)
```

### Monitor Job Status

You can check the status of your job as follows. The status indicates the current stage (e.g.,
QUEUED, INITIALIZING, DONE).

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

### Mid-Circuit Measurements

A classical measurement can control a later operation in the same circuit:

```python
circuit = QuantumCircuit(1, 1)
circuit.h(0)
circuit.measure(0, 0)  # Store the mid-circuit result in c0

with circuit.if_test((circuit.clbits[0], True)):
  circuit.x(0)  # Apply X only when c0 is 1

circuit.measure_all()  # Store the final result in a new bit, c1
```

Qiskit displays classical bits from highest to lowest index, so the output is `c1 c0`: the left bit
is the final measurement and the right bit is the mid-circuit measurement. For example:

- `0 0`: the mid-circuit result was 0, so no X was applied; the final result was 0.
- `0 1`: the mid-circuit result was 1, so X was applied; the final result was 0.

An example result from 100 shots is `{'0 0': 54, '0 1': 40, '1 1': 6}`. The additional `1 1` results
can be caused by noise or measurement errors on a real backend.
