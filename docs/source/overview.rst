.. ############################################################################
   This file contains reStructuredText, please do not edit it unless you are
   familar with reStructuredText markup as well as Sphinx specific markup.
   
   For information regarding reStructuredText markup see 
      http://sphinx.pocoo.org/rest.html
   
   For information regarding Sphinx specific markup see
      http://sphinx.pocoo.org/markup/index.html
      
   ############################################################################
   
.. ########################### SECTION HEADING REMINDER #######################
   # with overline, for parts
   * with overline, for chapters
   =, for sections
   -, for subsections
   ^, for subsubsections
   ", for paragraphs

.. -----------------------------------------------------------------------------

Overview
========

The abstract base class **Config** is defined in the module named **config**. It provides most of the 
configuration management funcationality, except typically for configuration file 
reading and writing -- both these methods are to be defined in a class that sub-classes **Config**.

Currently there are two modules that sub-class Config and provide configuration file
reading and writing for two different configuration file formats. These modules are:

   * **configjson** - provides a **JSON** configuration file format

   * **configyaml** - provides a **YAML** configuration file format

The abstract base class itself cannot be instantiated, if attempted, a **TypeError**
exception with be raised by the Python interpreter.


Testing
-------

The project includes unit test in the **tests** directory alone with test coverage results in
the **htmlcov** directory.


