import sys
from psutil import Process,NoSuchProcess
import os
import pyfiglet
import linecache
import threading
#import multiprocessing
import requests
import webbrowser
from bs4 import BeautifulSoup as bs4 
import re
from fake_useragent import UserAgent
import curses
#from curses.textpad import Textbox,rectangle
from curses import wrapper
from curses import textpad
from functools import reduce
import pyperclip
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



def StylizeCode(Text,text=None,x=None,y=False):
    global export_code
    holder =[]
    """Identifies and stylizes code in a question or answer."""
    # TODO: Handle blockquotes and markdown
    if text is not None and text not in Text:
        try:
            width = (x-6)//2
            format = "="*width
            tex = "\n"+format +'ANSWER'+format+"\n"
            Text.insert(0,tex)#"================ANSWER==============\n")
            #Text.insert(-1,tex)#"\n==================ANSWER===============")
        except:
            Text.insert(0,"================ANSWER==============\n")
            #Text.insert(-1,"\n==================ANSWER===============")


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
                    if text is not None and text in Text :
                        
                        holder.append(u"\n%s" % str(child))  
                    elif text is not None and text not in Text and y!=0:
                        holder.append(u"\n%s" % str(child))   
                    StylizedText.append(("code", u"\n%s" % str(child)))
                    newline = False
                else: # In-line code
                    if text is not None and text in Text:
                        holder.append(u"\n%s" % str(child))  
                    elif text is not None and text not in Text and y!=0:
                        holder.append(u"\n%s" % str(child))   
                    StylizedText.append(("code", u"%s" % str(child)))
            else: # Plaintext
                newline = child.endswith('\n')   
                StylizedText.append(u"%s" % str(child))

    if type(StylizedText[-2]) == tuple:
        # Remove newline from questions/answers that end with a code block
        if StylizedText[-2][1].endswith('\n'):
            if text is not None and text in Text:
                holder.append(StylizedText[-2][1][:-1])  
            elif text is not None and text not in Text and y!=0:
                 holder.append(StylizedText[-2][1][:-1])
            StylizedText[-2] = ("code", StylizedText[-2][1][:-1])
    if text is not None and text in Text:
        holder.insert(0,'#**Verified Answer**\n')              
    export_code.append("".join(holder)) if holder!=[] and y!=0 else holder       
             

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

def get_comments(soup):

    comments_ = []
    raw_comments_ = soup.find_all("ul", class_="js-comments-list")
    for raw_comments in raw_comments_:
        comments_.append([str(index + 1) + ' ' + raw_comment.get_text() + '\n' for index, raw_comment in
                              enumerate(raw_comments.find_all("span", class_='comment-copy'))])
    if len(comments_) <= 1:
        comments_.append(["No comments as there are no answers to this question..."])
    return comments_[1::]

def add_urls(tags):
    images = tags.find_all("a")

    for image in images:
        if hasattr(image, "href"):
            image.string = "{} [{}]".format(image.text, image['href'])


def SoF (url,x=None):
  HtmlText= ParseUrl(url)
  QTitle = HtmlText.find_all('a', class_="question-hyperlink")[0].get_text()
  QStatus = HtmlText.find("div", attrs={"itemprop": "upvoteCount"}).get_text() # Vote count
  QStatus += " Votes | Asked " + HtmlText.find("time", attrs={"itemprop": "dateCreated"}).get_text() # Date created
  answers = [soup.get_text() for soup in HtmlText.find_all("div", class_="js-post-body")][
              1:]
