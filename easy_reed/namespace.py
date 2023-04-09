# Standard Library Imports
from typing import Self, Any, Dict, Callable
from configparser import ConfigParser

class NameSpace():

    def __init__(self, name: str, filename: str, *, typemap: Dict[str, type] = None, interpolators: Dict[type, Callable]) -> Any:
        self._name = name
        self._config = ConfigParser(
            strict=True
        )

        for key, value in interpolators:
            errmsg = "An entry in the interpolators dictionary was incorrectly formatted:"
            if type(key) != type:
                raise ValueError(
                    f"{errmsg} the key must be type a object indicating what type the value (a Callable) converts to."
                    f"The offending key value pair: {key}, {value}"
                )
            if type(value) != Callable:
                raise ValueError(
                    f"{errmsg} the key must be type a object indicating what type the value (a Callable) converts to."
                    f"The offending key value pair: {key}, {value}"
                )
        
        with open(filename) as f:
            self._config.read_file(f)
        
    def __get__(self, config_key):
        if config_key not in self._config:
            raise KeyError(f"key {config_key} does not exist in the config NameSpace {self._name}")
        
        return self._config[config_key]