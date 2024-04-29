# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.1] - 2024-04-29
### Fixed
- Fix wizard for generating configs for projects and instances

## [0.5.0] - 2024-04-29
### Added
- Add tests for instance manager
- Add possibility to specify a config class per instance client
- Add wizard for generating configs for projects and instances

## [0.4.0] - 2024-04-21
### Added
- Tests for client interfaces of different backends
- Tests for generic config parser
- Import linter for checking a compliance with the layered architecture

### Changed
- Improve gh actions configuration
- Make use of `attrs` library for parsing config files

## [0.3.2] - 2024-04-18
### Added
- Improve documentation configuration
- CLI [reference](https://nekeal.github.io/cli_usage/) to the documentation

## [0.3.1] - 2024-04-17
### Added
- Help text for the `--assign-to-me` flag

## [0.3.0] - 2024-04-17
### Added
- Add possibility to assign issues to a current user when copying

## [0.2.0] - 2024-04-15
### Added
- Add method for finding issues by a title to the client interface
- Possibility to allow for duplicate issues when copying (based on title)

## [0.1.0] - 2024-04-14
### Added
- Add a first bunch of tests 🔨
- Add possibility of specifying issue's title and description format when copying

### Changed
- Move exception message directly to the exception class

### Fixed
- Gitlab client uses global issue id instead of internal one

## [0.0.4] - 2024-04-14
### Added
- Add config parser from toml files
- Add plugin based instance manager
- Make use of instance manager in auth-verify command

### Changed
- Adjust permissions for gh actions
- Implementation of Redmine issue client interface
- Extend instance manager with possibility to initialize issue client
- Adapt copy command to work with any configured project

## [0.0.2] - 2024-04-01
### Added
- Implementation of Gitlab issue client interface
- Service for copying issues between projects
- CLI for copying issues and verifying auth configuration with Gitlab ([b7eed84](https://github.com/nekeal/issx/commit/b7eed844239f0c251c9501a0c455ab457c4ed910))

[Unreleased]: https://github.com/nekeal/issx/compare/0.5.1...master
[0.5.1]: https://github.com/nekeal/issx/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/nekeal/issx/compare/0.4.0...0.5.0
[0.4.0]: https://github.com/nekeal/issx/compare/0.3.2...0.4.0
[0.3.2]: https://github.com/nekeal/issx/compare/0.3.1...0.3.2
[0.3.1]: https://github.com/nekeal/issx/compare/0.3.0...0.3.1
[0.3.0]: https://github.com/nekeal/issx/compare/0.2.0...0.3.0
[0.2.0]: https://github.com/nekeal/issx/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/nekeal/issx/compare/0.0.4...0.1.0
[0.0.4]: https://github.com/nekeal/issx/compare/0.0.2...0.0.4
[0.0.2]: https://github.com/nekeal/issx/tree/0.0.2

