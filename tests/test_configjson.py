#!/usr/bin/env python
#coding=utf-8
"""
config unit tests
"""
import os.path
import shutil

# module under test
import configjson

from config import ConfigFileNamesDirException

# unit testing framweork
import unittest

D = {'log' : 'whatever-log-filename.log', 'verbose' : True}

CUSTOM_CFG_FILE = 'custom.cfg'

DIR_CFG_FILE = 'configuration'

class ConfigJsonTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # Test Fixtures
    #--------------------------------------------------------------------------

    def setUp(self):
        # we have to use force=True in case the cfg file
        # was written by a previous test, the force True
        # forces initialization of the config to the 
        # default configuration and does not read the
        # config file
        self.c = configjson.Config(force=True)

    def tearDown(self):
        # cleanup cfg file trash
        custom  = os.path.abspath(CUSTOM_CFG_FILE)
        if os.path.exists(custom):
            os.remove(custom)

        default = os.path.abspath(self.c.DEFAULT_CFG_FILE)
        if os.path.exists(default):
            os.remove(default)

        dir_cfg = os.path.abspath(DIR_CFG_FILE)
        if os.path.exists(dir_cfg):
            shutil.rmtree(dir_cfg)


    #--------------------------------------------------------------------------
    # Test Cases    
    #--------------------------------------------------------------------------

    def test_default_init_and_cfg_getter(self):
        # setUp has initialized self.c
        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG)


    def test_cfg_setter_basic(self):
        # setUp has initialized self.c
        self.c.cfg = D

        self.assertEqual(self.c.cfg, D)


    def test_write_read_basic(self):
        """
        Test the write method by reading the cfg from the file system
        and check it matches what is in memory
        """
        # setUp has initialized self.c
        self.c.cfg = D
        self.c.write()
        from_file_sys = self.c.read()
        
        self.assertEqual(from_file_sys, self.c.cfg)

    def test_force_parameter(self):
        # setUp has initialized self.c
        self.c.cfg = D
        self.c.write()
        from_file_sys = self.c.read()

        self.c = configjson.Config(force=True)

        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG)

    def test_default_write_thru_disabled(self):
        """
        Test that the write thru feature is disabled by default.
        The self.c.cfg in memory does not match what is on the file system.
        """
        # setUp has initialized self.c
        # this is now in memory
        self.c.cfg = {'width': 12}
        s = self.c.cfg
        # read what c.cfg is in the file system
        # remember that read() returns c.cfg as
        # updated from the file system
        e = self.c.read()

        self.assertEqual(e, self.c.DEFAULT_CFG)
        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG)
        self.assertFalse(s == self.c.cfg)

    def test_write_thru_enabled_via_constructor(self):
        """
        Test that the write thru feature is disabled by default.
        The self.c.cfg in memory does not match what is on the file system.
        """
        # setUp has initialized self.c, cut we do not use it in this test
        self.c = configjson.Config(write_thru=True)

        # this is now in memory and in the file system
        self.c.cfg = {'width': 12}
        s = self.c.cfg
        # read what c.cfg is in the file system
        # remember that read() returns c.cfg as
        # updated from the file system
        e = self.c.read()

        self.assertEqual(e, {'width': 12})
        self.assertEqual(self.c.cfg, {'width': 12})
        self.assertTrue(s == self.c.cfg)

    def test_default_write_thru_property_getter(self):
        # setUp has initialized self.c
        self.assertFalse(self.c.writethru)

    def test_write_thru_property_setter(self):
        # setUp has initialized self.c
        self.c.writethru = True
        self.assertTrue(self.c.writethru)

    def test_write_thru_property_setter_invalid_input(self):
        # setUp has initialized self.c
        # non-boolean passed, should result in no change
        # to writethru property
        previous_writethru = self.c.writethru
        try:
            # sheuld be a boolean, expect a TypeError
            self.c.writethru = 12
        except TypeError:
            self.assertRaises(TypeError)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

    def test_invalid_dict_value_in_cfg_property_setter(self):
        # setUp has initialized self.c
        previous_cfg = self.c.cfg
        try:
            # should assing a dictionary, expect a TypeError
            self.c.cfg = (1, 2, 3)
        except TypeError:
            self.assertRaises(TypeError)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

    def test_write_thru_enabled_via_property(self):
        """
        Test that the write thru feature is disabled by default.
        The self.c.cfg in memory does not match what is on the file system.
        """
        # setUp has initialized self.c, write_thru False
        self.c.writethru = True

        # this is now in memory and in the file system
        self.c.cfg = {'width': 12, 'height' : 84}
        s = self.c.cfg
        # read what c.cfg is in the file system
        # remember that read() returns c.cfg as
        # updated from the file system
        e = self.c.read()

        self.assertEqual(e, {'width': 12, 'height' : 84})
        self.assertEqual(self.c.cfg, {'width': 12, 'height' : 84})
        self.assertTrue(s == self.c.cfg)

    def test_init_passing_in_a_cfg(self):
        """
        """
        # setUp has initialized self.c, but we do not use it here
        c = configjson.Config(cfg={'width' : 12, 'height' : 92}, force=True)
        self.assertEqual(c.cfg, {'width' : 12, 'height' : 92})

    def test_cfgfile_property_getter_default_value(self):
        """
        """
        # setUp has initialized self.c
        cfg_file = self.c.cfgfile
        self.assertEqual(os.path.basename(cfg_file), self.c.DEFAULT_CFG_FILE)

    def test_cfgfile_property_getter_passed_value(self):
        """
        """
        # setUp has initialized self.c, but we do not use it here
        custom_cfg_file = CUSTOM_CFG_FILE
        c = configjson.Config(cfgfile=custom_cfg_file)
        cfg_file = c.cfgfile
        self.assertEqual(os.path.basename(cfg_file), custom_cfg_file)

    def test_invalid_cfgfile_on_init(self):
        """
        Assert that if a non-string value is passed as cfgfile,
        then the default cfgfile is used
        """
        # setUp has initialized self.c, but we do not use it here
        c = configjson.Config(cfgfile=True)
        self.assertEqual(os.path.basename(c.cfgfile), c.DEFAULT_CFG_FILE)

    def test_invalid_cfgfile_assignment(self):
        """
        Assert that if a non-string value is set to cfgfile,
        then a TypeError is raised
        """
        original_cfgfile = self.c.cfgfile
        try:
            self.c.cfgfile = False
        except TypeError:
            self.assertRaises(TypeError)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

        self.assertTrue(self.c.cfgfile == original_cfgfile)


    def test_invalid_cfg_on_init(self):
        """
        Assert that if a non-dictionary value is passed as cfg,
        then the default cfg is used
        """
        # setUp has initialized self.c, but we do not use it here
        # cfg should be a dictionary, expect cfg to take on its default value
        c = configjson.Config(cfg=[1, 2, 3])

        self.assertEqual(c.cfg, c.DEFAULT_CFG)

    def test_invalid_write_thru_flag_on_init(self):
        """
        Assert that if a non-boolean value is passed as write_thru,
        then the default write_thru is used
        """
        # setUp has initialized self.c, but we do not use it here
        c = configjson.Config(write_thru=1)
        self.assertEqual(c.writethru, c.DEFAULT_WRITE_THRU)

    def test_invalid_force_flag_on_init(self):
        """
        Assert that if a non-boolean value is passed as force,
        then the default force is used.
        """
        # setUp has initialized self.c, but we do not use it here
        c = configjson.Config(force=1)
        # if the non default value of force had been used,
        # then the cfg would be the devault
        self.assertEqual(c._force, c.DEFAULT_FORCE)

    def test_custom_exception_cfgfile_names_a_dir_not_a_file(self):
        dir_cfg = os.path.abspath(DIR_CFG_FILE)
        if not os.path.exists(dir_cfg):
            os.makedirs(dir_cfg)

        try:
            d = configjson.Config(cfgfile=dir_cfg)
        except ConfigFileNamesDirException:
            self.assertRaises(ConfigFileNamesDirException)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)