"""
Fruit provider module to declare information provider functions.
"""
from typing import Callable

class Provider(object):
    __name: str = ""
    __help: str = ""
    __func: Callable[[any], str] = None

    def __init__(self, name: str, help: str, func: Callable[[any], str]):
        """
        Create a new information provider object
        
        Parameters
        ----------
        `name` : str
            Name of the information
        `help` : str
            Help text (description) of the information
        `func` : Callable[[any], str]:
            Information provider function, that returns the information as a string.
        """
        
        if type(name) is str:
            self.__name = name
        else:
            raise TypeError("The provider name must be a string!")
        
        if type(help) is str:
            self.__help = help
        else:
            raise TypeError("The provider help must be a string!")
        
        if callable(func):
            self.__func = func
        else:
            raise TypeError("The provider function must be a callable!")
