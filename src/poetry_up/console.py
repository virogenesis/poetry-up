"""Command-line interface."""
import os
from operator import attrgetter
from typing import Tuple

import click

from . import __version__, update
from .const import DescriptionHandlerChoices


@click.command()  # noqa: C901
@click.option(
    "--latest/--no-latest",
    help="Upgrade the version constraint if required.",
    default=True,
    show_default=True,
)
@click.option(
    "--install/--no-install",
    help="Install dependency into virtual environment.",
    default=True,
    show_default=True,
)
@click.option(
    "--commit/--no-commit",
    help="Commit the changes to Git.",
    default=True,
    show_default=True,
)
@click.option("--push/--no-push", help="Push the changes to remote.")
@click.option("--merge-request/--no-merge-request", help="Open a merge request.")
@click.option("--pull-request/--no-pull-request", help="Open a pull request.")
@click.option(
    "--package-description-handler",
    type=click.Choice(
        tuple(map(attrgetter("value"), DescriptionHandlerChoices)), case_sensitive=False
    ),
    default=DescriptionHandlerChoices.TITLE.value,
    help="Handler for Merge/Pull requests description",
)
@click.option(
    "-u",
    "--upstream",
    metavar="BRANCH",
    help="Specify the upstream branch",
    default="master",
    show_default=True,
)
@click.option(
    "-r",
    "--remote",
    metavar="REMOTE",
    help="Specify the remote to push to",
    default="origin",
    show_default=True,
)
@click.option(
    "-C",
    "--cwd",
    metavar="DIR",
    type=click.Path(exists=True, file_okay=False),
    help="Change to directory DIR before performing any actions",
)
@click.option("--dry-run", "-n", is_flag=True, help="Just show what would be done.")
@click.argument("packages", nargs=-1)
@click.version_option(version=__version__)
def main(  # noqa: C901
    latest: bool,
    install: bool,
    commit: bool,
    push: bool,
    merge_request: bool,
    pull_request: bool,
    package_description_handler,
    upstream: str,
    remote: str,
    dry_run: bool,
    packages: Tuple[str, ...],
    cwd: str = None,
) -> None:
    """Upgrade dependencies using Poetry."""
    if cwd is not None:
        os.chdir(cwd)

    options = update.Options(
        latest,
        install,
        commit,
        push,
        merge_request,
        pull_request,
        package_description_handler,
        upstream,
        remote,
        dry_run,
        packages,
    )
    updater = update.Updater(options)
    updater.run()