#   try:
#         question_stats = (HtmlText.find_all("div", class_="js-vote-count")[0].get_text())
#         asked_info = HtmlText.find("time").parent.get_text()
#         active_info = HtmlText.find("time").parent.findNext('div').get_text()
#         viewed_info =HtmlText.find("time").parent.findNext('div').findNext('div').get_text()
#         #QStatus = "Votes " + question_stats + " | " + asked_info + " | " + active_info + " | " + viewed_info
#   except:
#         Status = "Could not load statistics."
  QDescription = StylizeCode(HtmlText.find_all("div", class_="s-prose js-post-body")[0]) # TODO: Handle duplicates
  try:
      accepted_answer  = HtmlText.find_all("div",class_="accepted-answer")[0].find_all("div",class_="js-post-body")[0]#.get_text()
  except:
      accepted_answer = None
      text='answers'
  else:    
    if accepted_answer in answers:
        answers.remove(accepted_answer)
    try:
        width = (x-15)//2
        format = "="*width
        text = "\n"+format +'ACCEPTED ANSWER'+format+"\n"
    except:
        text = "\n===============ACCEPTED ANSWER============"    
    accepted_answer.insert(0,text)
    #accepted_answer.insert(-1,text)
    answers.insert(0,accepted_answer)
  finally:
    answers = [StylizeCode(answer,text,x,y) for y,answer in enumerate(HtmlText.find_all("div", class_="s-prose js-post-body"))][1:]
    if len(answers) == 0:
        answers.append(("no answers", u"\nNo answers for this question."))
    comments = get_comments(HtmlText)
    #print(comments)
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

# def ParseSof():
#     global qtitles,qdescriptions,qstatus,qanswers,trigger
#     for link in links:
#         QTitle,QDescription,QStatus,answers =SoF(link)
#         qtitles.append(QTitle)
#         qdescriptions.append(QDescription)
#         qstatus.append(QStatus)
#         qanswers.append(answers)
#     trigger = True    


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
  global trigger,links,titles,descriptions,urls,ErrorLineNumber
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



