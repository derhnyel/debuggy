import sys
from subprocess import Popen
import os
import pickle
import inspect
import linecache
import threading
#import win32com
#import win32api

#__all__=['comment']


"""Function to get the filename and path to Python script calling Debuggy Module
    linecache is used to get lines from python source file while attempting to optimize internally.
"""
def _get_caller_stack():
        # Get the full stack
        frame_stack = inspect.stack()

        # Get one level up from current
        caller_frame_record = frame_stack[-1]

        return caller_frame_record
        #caller_file_name = CallerFrame.filename  # Filename where caller lives

def _get_caller_script():
        #open caller script
        script = linecache.getlines(_get_caller_path())

        return script

def _get_caller_path():
     # Get the module object of the caller 
    calling_script = inspect.getmodule(_get_caller_stack()[0])

    #module name from this path
    caller_path = os.path.dirname(calling_script.__file__)

    return(caller_path)        
        
"""Function to accept line comments"""

#run on seperate thread
def comment(_comment:str,method=None):
    def _comment_thread():
        _default_methods = ('class','func','val',None)
        if method in _default_methods:
            _cache = open(os.path.join(__module_path__,'cache'),'wb')
            _lineno = _get_caller_stack()[2]
            _cache_dict[_lineno] = (method,_comment)
            pickle.dump(_cache_dict,_cache)
            _cache.flush() 
        else:
            raise ValueError("comment.method argument only accepts",_default_methods)
    threading._start_new_thread(_comment_thread,())




    #check and accept only class,func or val as object.
        
def _main():

    #Get process id of running script
    process_id = os.getpid()

    #Monitor Terminal Output and Capture Standard Error to Logger

    sys.stderr = __logger

    #Run main.py From Terminal With Subprocess
    __main = Popen(["python","main.py",str(process_id)])



#Execute,if Python File is Imported
if __name__ != '__main__':
    __name__ = 'Debuggy'
    __module_path__ = os.path.dirname(__file__)
    _caller = _get_caller_path()
    
    
    #log_file = os.path.join(_caller,'log')
    ##win32api.SetFileAttributes(log_file,win32con.FILE_ATTRIBUTE_HIDDEN)
    #os.system( "attrib %s +h "%(log_file,))
    
    #Open Logger in write mode
    __logger = open( os.path.join(_caller,'log'),'w')
    
    _cache_dict={}
    _main()
    
    
    


