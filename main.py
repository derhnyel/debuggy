import sys
from psutil import Process,NoSuchProcess
import os
import pyfiglet
import threading
#import multiprocessing
import requests
#import urwid
#import webbrowser
#from urwid.widget import (BOX, FLOW, FIXED)
from bs4 import BeautifulSoup as bs4 
import re
from fake_useragent import UserAgent
import curses
#from curses.textpad import Textbox,rectangle
from curses import wrapper
#import argparse
#import asyncio
#import pickle
import time

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
#end = '\033[0m'
end =''



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
    from search_engine_parser.core.engines.google import Search as GoogleSearch
    Error+=' site:stackoverflow.com'
    #search_results=[]
    gs = GoogleSearch()
    SearchArgs=(Error,1)
    #try:
    SearchDict=gs.search(*SearchArgs)
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
    return SearchDict#list(SearchDict)


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
        Response = requests.get(url, headers={"User-Agent": UAgent.random})
        if Response.status_code is not 200:
          sys.stdout.write("\n%s%s%s" % (red, "DeBuggy was unable to fetch results. "
                                            +Response.reason+"\n Try again Later.", end))
          Connection=False                                  
          sys.exit(1) 
    except requests.exceptions.RequestException:
        Connection=False
        sys.stdout.write("\n%s%s%s" % (red, "DeBuggy was unable to fetch results. "
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
        print(reverse+cyan+bold+question+prompt+end,file=sys.stdout)
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



def MonitorProcess():
  global ProcessState,ErrorMessage,ValidError
  ProcessState = execute()
  #clear terminal  
  with open('log.err','r') as log:
    ErrMessage = log.read()
    ValidError=print(red+bold+ErrMessage,file=sys.stdout) if CheckErrorMessage(ErrMessage) is False else True
    #print to terminal and capture input while results are being fetched and cached
    ErrorMessage = ErrMessage.split('\n')
  if ValidError:
    print(red+bold+ErrMessage,file=sys.stdout)
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





def FetchResult():#stdscr):
  global trigger,links,titles
  while True:
    if not ProcessState and ValidError:
      ErrorLineNumber,ErrMessage= CleanError()
      titles,links = GSearch(ErrMessage)
      if len(titles)==len(links) and len(titles)>0:
        print(red+bold+"Fetching Results, Please wait.",file=sys.stdout)  
        trigger=True
        break
      # elif not Connection:
      #   break  
    time.sleep(0.1)

def FetchResultNoThread():
  global trigger,links,titles,SefObject
  ErrorLineNumber,ErrMessage= CleanError()
  print(red+bold+"Fetching Results, Please wait.",file=sys.stdout)
  SefObject = GSearchNonThreaded(ErrMessage)
  trigger=True

      # elif not Connection:
      #   break  
      #time.sleep(0.1) 

def CreateWindow(stdscr,text):
      panel(stdscr)
      y,x = stdscr.getmaxyx()
      y1=round(y/5)
      x1=round(x/5)
      ResultWindow = curses.newwin(3*y1,3*x1,y1,x1)
      ResultWindow.refresh()
      ResultWindow.box()
      ResultWindow.move(1,1)
      ResultWindow.addstr(text)
      ResultWindow.refresh()
      ResultWindow.getch()
      curses.endwin()
      #panel = curses.panel.new_panel(stdscr)
def print_menu(stdscr,rw_idx,menu):
    stdscr.clear()
    panel(stdscr)
    y,x = stdscr.getmaxyx()
    for idx,row in enumerate(menu):
        x1 = 1 #divide by the lenght of each text that will be the start
        y1 = round(y/len(menu) + idx + 2)
        if idx == rw_idx:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y1,x1,row.upper())
            stdscr.attroff(curses.color_pair(2))
        else:    
            stdscr.addstr(y1,x1,row.upper())
    stdscr.refresh()

def panel(stdscr):
    y,x = stdscr.getmaxyx()
    PanelWindow = curses.newwin(3,x-1,0,1)
    PanelWindow.box()
    PanelWindow.refresh()
    PanelWindow.move(1,1)
    PanelWindow.addstr('Reserved Panel')
    PanelWindow.refresh()
    
    #PanelWindow.getch()

def App(stdscr):
      #print(SResult)
      menu = [result['title'] for result in SefObject]
      descriptions =  [result['description'] for result in SefObject]
      links= [result['link'] for result in SefObject]
      url= [result['raw_url'] for result in SefObject]
      #menu=["Boy",'girl','games','last','emememememememem','exitttttttt','nowwwwwwwwwwww']
      curses.curs_set(False)
      stdscr.immedok(True)
      stdscr.keypad(True)
      

    # for result in links:
    #   QTitle,QDescription,QStatus, answers=SoF(result)
    #   #   menu.append(result["title"])
    #color pair init with i d,foreground,backgroud 
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_YELLOW)
      curses.init_pair(4,curses.COLOR_RED,curses.COLOR_YELLOW)
      #height,width of windows(size of the windows),start(shifts down as value increases) and end(shift left as value increases) position
      current_row = 0   
      print_menu(stdscr,current_row,menu)
      panel(stdscr)
      while True:
          
           key = stdscr.getch()
           stdscr.clear()
           if key == curses.KEY_UP:
               print_menu(stdscr,current_row-1 if current_row-1 is not -1 else current_row,menu)
               if current_row-1 is not -1:
                   current_row-=1
           elif key == curses.KEY_DOWN:
               print_menu(stdscr,current_row+1 if current_row+1 is not len(menu) else current_row,menu)
               if current_row+1 is not len(menu):
                   current_row+=1
           elif key == curses.KEY_ENTER or key in [10,13]:
               if current_row==len(menu)-1:
                   break
               print_menu(stdscr,current_row,menu) 
               CreateWindow(stdscr,descriptions[current_row]) 
               #stdscr.getch()
           print_menu(stdscr,current_row,menu)
      stdscr.refresh()            
                    
    
      #stdscr.addstr(y,x,'home')

if __name__=='__main__':
  #wrapper(App)
  OsName=os.name
  #LoadAnimation("starting your console application...")
  os.system('cls' if OsName=='nt' else 'clear')
  DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
  print(cyan+DebuggyAnimation,file=sys.stdout)
  print(green+bold+"Checking Running Script for Errors...",file=sys.stdout)
  ProcessId = int(sys.argv[1])
  ProcessState,ValidError,trigger,Connection  = (True,False,False,True)
  links,titles,ErrorMessage,SefObject =(None,None,None,None)
  # p1 = multiprocessing.Process(target=main, args=())
  # p1.start()
#   FetchResultThread = threading.Thread(target=FetchResult,args=())
#   FetchResultThread.daemon = True
#   FetchResultThread.start()
  while True:
    if not ProcessState:
      FetchResultNoThread () 
      if trigger:
        wrapper(App)
        break
      elif not Connection:
        input("\nPress Enter To Exit.")
        break
    else:
      MonitorProcess()

  
  









       



