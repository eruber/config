#!/usr/bin/env python
#coding=utf-8
"""
Module configyaml

This class sub-classes the abstract base class, Config, in the config module
to provide YAM specific configuration read and write methods.

.. moduleauthor:: E.R. Uber <eruber@gmail.com>


"""
#------------------------------------------------------------------------------
# Python Standard Library
#------------------------------------------------------------------------------
import os.path

#------------------------------------------------------------------------------
# Application Specific 
#------------------------------------------------------------------------------
import config

#------------------------------------------------------------------------------
# Third Party Dependencies
#------------------------------------------------------------------------------
#import yaml
from ruamel.yaml import YAML

#------------------------------------------------------------------------------
class Config(config.Config):
    """
    Sub-class the base config.Config class and over-ride
    its read() and write() methods to support YAML.

    Class Attributes:

    .. note:: Class Attributes are not an attribute of an *instance* of a class (ie, the object); they are an attribute of the class itself.

    .. note:: The Class Attributes specified below over-ride the same Class Attributes defined in the abstract base class config.Config.

    """

    # Class Attributes, 
    # not an attribute of an *instance* of a class, but the class itself

    #: Default configuration file name, cfgfile, if none is specified during class instantiation
    DEFAULT_CFG_FILE   = "config.yaml"

    #: Default configuration dictionary, cfg, if none is specified during class instantiation.
    DEFAULT_CFG        = {}
    
    #: Default force parameter value, force, if none is specified during class instantiation.
    DEFAULT_FORCE      = False

    #: Default write_thru parameater value, write_thru, if none is specified during class instantiation.
    DEFAULT_WRITE_THRU = False

    #: Default configuration file text encoding, encoding, if none is specified during class instantiation.
    DEFAULT_ENCODING   = 'utf-8'


    def __init__(self, cfgfile=None, encoding=None, cfg=None, force=None, write_thru=None, **kwargs):

        if 'typ' not in kwargs:
            kwargs['typ'] = 'safe'

        self.yaml = YAML(**kwargs) # default if not specfied is round-trip

        # Call the base class's constructor
        super(Config, self).__init__(cfgfile=cfgfile, encoding=encoding, cfg=cfg, force=force, write_thru=write_thru)


    def read(self, **kwargs):
        """
        Reads the cfgfile and stores the results in the configuration dictionary, cfg.

        See `yaml documentation`_ for more details on what other keyword/value pairs,
        **kwargs**, might be available as arguments.

        For simple situations, the defaults work fine, no **kwargs** are typically required.
        
        Returns: 

            The configuration dictionary accessible by the cfg property.
        
        .. _yaml documentation: http://yaml.readthedocs.io/en/latest/overview.html

        """

        with open(self._cfgfile, encoding=self._encoding, mode='r') as cp:
            self._cfg = self.yaml.load(cp, **kwargs)

        return(self._cfg)


    def write(self, **kwargs):
        """
        Writes the configuration dictionary, cfg, to file system using the file name cfgfile.
        The file will be in YAML format.

        See `yaml documentation`_ for more details on what other keyword/value pairs,
        **kwargs**, might be available as arguments.

        For simple situations, the defaults work fine, no **kwargs** are typically required.

        Returns:

            None

        .. _yaml documentation: http://yaml.readthedocs.io/en/latest/overview.html

        """
        with open(self._cfgfile, encoding=self._encoding, mode='w') as cp:
            self.yaml.dump(self._cfg, cp, **kwargs)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":

    from unittest import main
    main(module='tests.test_configyaml', verbosity=2)




