import sys
import os
import inspect



"""Function to get the filename and path to Python script calling Debuggy Module
    get lines from python source file while attempting to optimize internally.
"""
def _get_caller_stack(active=False):
        # Get the full stack
        frame_stack = inspect.stack()
        # Get one level up from current
        if active:
            caller_frame_record = frame_stack[-4]
        else:
            caller_frame_record = frame_stack[-1]
        return caller_frame_record
        #caller_file_name = CallerFrame.filename  # Filename where caller lives

def _get_caller_path():
     # Get the module object of the caller 
    calling_script = inspect.getmodule(_get_caller_stack()[0])
    if calling_script==None:
       calling_script = inspect.getmodule(_get_caller_stack(active=True)[0])
    try:
       #module name from this path
       caller_path = os.path.dirname(calling_script.__file__)
    except:
        raise Exception("Debuggy doesn't support the use of interative Shells like idle,ipython,jupyternotebook etc.")
    return (caller_path)                


#print(os.getenv('SHELL'))
__module_path__ = os.path.dirname(__file__)
#__python_path__ = sys.executable
_caller_path = _get_caller_path()    
    #Open Logger
try:
    __logger = open( os.path.join(_caller_path,_get_caller_stack().filename.replace('.py','.err')),'w')
except PermissionError:
    raise PermissionError('Run script in an administrative terminal')

else:
    #Get process id of running script
    process_id = os.getpid()
    #Monitor Terminal Output and Capture Standard Error to Logger
    sys.stderr = __logger
    #Run main.py From Open Terminal(path to modules log_file)
    os.system('start cmd /c debuggy call -e %s -id %s -f %s'%(os.path.join(_caller_path,_get_caller_stack().filename.replace('.py','.err')),process_id,os.path.join(_caller_path,_get_caller_stack().filename)))
    #__main = Popen(["python","main.py",str(process_id)],shell=True,stdin=sys.stdin,stdout=sys.stdout,start_new_session=True)#,executable=USERS_DEFAULT_SHELL)   