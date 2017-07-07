#!/usr/bin/env python
#coding=utf-8
"""
config unit tests
"""
import os.path

# module under test
# this is an abstract base class
import config

# unit testing framweork
import unittest


class ConfigTest(unittest.TestCase):

    #--------------------------------------------------------------------------
    # Test Cases    
    #--------------------------------------------------------------------------

    def test_type_error_instantiating_abstract_base_class(self):
        try:
            self.c = config.Config(force=True)
        except TypeError:
            self.assertRaises(TypeError)
