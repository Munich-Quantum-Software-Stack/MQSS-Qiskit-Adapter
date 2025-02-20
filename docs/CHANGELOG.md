# Changelog

## Version 0.1.6

- Added the option to queue a job when backend is offline
- Added some more instructions to target as new backends are integrated

## Version 0.1.5

- Added `qasm3` flag to the backend to send circuit as QASM3 when set
- Added a property `num_pending_jobs` to the backend to get the num pending jobs

## Version 0.1.4

- Added the `online-backends` flag to the `backends` member of the `MQPProvider` to fetch only the online devices
- `timestamps` (`submitted`, `scheduled` and `completed`) are added to the results. It can be accessed as `result.timestamps["submitted"]`.
