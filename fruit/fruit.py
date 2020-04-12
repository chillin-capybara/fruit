"""
Tratatata...
"""

import click
import sys
from tabulate import tabulate
from fruit.modules.fruitloader import load
from fruit.modules.garden import Garden
import fruit.modules.console as console


@click.group()
def cli():
    pass


@cli.command()
@click.argument('path', default='.')
def collect(path:str):
    """
    List the fruit targets in the given path.
    \b

    PATH (default: .) - Path of the directory or .py file to scan.
    """
    try:
        # Load the config file
        load(path)

        # List the targets
        tbl = []

        for trg in Garden().get_targets():
            tbl.append((trg.name, trg.desc))
        
        console.echo(tabulate(tbl, headers=['Target', 'Description']), )
        console.echo()
        console.echo("List of providers: ")

        tbl.clear()
        for prov in Garden().get_providers():
            tbl.append((prov.name, prov.help))
        
        if len(tbl) > 0:
            console.echo()
            console.echo(tabulate(tbl, headers=['Provider', 'Description']), )
        else:
            console.echo("\tNo providers found!")


    except Exception as err:
        console.error(str(err))


@cli.command()
@click.argument('target', required=True, nargs=-1)
def make(target: str):
    """
    Make a fruit target from the parsed fruitconfig.py file.
    """
    load('.')
    # Pass all the targets to the make function
    Garden().make_multiple(*target)

@cli.command()
@click.argument('name', required=True)
def get(name: str):
    """Run an information provider to obtain data from the current project.
    
    \b
    Example::
        fruit get version
    
    """
    try:
        load('.')
        result = Garden().run_provider(name=name)

        console.echo(result)
    except Exception as exc:
        console.error(str(exc))


# Main application code of the project
def main():
    # Call the click handler
    cli()