import curses
from curses import wrapper
from curses import textpad
from stalkoverflow import parsers   
from stalkoverflow.color import *
import linecache
from stalkoverflow import editor_tui

links=None
titles=None
filename = None
eln = None
codes_to_export =[]
cache = {}






def stylize_print(mypad,new_text,width):
    """Function to stylize texts and codes for printing"""
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

def style_answers(mypad,answer_text,QStatus,columns):
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nANSWERS\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE) 
        mypad.attroff(curses.color_pair(3))
        [stylize_print(mypad,x,columns-4) for x in answer_text]

def style_description(mypad,description_text,QStatus,columns):
        mypad.attron(curses.color_pair(3)|curses.A_BOLD|curses.A_UNDERLINE)
        mypad.addstr('\nDESCRIPTION\n')
        mypad.addstr(QStatus)
        mypad.addstr('\n')
        mypad.attroff(curses.A_BOLD|curses.A_UNDERLINE)
        mypad.attroff(curses.color_pair(3))
        stylize_print(mypad,description_text,columns-4)        

def create_window(stdscr,menu,idx,ans=False,desc=False):
    global cache,codes_to_export
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
    stdscr.addstr(rows//2,columns//2-len('Loading')//2, "LOADING...")
    stdscr.refresh()
    
    if idx in cache.keys():
        QTitle,QDescription,QStatus,answers,codes_to_export=cache[idx]
        result=(QTitle,QDescription,QStatus,answers,codes_to_export)
    else:
        result = parsers.StackOverflow(links[idx],columns-4)
    
    try:
        QTitle,QDescription,QStatus,answers,codes_to_export = result
        cache[idx]=(QTitle,QDescription,QStatus,answers,codes_to_export)
    except:
        stdscr.addstr(rows//2,columns//2-len(result)//2, result)
        while True:
            stdscr.refresh()
            cmd = stdscr.getch()
            if cmd in [ord("q"),27,curses.KEY_BACKSPACE,127,8]:
                return ('title',idx)

    else:
        answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in answers]
        description_text = list(filter(lambda x : False if x=='\n' else x, QDescription))    
        mypad = curses.newpad(10000,columns-3)
        mypad_pos =  0
        mypad_shift = 0
        move = 'down'
        mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
        ResultWindow.addstr(y-5,x-10,'↓↓↓')
        ResultWindow.addstr(1,x-10,'↑↑↑')      
        style_answers(mypad, answer_text, QStatus, columns)
                
        while True:
            stdscr.refresh() 
            y,x = stdscr.getmaxyx()
            rows, columns = ResultWindow.getmaxyx()
            if mypad_pos==0 :
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
                import webbrowser
                webbrowser.open_new(links[idx])

            elif cmd in[curses.KEY_RIGHT, curses.KEY_LEFT] and ans:
                mypad.clear()
                ans=False
                desc=True
                mypad_pos =  0
                mypad_shift = 0
                style_description(mypad, description_text, QStatus, columns) 
            
            elif cmd in[curses.KEY_RIGHT, curses.KEY_LEFT] and desc:
                mypad.clear()
                mypad_pos =  0
                mypad_shift = 0
                ans=True
                desc=False
                style_answers(mypad, answer_text, QStatus, columns)
            elif cmd == ord('e'):
                mode = 'export' 
                return (mode,idx)
            elif cmd == curses.KEY_MOUSE:
                _,w,h,_,_ = curses.getmouse()
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
        idf = idx
        idx = idx+diff
        if len(men2[idx])>max_x:
            new_text= men2[idx][:max_x-3]+'...'
            new_text = new_text.replace("\n"," ")
            new_text= new_text.strip()
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


def text_pad(stdscr,text):
    '''Creating textpad with rectangle to print menu on '''
    h,w = stdscr.getmaxyx()
    box = [[0,2],[h-2,w-2]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
    top_menu = (text).encode('utf-8').center(w - 5)
    stdscr.addstr(0, 3, top_menu, curses.A_REVERSE)

#Stalk overflow


def buttom_menu(stdscr):
    '''Print Buttom Menu'''
    h,w = stdscr.getmaxyx()
    bottom_menu = "(↓)Next(↑)Prev Line|(→)Next(←)Prev Page|(q)Quit|(esc,backspace)Back|(b)Open Browser|(e)ExportCode|(c)CopyCode".encode('utf-8').center(w - 5)
    try:
        stdscr.addstr(h - 1, 3, bottom_menu, curses.A_REVERSE)
    except:
        stdscr.clear()
        stdscr.addstr(h - 1, 2,'...', curses.A_REVERSE)    

def main_window(stdscr):
      mode = 'title' 
      menu=titles
      curses.curs_set(False)
      stdscr.keypad(True)
      curses.mousemask(2)
      h,w = stdscr.getmaxyx()
      curses_default_color(stdscr)
      current_row = 0   
      top_label ='Debuggy'
      while True:

        print_menu(stdscr,current_row,menu,top_label)
        key = stdscr.getch()

        if mode=='title':
           stdscr.refresh()   
           if key == curses.KEY_UP and current_row-1 is not -1:
               current_row-=1
               print_menu(stdscr,current_row,menu,top_label)
           elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
               current_row+=1
               print_menu(stdscr,current_row,menu,top_label)
           elif key in [10,13,curses.KEY_RIGHT,curses.KEY_ENTER]:
               mode,idx= create_window(stdscr,menu,current_row,ans=True)
               if mode == 'export':
                    menu = codes_to_export
                    current_row = 0
                    stdscr.clear()
                    
                    top_label = 'Debuggy >>> Select Code To Export'     
           elif key == ord("q"):
             break         
           elif key == ord("b"):
             import webbrowser  
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
                    mode,idx=create_window(stdscr,menu,current_row,ans=True)
                    if mode is 'export':
                        menu = codes_to_export
                        current_row = 0
                        top_label = 'Debuggy >>> Select Code To Export' 
               except:
                   pass

        elif mode=='export':
            if codes_to_export !=[]:
                stdscr.refresh()
                if key == curses.KEY_UP and current_row-1 is not -1:
                    current_row-=1
                    print_menu(stdscr,current_row,menu,top_label)
                elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
                    current_row+=1
                    print_menu(stdscr,current_row,menu,top_label)
                elif key in [ord("q"),27,curses.KEY_BACKSPACE,127,8,curses.KEY_LEFT]:
                    stdscr.clear()
                    menu=titles
                    print_menu(stdscr,idx,menu,top_label) 
                    mode,idx = create_window(stdscr,menu,idx,ans=True)
                    if mode == 'title':
                        current_row = idx 
                        top_label = 'Debuggy'
                    else:
                        menu = codes_to_export
                elif key in [10,13,curses.KEY_ENTER]:
                    export_value = menu[current_row]
                    #insert export value to line where error occured on script
                    if filename:
                        script = replace_text(export_value) 
                        # with open(filename, "w") as myfile:
                        #     myfile.write(script)
                        editor_tui.curses_main(file = (script,filename),lineno=eln-1)
                        script = None

                         
                        #use subprocess or use an editor on main screen
                        #editor(filename)       
                        #save and overwrite script with the filename
                        #open editor on script
                    else:
                        export_value = menu[current_row]
                        import pyperclip
                        pyperclip.copy(export_value)
                        form_top_label=top_label
                        top_label = "Debbugy > Code Copied to Clipboard > {}".format(form_top_label)

                elif key == ord('c'):
                    export_value = menu[current_row]
                    import pyperclip
                    pyperclip.copy(export_value)
                    top_label = "Debuggy >>> Code Copied to Clipboard"
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
                            top_label= 'Debuggy' 
                            mode = create_window(stdscr,menu,current_row,ans=True)
                            if mode is not None:
                                current_row = 0
                    except:
                        pass
            else:
              while True:
                stdscr.addstr(h//2,w//2-len("No Codes To Export From Awnsers")//2, "No Codes To Export From Awnsers")
                stdscr.refresh()
                key = stdscr.getch() 
                if key in [ord("q"),27,curses.KEY_BACKSPACE,127,8]:
                    stdscr.clear()
                    menu=titles
                    print_menu(stdscr,idx,menu,top_label) 
                    mode,idx = create_window(stdscr,menu,idx,ans=True)
                    if mode == 'title':
                        current_row = idx 
                        top_label = 'Debuggy'
                    else:
                        menu = codes_to_export
                    break     
                       
def replace_text(replacement_text):
    linecache.clearcache()
    script = linecache.getlines(filename) 
    initial=len(script)
    errorlineno = eln-1
    error_code = "# Debuggy Commented The error Line: {} ".format(script[errorlineno] )
    script.pop(errorlineno)
    script.insert(errorlineno,replacement_text)
    script.insert(errorlineno,error_code)
    script = linecache.getlines(filename)
    present=len(script)
    diff = present-initial
    stop = errorlineno +diff
    print('diff {} initial {} present {} stop {}'.format(diff,initial,present,stop))
    return ''.join(script)
          

def start_app(lnks,ttls,file=None,errorlineno=None):
    global links,titles,filename,eln
    links,titles = lnks,ttls
    filename = file if file is not None else False
    eln = errorlineno
    wrapper(main_window)