def stylize_print(mypad,new_text,width,y=None):
    mypad.addstr("\n\n")
    for text in new_text:
        if type(text)==tuple:
           mypad.attron(curses.color_pair(4)|curses.A_BOLD)
           mypad.addstr(text[1])
           mypad.attroff(curses.color_pair(4)|curses.A_BOLD)
        else:
            mypad.attron(curses.color_pair(3))
            mypad.addstr(text)
            mypad.attroff(curses.color_pair(3)) 
    mypad.attron(curses.color_pair(3))        
    if y != None:
        divider = '*'*((width-len(str(y+1)))//2)
        divider = '\n\n'+divider+str(y+1)+divider
    else:
        divider = '*'*width
        divider = '\n\n'+divider
    mypad.addstr(divider)  
    mypad.attroff(curses.color_pair(3))


def CreateWindow(stdscr,menu,idx,ans=False,des=False):
    global cache
    curses.mousemask(-1)
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
    stdscr.addstr(rows//2,columns//2-len('Loading...')//2, "LOADING...")
    stdscr.refresh()
    
    if idx in cache.keys():
        QTitle,QDescription,QStatus,answers=cache[idx]
    else:
        QTitle,QDescription,QStatus,answers=SoF(links[idx],columns-4)
        cache[idx]=(QTitle,QDescription,QStatus,answers)
    answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
    new_text = list(filter(lambda x : False if x=='\n' else x, QDescription))    
    mypad = curses.newpad(10000,columns-3)
    mypad_pos =  0
    mypad_shift = 0
    mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
    move = 'down'
    ResultWindow.addstr(y-5,x-10,'↓↓↓')
    ResultWindow.addstr(1,x-10,'↑↑↑')      
    mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
    mypad.addstr('\nANSWERS\n')
    mypad.addstr(QStatus)
    mypad.addstr('\n')
    mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
    mypad.attroff(curses.color_pair(3))
    [stylize_print(mypad,x,columns-4,y) for y,x in enumerate(answer_text)]
    
    while True:
        stdscr.refresh() 
        y,x = stdscr.getmaxyx()
        rows, columns = ResultWindow.getmaxyx()
        if mypad_pos==0:
           mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1) 
        top_menu = ("Line %d to %d of 10000 of %s" % (mypad_pos + 1, mypad_pos + rows,QTitle)).encode('utf-8').center(columns - 4)
        ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
        cmd = ResultWindow.getch()
        if  cmd == curses.KEY_DOWN and mypad_pos!=10000:
            move='down'
            mypad_pos += 1
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
        elif cmd == curses.KEY_UP and mypad_pos!=0:
            move='up'
            mypad_pos -= 1
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
        
        elif cmd in [ord("q"),27,curses.KEY_BACKSPACE,127,8]:
            mypad.clear()
            ResultWindow.clear() 
            return ('title',idx)
        elif cmd == ord("b"):
            webbrowser.open_new(links[idx])
        # elif cmd == ord('d'):
        #     mypad.clear()
        #     mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        #     mypad.addstr('\nDESCRIPTION\n')
        #     mypad.addstr(QStatus)
        #     mypad.addstr('\n')
        #     mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
        #     #mypad.addstr(divider)  
        #     mypad.attroff(curses.color_pair(3))
        #     mypad_pos =  0
        #     mypad_shift = 0
        #     mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
        #     new_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
        #     stylize_print(mypad,new_text,columns-4)
        # elif cmd == ord('a'):
        #     mypad.clear()
        #     mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        #     mypad.addstr('\nANSWERS\n')
        #     mypad.addstr(QStatus)
        #     mypad.addstr('\n')
        #     mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
            #mypad.addstr(divider)  
            # mypad.attroff(curses.color_pair(3))
            # mypad_pos =  0
            # mypad_shift = 0
            # mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            # answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
            # [stylize_print(mypad,x,columns-4) for x in answer_text]
            #stylize_print(mypad,new_text,columns-4)
        elif cmd==curses.KEY_RIGHT and ans:
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
            stylize_print(mypad,new_text,columns-4)
            ans=False
            des=True
        elif cmd==curses.KEY_RIGHT and des:
            mypad.clear()
            mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
            mypad.addstr('\nANSWERS\n')
            mypad.addstr(QStatus)
            mypad.addstr('\n')
            mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
            #mypad.addstr(divider)  
            mypad.attroff(curses.color_pair(3))
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            [stylize_print(mypad,x,columns-4,y) for y,x in enumerate(answer_text)]
            ans=True
            des=False
        elif cmd==curses.KEY_LEFT and ans:
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
            stylize_print(mypad,new_text,columns-4)
            ans=False
            des=True
        elif cmd==curses.KEY_LEFT and des:
            mypad.clear()
            mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
            mypad.addstr('\nANSWERS\n')
            mypad.addstr(QStatus)
            mypad.addstr('\n')
            mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
            mypad.attroff(curses.color_pair(3))
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            [stylize_print(mypad,x,columns-4,y) for y,x in enumerate(answer_text)]
            ans=True
            des=False    
        elif cmd == ord('e'):
            mode = 'export'
            mypad.clear()
            ResultWindow.clear() 
            return (mode,idx)

            
        elif cmd == curses.KEY_MOUSE:
            _,w,h,_,_ = curses.getmouse()
            #ResultWindow.addstr(y-5,x-10,str(w)+str(h)) 
            if h in range(2,3) and  w in range(x-6,x-3) and mypad_pos!=0:
               mypad_pos -= 1
               move='up'
               mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
            if h in range(y-4,y-3) and  w in range(x-6,x-3):
               move = 'down' 
               mypad_pos += 1
               mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)   
            elif h==-1 and w==-1:
               if move =='down':   
                mypad_pos += 1
                mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)
               elif move =='up' and mypad_pos!=0:
                  mypad_pos -= 1
                  mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1)     
        
        

