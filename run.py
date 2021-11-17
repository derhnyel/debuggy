from sys import stderr
from subprocess import Popen
import os

#Execute,if Python File is Imported
if __name__ != '__main__':

    #Open Logger in write mode
    __logger = open('log','w')
    process_id = os.getpid()

    #Monitor Terminal Output and Capture Standard Error to Logger
    sys_error = stderr
    stderr = __logger

    #Run main.py From Terminal With Subprocess
    tracker = Popen(["python","main.py",str(process_id)])

