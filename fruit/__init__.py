"""
Python tool for creating make targets programmed via python.

Shared fruit configurations
---------------------------
To import a shared configuration, from (usually) a parent directory, first
add it to the system path.

Example::

    import sys
    sys.path.append('../../.fruit')

Then import the modules, you want to use via the `import ...` or the `from ... import ...`
syntax.

Example::

    import my_parent_module
    from my_parent_module2 import run_lint
"""


# Import console logging / printing functions
from fruit.modules.console import echo, error, warning

# Export decorators
from fruit.api.decorators import target, step, provider

# Export exceptions
from fruit.api.api import abort, finish, skip, fail

# Export the shell module
from fruit.api.shell import shell

from fruit.modules.config import config
