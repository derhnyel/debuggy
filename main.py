import sys
import subprocess
import psutil
import os
import logging
#os.getppid()

#os.getcwd()

class Debuggy:

    def __init__(self):
        self.running = None
        self.pid = os.getpid()
        self.process = psutil.Process(self.pid)

    def check_runtime(self):
        self.runtime_status = self.process.status()


    def __main__(self):
        self.check_runtime()
        if self.runtime_status == 'stopped':
            logging.info('Service Stopped')




