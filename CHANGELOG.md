# Changelog

All notable changes to the Solar Forecast Arbiter Dashboard will be documented
in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),.

## [Unreleased]

### Added

- Report form now includes inputs to select which metrics and categories to
  include in a Report.

- Ability to compare Forecasts to Aggregates in reports.

- Report signatures and HTML downloads for reports. Available at
  `/reports/<report_id>/downloads/html`. Note that there are no currently
  functioning links to this endpoint.

- CHANGELOG.md (this file) for tracking and communicating changes.


### Fixed

- Permissions acting on aggregates are now accessible via a Role's permission
  listing.


## [1.0beta2] - 2019-11-18

### Added
- Aggregates can be created through the dashboard. See  [Aggregate Documentation](https://solarforecastarbiter.org/documentation/dashboard/working-with-data/#create-new-aggregate) 

## [1.0beta] - 2019-10-4

### Added
- User management controls for organization admin. See [Dashboard Administration Documentation](https://solarforecastarbiter.org/documentation/dashboard/administration/)

- Start/End selection for plots on Forecast, Probabilistic Forecasts and
  Observation Pages. 

## [1.0alpha] - 2019-06-28

Initial Solar Forecast Arbiter Dashboard release. Includes site, forecast,
probabilistic forecast and report functionality.
