# Config

A simple Python configuration manager that supports either **JSON** or **YAML** formatted configuration files.
****
### Other Config Solutions
The are other more complex and feature rich solutions to managing a configuration -- the most notable are:

1. [configparser](https://docs.python.org/3/library/configparser.html) from the **Python Standard Library** for managing INI format configurations.
2. [ConfigObj](http://www.voidspace.org.uk/python/configobj.html) also manages INI format configurations and is, as its documentation states, "an ini file round tripper".

As configuration managers become more feature rich they start to approach a true persistent storage
solution. If you really want a persistent data store module rather than a config module,
check out the **shelve module** that persists Python objects.

You can find it in the **Python Standard Library** on-line documentation here -- [shelve](https://docs.python.org/3/library/shelve.html)

## Getting Started

Unfortunately, this project is not yet [pypi](https://packaging.python.org/) package compliant so it is not pip install-able yet. Therefore, fork this project or download the zip and un-archive it, and change directory into the root of the project.

To use the project either **import configjson** or **import configyaml** -- both of these modules sub-class the abstract base class module **config** to implement either **JSON** or **YAML** support.

See *Usage* section for more details.


### Prerequisites

This project was developed and tested using Python 3.6.0. Support for Python 2.x is not provided.

If you desire to use it with JSON support, there are zero prerequisites because it uses the **json** module in the **Python Standard Library**.

If you desire to use it with YAML support, the prerequisites are:

- [ruamel.yaml](https://yaml.readthedocs.io/en/latest/)

	```
	pip install ruamel.yaml
	```

This YAML package supports YAML 1.2.

## Unit Tests
To run all the unit tests, change directory into the root of the project and run the module **tests.py** from the console, as in:

	python tests.py

The resulting output should look similar to this:

	...............................................                           
	----------------------------------------------------------------------    
	Ran 47 tests in 0.076s                                                    
                                                                          
	OK      

Or run the unit test for each module **configjson.py**, **configyaml.py**, and **config.py** from the console, as in:

	python config.py
	python configjson.py
	python configyaml.py

Running the unit tests this way will result in more copious output since they have the verbosity level set to 2.

###Test Coverage
If you are interested in the test coverage of the above unit tests, see the contents of the **htmlcov** directory in the root of the project and load any of the following HTML files into a web browser:

- **index.html**
- **config_py.html**
- **configjson_py.html**
- **configyaml_py.html**

####Generating Test Coverage Information
This project used the most excellent **coverage** module -- see [Coverage.py](https://coverage.readthedocs.io/en/coverage-4.4.1/).

Install **coverage**:

	pip install coverage

Run the config unit tests:

	coverage run --branch tests.py

Generate a simple text report:

	coverage report
	
	Name            Stmts   Miss Branch BrPart  Cover
	-------------------------------------------------
	config.py          52      0     14      0   100%
	configjson.py      21      0      4      0   100%
	configyaml.py      38      0      8      0   100%
	-------------------------------------------------
	TOTAL             111      0     26      0   100%

Or generate an html report:

	coverage html

and l****ook at the results as described earlier in this section.

## Usage
Decide which configuration file format will be used -- YAML or JSON.

The most simple (and useless) JSON usage:

	python
	>>> import configjson
	>>> c = configjson.Config()
	>>> c.cfg
	{}

The above console session also produces a default configuration file named
**config.json** which contains {}.

The most simple (and useless) YAML usage:

	python
	>>> import configyaml       
	>>> c = configyaml.Config() 
	>>> c.cfg                   
	{}                          

The above console session also produces a default configuration file named
**config.yaml** which contains {}.

A more illustrative example, for **configyaml** and **configjson** together:

	python
	>>> import configyaml                                                                                                                                                                                                     
	>>> cfg_default = dict()                                                                                                                                                                                                  
	>>> cfg_default['Logging'] = dict()                                                                                                                                                                                       
	>>> cfg_default['Logging']['ConsoleLoggingLevel'] = 'INFO'                                                                                                                                                                
	>>> cfg_default['Logging']['FileLoggingLevel'] = 'DEBUG'                                                                                                                                                                  
	>>> cfg_default['Logging']['LogFileName'] = 'logfile.log'                                                                                                                                                                 
	>>> cfg_default['Application'] = dict()                                                                                                                                                                                   
	>>> cfg_default['Application']['verbosity'] = 2                                                                                                                                                                           
	>>> cfg_default['Application']['height'] = 45                                                                                                                                                                             
	>>> cfg_default['Application']['width'] = 225                                                                                                                                                                             
	>>> cfg_default['Application']['database'] = 'default'                                                                                                                                                                    
	>>> cfg_default['Application']['media'] = ['avi', '.mkv,', '.mp4', '.wmv']                                                                                                                                                
	>>> c = configyaml.Config(cfgobj=cfg_default, cfgfile='app_cfg.yaml')                                                                                                                                                     
	>>> c.cfg                                                                                                                                                                                                                 
	CommentedMap([('Logging', CommentedMap([('ConsoleLoggingLevel', 'INFO'), ('FileLoggingLevel', 'DEBUG'), ('LogFileName', 'logfile.log')])), ('Application', CommentedMap([('verbosity', 2), ('height', 45), ('width', 225),
	 ('database', 'default'), ('media', ['avi', '.mkv,', '.mp4', '.wmv'])]))])                                                                                                                                                
	>>> c.cfg['Logging']['LogFileName']                                                                                                                                                                                       
	'logfile.log'                                                                                                                                                                                                             
	>>> c.cfg['Application']['media']                                                                                                                                                                                         
	['avi', '.mkv,', '.mp4', '.wmv']                                                                                                                                                                                          
	>>> import pprint                                                                                                                                                                                                         
	>>> pp = pprint.PrettyPrinter(indent=4)                                                                                                                                                                                   
	>>> pp.pprint(c.cfg)                                                                                                                                                                                                      
	{   'Application': {   'database': 'default',                                                                                                                                                                             
	                       'height': 45,                                                                                                                                                                                      
	                       'media': ['avi', '.mkv,', '.mp4', '.wmv'],                                                                                                                                                         
	                       'verbosity': 2,                                                                                                                                                                                    
	                       'width': 225},                                                                                                                                                                                     
	    'Logging': {   'ConsoleLoggingLevel': 'INFO',                                                                                                                                                                         
	                   'FileLoggingLevel': 'DEBUG',                                                                                                                                                                           
	                   'LogFileName': 'logfile.log'}}                                                                                                                                                                         
	>>>                                                                                                                                                                                                                       
	>>> import configjson                                                                                                                                                                                                     
	>>> c2 = configjson.Config(cfgdict=cfg_default, cfgfile='app_cfg.json')                                                                                                                                                   
	>>> c2.cfg                                                                                                                                                                                                                
	{'Logging': {'ConsoleLoggingLevel': 'INFO', 'FileLoggingLevel': 'DEBUG', 'LogFileName': 'logfile.log'}, 'Application': {'verbosity': 2, 'height': 45, 'width': 225, 'database': 'default', 'media': ['avi', '.mkv,', '.mp4
	', '.wmv']}}                                                                                                                                                                                                              
	>>> pp.pprint(c2.cfg)                                                                                                                                                                                                     
	{   'Application': {   'database': 'default',                                                                                                                                                                             
	                       'height': 45,                                                                                                                                                                                      
	                       'media': ['avi', '.mkv,', '.mp4', '.wmv'],                                                                                                                                                         
	                       'verbosity': 2,                                                                                                                                                                                    
	                       'width': 225},                                                                                                                                                                                     
	    'Logging': {   'ConsoleLoggingLevel': 'INFO',                                                                                                                                                                         
	                   'FileLoggingLevel': 'DEBUG',                                                                                                                                                                           
	                   'LogFileName': 'logfile.log'}}                                                                                                                                                                         


The above rather long console session produced two configuration files -- **app_cfg.yaml** and **app_cfg.json**. 

Examining the contents of these two files yields:

**app_cfg.yaml**

	Logging:
	  ConsoleLoggingLevel: INFO
	  FileLoggingLevel: DEBUG
	  LogFileName: logfile.log
	Application:
	  verbosity: 2
	  height: 45
	  width: 225
	  database: default
	  media:
	  - avi
	  - .mkv,
	  - .mp4
	  - .wmv


**app_cfg.json**

	{
	    "Application": {
	        "database": "default",
	        "height": 45,
	        "media": [
	            "avi",
	            ".mkv,",
	            ".mp4",
	            ".wmv"
	        ],
	        "verbosity": 2,
	        "width": 225
	    },
	    "Logging": {
	        "ConsoleLoggingLevel": "INFO",
	        "FileLoggingLevel": "DEBUG",
	        "LogFileName": "logfile.log"
	    }
	}

The JSON file contains a configuration that looks more Python-like, but the YAML file is considered by many to be easier for a human to read/write, and unlike the JSON format, YAML supports rount-trip preservation of comments (not demonstrated above) -- see [ruamel.yaml](http://yaml.readthedocs.io/en/latest/overview.html) documentation for more details.

## YAML References
If you would like to explore the YAML syntax further, here are a few references that I found useful:

1. [Complete Idiot's Introduction to YAML](https://github.com/Animosity/CraftIRC/wiki/Complete-idiot's-introduction-to-yaml)
2. [YAML Syntax](http://docs.ansible.com/ansible/YAMLSyntax.html)
3. [The Official YAML Specification](http://www.yaml.org/)

## API

Both the **JSON** and **YAML** modules support *almost* the same module API.

For details concerning the API, see documentation in the **docs/build/html** directory. The file **index.html** provides the top level documentation entry point.

## Todo

1. Use [cookiecutter](https://github.com/audreyr/cookiecutter) and make this a pypi compliant project.

 
## Contributing

1. Fork it! See [GitHub Help Fork a Repo](https://help.github.com/articles/fork-a-repo/)
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request: see [GitHub Help - Creating a Pull Request](https://help.github.com/articles/creating-a-pull-request-template-for-your-repository/)


## Credits

[eruber](https://github.com/eruber) eruber@gmail.com

## License

This project is licensed under the MIT License - see the **LICENSE** file for details.