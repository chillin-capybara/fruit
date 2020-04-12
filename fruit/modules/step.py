"""
Module for implementing the inner steps of a target
"""
import fruit.modules.console as console
from fruit.globals import FMT_STEPHEADER, FMT_SKIPMESSAGE, FMT_FAILMESSAGE
import time


STATUS_OK = 0
STATUS_ERR = 1
STATUS_SKIPPED = -1

class SkipStepSignal(Exception):
    """Signal to indicate, whenever a step shall be skipped"""
    pass

class AbortStepSignal(Exception):
    """Signal to indicate, when a target make has to be stopped
    because of a step error."""
    pass

class FailStepSignal(Exception):
    """Signal to indicate that a step is failed but the make process
    may continue."""
    pass


class Step(object):
    name: str = ""  # Name of the step
    desc: str = ""  # Description of the step
    number: int = 0
    status: int = 1  # Error by default

    __timer0 : float = .0  # Start execution time of the step
    __elapsed_time : float = .0  # Measured elapsed time spent in the current step

    def __init__(self, name: str, desc: str, number: int):
        if type(name) is not str:
            raise TypeError("The step name must be a string!")
        if type(desc) is not str:
            raise TypeError("The step description bust be a string!")

        if type(number) is not int:
            raise TypeError("The step number must be an integer!")

        self.name = name
        self.desc = desc
        self.number = number

    def __tic(self):
        """
        Start measuring the execution time and store it in `__timer0`.
        """
        self.__timer0 = time.clock()

    def __toc(self) -> float:
        """
        Stop measuring the execution time and set the elapsed time.
        """
        # Set the active step
        self.__elapsed_time = time.clock() - self.__timer0

    def __enter__(self):
        """
        Enter the context of the current step.
        """
        console.echo()
        # Print the step header
        self.print_stephead()

        # Start measuring the execution time
        self.__tic()

        # Return the object, to use it directly as a context manager
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Leave the context of the current step. Stop the time measurements and perform post
        step actions.
        """
        self.__toc()

        if exc_type is SkipStepSignal:
            self.status = STATUS_SKIPPED
            console.warning(FMT_SKIPMESSAGE.format(reason = exc_value if type(exc_value) is str else ""))
        elif exc_type is FailStepSignal:
            # The step failed, but continue the execution
            self.status = STATUS_ERR

            if str(exc_value) is not None: # TODO: Reason display...
                console.error(FMT_FAILMESSAGE.format(reason = str(exc_value)))
            else:
                console.error((FMT_FAILMESSAGE.format(reason="")))
        
        elif exc_type is not None:
            self.status = STATUS_ERR

            # Raise an error signal to stop the complete execution
            if type(exc_value) is str:
                raise AbortStepSignal(exc_value)
            else:
                raise AbortStepSignal("Random value")
        else:
            self.status = STATUS_OK

        # Stop exception propagating
        return True

    def setstatus(self, value: int):
        """
        Set the status of the step to True (successful).
        """
        self.status = value

    def get_elapsed_time(self) -> float:
        """
        Get the execution time in seconds of the step, when it was already executed.

        Returns
        -------
        float
            Execution time

        Note
        ----
        When the step was not executed yet, the value will default back to 0.0
        """
        return self.__elapsed_time

    def getstatus(self) -> int:
        return self.status

    def print_stephead(self):
        """
        Print a formatted step header to the console to separate steps from each other.
        """
        console.echo(FMT_STEPHEADER.format(number=self.number, name=self.name))
