#!/usr/bin/env python
#coding=utf-8
"""
configjson


A simple configuration file manager based on JSON.

If you really want a persistent data store module rather than a config module,
chech out: 
            shelve - Python object persistence

you can find it in the Python Standard Library on-line documentation:

    https://docs.python.org/3/library/shelve.html

See the unit tests in test_config.py

"""
#------------------------------------------------------------------------------
# Python Standard Library
#------------------------------------------------------------------------------
import os.path
import json

#------------------------------------------------------------------------------
# Application Specific 
#------------------------------------------------------------------------------
import config

#------------------------------------------------------------------------------
# Third Party Dependencies
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
class Config(config.Config):
    """
    Sub-class the base config.Config class and over-ride
    its read() and write() methods with YAML versions
    """
    # Class Attributes, 
    # not an attribute of an *instance* of a class, but the class itself
    DEFAULT_CFG_FILE   = "config.json"
    DEFAULT_CFG        = {}
    DEFAULT_FORCE      = False
    DEFAULT_WRITE_THRU = False
    DEFAULT_ENCODING   = 'utf-8'

    def read(self):
        """
        Reads the cfgfile, returns cfg if not errors.
        """
        with open(self._cfgfile, encoding=self._encoding, mode='r') as cp:
            self._cfg = json.load(cp)

        return(self._cfg)


    def write(self):
        """
        Writes cfg to file system and return it. 
        """
        with open(self._cfgfile, encoding=self._encoding, mode='w') as cp:
            json.dump(self._cfg, cp, indent=4, sort_keys = True)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":

    from unittest import main
    main(module='tests.test_configjson', verbosity=2)




