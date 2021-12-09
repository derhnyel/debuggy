[![Build Status](https://travis-ci.org/--?branch=master)](https://travis-ci.org/--) [![Downloads](https://pepy.tech/badge/--/month)](https://pepy.tech/project/--)


#### Pure Python Stackoverflow Parser

Everything is done in 100% pure Python so it's extremely easy to install and use. Supports Python 2 & 3.
<hr>

Simple Example:

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
 #### Installation 

    pip install debuggy
    
<hr>

#### Command line
Debuggy comes with a CLI tool . You can use it as such:

```bash
debuggy --query "how to use loops"
```
![Demo](https://github.com/derhnyel/deBuggy/tree/main/assets/debuggy_query.gif)

```bash
usage: DeBuggy [-h] [-v] [-s SCRIPT] [-q QUERY] {call} ...

Command-line tool that automatically searches Google and displays results in
your terminal when you get a compiler error. Made by @Derhnyel

positional arguments:
  {call}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -s SCRIPT, --script SCRIPT
                        Run Script from Terminal
  -q QUERY, --query QUERY
                        Query stackoverflow with Error message
```