
from fruit.modules.garden import Garden
from fruit.modules.target import Target
from fruit.modules.step   import Step
from fruit.modules.provider import Provider

from typing import Callable

def target(name:str=None, help:str=None):

    def decorator(func:Callable[[], None]) -> Callable[[], None]:
        """Decorate the target function and register the target in the collection."""

        def warpper(func:Callable[[], None]) -> None:
            """Wrapped target function."""
            pass

        return warpper

    return decorator


def step(*args, **kwargs):

    def decorator(func):
        def wrapper(*args, **kwargs):
            garden = Garden()
            next_nr = garden.active_target().count_steps() + 1

            returnval = None #  In case of a skip call

            with Step(func.__name__, func.__doc__, next_nr) as stp:
                # Get the currently active step (for nested steps)
                stp_fallback = Garden().active_target().get_active_step()
                # Update the currently active step to the new step
                Garden().active_target().add_step(stp)

                returnval = func(*args, **kwargs)

                # Return back to the caller of the nested step
                Garden().active_target().fallback_step(stp_fallback)

            # Return the original result of the function call
            return returnval
        return wrapper
    return decorator

def provider(name:str=None, help:str=None) -> Callable:
    """
    Decorator function to create fruit information provider.

    Information provides are also shown with the command `fruit collect` 
    and can be executed via `fruit get <name>`.
    
    Parameters
    ----------
    `name` : str, optional
        Name of the provider, by default None. When left empty, the function name
        will be used.
    `help` : str, optional
        Help text of the provider, by default None. When left empty, then function docstring
        will be used.
    
    Returns
    -------
    Callable
        Decorated information provider function.
    """


    def decorator(func):

        # Check the name and help overrides
        if name is not None:
            p_name = name
        else:
            p_name = func.__name__
        
        if help is not None:
            p_help = help
        else:
            p_help = func.__doc__
        
        obj = Provider(name=p_name, help=p_help, func=func)
        Garden().add_provider(obj)

        def wrapper(func) -> str:
            # Call the class call implementation
            return obj() 
        
        return wrapper
    return decorator