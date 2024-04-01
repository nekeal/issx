import asyncio
from typing import Annotated

import typer
from gitlab import Gitlab
from rich.console import Console

from issx.clients import SupportedBackend
from issx.clients.gitlab import GitlabClient
from issx.services import CopyIssueService

app = typer.Typer(no_args_is_help=True)

BackendOption = Annotated[SupportedBackend, typer.Option()]


console = Console()


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
def auth_verify(backend_name: BackendOption = SupportedBackend.gitlab) -> None:
    try:
        gl = Gitlab.from_config()
    except Exception as e:
        console.print(f"Error when reading config file.\n" f"Details: {e}", style="red")
        raise typer.Exit(1) from e
    try:
        gl.auth()
    except Exception as e:
        console.print(
            f"Error when authenticating to {gl.url}.\nDetails: {e}", style="red"
        )
        raise typer.Exit(1) from e
    else:
        console.print(
            "Authentication successful",
            f"Instance: {gl.url}",
            f"User: {gl.user and gl.user.username}",
            sep="\n",
            style="green bold italic",
        )


if __name__ == "__main__":
    app()
