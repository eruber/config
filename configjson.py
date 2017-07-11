#!/usr/bin/env python
#coding=utf-8
"""
Module configjson

This class sub-classes the abstract base class, Config, in the config module
to provide JSON specific configuration read and write methods.

.. moduleauthor:: E.R. Uber <eruber@gmail.com>

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
    its read() and write() methods to support JSON.

    Class Attributes:

    .. note:: Class Attributes are not an attribute of an *instance* of a class (ie, the object); they are an attribute of the class itself.

    .. note:: The Class Attributes specified below over-ride the same Class Attributes defined in the abstract base class config.Config.

    """

    #: Default configuration file name, cfgfile, if none is specified during class instantiation
    DEFAULT_CFG_FILE   = "config.json"

    #: Default configuration dictionary, cfg, if none is specified during class instantiation.
    DEFAULT_CFG        = {}
    
    #: Default force parameter value, force, if none is specified during class instantiation.
    DEFAULT_FORCE      = False

    #: Default write_thru parameater value, write_thru, if none is specified during class instantiation.
    DEFAULT_WRITE_THRU = False

    #: Default configuration file text encoding, encoding, if none is specified during class instantiation.
    DEFAULT_ENCODING   = 'utf-8'


    def read(self, **kwargs):
        """
        Reads the cfgfile and stores the results in the configuration dictionary, cfg.

        See `json module in PSL`_ for a full treatment of the parameter list.


        Returns: 

            The configuration dictionary accessible by the cfg property.
        
        .. _json module in PSL: https://docs.python.org/3/library/json.html

        """
        with open(self._cfgfile, encoding=self._encoding, mode='r') as cp:
            self._cfg = json.load(cp,  **kwargs)

        return(self._cfg)


    def write(self, **kwargs):
        """
        Writes the configuration dictionary, cfg, to file system using the file name cfgfile.
        The file will be in JSON format.

        See `json module in PSL`_ for a full treatment of the key-word/default-value parameter list.

        Below are a few of the more frequently used paremeters with their default
        values specified:

            **skipkeys** = False - If True, dictionary keys not of bastic type (str, int, float, bool, None) will be skipped instead of raining a TypeError

            **indent** = None - Should be a non-negative integer or string used to prettyprint with that indent level
        
            **sort_keys** = False - If True, dictionary output will be sorted by key.
        
        Returns:

            None


        .. _json module in PSL: https://docs.python.org/3/library/json.html

        """
        if 'indent' not in kwargs:
            kwargs['indent'] = 4

        if 'sort_keys' not in kwargs:
            kwargs['sort_keys'] = True

        with open(self._cfgfile, encoding=self._encoding, mode='w') as cp:
            json.dump(self._cfg, cp, **kwargs)


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":

    from unittest import main
    main(module='tests.test_configjson', verbosity=2)




