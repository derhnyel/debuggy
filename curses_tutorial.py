import curses
from curses.textpad import Textbox,rectangle
from curses import wrapper
import time
from curses import textpad
import random
from functools import reduce
import locale
import sys

def main(filename, filecontent, encoding="utf-8"):
    try:
        menu=["Boy",'girl','games','last','emememememememem','exitttttttt','nowwwwwwwwwwww','assssssasakasas','asaassa','assajkas','asaskas','sklasas','klas','sajsaj',
      'asjask','kslas','jsskjs','assalsakl','sasssakl','ssasskl','dhdhddj','djkdskjdsds','dsjdkjdsdskds','dhdsjs']
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        stdscr.keypad(1)
        rows, columns = stdscr.getmaxyx()
        stdscr.border()
        bottom_menu = "(↓) Next line | (↑) Previous line | (→) Next page | (←) Previous page | (q) Quit"
        stdscr.addstr(rows - 1, 2, bottom_menu, curses.A_REVERSE)
        out = stdscr.subwin(rows - 2, columns - 2, 1, 1)
        out_rows, out_columns = out.getmaxyx()
        out_rows -= 1
        lines = list(map(lambda x: x + " " * (out_columns - len(x)), reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in range(0, len(x), out_columns)] for x in menu])))
        stdscr.refresh()
        line = 0
        while 1:
            top_menu = ("Lines %d to %d of %d of %s" % (line + 1, min(len(lines), line + out_rows), len(lines), filename)).encode(encoding).center(columns - 4)
            stdscr.addstr(0, 2, top_menu, curses.A_REVERSE)
            out.addstr(0, 0, "".join(lines[line:line+out_rows]))
            stdscr.refresh()
            out.refresh()
            c = stdscr.getch()
            if c == ord("q"):
                break
            elif c == curses.KEY_DOWN:
                if len(lines) - line > out_rows:
                    line += 1
            elif c == curses.KEY_UP:
                if line > 0:
                    line -= 1
            elif c == curses.KEY_RIGHT:
                if len(lines) - line >= 2 * out_rows:
                    line += out_rows
            elif c == curses.KEY_LEFT:
                if line >= out_rows:
                    line -= out_rows
    finally:
        curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.curs_set(1)
        curses.endwin()


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    encoding = locale.getpreferredencoding()
    try:
        filename = sys.argv[1]
    except:
        print("Usage: python %s FILENAME" % __file__)
    else:
        try:
            with open(filename) as f:
                filecontent = f.read()
        except:
            print("Unable to open file %s" % filename)
        else:
            main(filename, filecontent, encoding)        






# def create_food(snake,box):
#     food = None
#     while food is None:
#         food = [random.randint (box[0][0]+1,box[1][0]-1),random.randint (box[0][1]+1,box[1][1]-1)]
#         if food in snake:
#             food= None
#     return food

# def print_score(stdscr,score):
#     h,w = stdscr.getmaxyx()
#     score = 0
#     score_text = 'Score: {}'.format(score)
#     stdscr.addstr(0,w//2-len(score_text)//2,score_text)
#     stdscr.refresh()

# def main(stdscr):
#     curses.curs_set(0)
#     stdscr.nodelay(1)
#     stdscr.timeout(150)
#     h,w = stdscr.getmaxyx()
#     box = [[3,3],[h-3,w-3]]
#     textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])
#     stdscr.refresh()

#     snake = [[h//2,w//2+1],[h//2,w//2],[h//2,w//2-1]]
#     direction =curses.KEY_RIGHT

#     for y,x in snake:
#         stdscr.addstr(y,x,'#')

#     food = create_food(snake,box)
#     stdscr.addstr(food[0],food[1],"*")  
    

#     score = 0
#     print_score(stdscr,score)
    

#     while True:
#         key = stdscr.getch()

#         if key in [curses.KEY_RIGHT,curses.KEY_LEFT,curses.KEY_UP,curses.KEY_DOWN]:
#            direction = key

#         head=snake[0]


#         if direction == curses.KEY_RIGHT:
#             new_head = [head[0],head[1]+1]
#         elif direction == curses.KEY_LEFT:
#             new_head = [head[0],head[1]-1]
#         elif direction == curses.KEY_UP:
#             new_head = [head[0]-1,head[1]]
#         elif direction == curses.KEY_DOWN:
#             new_head = [head[0]+1,head[1]]

#         snake.insert(0,new_head)
#         stdscr.addstr(new_head[0],new_head[1],'#')
#         if snake[0] == food:
#             food = create_food(snake,box)
#             stdscr.addstr(food[0],food[1],'*')
#             score+=1
#             print_score(stdscr,score)

#         else:    
#             stdscr.addstr(snake[-1][0],snake[-1][1],' ')
#             snake.pop()

