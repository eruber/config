#!/usr/bin/env python
#coding=utf-8
"""
Module configyaml

This class sub-classes the abstract base class, **Config**, in the config module
to provide YAML specific configuration read and write methods.

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
import ruamel.yaml

from ruamel.yaml import YAML

#------------------------------------------------------------------------------
class Config(config.Config):
    """
    Sub-class the base config.Config class and over-ride
    its read() and write() methods to support YAML.

    **Constructor Arguments**

    This class changes one of the abstract base class constructor parameters -- it uses a first parameter of **cfgobj** rather than **cfgdict**.
    This is because the YAML interface allows the **cfgobj** parameter to be one of the following three types:

        1. a **string** containing valid YAML
        2. a **pathlib.Path()** object (see the `pathlib mdoule documentation`_ in the Python Standard Library docs) that references a file with valid YAML
        3. a **filepointer** that references a file with value YAML
    
    If **cfgobj** is any of the above three types, the YAML subsystem will be used to convert it to a dictionary; therefore, if a dictionary is
    passed as **cfgobj**, then no conversion is necessary and the interface becomes the same as that used by **configjson**.

    So the **cfgobj** can be passed as a string, a pathlib.Path() object, a filepointer, or a dictionary.

    For a definition of the other unchanged constructor parameters see `the config module API page`_.

    **Constructor Keyword Arguments**

    The remaining keyword arguments, ****kwargs**, are specific to the YAML subsystem's constructor and are discussed in the `YAML subsystem docs`_.
    While this reference is a well write usage guide, it does not, at the time of this writing, appear to be an exhaustive API reference;
    therefore some of the more commonly used ****kwargs** are listed below:

        - typ='safe'
            This ****kwarg** is used by default. It loads the YAML document without resolving unknow tags.

        - pure=True
            This ****Kwarg** enforces using the pure Python implementation (faster C libraries will be used when possible/available).

    **Properties**

    The YAML subsystem utilizes various properties to change its behavior that are defined in the `YAML subsystem docs`_. The more frequently used
    properties are listed below:

        - default_flow_style : a boolean
            default_flow_style = False   # serializes in block style, this is the default
            default_flow_style = True    # serializes in flow style

            Flow style uses explicit indicators rather than indentation (as in block style) to denote scope.
            For more details see `the YAML Spec`_.

        - indent : an integer
            Number of spaces to indent scope, default is 4.

        - block_seq_indent : an integer
            Number of space to indent a block sequence, default is 2.
            Note, the `YAML subsystem docs`_ strongly suggests that to always have indent >= block_seq_indent + 2 but this is not enforced. 
            Depending on your structure, not following this advice might lead to invalid output.

        - top_level_colon_align : a boolean
            Set True (and yaml.indent = 4) causes calculation based on the longest key.

        - prefix_colon : a string
            Setting this to ' 'prefixes an extra space between a mapping key and the colon

        - allow_duplicate_keys : a boolean
            Set this True if you want to allow duplicate key mappings, this is not allowed by default.

        - allow_unicode : a boolean
            By default this is True, to disable Unicode support, set this property to False.

    Here is an expample of setting some of the above properties::

        import configyaml

        c = configyaml.Config( ... )

        c.yaml.default_flow_style = False
        c.yaml.indent = 4
        c.yaml.block_seq_indent = 2

    Class Attributes:

    .. note:: Class Attributes are not an attribute of an *instance* of a class (ie, the object); they are an attribute of the class itself.

    .. note:: The Class Attributes specified below over-ride the same Class Attributes defined in the abstract base class config.Config.

    .. _the config module API page: config.html

    .. _pathlib mdoule documentation: https://docs.python.org/3/library/pathlib.html

    .. _YAML subsystem docs: https://yaml.readthedocs.io/en/latest/basicuse.html

    .. _the YAML Spec: http://www.yaml.org/spec/1.2/spec.html

    """

    # Class Attributes, 
    # not an attribute of an *instance* of a class, but the class itself

    #: Default configuration file name, **cfgfile**, if none is specified during class instantiation
    DEFAULT_CFG_FILE   = "config.yaml"

    #: Default configuration dictionary, **cfg**, if none is specified during class instantiation.
    DEFAULT_CFG_DICT    = {}
    
    #: Default force parameter value, **force**, if none is specified during class instantiation.
    DEFAULT_FORCE      = False

    #: Default write_thru parameater value, **write_thru**, if none is specified during class instantiation.
    DEFAULT_WRITE_THRU = False

    #: Default configuration file text encoding, **encoding**, if none is specified during class instantiation.
    DEFAULT_ENCODING   = 'utf-8'


    def __init__(self, cfgobj=None, cfgfile=None, encoding=None, force=None, write_thru=None, **kwargs):

        if not cfgobj:
            cfgobj = self.DEFAULT_CFG_DICT

        self._cfgobj = cfgobj

        if 'typ' not in kwargs:
            kwargs['typ'] = 'safe'

        self.yaml = YAML(**kwargs) # default if not specfied is round-trip

        self.yaml.default_flow_style = False  # blow style, not flow style
        self.yaml.indent = 4
        self.yaml.block_seq_indent = 2

        # cfgobj can be one of three types:
        #    a dict or 
        #    a filepointer, a string, or a pathlib.Path() object
        # if its not a dictionary, we attempt to convert it to a dictionary
        if isinstance(cfgobj, dict):
            cfgdict = cfgobj
        else:
            # cfgobj must be either a string, a fliepointer, or a pathlib.Path() object
            try:
                cfgdict = self.yaml.load(cfgobj)
            except ruamel.yaml.error.YAMLStreamError as e:
                raise(e)


        # Call the base class's constructor
        super(Config, self).__init__(cfgdict=cfgdict, cfgfile=cfgfile, encoding=encoding, force=force, write_thru=write_thru)


    def read(self, cfgobj=None, **kwargs):
        """
        The **cfgobj** parameter can be one of the following:

            1. a **string** containing valid YAML
            2. a **pathlib.Path()** object (see the `pathlib mdoule documentation`_ in the Python Standard Library docs) that references a file with valid YAML
            3. a **filepointer** that references a file with value YAML
    
        If **cfgobj** is any of the above three types, the YAML subsystem will be used to convert it to a dictionary and return it.
        The dictionary will also be accessible via the **cfg** property.

        If **cfgobj** is not defined, then the **cfgfile** will be loaded and its contents returned as a dictionary that is also accessible via the **cfg** property.

        See `yaml documentation`_ for more details on what other keyword/value pairs,
        **kwargs**, might be available as arguments.

        For simple situations, the defaults work fine, no **kwargs** are typically required.
        
        Returns: 

            The configuration dictionary which is also accessible by the **cfg** property.
        
        .. _yaml documentation: http://yaml.readthedocs.io/en/latest/overview.html

        """
        if cfgobj:
            try:
                self._cfgdict = self.yaml.load(cfgobj)
                return(self._cfgdict)
            except ruamel.yaml.error.YAMLStreamError as e:
                raise(e)

        else:
            # read from cfgfile
            with open(self._cfgfile, encoding=self._encoding, mode='r') as cp:
                self._cfgdict = self.yaml.load(cp, **kwargs)

            return(self._cfgdict)


    def write(self, cfgdict=None, stream=None, **kwargs):
        """
        This method writes its input, **cfgdict**, via the output **stream**. The file written will be in YAML format.

        If **cfgdict** is not defined, then this method uses the object's configuration dictionary, **cfg**, as input.

        If **stream** is not defined, then the object's **cfgfile** will be used to write the input to.

        Note that **stream** can be specified as sys.output to write the YAML file to console.

        Note that **stream** can also be specified as a filepointer or a pathlib.Path() object.

        If a transform of the string representation of the output is desired, a keyword **transform** can be used, as in::

            transform=transform_func

        where transform_func is a function that takes a string as input and returns a transformed string as output.

        See `yaml documentation`_ for more details on what other keyword/value pairs,
        **kwargs**, might be available as arguments.

        For simple situations, the defaults work fine, no **kwargs** are typically required.

        Returns:

            None

        .. _yaml documentation: http://yaml.readthedocs.io/en/latest/overview.html

        """
        with open(self._cfgfile, encoding=self._encoding, mode='w') as cp:
            self.yaml.dump(self._cfgdict, cp, **kwargs)

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__": # pragma: no cover

    from unittest import main
    main(module='tests.test_configyaml', verbosity=2)