def print_menu(stdscr,rw_idx,menu,text):
    h,w = stdscr.getmaxyx()
    len_menu = len(menu)
    max_y=h-3
    max_x = w-5
    new_text = False
    stdscr.clear()
    buttom_menu(stdscr)
    text_pad(stdscr,text)
    diff = 0
    men2 = menu.copy()
    if len_menu>max_y:
        if rw_idx>=max_y:
           diff = (rw_idx-max_y) +1  
           menu = menu[diff:max_y+diff]
        else:
            menu = menu[0:max_y]   
    for idx,row in enumerate(menu):
        row = row.replace('\n',' ') 
        row = row.strip()   
        idf=idx
        idx = idx+diff
        if len(men2[idx])>max_x:
            new_text= men2[idx][:max_x-3]+'...'
            new_text = new_text.replace("\n"," ")
            new_text= new_text.strip()
        else:
            new_text = False    
        x1 = 3 
        y1 = 2 +idf
        if idx == rw_idx:
            if new_text:
                stdscr.attron(curses.color_pair(2)|curses.A_BOLD)
                stdscr.addstr(y1,x1,new_text.upper())
                oc= w-4
                val=oc-len(new_text)
                pos=len(new_text)+3
                #val= w-1-len(new_text)
                dic=' '*(val-1)
                stdscr.addstr(y1,pos,dic)
                stdscr.attroff(curses.color_pair(2)|curses.A_BOLD)
            else:
                stdscr.attron(curses.color_pair(2)|curses.A_BOLD)
                stdscr.addstr(y1,x1,row.upper())
                oc= w-4
                val=oc-len(row)
                pos=len(row)+3
                dic=' '*(val-1)
                stdscr.addstr(y1,pos,dic)
                stdscr.attroff(curses.color_pair(2)|curses.A_BOLD)    
        else:
             if new_text:
                stdscr.addstr(y1,x1,new_text.upper())
             else:     
                stdscr.addstr(y1,x1,row.upper())
    stdscr.refresh()

