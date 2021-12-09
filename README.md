[![Build Status](https://travis-ci.org/--?branch=master)](https://travis-ci.org/--) [![Downloads](https://pepy.tech/badge/--/month)](https://pepy.tech/project/--)

|
.. image:: https://img.shields.io/pypi/v/sh.svg?style=flat-square
    :target: https://pypi.python.org/pypi/debuggy
    :alt: Version
.. image:: https://img.shields.io/pypi/dm/sh.svg?style=flat-square
    :target: https://pypi.python.org/pypi/debuggy
    :alt: Downloads Status
.. image:: https://img.shields.io/pypi/pyversions/sh.svg?style=flat-square
    :target: https://pypi.python.org/pypi/debuggy
    :alt: Python Versions
|

> "Stalk Overflow with `debuggy`"
#### Pure Python Stackoverflow Parser
Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3.
<hr>

Simple Example:
By importing debuggy as the first (1st) line of your python script, it keeps track of the scripts run time and parses any error message encountered.

```python
    >>> import debuggy
```

You can also use debuggy comments to add comments to your code and make debugging earsier. Comments can be made before functions, classes and declaration of variables stating the function of the preceeding code block, if an error occurs withing the code block the comment is used to track proceedures to execute the function properly.

```python
    >>> from debuggy import comment 
    >>> comment('function to add two numbers')
    >>> def Add (x,y):
            return x + y    

```
The type of preceeding code block can also be specified ,whether it is a function,class or variable using the 'type' argument with either 'func','class','var' as the type parameter.
```python
    >>> from debuggy import comment 
    >>> comment(comment = 'function to add two numbers' ,type='func')
    >>> def Add (x,y):
            return x + y    

```
 #### Installation 

    $ pip install debuggy

    or apt-get if you're using Linux:

    $ sudo apt-get install debuggy
    
<hr>

#### Command line
Debuggy comes with a CLI tool . You can use it as such:

```bash
$ debuggy --query "how to use loops"
```
![Demo](https://github.com/derhnyel/deBuggy/blob/main/assets/debuggy_query.gif)

__Supported file types:__ Python, Node.js, Ruby, Golang, and Java. These can be parsed into debuggy to track Errors by using the --script command.  
```bash
$ debuggy --script test.py
```

```bash
USAGE: DeBuggy [-h] [-v] [-s SCRIPT] [-q QUERY] {call} ...

Command-line tool that automatically searches Google and displays results in
your terminal when you get a compiler error. Made by @Derhnyel

positional arguments:
  {call}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show programs version number and exit
  -s SCRIPT, --script SCRIPT
                        Run Script from Terminal
  -q QUERY, --query QUERY
                        Query stackoverflow with Error message
```

## Manually building from source

- Install Python tools 3+ - (<https://www.python.org/downloads/>)
- Clone this repo `git clone git@github.com:derhnyel/deBuggy.git`
- Run unit tests with `make test`
- Build and install: `make install`

## Contributing

Want to contribute to Debuggy? Awesome! Check out the [contributing guidelines](CONTRIBUTE.md) to get involved.

__Pending Features:__
* Add Commenting feature
* Search result Optimization
* Add Support for more languages

## Support
=======
* `Eje Daniel <https://github.com/derhnyel>`_ - author/maintainer
