"""
Printing module to print logs and results
"""

from .target import Target
from .step import Step, STATUS_ERR, STATUS_OK, STATUS_SKIPPED, STATUS_UNKNOWN
import fruit.modules.console as console
import click
import tabulate
from typing import List
import time

WIDTH = (click.get_terminal_size()[0] - 10)

# Define ICONS
ICON_TARGET = "🌳🍎"
ICON_STEP   = "🥝"
ICON_OK     = "✅"
ICON_SKIP   = "⏩"
ICON_ERR    = "❌"
ICON_UNKNOWN = "❔"

def print_target_head(target: Target) -> None:
    """
    Print the target header when a target make starts
    
    Parameters
    ----------
    target : Target
        Target object
    """
    console.echo(f"{ICON_TARGET} Making '{target.name}' ...")
    console.echo("="*WIDTH)

def print_target_foot(target: Target) -> None:
    """
    Print the footer line when a target execution finished.
    
    Parameters
    ----------
    target : Target
        Target object
    """
    console.echo("="*WIDTH)

def print_step_head(step: Step, number: int) -> None:
    """
    Print the header line of a step, when the step is activated.
    
    Parameters
    ----------
    step : Step
        Step object
    """
    console.echo()
    console.echo(f"{ICON_STEP} Step {number} : {step.name}")
    console.echo()

def print_step_foot(step: Step, number: int) -> None:
    pass

def print_summary(last_target:Target, steps:List[Step]) -> None:
    """
    Print the summarized results as a table to the console. All run steps & substeps and targets
    will be summarized.
    
    Parameters
    ----------
    last_target : Target
        Target that the summary belonds to

    steps : List[Step]
        List of executed steps
    """
    table = []
    for each_step in steps:
        # Determine the status icon
        if each_step.status == STATUS_OK:
            icon = ICON_OK
            status = "OK"
        elif each_step.status == STATUS_SKIPPED:
            icon = ICON_SKIP
            status = "Skipped"
        elif  each_step.status == STATUS_ERR:
            icon = ICON_ERR
            status = "Failed"
        else:
            icon = ICON_UNKNOWN
            status = "Unknown"
        
        name = each_step.name
        xtime = "%.3f" % each_step.time
        table.append((icon, status, xtime, name))
    
    console.echo()
    console.echo(f"Summary of target '{last_target.name}':")
    console.echo()
    console.echo(tabulate.tabulate(table, headers=('', 'Status', 'Time', 'Name')))

def print_summary_abort(last_target:Target, steps:List[Step]) -> None:
    """
    Print the summarized results of an aborted target as a table to the console. 
    All run steps & substeps and targets will be summarized.

    Parameters
    ----------

    last_target : Target
        Target that the summary belonds to

    steps : List[Step]
        List of executed steps
    """
    table = []
    for each_step in steps:
        # Determine the status icon
        if each_step.status == STATUS_OK:
            icon = ICON_OK
            status = "OK"
        elif each_step.status == STATUS_SKIPPED:
            icon = ICON_SKIP
            status = "Skipped"
        elif  each_step.status == STATUS_ERR:
            icon = ICON_ERR
            status = "Failed"
        else:
            icon = ICON_UNKNOWN
            status = "Unknown"
        
        name = each_step.name
        xtime = "%.3f" % each_step.time
        table.append((icon, status, xtime, name))
    
    table.append((ICON_ERR, 'Aborted', 'N/A', last_target.name))

    console.echo()
    console.echo(f"Summary of target '{last_target.name}':")
    console.echo()
    console.echo(tabulate.tabulate(table, headers=('', 'Status', 'Time', 'Name')))