#!/usr/bin/env python
#coding=utf-8
"""
config

Abstract Base Class for implementing a simple configuration manager.
Sub-class it and provide your own read/write methods.

If you really want a persistent data store module rather than a config module,
chech out: 
            shelve - Python object persistence

you can find it in the Python Standard Library on-line documentation:

    https://docs.python.org/3/library/shelve.html

"""
import os.path
import abc

#------------------------------------------------------------------------------
class ConfigFileNamesDirException(Exception):
    """
    Custom exeception
    """
    pass

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
class Config(metaclass=abc.ABCMeta):

    # Class Attributes, 
    # not an attribute of an *instance* of a class, but the class itself
    DEFAULT_CFG_FILE   = "config.cfg"
    DEFAULT_CFG        = {}
    DEFAULT_FORCE      = False
    DEFAULT_WRITE_THRU = False
    DEFAULT_ENCODING   = 'utf-8'

    def __init__(self, cfgfile=None, encoding=None, cfg=None, force=None, write_thru=None):
        """
        cfgfile - configurate file name, relative or absolute

        encoding - default str encoding for Python 3 is utf-8, use this parameter
                   to change the unicode encoding used to read/write the cfgfile 
        
        cfg     - configuration dictionary, defaults to empty
        
        force   - boolean, if True, forces Config object initialization 
                  to init the config to the default cfg rather than read
                  it from the file system it the cfg exits in the file system

        write_thru - boolean, if True, any changes made in memory to cfg
                     by using the setter property will be immediated written 
                     thru to the file system
        """
        cfg_file = cfgfile if isinstance(cfgfile, str) else self.DEFAULT_CFG_FILE

        self._cfgfile    = os.path.abspath(cfg_file)
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
        Reads the cfgfile, returns cfg if not errors.
        This method should be over-ridden in a sub-class.
        """
        #raise NotImplementedError

    @abc.abstractmethod
    def write(self):
        """
        Writes cfg to file system and return it.
        This method should be over-ridden in a sub-class.
        """
        #raise NotImplementedError

    @property
    def cfg(self):
        """
        Returns the instance of the configuration dictionary
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


    @property
    def writethru(self):
        """
        Returns the boolean value of the write thru property
        """
        return(self._write_thru)

    @writethru.setter
    def writethru(self, boolean_value):
        """
        Modifies the boolean value of the write thru property
        """
        if isinstance(boolean_value, bool):
            self._write_thru = boolean_value

    @property
    def cfgfile(self):
        """
        Returns the full absolute path of the cfgfile
        """
        return(self._cfgfile)

    @cfgfile.setter
    def cfgfile(self, file_name):
        if isinstance(file_name, str):
            self._cfgfile = os.path.abspath(file_name)


if __name__ == "__main__":

    from unittest import main
    main(module='tests.test_config', verbosity=2)

