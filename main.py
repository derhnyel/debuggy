import sys
from psutil import Process,NoSuchProcess
import os
import pyfiglet
import threading
#import multiprocessing
import requests
#import urwid
import webbrowser
#from urwid.widget import (BOX, FLOW, FIXED)
from bs4 import BeautifulSoup as bs4 
import re
from fake_useragent import UserAgent
import curses
#from curses.textpad import Textbox,rectangle
from curses import wrapper
from curses import textpad
from functools import reduce
#import argparse
#import asyncio
#import pickle
import time
from search_engine_parser.core.engines.google import Search as GoogleSearch

#
#from collections import deque

#from termcolor import colored, cprint
#import time
# Scroll actions
SCROLL_LINE_UP = "line up"
SCROLL_LINE_DOWN = "line down"
SCROLL_PAGE_UP = "page up"
SCROLL_PAGE_DOWN = "page down"
SCROLL_TO_TOP = "to top"
SCROLL_TO_END = "to end"

# Scrollbar positions
SCROLLBAR_LEFT = "left"
SCROLLBAR_RIGHT = "right"


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
end = '\033[0m'
#end =''



def StylizeCode(Text):
    """Identifies and stylizes code in a question or answer."""
    # TODO: Handle blockquotes and markdown
    StylizedText = []
    CodeBlocks = [block.get_text() for block in Text.find_all("code")]
    BlockQuotes = [block.get_text() for block in Text.find_all("blockquote")]
    newline = False

    for child in Text.recursiveChildGenerator():
        name = getattr(child, "name", None)

        if name is None: # Leaf (terminal) node
            if child in CodeBlocks:
                if newline: # Code block
                    #if code_blocks.index(child) == len(code_blocks) - 1: # Last code block
                        #child = child[:-1]
                    StylizedText.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    StylizedText.append(("code", u"%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')
                StylizedText.append(u"%s" % str(child))

    if type(StylizedText[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if StylizedText[-2][1].endswith('\n'):
            StylizedText[-2] = ("code", StylizedText[-2][1][:-1])

    return StylizedText

def GSearchNonThreaded(Error):
    global Connection
    Error='python ' +Error +' site:stackoverflow.com'
    #search_results=[]
    try:
      #time.now
      gs = GoogleSearch()
      SearchArgs=(Error,1)
      gs.clear_cache()
      SearchDict=gs.search(*SearchArgs)
    except Exception as e:
       sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold, "DeBuggy was unable to fetch results. "
                                            +str(e)+"\n Try again Later.", end))
       Connection = False
       return Connection
    titles=[]
    descriptions=[]
    urls=[]
    links=[]
    for result in SearchDict:
        titles.append(result['title'])
        descriptions.append(result['description'])
        links.append(result['link'])
        urls.append(result['raw_url'])
    # for result in SearchDict:
    # #   #if 'stackoverflow' in result["link"]:
    # #     print(
    # #     result["link"])/URL
    # #     print(result["title"])/Title
    # #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # #     print(result["description"])/Awnsers
    # #     print('#####################################################################################')  
    # #     print('------------------------------------------------------------------------------------')
    #         search_results.append({
    #         "Title": result["title"],
    #         #"Body": result.find_all("div", class_="excerpt")[0].text,
    #         #"Votes": int(result.find_all("span", class_="vote-count-post ")[0].find_all("strong")[0].text),
    #         "Answers": result["description"],
    #         "URL": result["link"]})
    return (titles,descriptions,links,urls)#list(SearchDict)


def GSearch(Error):
  url = 'https://google.com/search?q=' 
  site = ' site:stackoverflow.com'
  souper=ParseUrl(url+Error+site)
  def has_href_but_no_class(tag):
      return tag.has_attr('href') and not tag.has_attr('class')

  TitlesInTags =souper.select('div h3') 
  titles=[TitlesInTags[title].text for title in range(len(TitlesInTags))]

  LinksInTags=souper.find_all(has_href_but_no_class)

  format=re.compile(r'/(.*)?q=(.*)') 

  links=[]
  for link_href in LinksInTags:
      link = link_href['href']
      regex = format.search(link)
      try:
          if regex.group(1) in 'url?' and '.google.com/' not in regex.group(2):
              links.append(regex.group(2))
      except:
          pass
  #results=[]
  # for index in range(len(titles)):
  #     SearchDict ={}
  #     SearchDict['title']=titles[index]
  #     SearchDict['link']=links[index]
  #     results.append(SearchDict)
      #SearchDict['description']=descriptions[index]
  
  return (titles,links)    



def SoF (url):
  HtmlText= ParseUrl(url)
  QTitle = HtmlText.find_all('a', class_="question-hyperlink")[0].get_text()
  QStatus = HtmlText.find("div", attrs={"itemprop": "upvoteCount"}).get_text() # Vote count
  QStatus += " Votes | Asked " + HtmlText.find("time", attrs={"itemprop": "dateCreated"}).get_text() # Date created
  QDescription = StylizeCode(HtmlText.find_all("div", class_="s-prose js-post-body")[0]) # TODO: Handle duplicates

  answers = [StylizeCode(answer) for answer in HtmlText.find_all("div", class_="s-prose js-post-body")][1:]
  if len(answers) == 0:
      answers.append(("no answers", u"\nNo answers for this question."))

  return QTitle,QDescription,QStatus, answers




def ParseUrl(url):
    UAgent = UserAgent()
    global Connection
    """Turns a given URL into a BeautifulSoup object."""
    try:
        Response = requests.get(url, headers={"User-Agent": UAgent.random},timeout=10)
        if Response.status_code is not 200:
          sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold,"DeBuggy was unable to fetch results. "
                                            +Response.reason+"\n Try again Later.", end))
          Connection=False                                  
          sys.exit(1) 
    except requests.exceptions.RequestException:
        Connection=False
        sys.stdout.write("\n%s%s%s%s%s" % (red,underline,bold,"DeBuggy was unable to fetch results. "
                                            "Please make sure you are connected to the internet.\n", end))
        sys.exit(1)
    if "\.com/nocaptcha" in Response.url: # URL is a captcha page
        return None
    else:
        return bs4(Response.text, "html.parser")  

    # except Exception as e:
    #   print(e)




