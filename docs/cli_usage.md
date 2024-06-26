# `issx`

**Usage**:

```console
$ issx [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `auth-verify`: Verify the authentication to the instance.
* `config`: Config commands
* `copy`: Copy an issue from one project to another.

## `issx auth-verify`

Verify the authentication to the instance.

**Usage**:

```console
$ issx auth-verify [OPTIONS]
```

**Options**:

* `--instance TEXT`: [required]
* `--help`: Show this message and exit.

## `issx config`

Config commands

**Usage**:

```console
$ issx config [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

**Commands**:

* `generate-instance`: Generate instance's new_config string
* `generate-project`: Generate project's new_config string.

### `issx config generate-instance`

Generate instance's new_config string

**Usage**:

```console
$ issx config generate-instance [OPTIONS]
```

**Options**:

* `--instance TEXT`: Name of then instance to generate new_config for. Only alphanumeric and -_ allowed  [required]
* `--help`: Show this message and exit.

### `issx config generate-project`

Generate project's new_config string. Instance must be already configured.

**Usage**:

```console
$ issx config generate-project [OPTIONS]
```

**Options**:

* `--project TEXT`: Name of then project to generate new_config for. Only alphanumeric and -_ allowed  [required]
* `--help`: Show this message and exit.

## `issx copy`

Copy an issue from one project to another.

**Usage**:

```console
$ issx copy [OPTIONS] ISSUE_ID
```

**Arguments**:

* `ISSUE_ID`: [required]

**Options**:

* `--source TEXT`: Source project name configured in the config file  [required]
* `--target TEXT`: Target project name configured in the config file  [required]
* `-T, --title-format TEXT`: Template of a new issue title. Can contain placeholders of the issue attributes: {id}, {title}, {description}, {web_url}, {reference}
* `-D, --description-format TEXT`: Template of a new issue description. Can contain placeholders of the issue attributes: {id}, {title}, {description}, {web_url}, {reference}  [default: {description}]
* `-A, --allow-duplicates`: Allow for duplicate issues. If set, the command will return the first issue found with the same title. If no issues are found, a new issue will be created.
* `-M, --assign-to-me`: Whether to assign a newly created issue to the current user
* `--help`: Show this message and exit.
