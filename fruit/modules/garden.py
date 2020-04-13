"""
Fruit garden is the master collection singleton of the application
"""
from .patterns import SingletonMeta
from .target   import Target, FruitError
from .step     import Step, SkipStepSignal, FailStepSignal, AbortStepSignal
from .provider import Provider
import fruit.modules.console as console

class Garden(metaclass=SingletonMeta):

    __targets : list = None
    __providers: list = None
    __active_target : Target = None

    # Overall returncode of the file. Each target call resets it
    __returncode: int = 1

    def __init__(self):

        # Initialize the collection the first time
        if self.__targets is None:
            self.__targets = []

        # Initialize the provider list
        if self.__providers is None:
            self.__providers = []

    def add_provider(self, provider: Provider) -> None:
        """
        Append an information provider to the global collection of providers.

        Parameters
        ----------
        `provider` : Provider
            Provider object to append

        Raises
        ------
        TypeError
            Raised, when the passed object is not a provider.
        """
        if isinstance(provider, Provider):
            self.__providers.append(provider)
        else:
            raise TypeError("The given object is not an information provider!")

    def run_provider(self, name: str) -> str:
        """
        Execute an information provider to objtain the requested values.

        Parameters
        ----------
        `name` : str
            Name of the provider to get.

        Returns
        -------
        str
            Provided value.
        """
        # TODO: Add argument propagation!!!
        flt = list(filter(lambda p: p.name == name, self.__providers))

        if len(flt) < 1:
            raise ValueError(f"The provider '{name}' is not found!")
        else:
            prov, = flt
            return prov()

    def get_providers(self):
        """
        Get the list of registered providers.

        Yields
        -------
        Provider
            All registered providers.
        """
        for each_provider in self.__providers:
            yield each_provider

    def add_target(self, target: Target):
        """
        Add a fruit target to the collection of targets

        Parameters
        ----------
        `target` : Target
            Target object
        """
        self.__targets.append(target)

    def make_target(self, target_name: str):
        """
        Execute the target with the selected name

        Parameters
        ----------
        `target_name` : str
            Target name to make
        """
        flt_target = list(filter(lambda trg: trg.name == target_name, self.__targets))

        if len(flt_target) < 1:
            raise ValueError("The target '{}' is not found!".format(target_name))
        else:
            cl, = flt_target
            cl()

    def make_multiple(self, *targets):
        """
        Make every listed target. When a target is not found the make process will be
        aborted.
        """
        print(targets)
        # Call the make command on each passed target
        for each_targetname in targets:
            self.make_target(each_targetname)

    def delegate_OnTargetActivate(self, sender: Target) -> None:
        """
        Event handler for handling target activation events.

        Parameters
        ----------
        `caller` : Target
            Target, that has been activated via a function call.
        """
        print(sender.name + " was activated!")
    
    def delegate_OnTargetDeactivate(self, sender: Target) -> None:
        """
        Event handler for target deactivation. Will be called, when a target finished executing.

        Parameters
        ----------
        `sender` : Target
            Target, that triggered the event.
        """
        print(f"Finished target: {sender.name}")
    
    def delegate_OnStepActivate(self, sender: Step) -> None:
        pass
    
    def delegate_OnStepSkipped(self, sender: Step, exception: SkipStepSignal) -> None:
        pass

    def delegate_OnStepFailed(self, sender: Step, exception: FailStepSignal) -> None:
        pass
    
    def delegate_OnStepAborted(self, sender: Step, exception: AbortStepSignal) -> None:
        pass
    
    def delegate_OnStepDeactivate(self, sender: Step) -> None:
        pass

    def get_targets(self):
        for each_target in self.__targets:
            yield each_target

    @property
    def returncode(self) -> int:
        """Return code of the application"""
        return self.__returncode
