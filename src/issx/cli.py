import asyncio
from typing import Annotated

import typer
from gitlab import Gitlab
from rich.console import Console

from issx.clients import SupportedBackend
from issx.clients.gitlab import GitlabClient, GitlabInstanceClient
from issx.clients.redmine import RedmineClient, RedmineInstanceClient
from issx.instance_managers import GenericConfigParser, InstanceManager
from issx.services import CopyIssueService

app = typer.Typer(no_args_is_help=True)

BackendOption = Annotated[SupportedBackend, typer.Option()]
InstanceNameOption = Annotated[str, typer.Option("--instance")]

console = Console()

InstanceManager.register_backend(
    SupportedBackend.gitlab, GitlabInstanceClient, GitlabClient
)
InstanceManager.register_backend(
    SupportedBackend.redmine, RedmineInstanceClient, RedmineClient
)


@app.command()
def copy(
    source_project_id: Annotated[int, typer.Option()],
    target_project_id: Annotated[int, typer.Option()],
    issue_id: int,
    source_backend_name: BackendOption = SupportedBackend.gitlab,
    target_backend_name: BackendOption = SupportedBackend.gitlab,
) -> int:
    typer.echo(
        f"Copying issue {issue_id} from project {source_project_id}"
        f" to project {target_project_id}"
    )
    gl = Gitlab.from_config()
    source_client = GitlabClient(gl, source_project_id)
    target_client = GitlabClient(gl, target_project_id)
    new_issue = asyncio.run(
        CopyIssueService(source_client, target_client).copy(issue_id)
    )
    typer.echo(f"New issue created: {new_issue}")
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
