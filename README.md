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
![Demo Import](https://github.com/derhnyel/deBuggy/blob/main/assets/import.gif)

 #### Installation 

    $ pip install debuggy
    
<hr>

#### Command line
Debuggy comes with a CLI tool . You can use it as such:

```bash
$ debuggy --query "how to use loops"
$ debuggy q concurency in python
```
![Demo Query](https://github.com/derhnyel/deBuggy/blob/main/assets/query.gif)

__Supported file types:__ Python, Node.js, Ruby, Golang, and Java. These can be parsed into debuggy to track Errors by using the --script command.  
```bash
$ debuggy --script test.py
$ debuggy s test.py
```
![Demo Script](https://github.com/derhnyel/deBuggy/blob/main/assets/script.gif)
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
Debuggy also comes with a terminal IDE which can be used to write codes for different languages
Run command
```bash
$ debuggy editor

$ debuggy editor test.py
```
![Demo Script](https://github.com/derhnyel/deBuggy/blob/main/assets/editor.gif)

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
Supports 
[Shobrook](https://github.com/shobrook) Repository [Rebound](https://github.com/shobrook/Rebound).
Inspired by [tdryer](https://github.com/tdryer) Repository [editor](https://github.com/tdryer/editor).

Distributed under the MIT license. See [LICENSE](https://github.com/derhnyel/deBuggy/blob/master/LICENSE) for more information.
* [Eje Daniel](https://github.com/derhnyel) - author/maintainer