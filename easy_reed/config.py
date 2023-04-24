# Standard Library Imports
from typing import Self, Any, Dict, Tuple

# Application Imports
from easy_reed._logger import logger
from easy_reed.namespace import NameSpace

class Config():
    """
    
    
    """

    def __init__(self) -> Self:
        self._config = {}

    def __get__(self, arg: str, ) -> Any:
        """ fetches
        
        """
        if arg not in self._config:
            raise KeyError("f{arg} is missing from the config")
        return self._config[arg]

    def __set__(self, key: str, value: Any) -> ValueError:
        raise ValueError("The easy_reed Config object does not allow developers to add config fields directly in code.  This must be done from a configuration file.")
    
    def add_namespace(namespace: NameSpace):
        pass

    def register(self, filename: str, *, typemap: Dict[str, Any] = None):
        pass