#         if (snake[0][0] in [box[0][0],box[1][0]] or snake[0][1] in [box[0][1],box[1][1]] or snake[0] in snake[1:]):
#             msg="GAME OVER"
#             stdscr.addstr(h//2,w//2-len(msg)//2,msg)
#             stdscr.nodelay(0)
#             stdscr.refresh()
#             stdscr.getch()
#             break    


#         stdscr.refresh()                     

    #stdscr.getch()





# menu = ['title','head','body','start','head']
# def print_menu(stdscr,rw_idx):
#     stdscr.clear()
#     #h,w = stdscr.getmaxyx()
#     for idx,row in enumerate(menu):
#         x = 10
#         y = 0 + len(menu) + idx
#         if idx == rw_idx:
#             stdscr.attron(curses.color_pair(2))
#             stdscr.addstr(y,x,row)
#             stdscr.attroff(curses.color_pair(2))
#         else:    
#             stdscr.addstr(y,x,row)
#     stdscr.refresh()    


# def main(stdscr):
#     #color pair init with i d,foreground,backgroud 
#     curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
#     curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
#     curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_YELLOW)
#     curses.init_pair(4,curses.COLOR_RED,curses.COLOR_YELLOW)

   
#     curses.curs_set(False)

#     current_row = 0

#     print_menu(stdscr,current_row)
#     while True: 
#         key = stdscr.getch()
#         stdscr.clear()

#         if key == curses.KEY_UP:
#             print_menu(stdscr,current_row-1 if current_row-1 is not -1 else current_row)
#             if current_row-1 is not -1:
#                 current_row-=1
#         elif key == curses.KEY_DOWN:
#             print_menu(stdscr,current_row+1 if current_row+1 is not len(menu) else current_row)
#             if current_row+1 is not len(menu):
#                 current_row+=1
#         elif key == curses.KEY_ENTER or key in [10,13]:
#             #y,x = stdscr.getmaxyx()
#             stdscr.addstr(0,0,menu[current_row])
#             stdscr.refresh()      
#             stdscr.getch()
#             if current_row==len(menu)-1:
#                 break
 
#         print_menu(stdscr,current_row)

            

#         stdscr.refresh()            
                  
   
#     #stdscr.addstr(y,x,'home')

wrapper(main)




 
    # #rows,column in screen
    # (curses.LINES -1,curses.COLS -1)
    # pad = curses.newpad(100,100)
    # stdscr.refresh() 
    # for i in  range(100):
    #     for j in range(26):
    #         char= chr(67 + j)
    #         pad.addstr(char,curses.color_pair(3))

#start at (a segment of the whole screen allocated to the pad),topleft hand corner of the screen where i want content to start showing in the pad,the width and height
    # for i in range(50):
    #     stdscr.clear()
    #     stdscr.refresh()
    #     pad.refresh(0,0,5,i,15,25+i)   
    #     time.sleep(0.2)         
    #height,width,row,column
    # counter_win = curses.newwin(1,20,10,10)
    # stdscr.addstr('hello world')
    # stdscr.refresh()
    # for i in range(100):
    #     counter_win.clear()

    #     color = curses.color_pair(2)
    #     #row ,column,text,attribute | attribute

    #     if i%2==0:
    #         color = curses.color_pair(1)
    #     counter_win.addstr(f'Count: {i}',color)
    #     #stdscr.addstr(10,12,'Hskskskjy')
    #     counter_win.refresh()
    #     time.sleep(0.1)
    # # gets the ordinal value
    # stdscr.getch()
     
    # #gets the key press 
    # stdscr.getkey()
    # stdscr.nodelay(True)
    # x,y = 0,0
    # string_x=0
    # while True:
        
    #     try:
    #         key = stdscr.getkey()
    #     except:
    #         key=None    
    #     if key == "KEY_LEFT":
    #         x-=1
    #     elif key== "KEY_RIGHT":
    #         x+=1
    #     elif key =="KEY_UP":
    #         y-=1
    #     elif key =="KEY_DOWN":
    #         y+=1
    #     stdscr.clear()
    #     string_x+=1
    #     stdscr.addstr(0,string_x//50,'Hello, world')
    #     stdscr.addstr(y,x,"0")
    #     stdscr.refresh()
    #wwindow takes,height,width,startposition
    # win = curses.newwin(3,18,2,2) 
    # box=  Textbox(win)
    # rectangle(stdscr,1,1,5,20)
    # stdscr.refresh()
    # box.edit()
    # text =box.gather()
    #stdscr.border()
    # stdscr.getch()
    #no cursor



    #stdscr.attron(curses.color_pair())
    #stdscr.attroff(curses.color_pair())
