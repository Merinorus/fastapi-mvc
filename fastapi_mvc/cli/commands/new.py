"""FastAPI MVC CLI new command implementation."""
import sys
import subprocess
import os
from datetime import datetime

import click
from cookiecutter.exceptions import OutputDirExistsException
from cookiecutter.main import cookiecutter


@click.command()
@click.argument(
    "APP_NAME",
    nargs=1,
    type=click.STRING,
    required=True,
)
@click.option(
    "-R",
    "--skip-redis",
    help="Skip Redis utility files.",
    is_flag=True,
)
@click.option(
    "-A",
    "--skip-aiohttp",
    help="Skip aiohttp utility files.",
    is_flag=True,
)
@click.option(
    "-V",
    "--skip-vagrantfile",
    help="Skip Vagrantfile.",
    is_flag=True,
)
@click.option(
    "-H",
    "--skip-helm",
    help="Skip Helm chart files.",
    is_flag=True,
)
@click.option(
    "-G",
    "--skip-actions",
    help="Skip GitHub actions files.",
    is_flag=True,
)
@click.option(
    "--license",
    help="Choose license.",
    type=click.Choice([
        "MIT",
        "BSD2",
        "BSD3",
        "ISC",
        "Apache"
    ]),
)
@click.option(
    "--repo-url",
    help="Repository url.",
    type=click.STRING,
)
def new(app_name, **options):
    """Create a new FastAPI application.

    The 'fastapi-mvc new' command creates a new FastAPI application with a
    default directory structure and configuration at the current path.
    \f

    Args:
        app_name(str): CLI command argument - new application name.
        options(dict): CLI command options.

    """
    template_dir = os.path.abspath(
        os.path.join(
            os.path.abspath(__file__),
            "../../../template",
        )
    )

    try:
        user = subprocess.check_output(
            ["git", "config", "--get", "user.name"]
        ).decode("utf-8").strip()
        email = subprocess.check_output(
            ["git", "config", "--get", "user.email"]
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError:
        user = None
        email = None

    context = {
        "project_name": app_name,
        "redis": "no" if options["skip_redis"] else "yes",
        "aiohttp": "no" if options["skip_aiohttp"] else "yes",
        "github_actions": "no" if options["skip_actions"] else "yes",
        "vagrantfile": "no" if options["skip_vagrantfile"] else "yes",
        "helm": "no" if options["skip_helm"] else "yes",
        "author": user,
        "email": email,
        "repo_url": options["repo_url"],
        "year": datetime.today().year,
    }

    try:
        cookiecutter(
            template_dir,
            extra_context=context,
            no_input=True,
        )
    except OutputDirExistsException as ex:
        click.echo(ex)
        sys.exit(1)

    click.echo(
        "FastAPI {app_name} project created successfully".format(
            app_name=app_name
        )
    )
