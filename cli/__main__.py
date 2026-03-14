"""Entry point for the OpenGym CLI."""

import click

from cli.compare_cmd import compare_reports
from cli.encrypt_cmd import encrypt_tests
from cli.fetch import fetch
from cli.keygen_cmd import init_key
from cli.list_cmd import list_challenges
from cli.run import run
from cli.score import score


@click.group()
@click.version_option(package_name="opengym-ai")
def main():
    """OpenGym — Test if your AI agent actually works."""
    pass


main.add_command(encrypt_tests, name="encrypt-tests")
main.add_command(init_key)
main.add_command(fetch)
main.add_command(list_challenges, name="list")
main.add_command(run)
main.add_command(score)
main.add_command(compare_reports)


if __name__ == "__main__":
    main()
