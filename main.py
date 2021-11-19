import sys
from psutil import Process,NoSuchProcess
#import argparse
import asyncio
import pickle
import time



class Buggy:
  def __init__(self):
    self.ProccessId = int(sys.argv[1])
    self.ProcessState = 'alive'
    self.ErrorMessage = None

    

  def MonitorProcess(self):
    try:      
      while self.ProcessState is 'alive':
          RunningProcess = Process(self.ProccessId)
          TrackProcess = True if RunningProcess else False
          print(RunningProcess.status())
          time.sleep(2)

    except NoSuchProcess as e:
          self.ProcessState = 'dead'

    finally:      
          with open('log','r') as log:
              self.ErrorMessage=log.read()
              print(self.ErrorMessage)
          pickle_off=  open('cache','rb')    
          emp=pickle.load(pickle_off)   
  #async def Parser(self):
   #   res = await self.MonitorProcess() 
    #stackoverflow
    #stackexchange
    #gitcommunity

    #check if error message has been geerated
    
ErrorParser = Buggy()

bugZy = ErrorParser.MonitorProcess()



       


#parser = argparse.ArgumentParser (prog='deBuggy',description='Used For Error Parsing')
#parser.add_argument()
# parser.add_argument("pid", type=str, help='Process Id of Current Running Python Process')
# parser.add_argument('-m','--mtr', help='monitor current process',action='store_true')
# args = parser.parse_args()
# bugZy = Debuggy(int(args.pid))
# if args.mtr:
#   print('monitor: %s' % args.pid)
#   bugZy.MonitorProcess()



syntax_error= """\nForgetting to put a : at the end of an if, elif, else, for, while, class, or def statement. (Causes “SyntaxError: invalid syntax”)
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

