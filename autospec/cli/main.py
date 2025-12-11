"""AutoSpec CLI entry point"""
import sys
import click
from pathlib import Path
from ..pipeline.autospec_runner import AutoSpecRunner
from ..config import FRAMA_C_TIMEOUT


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AutoSpec - Automated Specification Generation for C Programs"""
    pass


@cli.command()
@click.argument('c_file', type=click.Path(exists=True, path_type=Path))
@click.option('--timeout', default=FRAMA_C_TIMEOUT, help='Verification timeout in seconds')
@click.option('--verbose', is_flag=True, help='Enable verbose output')
def verify(c_file: Path, timeout: int, verbose: bool):
    """Verify a C file with Frama-C WP"""
    click.echo(f"Verifying {c_file}...")
    
    runner = AutoSpecRunner(timeout=timeout)
    verdict = runner.run(c_file)
    
    if verbose and verdict.details:
        click.echo("\n--- Detailed Output ---")
        click.echo(verdict.details)
        click.echo("--- End Output ---\n")
    
    click.echo(f"\n{verdict}")
    
    # Exit with appropriate code
    if verdict.is_valid():
        click.echo(click.style("✓ Verification successful!", fg="green"))
        sys.exit(0)
    else:
        click.echo(click.style("✗ Verification failed or incomplete", fg="red"))
        sys.exit(1)


if __name__ == '__main__':
    cli()

