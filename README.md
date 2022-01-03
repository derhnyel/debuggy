[![CircleCI](https://circleci.com/gh/derhnyel/deBuggy/tree/main.svg?style=shield)](https://circleci.com/gh/derhnyel/deBuggy/tree/main) [![CircleCI](https://circleci.com/gh/derhnyel/deBuggy/tree/main.svg?style=svg)](https://circleci.com/gh/derhnyel/deBuggy/tree/main) [![PyPI version](https://badge.fury.io/py/debuggy.svg)](https://badge.fury.io/py/debuggy) 
[![Pypi Downloads](https://pepy.tech/badge/debuggy)](https://pepy.tech/project/debuggy)

> "Stalk Overflow with `debuggy`"
#### Error Parser
Everything is done in Python so it's extremely easy to install and use. Supports Python 3. Debuggy is used to execute scripts, it creates a wrap around the script with the help of sub processes, and listens for errors, capturing and parsing them through popular discussion forums. This is then styled and displayed on the terminal with the help of python curses.
<hr>

## Usage
Simple Example:
By importing debuggy as the first (1st) line of your python script, it keeps track of the scripts run time and parses any error message encountered.

```python
    >>> import debuggy
```

You can also use debuggy comments to add comments to your code and make debugging earsier. Comments can be made before functions, classes and declaration of variables stating the function of the preceeding code block, if an error occurs within the code block , the comment is used to track proceedures to execute the function properly.

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
![Demo Query](https://github.com/derhnyel/deBuggy/blob/main/assets/debuggy_query.gif)

__Supported file types:__ Python, Node.js, Ruby, Golang, and Java. These can be parsed into debuggy to track Errors by using the --script command.  
```bash
$ debuggy --script test.py
```
![Demo Script](https://github.com/derhnyel/deBuggy/blob/main/assets/debuggy_script.gif)
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


## Meta
Inspired by [Shobrook](https://github.com/shobrook) Repository [Rebound](https://github.com/shobrook/Rebound).

Distributed under the MIT license. See [LICENSE](https://github.com/derhnyel/deBuggy/blob/master/LICENSE) for more information.
* [Eje Daniel](https://github.com/derhnyel) - author/maintainer
