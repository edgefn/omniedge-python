"""The official Python library for the OmniEdge API."""

__version__ = "0.1.0"

from .omniedge_core import (
    __openapi_doc_version__,
    __gen_version__,
    __user_agent__
)


from .omniedge_core.sdk import OmniEdge
from . import models
from  .omniedge_core import errors
from .omniedge_core.sdkconfiguration import *



VERSION: str = __version__


__all__ = [
    "models",
    "errors",
    "OmniEdge",
    "__version__",
    "VERSION",
]



def main():
    """Main entry point for omniedge-python."""
    print("Hello from omniedge-python!")

