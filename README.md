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

## Basic usage

The basic functionality of `issx` is provided through the `issx` command-line interface (CLI).
For a full list of available commands and options, please refer to the [CLI reference](https://nekeal.github.io/issx/cli_reference).

!!! warning
    The `issx` CLI requires a configuration file to be present in the working directory (`issx.toml`) or in `~/.config/issx.toml`.
    Refer to the [Configuration file](#configuration-file) section for more information.

### Initializing the configuration file

There is a set of dedicated commands to initialize the configuration file and add instances and projects to it.

#### Generate a new instance's configuration

```shell
> issx config generate-instance --instance gitlab-cloud

Enter backend [gitlab/redmine]: gitlab
Enter url: https://gitlab.com
Enter token: token

[instances.gitlab-cloud]
backend = 'gitlab'
url = 'https://gitlab.com'
token = 'token'
```
The output should be then copied to the [Configuration file](#configuration-file).

#### Generate a new project's configuration

```shell
> issx config generate-project --project my-personal-project
Enter instance: gitlab-cloud   # The name of the instance that is already configured
Enter project: 11111111        # Identifier of the project characteristic for the instance's backend

[projects.my-personal-project]
instance = 'gitlab-cloud'
project = '11111111'
````

The output should be then copied to the [Configuration file](#configuration-file).

### Copying issues
It allows to copy issues from one [configured](#configuration-file) project to another.

```shell title="Copy an issue"
issx copy --source=<project_name> --target=<project_name> <issue-id>
```

where `source` and `target` are the names of the projects configured in the configuration file.

Optionally you can customize the issue title and description by providing `--title-format/-T` and `--description-format/-D` flags.
The format should be a string with placeholders for the issue fields (e.g. `{title}`, `{description}`, `{id}` etc.).

Assigning the issue to the current user is also possible by providing `--assign-to-me/-M` flag.

```shell title="Copy an issue with custom title and description assigning it to the current user"
issx copy --source=<project_name> --target=<project_name>  -T "[copied] {title}" -D "Description: {description}" -M <issue-id>
```

### Verifying authentication
To validate the authentication with a newly configured instance, you can use command `issx auth-verify`:
```shell
issx auth-verify --instance=<instance_name>
```

## Configuration file

The configuration file can be either in the working directory (`issx.toml`) or in `~/.config/issx.toml`.

It should have the following structure:

```toml
[instances.INSTANCE_NAME]
    backend = "gitlab" / "redmine"
    url = "<absolute url to the instance>"
    token = "<API token used for authentication>"

[projects.PROJECT_NAME]
    instance = "INSTANCE_NAME"
    project = "<project_id>"
```

`Instances` section is used to configure the instances of the services (e.g. Gitlab, Redmine)
that `issx` will interact with.

`Projects` section is used to configure the projects that `issx` will work with. Each project should be associated with
an instance.
`project` field should contain the project id available in the chosen instance (usually it is a number).

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

The documentation is automatically generated from the content of the [docs directory](https://github.com/nekeal/issx/tree/master/docs) and from the docstrings
 of the public signatures of the source code. The documentation is updated and published as a [Github Pages page](https://pages.github.com/) automatically as part each release.

### Releasing

Trigger the [Draft release workflow](https://github.com/nekeal/issx/actions/workflows/draft_release.yml)
(press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the
[GitHub releases](https://github.com/nekeal/issx/releases) and publish it. When
 a release is published, it'll trigger [release](https://github.com/nekeal/issx/blob/master/.github/workflows/release.yml) workflow which creates PyPI
 release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatting (`ruff format`), linters (e.g. `ruff` and `mypy`), and other quality
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
