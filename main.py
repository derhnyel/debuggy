import sys
from psutil import Process,NoSuchProcess
import argparse

parser = argparse.ArgumentParser (prog='deBuggy',description='Used For Error Parsing')

parser.add_argument()
parser.add_argument('--pid', help='Process id of Current Running Python Process')
parser.add_argument('--foo', help='foo of the %(prog)s program')
class Debuggy():
  def __init__(self):
    self.ProccessId = int(sys.argv[1])
    self.ProcessState = None
    self.ErrorMessage = None


  def MonitorProcess(self):
    try:
      self.ProcessState = 'alive'
      while self.ProcessState is 'alive':
          TrackProcess = True if Process(self.ProccessId) else False
    
    except NoSuchProcess as e:
          self.ProcessState = 'dead'
          with open('log','r') as log:
              self.ErrorMessage= log.read()
              print(self.ErrorMessage) 

# syntax_error= """\nForgetting to put a : at the end of an if, elif, else, for, while, class, or def statement. (Causes “SyntaxError: invalid syntax”)
# \nThis error happens with code like this:
# \nif spam == 42 
#                ^      
#     print('Hello!')"""

#import os
#import time
#       #filename.close()
#   finally:
#       sys.stdout = sys_out
#sys.exit() 
#filename = open('dump.txt','w')
#sys_out = sys.stdout
#sys.stdout = filename
# k  = sys.path
# p = sys.platform
# error = None

