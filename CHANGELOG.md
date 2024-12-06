# Changelog

## Version 0.1.3

### Added

- added the `online-backends` flag to the `backends` member of the `MQPProvider` to fetch only the online devices
- `timestamps` (`submitted`, `scheduled` and `completed`) are added to the results. It can be accessed as `result.timestamps["submitted"]`.
