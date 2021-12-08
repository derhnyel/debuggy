import curses
import webbrowser
from curses import wrapper
from curses import textpad
from stalkoverflow import parsers   
from stalkoverflow.color import *


links=None
titles=None
cache = {}
"""Function to stylize texts and codes for printing"""
def stylize_print(mypad,new_text,width):
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
    divider = '*'*width
    divider = '\n\n'+divider
    mypad.attron(curses.color_pair(3))
    mypad.addstr(divider)  
    mypad.attroff(curses.color_pair(3))

def style_answers(mypad,answers,QStatus,columns):
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nANSWERS\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE) 
        mypad.attroff(curses.color_pair(3))

        answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
        [stylize_print(mypad,x,columns-4) for x in answer_text]

def style_description(mypad,QDescription,QStatus,columns):
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nDESCRIPTION\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
        mypad.attroff(curses.color_pair(3))
        description_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
        stylize_print(mypad,description_text,columns-4)        

def create_window(stdscr,menu,idx,ans=False,desc=False):
    global cache
    curses.mousemask(0)
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
    stdscr.addstr(rows//2,columns//2-len('Loading')//2, "LOADING...")
    
    if idx in cache.keys():
        QTitle,QDescription,QStatus,answers=cache[idx]
    else:
        QTitle,QDescription,QStatus,answers = parsers.StackOverflow(links[idx])
        cache[idx]=(QTitle,QDescription,QStatus,answers)
    mypad = curses.newpad(10000,columns-3)
    mypad_pos =  0
    mypad_shift = 0
    mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
    if ans:        
       style_answers(mypad, answers, QStatus, columns)
        
    elif desc:
       style_description((mypad, QDescription, QStatus, columns))
    
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
            mypad_pos =  0
            mypad_shift = 0
            style_description(mypad, QDescription, QStatus, columns)
        elif cmd == ord('a'):
            mypad.clear()
            mypad_pos =  0
            mypad_shift = 0
            style_answers(mypad, answers, QStatus, columns)
        elif cmd==curses.KEY_RIGHT and ans:
            mypad.clear()
            ans=False
            desc=True
            mypad_pos =  0
            mypad_shift = 0
            style_description(mypad, QDescription, QStatus, columns) 
        elif cmd==curses.KEY_RIGHT and desc:
            mypad.clear()
            mypad_pos =  0
            mypad_shift = 0
            ans=True
            desc=False
            style_answers(mypad, answers, QStatus, columns)                 
    curses.mousemask(1)



def print_menu(stdscr,rw_idx,menu):
    def select_spaces(text):
        stdscr.attron(curses.color_pair(2)|curses.A_BOLD)
        stdscr.addstr(y1,x1,text.upper())
        oc= w-4
        val=oc-len(text)
        pos=len(text)+3
        spaces=' '*(val-1)
        stdscr.addstr(y1,pos,spaces)
        stdscr.attroff(curses.color_pair(2)|curses.A_BOLD)
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
        x1,y1 =(3,2 +idf)
        if idx == rw_idx:
            if new_text:
                select_spaces(new_text)
            else:
               select_spaces(row)    
        else:
             if new_text:
                stdscr.addstr(y1,x1,new_text.upper())
             else:        
                stdscr.addstr(y1,x1,row.upper())
    stdscr.refresh()

'''Creating textpad with rectangle to print menu on '''
def text_pad(stdscr):
    h,w = stdscr.getmaxyx()
    box = [[0,2],[h-2,w-2]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    top_menu = ("DeBuggy").encode('utf-8').center(w - 5)
    stdscr.addstr(0, 3, top_menu, curses.A_REVERSE)

#Stalk overflow

'''Print Buttom Menu'''
def buttom_menu(stdscr):
    h,w = stdscr.getmaxyx()
    bottom_menu = "(↓)Next(↑)Prev Line|(→)Next(←)Prev Page|(q)Quit|(esc)Back|(b)Browser|(d)Description|(a)Answers".encode('utf-8').center(w - 5)
    try:
        stdscr.addstr(h - 1, 3, bottom_menu, curses.A_REVERSE)
    except:
        stdscr.clear()
        stdscr.addstr(h - 1, 2,'...', curses.A_REVERSE)    

def main_window(stdscr): 
      menu=titles
      curses.curs_set(False)
      stdscr.immedok(True)
      stdscr.keypad(True)
      text_pad(stdscr)
      curses.mousemask(2)
      h,_ = stdscr.getmaxyx()
      curses_default_color(stdscr)
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
               create_window(stdscr,menu,current_row,ans=True)
               print_menu(stdscr,current_row,menu)
           elif key == ord("q"):
             break         
           elif key == ord("b"):
             webbrowser.open_new(links[current_row])
           elif key == ord('d'):
               create_window(stdscr,menu,current_row,desc = True)
               print_menu(stdscr,current_row,menu)
           elif key==ord('a'):
               create_window(stdscr,menu,current_row,ans=True)
               print_menu(stdscr,current_row,menu)     
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
                    create_window(stdscr,menu,current_row,ans=True)
                    print_menu(stdscr,current_row,menu)  
               except:
                   pass

def start_app(lnks,ttls):
    global links,titles
    links,titles = lnks,ttls
    wrapper(main_window)


































# text = '\n# Saves the XKCD comic page for offline read\n\nimport requests, os, bs4, shutil\n\nurl = \'http://xkcd.com/\'\n\nif os.path.isdir(\'xkcd\') == True: # If xkcd folder already exists\n    shutil.rmtree(\'xkcd\') #delete it\nelse: # otherwise\n    os.makedirs(\'xkcd\') # Creates xkcd foulder.\n\n\nwhile not url.endswith(\'#\'): # If there are no more posts, it url will endswith #, exist while loop\n    # Download the page\n    print \'Downloading %s page...\' % url\n    res = requests.get(url) # Get the page\n    res.raise_for_status() # Check for errors\n\n    soup = bs4.BeautifulSoup(res.text) # Dowload the page\n    # Find the URL of the comic im age\n    comicElem = soup.select(\'#comic img\') # Any #comic img it finds will be saved as a list in comicElem \n    if comicElem == []: # if the list is empty\n        print \'Couldn\\\'t find the image!\'\n    else:\n      comicUrl = comicElem[0].get(\'src\') # Get the first index in comicElem (the image) and save to\n        #comicUrl\n\n        # Download the image\n        print \'Downloading the %s image...\' % (comicUrl)\nres = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n        res.raise_for_status() # Check for errors\n\n        # Save image to ./xkcd\n        imageFile = open(os.path.join(\'xkcd\', os.path.basename(comicUrl)), \'wb\')\n        for chunk in res.iter_content(10000):\n            imageFile.write(chunk)\n        imageFile.close()\n    # Get the Prev btn\'s URL\n    prevLink = soup.select(\'a[rel="prev"]\')[0]\n    # The Previous button is first <a rel="prev" href="/1535/" accesskey="p">&lt; Prev</a>\n    url = \'http://xkcd.com/\' + prevLink.get(\'href\')\n    # adds /1535/ to http://xkcd.com/\n\nprint \'Done!\'\n'


# description=[
# '\n',"I'm learning Python by following Automate the Boring Stuff. This program is supposed to go to ",'http://xkcd.com/', ' and download all the images for offline viewing. ', 
# '\n', "I'm on version 2.7 and Mac. ", 
# '\n', 'For some reason, I\'m getting errors like "No schema supplied" and errors with using request.get() itself. ', 
# '\n', 'Here is my code:', 
# '\n', ('code', '\n# Saves the XKCD comic page for offline read\n\nimport requests, os, bs4, shutil\n\nurl = \'http://xkcd.com/\'\n\nif os.path.isdir(\'xkcd\') == True: # If xkcd folder already exists\n    shutil.rmtree(\'xkcd\') # delete it\nelse: # otherwise\n    os.makedirs(\'xkcd\') # Creates xkcd foulder.\n\n\nwhile not url.endswith(\'#\'): # If there are no more posts, it url will endswith #, exist while loop\n    # Download the page\n    print \'Downloading %s page...\' % url\n    res = requests.get(url) # Get the page\n    res.raise_for_status() # Check for errors\n\n    soup = bs4.BeautifulSoup(res.text) # Dowload the page\n    # Find the URL of the comic image\n    comicElem = soup.select(\'#comic img\') # Any #comic img it finds will be saved as a list in comicElem\n    if comicElem == []: # if the list is empty\n        print \'Couldn\\\'t find the image!\'\n    else:\n        comicUrl = comicElem[0].get(\'src\') # Get the first index in comicElem (the image) and save to\n        # comicUrl\n\n        # Download the image\n        print \'Downloading the %s image...\' % (comicUrl)\n        res = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n        res.raise_for_status() # Check for errors\n\n        # Save image to ./xkcd\n        imageFile = open(os.path.join(\'xkcd\', os.path.basename(comicUrl)), \'wb\')\n        for chunk in res.iter_content(10000):\n            imageFile.write(chunk)\n        imageFile.close()\n    # Get the Prev btn\'s URL\n    prevLink = soup.select(\'a[rel="prev"]\')[0]\n    # The Previous button is first <a rel="prev" href="/1535/" accesskey="p">&lt; Prev</a>\n    url = \'http://xkcd.com/\' + prevLink.get(\'href\')\n    # adds /1535/ to http://xkcd.com/\n\nprint \'Done!\'\n'),
# '\n', 'Here are the errors:', 
# '\n', ('code', '\nTraceback (most recent call last):\n  File "/Users/XKCD.py", line 30, in <module>\n    res = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n  File "/Library/Python/2.7/site-packages/requests/api.py", line 69, in get\n    return request(\'get\', url, params=params, **kwargs)\n  File "/Library/Python/2.7/site-packages/requests/api.py", line 50, in request\n    response = session.request(method=method, url=url, **kwargs)\n  File "/Library/Python/2.7/site-packages/requests/sessions.py", line 451, in request\n    prep = self.prepare_request(req)\n  File "/Library/Python/2.7/site-packages/requests/sessions.py", line 382, in prepare_request\n    hooks=merge_hooks(request.hooks, self.hooks),\n  File "/Library/Python/2.7/site-packages/requests/models.py", line 304, in prepare\n    self.prepare_url(url, params)\n  File "/Library/Python/2.7/site-packages/requests/models.py", line 362, in prepare_url\n    to_native_string(url, \'utf8\')))\nrequests.exceptions.MissingSchema: Invalid URL \'//imgs.xkcd.com/comics/the_martian.png\': No schema supplied. Perhaps you meant http:////imgs.xkcd.com/comics/the_martian.png?\n'), 
# '\n', "The thing is I've been reading the section in the book about the program multiple times, reading the Requests doc, as well as looking at other questions on here. My syntax looks right. ",
# '\n', 'Thanks for your help!', '\n', 'Edit: ', '\n', "This didn't work: ", 
# '\n',('code', '\ncomicUrl = ("http:"+comicElem[0].get(\'src\')) \n'),
# '\n', 'I thought adding the http: before would get rid of the no schema supplied error. ', '\n'] 
# regex=re.compile(r'(\n\n+)')
# spaces  =0
# k = text.split("\n")



# def text_spaces(text):
#              spaces = 0
#              #global spaces
#          #for l in text:
#              if type(text) is tuple:
#                 text = text[1]
#              matches = regex.finditer(text)
#              for i in matches:
#                  result = i.groups()
#                  if result[0]=='\n\n':
#                      spaces+=1
#                  elif result[0]=='\n\n\n':
#                      spaces+=2
#                  else:
#                      spaces+=0
#              return spaces


# #spaces = sum(list(text_spaces(x) for x in description))
# new_text = list(filter(lambda x : False if x=='\n' else x, description))

# #print(len(text))
# # def remove_new_line(text,divider):
# #     #new_list=[]    
# #     #for i in description:
# #         if type(i) is tuple:
# #             p= i[1].lstrip('\n')
# #             new_list.append(p)
# #         elif i =='\n': 
# #             pass        
# #         else:
# #             new_list.append(i)
# #     new_list.append(divider)

# max_scroll = len(k)+spaces+20
# #print(k)
# print(len(k))
# print(len(description))
# print(len(new_text))






# def main(stdscr):
#     curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
#     curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
#     curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
#     curses.init_pair(4,curses.COLOR_RED,curses.COLOR_YELLOW)
#     mypad_pos = 0
#     y,x =stdscr.getmaxyx() 
#     mypad = curses.newpad(len(text),x)
#     #print(x)
#     #new_pad= []
#     for z in new_text:
#         if type(z)==tuple:
#            mypad.attron(curses.color_pair(4)|curses.A_BOLD)
#            mypad.addstr(z[1])
#            mypad.attroff(curses.color_pair(4)|curses.A_BOLD)
#         else:
#             mypad.attron(curses.color_pair(3))
#             mypad.addstr(z)
#             mypad.attroff(curses.color_pair(3))
    
#     divider = '*'*x
#     divider = '\n\n'+divider
#     mypad.attron(curses.color_pair(3))
#     mypad.addstr(divider)  
#     mypad.attroff(curses.color_pair(3))      
#         # for i,j in enumerate(k):
#     #     try:
#     #         mypad.addstr(j)
#     #         mypad.addstr("\n")
#     #     except:
#     #         st+=1
#     #         new_pad = text[st:i+st]
#     #         break
#     #print(''.join(new_pad)) 
#     #         
#     mypadshift = 0
#     mypad.refresh(mypad_pos, 0, 0, 0,y-1,x-1)
#     #stdscr.refresh()        
#     while True:
#         #print(mypad_pos)
#         #mypad.refresh(1, 0, 0, 0,y-1,x-1)
#         cmd = stdscr.getch()
#         if  cmd == curses.KEY_DOWN:
#             mypad_pos += 1
#             mypad.refresh(mypad_pos, mypadshift, 0, 0, y-1, x-1)
#         elif cmd == curses.KEY_UP and mypad_pos!=0:
#             mypad_pos -= 1
#             mypad.refresh(mypad_pos, mypadshift, 0, 0, y-1, x-1)
#         #elif cmd==curses.KEY_LEFT:
#         #    mypadshift-=1
#         #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)
#         #elif cmd == curses.KEY_RIGHT:    
#         #    mypadshift+=1
#         #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)
#         elif cmd == ord('q'):
#             break  


# curses.wrapper(main)        