def text_pad(stdscr,text):
    h,w = stdscr.getmaxyx()
    box = [[0,2],[h-2,w-2]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    top_menu = (text).encode('utf-8').center(w - 5)
    stdscr.addstr(0, 3, top_menu, curses.A_REVERSE)

def buttom_menu(stdscr):
    h,w = stdscr.getmaxyx()
    bottom_menu = "(↓)Next(↑)Prev Line|(→)Next(←)Prev Page|(q)Quit|(esc,backspace)Back|(b)Open Browser".encode('utf-8').center(w - 5) #|(d)Description|(a)Answers
    try:
        stdscr.addstr(h - 1, 3, bottom_menu, curses.A_REVERSE)
    except:
        stdscr.clear()
        stdscr.addstr(h - 1, 2,'...', curses.A_REVERSE)    

def App(stdscr):
      mode = 'title'
      menu=titles 
      #curses.curs_set(False)
      #stdscr.immedok(True)
      stdscr.keypad(True)
      text_pad(stdscr,'Debuggy')
      curses.mousemask(2)
      h,_ = stdscr.getmaxyx()
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
      curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
      current_row = 0 
      curses.curs_set(False)
      text ='Debuggy'  
      while True:
        print_menu(stdscr,current_row,menu,text)
        key = stdscr.getch()    
        if mode == 'title' : 
           stdscr.refresh()
           if key == curses.KEY_UP and current_row-1 is not -1:
               current_row-=1
               print_menu(stdscr,current_row,menu,text)
           elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
               current_row+=1
               print_menu(stdscr,current_row,menu,text)
           elif key in [10,13,curses.KEY_RIGHT,curses.KEY_ENTER]:
               mode,idx = CreateWindow(stdscr,menu,current_row,ans=True)   
               if mode == 'export':
                    menu = export_code
                    current_row = 0
                    text = 'Debuggy >>> Select Code To Export'     
               #print_menu(stdscr,current_row,menu)
           elif key == ord("q"):
             break         
           elif key == ord("b"):
             webbrowser.open_new(links[current_row])    
           elif key == curses.KEY_MOUSE:
               _,x,y,_,_ = curses.getmouse()
               start_y = 2
               end_y = h-3
               if len(menu)> end_y:
                   continue
               else:
                   index = y-start_y
               try:
                 if y in range(start_y,end_y+1) and  x in range(3,len(menu[index])+5):
                    current_row=index
                    mode,idx = CreateWindow(stdscr,menu,current_row,ans=True)
                    if mode is 'export':
                        menu = export_code
                        current_row = 0
                        text = 'Debuggy >>> Select Code To Export'
                    #print_menu(stdscr,current_row,menu)  
               except:
                   pass
        elif mode=='export':
            if export_code !=[]: 
                #print_menu(stdscr,current_row,menu)
                stdscr.refresh()
                #key = stdscr.getch()
                if key == curses.KEY_UP and current_row-1 is not -1:
                    current_row-=1
                    print_menu(stdscr,current_row,menu,text)
                elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
                    current_row+=1
                    print_menu(stdscr,current_row,menu,text)
                # elif key in [10,13,curses.KEY_RIGHT,curses.KEY_ENTER]:
                #     mode = CreateWindow(stdscr,menu,current_row,ans=True)
                #     if mode is not None:
                #         current_row = 0
                    #print_menu(stdscr,current_row,menu)
                elif key in [ord("q"),27,curses.KEY_BACKSPACE,127,8,curses.KEY_LEFT]:
                    stdscr.clear()
                    menu=titles
                    print_menu(stdscr,idx,menu,text)
                    mode,idx = CreateWindow(stdscr,menu,idx,ans=True)
                    if mode == 'title':
                        stdscr.clear()
                        current_row = idx 
                        menu=titles
                        text = 'Debuggy'
                elif key == ord("b"):
                    webbrowser.open_new(links[current_row])    
                elif key == curses.KEY_MOUSE:
                    _,x,y,_,_ = curses.getmouse()
                    start_y = 2
                    end_y = h-3
                    if len(menu)> end_y:
                        continue
                    else:
                        index = y-start_y
                    try:
                        if y in range(start_y,end_y+1) and  x in range(3,len(menu[index])+5):
                            current_row=index
                            text = 'Debuggy' 
                            mode = CreateWindow(stdscr,menu,current_row,ans=True)
                            if mode is not None:
                                current_row = 0
                            #print_menu(stdscr,current_row,menu)  
                    except:
                        pass
            else:
                stdscr.addstr(y//2,x//2-len("No Codes To Export From Awnsers")//2, "No Codes To Export From Awnsers")
                key = stdscr.getch() 
                if key in [ord("q"),27,curses.KEY_BACKSPACE,127,8]:
                    current_row = idx 
                    menu=titles
                    mode,idx = CreateWindow(stdscr,menu,idx,ans=True)
                       
            
                 
#def _get_caller_script():
        #open caller script
        #print(_get_caller_path().filename)
        
        
        #frame_stack = inspect.stack()
        #print(frame_stack)
        #script.pop(3)
        #script.insert(3,'dsmds')
        #print(script)
       # return script

def replace_text():
    #script = _get_caller_script()
    script = linecache.getlines(filename)
    print(script[ErrorLineNumber-1])

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
  filename = sys.argv[3]
  ProcessState,ValidError,trigger,Connection  = (True,False,False,True)
  links,titles,ErrorMessage,descriptions,url,ErrorLineNumber=(None,None,None,None,None,None)
  qtitles,qdescriptions,qanswers,qstatus,export_code=([],[],[],[],[])
  #replacement=[]
  #dict_={}
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
        #print(replacement)

        # _,_,_,answers=SoF(links[0])
        # for i in answers:
        #   print(i)
        #   break
        break
      elif not Connection:
        input(reverse+bold+red+"\nPress Enter To Exit ")
        break
    else:
      MonitorProcess()#it now outputs a return


#return ('title',idx)

             
    #curses.mousemask(1)




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
#                 line += out_row

#New way to search Google 

#   def get_questions_for_query_google(query, count=10):
#     """
#     Fetch questions for a query using Google search.
#     Returned question urls are URLS to SO homepage.
#     At most 10 questions are returned. (Can be altered by passing count)
#     :param query: User-entered query string
#     :return: list of [ (question_text, question_description, question_url) ]
#     """
#     i = 0
#     questions = []
#     random_headers()
#     search_results = requests.get(google_search_url + query, headers=header)
#     captcha_check(search_results.url)
#     soup = BeautifulSoup(search_results.text, 'html.parser')
#     try:
#         soup.find_all("div", class_="g")[0]  # For explicitly raising exception
#     except IndexError:
#         socli.printer.print_warning("No results found...")
#         sys.exit(0)
#     for result in soup.find_all("div", class_="g"):
#         if i == count:
#             break
#         try:
#             question_title = result.find("h3").get_text().replace(' - Stack Overflow', '')
#             # Instant answers will raise IndexError here
#             question_desc = result.find("div", recursive=False).find("div", recursive=False) \
#                 .findAll("div", recursive=False)[1].findAll("div", recursive=False)[1] \
#                 .getText()

#             question_url = result.find("a").get("href")  # Retrieves the Stack Overflow link
#             question_url = fix_google_url(question_url.lower())
#             if question_url is None:
#                 i = i - 1
#                 continue

#             questions.append([question_title, question_desc, question_url])
#             i += 1
#         except (NameError, AttributeError, IndexError):
#             continue

#     # Check if there are any valid question posts
#     if not questions:
#         socli.printer.print_warning("No results found...")
#         sys.exit(0)
#     return questions
  

# def get_question_stats_and_answer_and_comments(url):
#     """
#     Fetch the content of a StackOverflow page for a particular question.
#     :param url: full url of a StackOverflow question
#     :return: tuple of ( question_title, question_desc, question_stats, answers, comments, dup_url )
#     """
#     random_headers()
#     res_page = requests.get(url, headers=header)
#     captcha_check(res_page.url)
#     soup = BeautifulSoup(res_page.text, 'html.parser')
#     dup_url = None
#     question_title, question_desc, question_stats, dup_url = get_stats(soup)
#     answers = [s.get_text() for s in soup.find_all("div", class_="js-post-body")][
#               1:]  # first post is question, discard it.
#     accepted_answer  = soup.find_all("div",class_="accepted-answer")[0].find_all("div",class_="js-post-body")[0].get_text()
#     if accepted_answer in answers:
#         answers.remove(accepted_answer)
#     accepted_answer = "=============ACCEPTED_ANSWER===========\n" + accepted_answer + "\n===============ACCEPTED_ANSWER============"
#     answers.insert(0,accepted_answer)
#     comments = get_comments(soup)
#     if len(answers) == 0:
#         answers.append('No answers for this question ...')
#     return question_title, question_desc, question_stats, answers, comments, dup_url




#   def get_stats(soup):
#     """
#     Get Question stats
#     :param soup:
#     :return: tuple of (question_title, question_desc, question_stats, dup_url)
#     """
#     question_title = (soup.find_all("a", class_="question-hyperlink")[0].get_text())
#     question_stats = (soup.find_all("div", class_="js-vote-count")[0].get_text())
#     dup_url = None
#     try:

#         asked_info = soup.find("time").parent.get_text()
#         active_info = soup.find("time").parent.findNext('div').get_text()
#         viewed_info = soup.find("time").parent.findNext('div').findNext('div').get_text()
#         question_stats = "Votes " + question_stats + " | " + asked_info + " | " + active_info + " | " + viewed_info
#     except:
#         question_stats = "Could not load statistics."
#     question_desc = (soup.find_all("div", class_="js-post-body")[0])
#     if '[duplicate]' in question_title:
#         dup_answer = (soup.find_all("div", class_="js-post-body")[0])
#         link = dup_answer.find('a')['href']
#         link = so_url + link
#         dup_url = copy.deepcopy(link)
#         # using deepcopy else after the decompose of the first div, the url will be lost.
#         question_desc.find('div').decompose()
#     add_urls(question_desc)
#     question_desc = question_desc.get_text()
#     question_stats = ' '.join(question_stats.split())
#     return question_title, question_desc, question_stats, dup_url









       



