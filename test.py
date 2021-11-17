import psutil
import os
import threading

from multiprocessing import Process

import time


pid = os.getppid()
print(pid)
#print(process.children)
#print(process.status())
#print(process.threads())
def run():
  #print(process)  
  while True:
      process = psutil.Process(pid)
      print(process.name())
    #   p = process.threads()
      
    #   for i in p:
    #        print(i)
      #time.sleep(1)
      
threading._start_new_thread(run,())
# recieve_thread = threading.Thread(target=run)
# recieve_thread.daemon = True
# recieve_thread.start()  
if __name__ == '__main__':
   p = Process(target=run)
   p.start()
   p.join()

for i in range(10):
    print(i)
#print(process.children)
#print(process.status())
#print(process.threads())    
#print(pid)    
    
  

