#!/usr/bin/env python
#coding=utf-8
"""
configyaml unit tests
"""
import os.path

# module under test
import configyaml

# unit testing framweork
import unittest

D = {'log' : 'whatever-log-filename.log', 'verbose' : True}

CUSTOM_CFG_FILE1 = 'custom.cfg'
CUSTOM_CFG_FILE2 = 'configurate.yaml'

class ConfigYamlTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # Test Fixtures
    #--------------------------------------------------------------------------

    def setUp(self):
        # we have to use force=True in case the cfg file
        # was written by a previous test, the force True
        # forces initialization of the config to the 
        # default configuration and does not read the
        # config file
        self.c = configyaml.Config(force=True)

    def tearDown(self):
        # cleanup cfg file trash
        custom  = os.path.abspath(CUSTOM_CFG_FILE1)
        if os.path.exists(custom):
            os.remove(custom)

        default = os.path.abspath(self.c.DEFAULT_CFG_FILE)
        if os.path.exists(default):
            os.remove(default)

        custom2 = os.path.abspath(CUSTOM_CFG_FILE2)
        if os.path.exists(custom2):
            os.remove(custom2)


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

        self.c = configyaml.Config(force=True)

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
        self.c = configyaml.Config(write_thru=True)

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
        self.c.writethru = 12
        self.assertTrue(self.c.writethru == previous_writethru)

    def test_invalid_dict_value_in_cfg_property_setter(self):
        # setUp has initialized self.c
        previous_cfg = self.c.cfg
        self.c.cfg = (1, 2, 3)
        self.assertTrue(previous_cfg == self.c.DEFAULT_CFG)

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
        c = configyaml.Config(cfg={'width' : 12, 'height' : 92}, force=True)
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
        custom_cfg_file = CUSTOM_CFG_FILE1
        c = configyaml.Config(cfgfile=custom_cfg_file)
        cfg_file = c.cfgfile
        self.assertEqual(os.path.basename(cfg_file), custom_cfg_file)

    def test_invalid_cfgfile_on_init(self):
        """
        Assert that if a non-string value is passed as cfgfile,
        then the default cfgfile is used
        """
        # setUp has initialized self.c, but we do not use it here
        c = configyaml.Config(cfgfile=True)
        self.assertEqual(os.path.basename(c.cfgfile), c.DEFAULT_CFG_FILE)

    def test_invalid_cfg_on_init(self):
        """
        Assert that if a non-dictionary value is passed as cfg,
        then the default cfg is used
        """
        # setUp has initialized self.c, but we do not use it here
        c = configyaml.Config(cfg=[1, 2, 3])
        self.assertEqual(c.cfg, c.DEFAULT_CFG)

    def test_invalid_write_thru_flag_on_init(self):
        """
        Assert that if a non-boolean value is passed as write_thru,
        then the default write_thru is used
        """
        # setUp has initialized self.c, but we do not use it here
        c = configyaml.Config(write_thru=1)
        self.assertEqual(c.writethru, c.DEFAULT_WRITE_THRU)

    def test_invalid_force_flag_on_init(self):
        """
        Assert that if a non-boolean value is passed as force,
        then the default force is used.
        """
        # setUp has initialized self.c, but we do not use it here
        c = configyaml.Config(force=1)
        # if the non default value of force had been used,
        # then the cfg would be the devault
        self.assertEqual(c._force, c.DEFAULT_FORCE)

    def test_yaml(self):
        D = dict()
        D['Application'] = dict()
        D['Shell'] = dict()
        D['Application']['name'] = 'coolapp'
        D['Application']['log']  = 'coolapp.log'
        D['Shell']['debug'] = 'off'
        D['Shell']['size'] = (42, 123)
        D['Shell']['coins'] = [12, 33]

        c = configyaml.Config(cfgfile=CUSTOM_CFG_FILE2, cfg=D, force=True)
        self.assertEqual(c.cfg, D)