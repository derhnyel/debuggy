[![CircleCI](https://circleci.com/gh/derhnyel/deBuggy/tree/main.svg?style=shield)](https://circleci.com/gh/derhnyel/deBuggy/tree/main) [![CircleCI](https://circleci.com/gh/derhnyel/deBuggy/tree/main.svg?style=svg)](https://circleci.com/gh/derhnyel/deBuggy/tree/main) [![PyPI version](https://badge.fury.io/py/debuggy.svg)](https://badge.fury.io/py/debuggy) 
[![Pypi Downloads](https://pepy.tech/badge/debuggy)](https://pepy.tech/project/debuggy)

> "Stalk Overflow with `debuggy`"
#### Error Parser
Everything is done in Python so it's extremely easy to install and use. Supports Python 3. Debuggy is used to execute scripts, it creates a wrap around the script with the help of sub processes, and listens for errors, capturing and parsing them through popular discussion forums. This is then styled and displayed on the terminal with the help of python curses.
<hr>

 ## Installation 
 #### Using Pip 
    For Linux and Mac OS.
    $ sudo pip3 install debuggy
    
    For Windows OS.
    $ pip install debuggy[win]
#### Apt Install
    $ sudo apt install python3-debuggy    
<hr>

#### Manually building from source

- Install Python tools 3+ - (<https://www.python.org/downloads/>)
- Clone this repo `git clone git@github.com:derhnyel/deBuggy.git`
- Run unit tests with `make test`
- Build and install: `make install`
## Usage
Simple Example:
By importing debuggy as the first (1st) line of your python script, it keeps track of the scripts run time and parses any error message encountered.

```python
    >>> import debuggy
```
![Demo Import](https://github.com/derhnyel/deBuggy/blob/main/assets/import.gif)

#### Command line
Debuggy comes with a CLI tool . You can use it as such:
```bash
USAGE: DeBuggy [-h] [-v] [-s SCRIPT] [-q QUERY] {call,editor,s,q} ...

Command-line tool that automatically searches Google and displays results in
your terminal when you get a compiler error. Made by @Derhnyel

positional arguments:
  {call,editor,s,q}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show programs version number and exit
  -s SCRIPT, --script SCRIPT , s SCRIPT
                        Run Script from Terminal
  -q QUERY, --query QUERY , q QUERY
                        Query stackoverflow with Error message
  editor                
                        Open Terminal Editor                          
```

```bash

$ debuggy q concurency in python
```
![Demo Query](https://github.com/derhnyel/deBuggy/blob/main/assets/query.gif)

__Supported file types:__ Python, Node.js, Ruby, Golang, and Java. These can be parsed into debuggy to track Errors by using the --script command.  
```bash

$ debuggy s test.py
```
![Demo Script](https://github.com/derhnyel/deBuggy/blob/main/assets/run_script.gif)

Debuggy also comes with a terminal IDE which can be used to write codes for different languages.This can be accessed by using the command
```bash
$ debuggy editor

$ debuggy editor test.py
```
![Demo Editor](https://github.com/derhnyel/deBuggy/blob/main/assets/editor.gif)

#### Debuggy TUI Commands
- DOWN ARROW KEY (↓) - HIGHLIGHT NEXT LINE
- UP ARROW KEY (↑) - HIGHLIGHT PREVIOUS LINE
- ENTER KEY (enter) - SELECT HIGHLIGHTED LINE | OPEN QUESTION PAGE
- LOWERCASE q KEY (q) - QUIT CURRENT VIEW | QUIT TUI 
- ESCAPE,BACKSPACE KEYS (esc,backspace) - MOVE BACK TO PREVIOUS VIEW
- LOWERCASE b KEY (b) - OPENS CURRENT HIGHLIGHTED LINK IN BROWSER
###### WHILE IN STACKOVERFLOW QUESTION PAGE: 
- (→) and (←) MOVES BETWEEN ANSWERS AND DESCRIPTIONS
- RIGHT ARROW KEY (→) - NEXT PAGE VIEW 
- LEFT ARROW KEY (←) - PREVIOUS PAGE VIEW
- LOWERCASE e KEY (e) - EXPORT CODES FROM ANSWERS TO CLIPBOARD OR SCRIPT IF PRESENT | OPENS EXPORT MENU
###### WHILE IN CODES TO EXPORT MENU:
- LOWERCASE c KEY (c)- COPY CODE TO CLIPBOARD
- ENTER KEY (enter) - SELECT HIGHLIGHTED LINE | OPEN EDITOR IF SCRIPT IS PRESENT ELSE COPIES CODE SNIPPET TO CLIPBOARD

#### Debuggy Editor Commands
The Editor has two modes, Normal and Insert modes. It Opens in normal mode by default. 
- DOWN ARROW KEY (↓) - MOVE CURSOR TO NEXT LINE
- UP ARROW KEY (↑) - MOVE CURSOR TO PREVIOUS LINE
- RIGHT ARROW KEY (→) - MOVE CURSOR RIGHT
- LEFT ARROW KEY (←) - MOVE CURSOR LEFT
###### KEY PRESS ACTIONS IN NORMAL MODE:
- LOWERCASE w KEY (w) - WRITE TO FILE (Editor should be initialized with a filename)
- LOWERCASE a KEY (a) -  Enter Insert mode after cursor position
- LOWERCASE i KEY (i) -  Enter Insert mode
- LOWERCASE x KEY (x) - Delete a character
- KEY DOLLAR SIGN ($) - Move to end of line
- KEY ZERO (0) - Move to beginning of line
- UPPERCASE O KEY (O) - Enter and Insert line before current
- LOWERCASE o KEY (o) - Enter and Insert line after current 
- LOWERCASE q KEY (q) - Quit Editor
###### KEY PRESS ACTIONS IN INSERT MODE:
- KEY BACKSPACE (backspace) - REMOVES PREVIOUS CHARACTER
- KEY ESCAPE (esc) - EXITS INSERT MODE AND RETURNS TO NORMAL MODE

## Contributing

Want to contribute to Debuggy? Awesome! Check out the [contributing guidelines](CONTRIBUTE.md) to get involved.

__Pending Features:__
* Add Commenting feature
* Search result Optimization
* Add Support for more languages

## Meta
Credits: 
* [Shobrook](https://github.com/shobrook) Repository [Rebound](https://github.com/shobrook/Rebound).
* [tdryer](https://github.com/tdryer) Repository [editor](https://github.com/tdryer/editor).


Distributed under the MIT license. See [LICENSE](https://github.com/derhnyel/deBuggy/blob/master/LICENSE) for more information.
* [Eje Daniel](https://github.com/derhnyel) - author/maintainer