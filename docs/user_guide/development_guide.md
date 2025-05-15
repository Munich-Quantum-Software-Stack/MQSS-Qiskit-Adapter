# Development Guide

## Project Overview

This project provides a Qiskit adapter for MQSS, allowing users to access MQSS backends through
Qiskit. The main components of the project are:

- `adapter.py`: Contains the [`MQSSQiskitAdapter`](../api/mqss_adapter.md) class, which serves as
  the main entry point for accessing MQSS backends.
- `backend.py`: Contains the [`MQSSQiskitBackend`](../api/mqss_backend.md) class, which interfaces
  with the MQSS backends.
- `job.py`: Contains the [`MQSSQiskitJob`](../api/mqss_job.md) class, which handles job
  cancellation, status checking, and result retrieval.
- `mqss_resource.py`: Contains functions to retrieve the coupling map and target for the MQSS
  backend.

## Prerequisites

Before you start developing, ensure you have the following installed:

- Python 3.9 to 3.13
- [`uv`](https://docs.astral.sh/uv/) package manager for python

## Setting Up the Development Environment

**Clone the repository:**

```sh
git clone https://github.com/Munich-Quantum-Software-Stack/MQSS-Qiskit-Adapter.git
cd MQSS-Qiskit-Adapter
```

**Create a virtual environment and install the dependencies:**

```sh
uv sync
```

## Running Tests

To run the tests, use `pytest`:

```sh
uv run pytest
```

## Building Documentation

To build the documentation, follow these steps:

**Install MkDocs and the Material theme:**

```sh
uv sync
```

**Build the documentation:**

```sh
uv run mkdocs build
```

**Local deployment**

Run the following and browse the documentation locally at:
[http://localhost:8000](http://localhost:8000)

```sh
uv run mkdocs serve
```
