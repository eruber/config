#!/usr/bin/env python
#coding=utf-8
"""
configyaml unit tests
"""
import os.path
import shutil
from pathlib import Path

# module under test
import configyaml

from config import ConfigFileNamesDirException

# unit testing framweork
import unittest

D = {'log' : 'whatever-log-filename.log', 'verbose' : True}

CUSTOM_CFG_FILE1 = 'custom.cfg'
CUSTOM_CFG_FILE2 = 'configurate.yaml'
TEST_77          = "test_77.yaml"
TEST_77_UPDATED  = "test_77_updated.yaml"

DIR_CFG_FILE = 'configuration'

inp_str_1 = """\
# example
name:
  # details
  family: Smith   # very common
  given: Alice    # one of the siblings
  cousins: 3      # number of first cousins
"""

inp_str_1_udpated = """\
# example
name:
  # details
  family: Smith   # very common
  given: Francesca # one of the siblings
  cousins: 3      # number of first cousins
"""
PATH_LIB_1 = 'tests/yaml_config.cfg'

INP_STR_1_DICT = dict()
INP_STR_1_DICT['name'] = dict()
INP_STR_1_DICT['name']['family']  = 'Smith'
INP_STR_1_DICT['name']['given']    = 'Alice'
INP_STR_1_DICT['name']['cousins'] = 3


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

        dir_cfg = os.path.abspath(DIR_CFG_FILE)
        if os.path.exists(dir_cfg):
            shutil.rmtree(dir_cfg)

        test77 = os.path.abspath(TEST_77)
        if os.path.exists(test77):
            os.remove(test77)

        test77upd = os.path.abspath(TEST_77_UPDATED)
        if os.path.exists(test77upd):
            os.remove(test77upd)

        pathlib_1 = os.path.abspath(PATH_LIB_1)
        if os.path.exists(pathlib_1):
            os.remove(pathlib_1)


    #--------------------------------------------------------------------------
    # Test Cases    
    #--------------------------------------------------------------------------

    def test_default_init_and_cfg_getter(self):
        # setUp has initialized self.c
        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG_DICT)


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

        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG_DICT)

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

        self.assertEqual(e, self.c.DEFAULT_CFG_DICT)
        self.assertEqual(self.c.cfg, self.c.DEFAULT_CFG_DICT)
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
        try:
            # This should be a boolean, so expect a TypeError
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
            # This should be a dictionary, so expect a TypeError
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
        c = configyaml.Config(cfgobj={'width' : 12, 'height' : 92}, force=True)
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
        c = configyaml.Config(cfgfile=custom_cfg_file, force=True)
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
        import ruamel.yaml.error as ERR
        # setUp has initialized self.c, but we do not use it here
        try:
            c = configyaml.Config(cfgobj=[1, 2, 3])
        except ERR.YAMLStreamError:
            self.assertRaises(ERR.YAMLStreamError)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

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

        c = configyaml.Config(cfgfile=CUSTOM_CFG_FILE2, cfgobj=D, force=True)
        self.assertEqual(c.cfg, D)

    def test_custom_exception_cfgfile_names_a_dir_not_a_file(self):
        dir_cfg = os.path.abspath(DIR_CFG_FILE)
        if not os.path.exists(dir_cfg):
            os.makedirs(dir_cfg)

        try:
            d = configyaml.Config(cfgfile=dir_cfg)
        except ConfigFileNamesDirException:
            self.assertRaises(ConfigFileNamesDirException)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

    def test_cfg_obj_is_a_string_comments_preserved_round_trip(self):
        """
        """
        c = configyaml.Config(cfgobj=inp_str_1, cfgfile=TEST_77, force=True)
        cfgdict = c.read(inp_str_1)
        self.assertEqual(cfgdict['name']['given'], 'Alice')
        cfgdict['name']['given'] = 'Francesca'
        c.write()
        cfgdict2 = c.read()
        self.assertEqual(cfgdict2['name']['given'], 'Francesca')

        c2 = configyaml.Config(cfgobj=inp_str_1_udpated, cfgfile=TEST_77_UPDATED, force=True)
        self.assertEqual(c.cfg, c2.cfg)


    def test_invalid_cfgobj_passed_to_read(self):
        """
        """
        import ruamel.yaml.error as ERR
        try:
            self.c.read(cfgobj=[1,2,3])
        except ERR.YAMLStreamError:
            self.assertRaises(ERR.YAMLStreamError)
        else:
            should_not_get_here_should_have_asserted_earlier = True
            self.assertFalse(should_not_get_here_should_have_asserted_earlier)

    def test_init_typ_kwarg(self):
        c = configyaml.Config(typ='safe')
        self.assertEqual(c.cfg, c.DEFAULT_CFG_DICT)

    def test_cfg_obj_is_a_path_obj(self):
        """
        """
        p = Path(PATH_LIB_1)
        size = p.write_text(inp_str_1)

        c = configyaml.Config(cfgobj=p, force=True)

        # Cannot do this since with round-trip comment preservation, the c.cfg
        # is not actually a dictionary, but a dictionary like object called
        # a CommentMap
        #self.assertEqual(c.cfg, INP_STR_1_DICT)

        self.assertEqual(c.cfg['name']['family'], INP_STR_1_DICT['name']['family'])
        self.assertEqual(c.cfg['name']['given'], INP_STR_1_DICT['name']['given'])
        self.assertEqual(c.cfg['name']['cousins'], INP_STR_1_DICT['name']['cousins'])
        
       
        

