import sys
from psutil import Process,NoSuchProcess



class Debuggy():
  def __init__(self):
    self.process_id = int(sys.argv[1])
    self.process = None


  def monitor_process(self):
    try:
      self.process = 'alive'
      while self.process is 'alive':
          track_process = Process(self.process_id)
    
    except NoSuchProcess:
          self.process = 'dead'
          with open('log','r') as log:
              error = log.read()
              print(error) 

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
