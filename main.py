from re import A, L
import sys
from psutil import Process,NoSuchProcess
import os
#import argparse
#import asyncio
#import pickle
#import time
#import threading
from search_engine_parser.core.engines.google import Search as GoogleSearch
#from collections import deque
import pyfiglet
#from termcolor import colored, cprint
import time

bold='\033[01m'
underline='\033[04m'
reverse='\033[07m'
black='\033[30m'
red='\033[31m'
green='\033[32m'
orange='\033[33m'
blue='\033[34m'
purple='\033[35m'
cyan='\033[36m'
lightgrey='\033[37m'
darkgrey='\033[90m'
lightred='\033[91m'
lightgreen='\033[92m'
yellow='\033[93m'
lightblue='\033[94m'
pink='\033[95m'
lightcyan='\033[96m'
#end = '\033[0m'
end =''


# def LoadAnimation(LoadString):
  
#     # String to be displayed when the application is loading
    
#     StringLength = len(LoadString)
  
  
#     # String for creating the rotating line
#     animation = "|/-\\"
#     AniCount = 0
      
#     # used to keep the track of
#     # the duration of animation
#     CountTime = 0        
      
#     # pointer for travelling the loading string
#     pointer = 0                     
  
#     while (CountTime != 100):  
#         # used to change the animation speed
#         # smaller the value, faster will be the animation
#         time.sleep(0.01)                          
#         # converting the string to list
#         # as string is immutable
#         ListString = list(LoadString) 
#         # ascii->obtaining the ASCII code
#         ascii = ord(ListString[pointer])
#         # cache->for storing altered ASCII code
#         cache = 0                             
#         # if the character is "." or " ", keep it unaltered
#         # switch uppercase to lowercase and vice-versa 
#         if ascii != 32 and ascii != 46:             
#             if ascii>90:
#                 cache = ascii-32
#             else:
#                 cache = ascii + 32
#             ListString[pointer]= chr(cache)
#         # for storing the resulting string
#         ResultString =''             
#         for index in range(StringLength):
#             ResultString = ResultString + ListString[index]      
#         # displaying the resulting string
#         sys.stdout.write("\r"+ResultString + animation[AniCount])
#         sys.stdout.flush()
#         # Assigning loading string
#         # to the resulting string
#         LoadString= ResultString
#         AniCount = (AniCount + 1)% 4
#         pointer =(pointer + 1)% StringLength
#         CountTime = CountTime + 1
#    os.system('cls' if OsName=='nt' else 'clear')
def UserConfirm(question):
      ValidInputs = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
      prompt = "[Y/n] "
      while True:
        print(reverse+cyan+bold+question+prompt+end,file=sys.stdout)
        UserChoice= input()
        #for inputs in sys.stdin:
        #  UserChoice = input
        #  break
        #UserChoice=sys.stdin.read()
        if UserChoice in ValidInputs:
          return ValidInputs[UserChoice]
        #PrintColor = lambda x,y,z:cprint(x,y,z) 
        #text = colored("Please respond with 'yes' or 'no' (or 'y' or 'n').\n",'blue',attrs=['reverse','blink'])  
        #print(text)
        print(reverse+blue+"Please respond with 'yes' or 'no' (or 'y' or 'n').\n",file=sys.stdout)


def CheckErrorMessage(ErrorMessage):
    """Filters the ErrorMessage and returns valid."""
    if ErrorMessage=='':
        return False
    else:
        if any(error in ErrorMessage for error in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            return False
        else:
            return True  
def execute():
  try:      
      while True:
          RunningProcess = Process(ProcessId)
  except NoSuchProcess as e:
        return False
  
def MonitorProcess(ProcessId):
  global ProcessState
  ProcessState = execute()
  #clear terminal  
  with open('log','r') as log:
    ErrorMessage = log.read()
    ValidError=print(red+bold+ErrorMessage,file=sys.stdout) if CheckErrorMessage(ErrorMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
  if ValidError:
    print(red+bold+ErrorMessage,file=sys.stdout)
    DisplayResult = UserConfirm('DeBuggy Wants to Display Search Results?: ')
    if DisplayResult:
        ErrorMessage = ErrorMessage.split('\n')
        [print(i) for i in ErrorMessage]
        #RootNode code from traceback =2
       #Root Module imported and method =3
       #base for raise Exceptions =-2
       #base for error and cause = -1
        return ErrorMessage 
    else:
      sys.exit()    
  else:
    sys.exit()
          

          #pickle_off=  open('cache','rb')    
          #emp=pickle.load(pickle_off) 

    


#if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            #return None
  #async def Parser(self):
   #   res = await self.MonitorProcess() 
    #stackoverflow
    #stackexchange
    #gitcommunity

    #check if error message has been geerated
    #def CleanError():  
   
if __name__=='__main__':
  #queue = deque()
  OsName=os.name
  #LoadAnimation("starting your console application...")
  os.system('cls' if OsName=='nt' else 'clear')
  DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
  print(cyan+DebuggyAnimation)
  print(green+bold+"Checking Running Script for Errors...",file=sys.stdout)
  ProcessId = int(sys.argv[1])
  ProcessState  = True
  ErrorMessage = MonitorProcess(ProcessId)






       


#parser = argparse.ArgumentParser (prog='deBuggy',description='Used For Error Parsing')
#parser.add_argument()
# parser.add_argument("pid", type=str, help='Process Id of Current Running Python Process')
# parser.add_argument('-m','--mtr', help='monitor current process',action='store_true')
# args = parser.parse_args()
# bugZy = Debuggy(int(args.pid))
# if args.mtr:
#   print('monitor: %s' % args.pid)
#   bugZy.MonitorProcess()



# syntax_error= """\nForgetting to put a : at the end of an if, elif, else, for, while, class, or def statement. (Causes “SyntaxError: invalid syntax”)
# # \nThis error happens with code like this:
# # \nif spam == 42 
# #                ^      
# #     print('Hello!')"""

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