def UserConfirm(question):
      ValidInputs = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
      prompt = "[Y/n] "
      while True:
        print(reverse+cyan+bold+question+prompt,end,file=sys.stdout)
        UserChoice= input().lower()
        #for inputs in sys.stdin:
        #  UserChoice = input
        #  break
        #UserChoice=sys.stdin.read()
        if UserChoice in ValidInputs:
          return ValidInputs[UserChoice]
        #PrintColor = lambda x,y,z:cprint(x,y,z) 
        #text = colored("Please respond with 'yes' or 'no' (or 'y' or 'n').\n",'blue',attrs=['reverse','blink'])  
        #print(text)
        print(reverse+blue+"Please respond with 'yes' or 'no' (or 'y' or 'n').\n",end,file=sys.stdout)



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



def MonitorProcess():
  global ProcessState,ErrorMessage,ValidError
  ProcessState = execute()
  #clear terminal  
  with open(LogPath,'r') as log:
    ErrMessage = log.read()
    ValidError=print(red+bold+ErrMessage,file=sys.stdout) if CheckErrorMessage(ErrMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
    ErrorMessage = ErrMessage.split('\n')
  if ValidError:
    print(red+bold+ErrMessage,end,file=sys.stdout)
    DisplayResult = UserConfirm('DeBuggy Wants to Display Search Results?: ')
    if DisplayResult:
        ErrorMessage = ErrMessage.split('\n')
        #[print(i) for i in ErrorMessage]
        
        #return ErrorMessage 
    else:
      sys.exit(1)    
  else:
    sys.exit(1)
          

          #pickle_off=  open('cache','rb')    
          #emp=pickle.load(pickle_off) 


def CleanError():
  error = ErrorMessage[-2]#.split(':')
  ErrorLineno = int(ErrorMessage[1].split(',')[1].strip(' line'))
  error = error
  return (ErrorLineno,error)
  #get module name

## Main ##

def ParseSof():
    global qtitles,qdescriptions,qstatus,qanswers,trigger
    for link in links:
        QTitle,QDescription,QStatus,answers =SoF(link)
        qtitles.append(QTitle)
        qdescriptions.append(QDescription)
        qstatus.append(QStatus)
        qanswers.append(answers)
    trigger = True    


def FetchResult():#stdscr):
  global trigger,links,titles
  while True:
    if not ProcessState and ValidError:
      ErrorLineNumber,ErrMessage= CleanError()
      titles,links = GSearch(ErrMessage)
      if len(titles)==len(links) and len(titles)>0:
        print(red+bold+"Fetching Results, Please wait.",file=sys.stdout)  
        trigger=True
        #ParseSof()
        break
      # elif not Connection:
      #   break  
    time.sleep(0.1)

def FetchResultNoThread():
  global trigger,links,titles,descriptions,urls
  ErrorLineNumber,ErrMessage= CleanError()
  print(red+bold+"Fetching Results, Please wait...",end,file=sys.stdout)
  jj = GSearchNonThreaded(ErrMessage)
  if jj:
    titles,descriptions,links,urls = jj
    trigger=True
  #ParseSof()

      # elif not Connection:
      #   break  
      #time.sleep(0.1) 



def stylize_print(mypad,new_text,x):
    mypad.addstr("\n\n")
    for z in new_text:
        if type(z)==tuple:
           mypad.attron(curses.color_pair(4)|curses.A_BOLD)
           mypad.addstr(z[1])
           mypad.attroff(curses.color_pair(4)|curses.A_BOLD)
        else:
            mypad.attron(curses.color_pair(3))
            mypad.addstr(z)
            mypad.attroff(curses.color_pair(3))    
    divider = '*'*x
    divider = '\n\n'+divider
    mypad.attron(curses.color_pair(3))
    mypad.addstr(divider)  
    mypad.attroff(curses.color_pair(3))

def CreateWindow(stdscr,menu,idx,ans=False,des=False):
    global cache
    curses.mousemask(0)
    #buttom_menu(stdscr)
    y,x = stdscr.getmaxyx()

    ResultWindow = curses.newwin(y-3,x-6,1,4)
    ResultWindow.keypad(True)
    ResultWindow.clear()
    ResultWindow.immedok(True)
    ResultWindow.box()
    ResultWindow.border()
    buttom_menu(stdscr)
    rows, columns = ResultWindow.getmaxyx()
    top_menu =(menu[idx]).encode('utf-8').center(columns - 4)
    ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
    stdscr.addstr(rows//2,columns//2-len('Loading...')//2, "LOADING")
    
    if idx in cache.keys():
        QTitle,QDescription,QStatus,answers=cache[idx]
    else:
        QTitle,QDescription,QStatus,answers=SoF(links[idx])
        cache[idx]=(QTitle,QDescription,QStatus,answers)
    mypad = curses.newpad(10000,columns-3)
    mypad_pos =  0
    mypad_shift = 0
    mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
    divider = '*'*x
    if ans:        
        
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nANSWERS\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
        #mypad.addstr(divider)  
        mypad.attroff(curses.color_pair(3))

        answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
        [stylize_print(mypad,x,columns-4) for x in answer_text]
    elif des:
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nDESCRIPTION\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
        #mypad.addstr(divider)  
        mypad.attroff(curses.color_pair(3))
        description_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
        stylize_print(mypad,description_text,columns-4)
    
    while True:
        y,x = stdscr.getmaxyx()
        rows, columns = ResultWindow.getmaxyx()
        if mypad_pos==0:
           mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1) 
        top_menu = ("Line %d to %d of 10000 of %s" % (mypad_pos + 1, mypad_pos + rows,QTitle)).encode('utf-8').center(columns - 4)
        ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
        cmd = ResultWindow.getch()
        if  cmd == curses.KEY_DOWN:
            mypad_pos += 1
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
        elif cmd == curses.KEY_UP and mypad_pos!=0:
            mypad_pos -= 1
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
        elif cmd in [ord("q"),27,curses.KEY_LEFT]:
            break
        elif cmd == ord("b"):
            pass
            webbrowser.open_new(links[idx])
        elif cmd == ord('d'):
            mypad.clear()
            mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
            mypad.addstr('\nDESCRIPTION\n')
            mypad.addstr(QStatus)
            mypad.addstr('\n')
            mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
            #mypad.addstr(divider)  
            mypad.attroff(curses.color_pair(3))
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            new_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
            stylize_print(mypad,new_text,columns-4)
        elif cmd == ord('a'):
            mypad.clear()
            mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
            mypad.addstr('\nANSWERS')
            mypad.addstr(QStatus)
            mypad.addstr('\n')
            mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
            #mypad.addstr(divider)  
            mypad.attroff(curses.color_pair(3))
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
            [stylize_print(mypad,x,columns-4) for x in answer_text]
            #stylize_print(mypad,new_text,columns-4)
    curses.mousemask(1)




# def CreateWindow(stdscr,menu,idx):
#     global cache
#     buttom_menu(stdscr)
#     y,x = stdscr.getmaxyx()
#     ResultWindow = curses.newwin(y-3,x-6,1,4)
#     ResultWindow.keypad(True)
#     ResultWindow.clear()
#     ResultWindow.immedok(True)
#     ResultWindow.box()
#     ResultWindow.border()
#     curses.cbreak()
#     rows, columns = ResultWindow.getmaxyx()
#     out = stdscr.subwin(rows - 3, columns - 4, 3, 6)
#     out_rows, out_columns = out.getmaxyx()
#     out_rows -= 1
#     #stdscr.refresh()
#     line = 0
#     top_menu = (menu[idx]).encode('utf-8').center(columns - 4)
#     ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
#     out.clear()
#     out.addstr(out_rows//2,out_columns//2-len('Loading...')//2, "LOADING")
#     # while not trigger:
#     #     continue
#     lines = list(map(lambda x: x + " " * (out_columns - len(x)), reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in range(0, len(x), out_columns)] for x in menu])))

#     if idx in cache.keys():
#         QTitle,QDescription,QStatus,answers=cache[idx]
#     else:
#         QTitle,QDescription,QStatus,answers=SoF(links[idx])
#         cache[idx]=(QTitle,QDescription,QStatus,answers)
#     print(QDescription)



#     out.clear()
#     while True:  
#         out.addstr(0, 0, "".join(lines[line:line+out_rows]))
#         #stdscr.refresh()
#         out.refresh()
#         c = ResultWindow.getch()
#         if c in [ord("q"),27,curses.KEY_LEFT]:
#             break
#         elif c == ord("b"):
#              webbrowser.open_new(links[idx])
#         elif c == curses.KEY_DOWN:
#             if len(lines) - line > out_rows:
#                 line += 1
#         elif c == curses.KEY_UP:
#             if line > 0:
#                 line -= 1
#         elif c == curses.KEY_RIGHT:
#             if len(lines) - line >= 2 * out_rows:
#                 line += out_rows

def print_menu(stdscr,rw_idx,menu):
    h,w = stdscr.getmaxyx()
    len_menu = len(menu)
    max_y=h-3
    max_x = w-5
    new_text = False
    stdscr.clear()
    buttom_menu(stdscr)
    text_pad(stdscr)
    diff = 0
    men2 = menu.copy()
    if len_menu>max_y:
        if rw_idx>=max_y:
           diff = (rw_idx-max_y) +1  
           menu = menu[diff:max_y+diff]
        else:
            menu = menu[0:max_y]   
    for idx,row in enumerate(menu):
        idf=idx
        idx = idx+diff
        if len(men2[idx])>max_x:
            new_text= men2[idx][:max_x-3]+'...'
        else:
            new_text = False    
        x1 = 3 #divide by the lenght of each text that will be the start
        y1 = 1 +idf
        if idx == rw_idx:
            if new_text:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y1,x1,new_text.upper())
                stdscr.attroff(curses.color_pair(2))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y1,x1,row.upper())
                stdscr.attroff(curses.color_pair(2))    
        else:
             if new_text:
                stdscr.addstr(y1,x1,new_text.upper())
             else:        
                stdscr.addstr(y1,x1,row.upper())
    stdscr.refresh()

