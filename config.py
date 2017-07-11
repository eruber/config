#!/usr/bin/env python
#coding=utf-8
"""
Module config

.. moduleauthor:: E.R. Uber <eruber@gmail.com>

"""
import os.path
import abc

#------------------------------------------------------------------------------
class ConfigFileNamesDirException(Exception):
    """
    Custom exeception covering the logical case that the **cfgfile** specified is
    indeed not a file, but a directory. I know, who would do such a thing?
    """
    pass

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
class Config(metaclass=abc.ABCMeta):
    """
    Abstract Base Class for implementing a simple configuration manager.
    Sub-class it and provide your own read/write methods. 

    Args:

        **cfgfile** - a string 

        Specifies the configuration file name, relative or absolute.
        The default is the value of the **DEFAULT_CFG_FILE** attribute.

        **encoding** - a string 

        Specifies the string encoding for the configuration filem, **cfgfile**.
        Use this parameter to change the unicode encoding used to read/write the **cfgfile**.
        The default is the value of the **DEFAULT_ENCODING** attribute.
    
        **cfg**  - a dictionary

        Specifies the configuration state used to initialize the configuration file, **cfgfile**, if it does not
        already exist; if it does exist, this dictionary will be over-written by the contents of the
        configuration file, **cfgfile**. To force re-iniitalization of the **cfgfile** with this dictionary
        after the file already exists, use the **force** parameter. The default is the value of the
        DEFAULT_CFG attribute.
    
        **force**   - a boolean

        If True, forces the contents of the configuration dictionary specified, **cfg**, to over-write any
        existing **cfgfile**. The default behavior is for the configuration file to be read and used to initialize 
        the configuration dictionary, **cfg**. The default is the value of the **DEFAULT_FORCE** attribute.

        **write_thru** - a boolean

        If True, any changes made to the **cfg** property via an assignment will result in the configuration file, 
        **cfgfile**, being immediately updated. If False, the configurate dictionary and the configuration file will not
        be in sync until the write method is executed. The default is the value of the **DEFAULT_WRITE_THRU** attribute.

    .. note:: If any of the class constructor parameters passed are not of the correct type,
              the default value for that parameter will be used. See Class Attributes for
              default values.

    Returns:

        An object instatiation of the Confg Manager class, Config, as defined herein.

    Raises:

        TypeError

    .. warning:: Instantiating this class directly will result in a TypeError exception being raised. 

    See test_config.py in the tests directory which includes this test.

    Class Attributes:

    .. note:: Class Attributes are not an attribute of an *instance* of a class (ie, the object); they are an attribute of the class itself.

    .. note:: All Class Attributes can be over-ridden by the sub-class.

    """

    #--------------------------------------------------------------------------
    # Class Attributes, 
    # not an attribute of an *instance* of a class, but the class itself
    #--------------------------------------------------------------------------


    #: Default configuration file name, cfgfile, if none is specified during class instantiation.
    DEFAULT_CFG_FILE   = "config.cfg"

    #: Default configuration dictionary, cfg, if none is specified during class instantiation.
    DEFAULT_CFG        = {}

    #: Default force parameter value, force, if none is specified during class instantiation.
    DEFAULT_FORCE      = False

    #: Default write_thru parameater value, write_thru, if none is specified during class instantiation.
    DEFAULT_WRITE_THRU = False

    #: Default configuration file text encoding, encoding, if none is specified during class instantiation.
    DEFAULT_ENCODING   = 'utf-8'


    def __init__(self, cfgfile=None, encoding=None, cfg=None, force=None, write_thru=None):

        self._cfgfile    = os.path.abspath(cfgfile if isinstance(cfgfile, str) else self.DEFAULT_CFG_FILE)
        self._encoding   = encoding if isinstance(encoding, str) else self.DEFAULT_ENCODING
        self._cfg        = cfg if isinstance(cfg, dict) else self.DEFAULT_CFG
        self._force      = force if isinstance(force, bool) else self.DEFAULT_FORCE
        self._write_thru = write_thru if isinstance(write_thru, bool) else self.DEFAULT_WRITE_THRU

        self._cfg_def_passed = cfg

        self._initCfg()

    def _initCfg(self):
        """
        If the cfgfile already exits in the file system, load it; however,
        if it does not exist, initalize the configuration in the file system
        with the cfg passed to the constructor above.

        NOTE: A side-effect is that if the path to the cfgfile does not
              exist, it will be created. 
        """
        if self._force:
            # Ignore if cfg exists in file system, and init it to the
            # default cfg.
            # WARNING - This overwrites the cfg in the file system
            os.makedirs(os.path.dirname(self._cfgfile), exist_ok=True)
            self.write()
        else:
            if os.path.exists(self._cfgfile):
                if os.path.isfile(self._cfgfile):
                    self._cfg = self.read()
                else:
                    msg = format("'%s' names a directory! It should be a file. Please remove it or change config file name, and try again." % self._cfgfile)
                    raise ConfigFileNamesDirException(msg);
            else:
                # The configuration file does not exist, 
                # make sure it has a directory to live in,
                # and create it.
                os.makedirs(os.path.dirname(self._cfgfile), exist_ok=True)
                self.write()


    @abc.abstractmethod
    def read(self):
        """
        Reads the **cfgfile**.

        Returns: 

            The configuration dictionary accessible by the **cfg** property.

        .. note:: This method should be over-ridden by a sub-class.
        
        """

    @abc.abstractmethod
    def write(self):
        """
        Writes **cfg** to file system using the file name **cfgfile**.

        Returns:

            None

        .. note:: This method should be over-ridden by a sub-class.

        """

    @property
    def cfg(self):
        """
        Property

        **cfg** - the configuration dictionary

        Returns the configuration dictionary.

        Can be used to set the configuration dictionary.
        If set and the **writethru** property is True, then
        the dictionary will be immdediately written to the file system using the filename **cfgfile**.

        Raises:

            TypeError if **cfg** assignment value is not a dictionary.

        """
        return(self._cfg)

    @cfg.setter
    def cfg(self, dict_value):
        """
        Sets the internal cfg dictionary, unless dict_value is
        not a dictionary, then nothing happens.
        Note, if writethru is enabled, the file system will
        be updated.
        """
        if isinstance(dict_value, dict):
            self._cfg = dict_value
            if self._write_thru:
                self.write()
        else:
            raise TypeError("Assignment value to cfg vmust be a dictionary!")


    @property
    def writethru(self):
        """
        Property

        **writethru** - a boolean

        If set to True, any dictionary assignments to the **cfg** property will result in the **cfgfile** being updated.

        If set to False, any dictionary assignments to the **cfg** property will be to the dictionary in memory only, 
        not to the **cfgfile**. An explicit **write()** will have to be done by the user to update **cfgfile**.

        Raises:

            TypeError if **writethru** assignment value is not a boolean.

        """
        return(self._write_thru)

    @writethru.setter
    def writethru(self, boolean_value):
        """
        Modifies the boolean value of the write thru property
        """
        if isinstance(boolean_value, bool):
            self._write_thru = boolean_value
        else:
            raise TypeError("Assignment value to writethru must be a boolean!!")

    @property
    def cfgfile(self):
        """
        Property

        **cfgfile** - a string 

        Returns the *full absolute path* of the **cfgfile**.

        Can used to set the **cfgfile** name.

        Raises:

            TypeError if **cfgfile** assignment value is not a string.

        """
        return(self._cfgfile)

    @cfgfile.setter
    def cfgfile(self, file_name):
        if isinstance(file_name, str):
            self._cfgfile = os.path.abspath(file_name)
        else:
            raise TypeError("Assignment value to cfgfile must be a string!!")


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
if __name__ == "__main__":

    from unittest import main
    main(module='tests.test_config', verbosity=2)

