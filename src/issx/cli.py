import asyncio
from typing import Annotated

import typer
from rich.console import Console
from rich.text import Text

from issx.cli_utils import RichConfigReader
from issx.clients.gitlab import GitlabClient, GitlabInstanceClient
from issx.clients.redmine import RedmineClient, RedmineInstanceClient
from issx.domain import SupportedBackend
from issx.domain.config import InstanceConfig, ProjectFlatConfig
from issx.instance_managers.config_parser import GenericConfigParser
from issx.instance_managers.managers import InstanceManager
from issx.services import CopyIssueService

app = typer.Typer(no_args_is_help=True)
config_app = typer.Typer(name="config", no_args_is_help=True)
app.add_typer(config_app, name="config")

BackendOption = Annotated[SupportedBackend, typer.Option()]
InstanceNameOption = Annotated[str, typer.Option("--instance")]
ProjectOption = Annotated[
    str, typer.Option("--project", help="Project name configured in the config file")
]
console = Console()

InstanceManager.register_backend(
    SupportedBackend.gitlab, GitlabInstanceClient, GitlabClient
)
InstanceManager.register_backend(
    SupportedBackend.redmine, RedmineInstanceClient, RedmineClient
)


@app.command()
def copy(
    source_project_name: Annotated[
        str,
        typer.Option(
            "--source", help="Source project name configured in the config file"
        ),
    ],
    target_project_name: Annotated[
        str,
        typer.Option(
            "--target", help="Target project name configured in the config file"
        ),
    ],
    issue_id: int,
    title_format: Annotated[
        str,
        typer.Option(
            "--title-format",
            "-T",
            help="Template of a new issue title. Can contain placeholders of the"
            " issue attributes: {id}, {title}, {description}, {web_url}, {reference}",
        ),
    ] = "{title}",
    description_format: Annotated[
        str,
        typer.Option(
            "--description-format",
            "-D",
            help="Template of a new issue description. Can contain placeholders of the"
            " issue attributes: {id}, {title}, {description}, {web_url}, {reference}",
        ),
    ] = "{description}",
    allow_duplicates: Annotated[
        bool,
        typer.Option(
            "--allow-duplicates",
            "-A",
            help="Allow for duplicate issues. If set, the command will return the first"
            " issue found with the same title. If no issues are found,"
            " a new issue will be created.",
        ),
    ] = False,
    assign_to_me: Annotated[
        bool,
        typer.Option(
            "--assign-to-me",
            "-M",
            help="Whether to assign a newly created issue to the current user",
        ),
    ] = False,
) -> int:
    """Copy an issue from one project to another."""

    console.print(
        Text.assemble(
            f"Copying issue {issue_id} from project ",
            (source_project_name, "bold magenta"),
            " to project ",
            (target_project_name, "bold magenta"),
        )
    )
    config = GenericConfigParser.from_file()
    instance_manager = InstanceManager(config)
    try:
        source_client = instance_manager.get_project_client(source_project_name)
        target_client = instance_manager.get_project_client(target_project_name)
    except Exception as e:
        console.print_exception()
        console.print("Error when configuring client instance.\n", style="red")
        raise typer.Exit(1) from e
    new_issue = asyncio.run(
        CopyIssueService(source_client, target_client).copy(
            issue_id,
            title_format,
            description_format,
            allow_duplicates=allow_duplicates,
            assign_to_me=assign_to_me,
        )
    )
    console.print(f"Success!\n{new_issue}", style="green")
    return 0


@app.command()
def auth_verify(instance_name: InstanceNameOption) -> None:
    """Verify the authentication to the instance."""
    config = GenericConfigParser.from_file()
    instance_manager = InstanceManager(config)
    try:
        instance = instance_manager.get_instance_client(instance_name)
    except Exception as e:
        console.print_exception()
        console.print("Error when configuring client instance.\n", style="red")
        raise typer.Exit(1) from e
    try:
        username = asyncio.run(instance.auth())
        if not username:
            raise Exception("Authentication failed")
    except Exception as e:
        console.print_exception()
        console.print(
            f"Error when authenticating to {instance.get_instance_url()}",
            style="red",
        )
        raise typer.Exit(1) from e
    else:
        console.print(
            "Authentication successful",
            f"Instance: {instance.get_instance_url()}",
            f"User: {username}",
            sep="\n",
            style="green bold italic",
        )


@config_app.command()
def generate_instance(
    instance_name: Annotated[
        str,
        typer.Option(
            "--instance",
            help="Name of then instance to generate new_config for."
            " Only alphanumeric and -_ allowed",
        ),
    ],
) -> None:
    """Generate instance's new_config string"""

    new_config = RichConfigReader().read(InstanceConfig)
    console.print()
    console.print(Text(new_config.as_toml(f"instances.{instance_name}")))

    console.print(
        "\nSuccess!\nCopy the above config to your config file", style="green"
    )


@config_app.command()
def generate_project(
    project_name: Annotated[
        str,
        typer.Option(
            "--project",
            help="Name of then project to generate new_config for."
            " Only alphanumeric and -_ allowed",
        ),
    ],
) -> None:
    """Generate project's new_config string. Instance must be already configured."""

    new_config = RichConfigReader().read(ProjectFlatConfig)

    console.print()
    console.print(Text(new_config.as_toml(f"projects.{project_name}")))
    config = GenericConfigParser.from_file()

    try:
        config.get_instance_config(new_config.instance)
    except KeyError:
        console.print(
            f"\nWarning: instance [bold]{new_config.instance}[/bold] not found"
            f" in the config file. If you want to generate a missing config run"
            f" [bold]issx config generate-instance --instance {new_config.instance}"
            f"[/bold] command",
            style="yellow",
        )

    console.print(
        "\nSuccess!\nCopy the above config to your config file", style="green"
    )


if __name__ == "__main__":
    app()
