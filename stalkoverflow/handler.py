from psutil import Process,NoSuchProcess
import sys
from stalkoverflow.color import bcolors
from stalkoverflow import parsers
from stalkoverflow import ui
import re
from subprocess import PIPE, Popen
from threading import Thread
from queue import Queue

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
  """Checks IF scripts process Id is still Alive"""  
  try:
      print(bcolors.green+bcolors.bold+"Checking Running Script for Errors...",file=sys.stdout)      
      while True:
          RunningProcess = Process(ProcessId)
  except NoSuchProcess as e:
        return False

def CleanError(ErrorMessage):
  """Clean Errors from Log File when using import statement"""
  error = ErrorMessage[-2]#.split(':')
  ErrorLineno = int(ErrorMessage[1].split(',')[1].strip(' line'))
  error = error
  return (ErrorLineno,error)


def script_language(_path):
    """Returns the language a file is written in."""
    if _path.endswith(".py"):
      return "python"
    elif _path.endswith(".js"):
      return "node"
    elif _path.endswith(".go"):
      return "go run"
    elif _path.endswith(".rb"):
        return "ruby"
    elif _path.endswith(".java"):
        return 'javac' # Compile Java Source File
    elif _path.endswith(".class"):
        return 'java' # Run Java Class File  
    else:
      return 'unknown'      


def read(pipe, funcs):
    """Reads and pushes piped output to a shared queue and appropriate lists."""
    for line in iter(pipe.readline, b''):
        for func in funcs:
            func(line.decode("utf-8"))
    pipe.close()


def write(get):
    """Pulls output from shared queue and prints to terminal."""
    for line in iter(get, None):
        print(line)


## Main ##


def listen4errors(command):
    """Executes a given command and clones stdout/err to both variables and the
    terminal (in real-time)."""
    process = Popen(
        command,
        cwd=None,
        shell=False,
        close_fds =(sys.platform != 'win32'),
        stdout=PIPE,
        stderr=PIPE,
        bufsize=1
    )
#close_fds=True if (sys.version_info[0]==3 and sys.version_info[1]>=7) or (sys.platform != 'win32') else False,
    output, errors = [], []
    pipe_queue = Queue() # Wowee, thanks CS 225

    # Threads for reading stdout and stderr pipes and pushing to a shared queue
    stdout_thread = Thread(target=read, args=(process.stdout, [pipe_queue.put, output.append]))
    stderr_thread = Thread(target=read, args=(process.stderr, [pipe_queue.put, errors.append]))

    writer_thread = Thread(target=write, args=(pipe_queue.get,)) # Thread for printing items in the queue

    # Spawns each thread
    for thread in (stdout_thread, stderr_thread, writer_thread):
        thread.daemon = True
        thread.start()

    process.wait()

    for thread in (stdout_thread, stderr_thread):
        thread.join()

    pipe_queue.put(None)

    output = ' '.join(output)
    errors = ' '.join(errors)

    #if "java" != command[0] and not os.path.isfile(command[1]): # File doesn't exist, for java, command[1] is a class name instead of a file
    #    return (None, None)
    #else:
    return (output, errors)



def get_error_message(error, language):
    """Filters the stack trace from stderr and returns only the error message."""
    if error == '':
        return None
    elif language == "python":
        if any(e in error for e in ["KeyboardInterrupt", "SystemExit", "GeneratorExit"]): # Non-compiler errors
            return None
        else:
            return error.split('\n')[-2].strip()
    elif language == "node":
        return error.split('\n')[4][1:]
    elif language == "go run":
        return error.split('\n')[1].split(": ", 1)[1][1:]
    elif language == "ruby":
        error_message = error.split('\n')[0]
        return error_message[error_message.rfind(": ") + 2:]
    elif language == "javac":
        m = re.search(r'.*error:(.*)', error.split('\n')[0])
        return m.group(1) if m else None
    elif language == "java":
        for line in error.split('\n'):
            # Multiple error formats
            m = re.search(r'.*(Exception|Error):(.*)', line)
            if m and m.group(2):
                return m.group(2)

            m = re.search(r'Exception in thread ".*" (.*)', line)
            if m and m.group(1):
                return m.group(1)

        return None


def UserConfirm(question):
      """Validates User Choice"""
      ValidInputs = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
      prompt = "[Y/N] "
      while True:
        print(bcolors.reverse+bcolors.cyan+bcolors.bold+question+prompt,bcolors.end,file=sys.stdout)
        UserChoice= input().lower()
        if UserChoice in ValidInputs:
          return ValidInputs[UserChoice]
        print(bcolors.reverse+bcolors.blue+"Please respond with 'yes' or 'no' (or 'y' or 'n').\n",bcolors.end,file=sys.stdout)           


def ProcessScript(script):
   language = script_language(script)
   if language=='unknown':
      print("\n%s%s%s" % (bcolors.red, "Sorry, Debuggy doesn't support this file type.\n", bcolors.end))
      sys.exit(1)
   if language == 'java':
          script = [f.replace('.class', '') for f in script]
  #  if language=='javac':
  #    language = 'java' 
   output, error = listen4errors("%s %s"%(language,script))
   if (output, error) == (None, None) or ("can't open file" in error and "No such file or directory" in error): # Invalid file
            print(bcolors.red+bcolors.bold+'Invalid File'+bcolors.end)
            sys.exit(1)      
   error_msg = get_error_message(error, language) # Prepares error message for search
   eln,_=CleanError(error)         
   if error_msg==None :
     sys.exit(1) 
   DisplayResult = UserConfirm('DeBuggy Wants to Search And Display Results?: ')
   if DisplayResult:   
      Error='%s %s %s' %(language,error_msg,' site:stackoverflow.com')
      titles,_,links,_=parsers.GSearch(Error)
      ui.start_app(links,titles,file = script,errorlineno=eln) if language=='python' else ui.start_app(links,titles)



def execute(LogPath,ProcessId,filename=None):
  """Executes Error Log File and Spawn UI"""  
  ProcessState = MonitorProcess(ProcessId)#Monitor Process
  with open(LogPath,'r') as log:
    ErrMessage = log.read()#open error log
    ValidError=print(bcolors.red+bcolors.bold+ErrMessage,file=sys.stdout) if CheckErrorMessage(ErrMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
    ErrorMessage = ErrMessage.split('\n')
  if ValidError:
    print(bcolors.red+bcolors.bold+ErrMessage,bcolors.end,file=sys.stdout)
    DisplayResult = UserConfirm('DeBuggy Wants to Search And Display Results?: ')
    if DisplayResult:
        ErrorMessage = ErrMessage.split('\n')
        error_line_no,Error = CleanError(ErrorMessage)# Extract meaningful text from error log
        #return error,lineno,ProcessState,ValidError
        Error='%s %s %s' %('python',Error,' site:stackoverflow.com')#Add tag to search query
        titles,_,links,_= parsers.GSearch(Error)#Fetch Results
        if titles!=[]:
            ui.start_app(links,titles,file=filename,errorlineno=error_line_no)#Start UI
        else:
            print(bcolors.red+"No search Result Found"+bcolors.end)
            input("Press Enter To Continue")
        #return ErrorMessage 
    else:
      sys.exit(1)    
  else:
    sys.exit(1)