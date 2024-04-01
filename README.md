# Issx

[![PyPI](https://img.shields.io/pypi/v/issx?style=flat-square)](https://pypi.python.org/pypi/issx/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/issx?style=flat-square)](https://pypi.python.org/pypi/issx/)
[![PyPI - License](https://img.shields.io/pypi/l/issx?style=flat-square)](https://pypi.python.org/pypi/issx/)
[![Coookiecutter - Nekeal](https://img.shields.io/badge/cookiecutter-nekeal-00a86b?style=flat-square&logo=cookiecutter&logoColor=D4AFff&link=https://github.com/nekeal/cookiecutter-python-package)](https://github.com/nekeal/cookiecutter-python-package)

---

[Documentation](https://nekeal.github.io/issx) |
[Source Code](https://github.com/nekeal/issx) |
[PyPI](https://pypi.org/project/issx/)

---

Tool for synchronizing issues between different services (e.g. GitHub, Gitlab Jira, etc.)

## Disclaimer

Please note that `issx` is currently in the early stages of development. As such,
it may be subject to significant changes and improvements.
The links to PyPI and documentation provided above are placeholders and may not be operational yet.
Users are encouraged to consult the GitHub repository for the latest updates and information on this project.
We appreciate your interest and patience as we work to enhance `issx`.


## Installation

### Using pip
```sh
pip install issx
```

### Using pipx
```sh
pipx install issx
```

## Usage

The basic functionality of `issx` is provided through the `issx` command-line interface (CLI).

Currently, there is only one command available: `copy`.

It allows to copy issues from one place to another.
As for now, it supports copying issues between **projects in the same backend** (Gitlab).

```shell
issx copy --source-project-id=<id> --target-project-id=<id> <issue-id>
```

where `source-project-id` and `target-project-id` are the IDs of the projects in the same backend and
`issue-id` is the ID of the issue to be copied.

### Authentication

#### Gitlab
For the Gitlab backend we use the `python-gitlab` package with file-based [configuration](https://python-gitlab.readthedocs.io/en/stable/cli-usage.html#configuration-file-format).
`issx` will use the configured default section from the configuration file located in `~/.python-gitlab.cfg`
(`private_instance` in the example below).

```
[global]
default = private_instance

[private_instance]
url = https://private-gitlab.com/
private_token = <your_private_token>
```

To validate the authentication, you can use command:
```shell
issx auth-verify
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.11+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest
```

### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github project page
 ](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/nekeal/issx/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/nekeal/issx/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/nekeal/issx/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `ruff`), linters (e.g. `mypy`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

This project was generated using the [nekeal-python-package-cookiecutter](https://github.com/nekeal/cookiecutter-python-package) template.