def text_pad(stdscr):
    h,w = stdscr.getmaxyx()
    box = [[0,2],[h-2,w-2]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    top_menu = ("DeBuggy").encode('utf-8').center(w - 5)
    stdscr.addstr(0, 3, top_menu, curses.A_REVERSE)

def buttom_menu(stdscr):
    h,w = stdscr.getmaxyx()
    bottom_menu = "(↓)Next(↑)Prev Line|(→)Next(←)Prev Page|(q)Quit|(esc)Back|(b)Browser|(d)Description|(a)Answers".encode('utf-8').center(w - 5)
    try:
        stdscr.addstr(h - 1, 3, bottom_menu, curses.A_REVERSE)
    except:
        stdscr.clear()
        stdscr.addstr(h - 1, 2,'...', curses.A_REVERSE)    

def App(stdscr): 
      menu=titles
      curses.curs_set(False)
      stdscr.immedok(True)
      stdscr.keypad(True)
      text_pad(stdscr)
      curses.mousemask(2)
      h,_ = stdscr.getmaxyx()
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
      curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
      current_row = 0   
      print_menu(stdscr,current_row,menu)
      while True:
           key = stdscr.getch()
           if key == curses.KEY_UP and current_row-1 is not -1:
               current_row-=1
               print_menu(stdscr,current_row,menu)
           elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
               current_row+=1
               print_menu(stdscr,current_row,menu)
           elif key in [10,13,curses.KEY_RIGHT,curses.KEY_ENTER]:
               CreateWindow(stdscr,menu,current_row,ans=True)
               print_menu(stdscr,current_row,menu)
           elif key == ord("q"):
             break         
           elif key == ord("b"):
             webbrowser.open_new(links[current_row])
           elif key == ord('d'):
               CreateWindow(stdscr,menu,current_row,des = True)
               print_menu(stdscr,current_row,menu)
           elif key==ord('a'):
               CreateWindow(stdscr,menu,current_row,ans=True)
               print_menu(stdscr,current_row,menu)     
           elif key == curses.KEY_MOUSE:
               _,x,y,_,_ = curses.getmouse()
               start_y = 1
               end_y = h-3
               if len(menu)> end_y:
                   continue
               else:
                   index = y-start_y
               try:
                 if y in range(start_y,end_y+1) and  x in range(3,len(menu[index])+5):
                    current_row=index
                    CreateWindow(stdscr,menu,current_row,ans=True)
                    print_menu(stdscr,current_row,menu)  
               except:
                   pass
                

if __name__=='__main__':
  #wrapper(App)
  OsName=os.name
  #LoadAnimation("starting your console application...")
  os.system('cls' if OsName=='nt' else 'clear')
  DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
  print(cyan+DebuggyAnimation,file=sys.stdout)
  print(green+bold+"Checking Running Script for Errors...",file=sys.stdout)
  ProcessId = int(sys.argv[1])
  LogPath = sys.argv[2]
  ProcessState,ValidError,trigger,Connection  = (True,False,False,True)
  links,titles,ErrorMessage,descriptions,url =(None,None,None,None,None)
  qtitles,qdescriptions,qanswers,qstatus=([],[],[],[])
  cache ={}
  # p1 = multiprocessing.Process(target=main, args=())
  # p1.start()
#   FetchResultThread = threading.Thread(target=FetchResult,args=())
#   FetchResultThread.daemon = True
#   FetchResultThread.start()
  while True:
    if not ProcessState:
      FetchResultNoThread() 
      if trigger:
        # trigger = False  
        # FetchResultThread = threading.Thread(target=ParseSof,args=())
        # FetchResultThread.daemon = True
        # FetchResultThread.start()
        wrapper(App)
        # _,_,_,answers=SoF(links[0])
        # for i in answers:
        #   print(i)
        #   break
        break
      elif not Connection:
        input(reverse+bold+red+"\nPress Enter To Exit ")
        break
    else:
      MonitorProcess()

  
  









       



