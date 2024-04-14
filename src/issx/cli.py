import asyncio
from typing import Annotated

import typer
from rich.console import Console
from rich.text import Text

from issx.clients import SupportedBackend
from issx.clients.gitlab import GitlabClient, GitlabInstanceClient
from issx.clients.redmine import RedmineClient, RedmineInstanceClient
from issx.instance_managers import GenericConfigParser, InstanceManager
from issx.services import CopyIssueService

app = typer.Typer(no_args_is_help=True)

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
) -> int:
    console.print(
        Text.assemble(
            f"Copying issue {issue_id} from project ",
            (source_project_name, "bold magenta"),
            " to project ",
            (target_project_name, "bold magenta"),
        )
    )
    config = GenericConfigParser()
    instance_manager = InstanceManager(config)
    try:
        source_client = instance_manager.get_project_client(source_project_name)
        target_client = instance_manager.get_project_client(target_project_name)
    except Exception as e:
        console.print_exception()
        console.print("Error when configuring client instance.\n", style="red")
        raise typer.Exit(1) from e
    new_issue = asyncio.run(
        CopyIssueService(source_client, target_client).copy(issue_id)
    )
    console.print(f"Success!\n{new_issue}", style="green")
    return 0


@app.command()
def auth_verify(instance_name: InstanceNameOption) -> None:
    config = GenericConfigParser()
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


if __name__ == "__main__":
    app()
