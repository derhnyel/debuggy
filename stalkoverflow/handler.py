from psutil import Process,NoSuchProcess
import sys
from stalkoverflow.color import bcolors
from stalkoverflow import parsers
from stalkoverflow import ui



def CheckErrorMessage(ErrorMessage):
    """Filters the ErrorMessage and returns valid."""
    if ErrorMessage=='':
        return False
    else:
        if any(error in ErrorMessage for error in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            return False
        else:
            return True  
def MonitorProcess(ProcessId):
  try:
      print(bcolors.green+bcolors.bold+"Checking Running Script for Errors...",file=sys.stdout)      
      while True:
          RunningProcess = Process(ProcessId)
  except NoSuchProcess as e:
        return False

def CleanError(ErrorMessage):
  error = ErrorMessage[-2]#.split(':')
  ErrorLineno = int(ErrorMessage[1].split(',')[1].strip(' line'))
  error = error
  return (ErrorLineno,error)


def UserConfirm(question):
      ValidInputs = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
      prompt = "[Y/n] "
      while True:
        print(bcolors.reverse+bcolors.cyan+bcolors.bold+question+prompt,bcolors.end,file=sys.stdout)
        UserChoice= input().lower()
        if UserChoice in ValidInputs:
          return ValidInputs[UserChoice]
        print(bcolors.reverse+bcolors.blue+"Please respond with 'yes' or 'no' (or 'y' or 'n').\n",bcolors.end,file=sys.stdout)

def execute(LogPath,ProcessId):
  #global ProcessState,ErrorMessage,ValidError
  ProcessState = MonitorProcess(ProcessId)
  #clear terminal  
  with open(LogPath,'r') as log:
    ErrMessage = log.read()
    ValidError=print(bcolors.red+bcolors.bold+ErrMessage,file=sys.stdout) if CheckErrorMessage(ErrMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
    ErrorMessage = ErrMessage.split('\n')
  if ValidError:
    print(bcolors.red+bcolors.bold+ErrMessage,bcolors.end,file=sys.stdout)
    DisplayResult = UserConfirm('DeBuggy Wants to Search And Display Results?: ')
    if DisplayResult:
        ErrorMessage = ErrMessage.split('\n')
        _,Error = CleanError(ErrorMessage)
        #return error,lineno,ProcessState,ValidError
        Error='%s %s %s' %('python',Error,' site:stackoverflow.com')
        titles,_,links,_=parsers.GSearch(Error)
        ui.start_app(links,titles)
        #return ErrorMessage 
    else:
      sys.exit(1)    
  else:
    sys.exit(1)