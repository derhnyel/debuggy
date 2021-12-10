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

