
import curses
from curses import wrapper
from curses import textpad
from functools import reduce

import re
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


description=[
'\n',"I'm learning Python by following Automate the Boring Stuff. This program is supposed to go to ",'http://xkcd.com/', ' and download all the images for offline viewing. ', 
'\n', "I'm on version 2.7 and Mac. ", 
'\n', 'For some reason, I\'m getting errors like "No schema supplied" and errors with using request.get() itself. ', 
'\n', 'Here is my code:', 
'\n', ('code', '\n# Saves the XKCD comic page for offline read\n\nimport requests, os, bs4, shutil\n\nurl = \'http://xkcd.com/\'\n\nif os.path.isdir(\'xkcd\') == True: # If xkcd folder already exists\n    shutil.rmtree(\'xkcd\') # delete it\nelse: # otherwise\n    os.makedirs(\'xkcd\') # Creates xkcd foulder.\n\n\nwhile not url.endswith(\'#\'): # If there are no more posts, it url will endswith #, exist while loop\n    # Download the page\n    print \'Downloading %s page...\' % url\n    res = requests.get(url) # Get the page\n    res.raise_for_status() # Check for errors\n\n    soup = bs4.BeautifulSoup(res.text) # Dowload the page\n    # Find the URL of the comic image\n    comicElem = soup.select(\'#comic img\') # Any #comic img it finds will be saved as a list in comicElem\n    if comicElem == []: # if the list is empty\n        print \'Couldn\\\'t find the image!\'\n    else:\n        comicUrl = comicElem[0].get(\'src\') # Get the first index in comicElem (the image) and save to\n        # comicUrl\n\n        # Download the image\n        print \'Downloading the %s image...\' % (comicUrl)\n        res = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n        res.raise_for_status() # Check for errors\n\n        # Save image to ./xkcd\n        imageFile = open(os.path.join(\'xkcd\', os.path.basename(comicUrl)), \'wb\')\n        for chunk in res.iter_content(10000):\n            imageFile.write(chunk)\n        imageFile.close()\n    # Get the Prev btn\'s URL\n    prevLink = soup.select(\'a[rel="prev"]\')[0]\n    # The Previous button is first <a rel="prev" href="/1535/" accesskey="p">&lt; Prev</a>\n    url = \'http://xkcd.com/\' + prevLink.get(\'href\')\n    # adds /1535/ to http://xkcd.com/\n\nprint \'Done!\'\n'),
'\n', 'Here are the errors:', 
'\n', ('code', '\nTraceback (most recent call last):\n  File "/Users/XKCD.py", line 30, in <module>\n    res = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n  File "/Library/Python/2.7/site-packages/requests/api.py", line 69, in get\n    return request(\'get\', url, params=params, **kwargs)\n  File "/Library/Python/2.7/site-packages/requests/api.py", line 50, in request\n    response = session.request(method=method, url=url, **kwargs)\n  File "/Library/Python/2.7/site-packages/requests/sessions.py", line 451, in request\n    prep = self.prepare_request(req)\n  File "/Library/Python/2.7/site-packages/requests/sessions.py", line 382, in prepare_request\n    hooks=merge_hooks(request.hooks, self.hooks),\n  File "/Library/Python/2.7/site-packages/requests/models.py", line 304, in prepare\n    self.prepare_url(url, params)\n  File "/Library/Python/2.7/site-packages/requests/models.py", line 362, in prepare_url\n    to_native_string(url, \'utf8\')))\nrequests.exceptions.MissingSchema: Invalid URL \'//imgs.xkcd.com/comics/the_martian.png\': No schema supplied. Perhaps you meant http:////imgs.xkcd.com/comics/the_martian.png?\n'), 
'\n', "The thing is I've been reading the section in the book about the program multiple times, reading the Requests doc, as well as looking at other questions on here. My syntax looks right. ",
'\n', 'Thanks for your help!', '\n', 'Edit: ', '\n', "This didn't work: ", 
'\n',('code', '\ncomicUrl = ("http:"+comicElem[0].get(\'src\')) \n'),
'\n', 'I thought adding the http: before would get rid of the no schema supplied error. ', '\n']    
awnsers= [
    ['\n', "No schema means you haven't supplied the ", 
('code', 'http://'), ' or ', ('code', 'https://'), ' supply these and it will do the trick.', 
'\n', 'Edit: Look at this URL string!:', '\n', 
('code', "\nURL '//imgs.xkcd.com/comics/the_martian.png':"), '\n'], 
['\n', 'change your ', 
('code', 'comicUrl'),' to this', '\n', ('code', '\ncomicUrl = comicElem[0].get(\'src\').strip("http://")\ncomicUrl="http://"+comicUrl\nif \'xkcd\' not in comicUrl:\n    comicUrl=comicUrl[:7]+\'xkcd.com/\'+comicUrl[7:]\n\nprint "comic url",comicUrl'),'\n'], 
['\n', 'Explanation:', '\n', "A few XKCD pages have special content that isn’t a simple image file. That’s fine; you can just skip those. If your selector doesn’t find any elements, then soup.select('#comic img') will return a blank list. ",'\n', 'Working Code:', '\n', 
('code', '\nimport requests,os,bs4,shutil\n\nurl=\'http://xkcd.com\'\n\n#making new folder\nif os.path.isdir(\'xkcd\') == True:\n    shutil.rmtree(\'xkcd\')\nelse:\n    os.makedirs(\'xkcd\')\n\n\n#scrapiing information\nwhile not url.endswith(\'#\'):\n    print(\'Downloading Page %s.....\' %(url))\n    res = requests.get(url)          #getting page\n    res.raise_for_status()\n    soup = bs4.BeautifulSoup(res.text)\n\n    comicElem = soup.select(\'#comic img\')     #getting img tag under  comic divison\n    if comicElem == []:                        #if not found print error\n        print(\'could not find comic image\')\n\n    else:\n        try:\n            comicUrl = \'http:\' + comicElem[0].get(\'src\')             #getting comic url and then downloading its image\n            print(\'Downloading image %s.....\' %(comicUrl))\n            res = requests.get(comicUrl)\n            res.raise_for_status()\n\n        except requests.exceptions.MissingSchema:\n        #skip if not a normal image file\n            prev = soup.select(\'a[rel="prev"]\')[0]\n            url = \'http://xkcd.com\' + prev.get(\'href\')\n            continue\n\n        imageFile = open(os.path.join(\'xkcd\',os.path.basename(comicUrl)),\'wb\')     #write  downloaded image to hard disk\n        for chunk in res.iter_content(10000):\n            imageFile.write(chunk)\n        imageFile.close()\n\n        #get previous link and update url\n        prev = soup.select(\'a[rel="prev"]\')[0]\n        url = "http://xkcd.com" + prev.get(\'href\')\n\n\nprint(\'Done...\')'), '\n'], 
['\n', 'Actually this is not a bigdeal.you can see the comicUrl somewhat like this ',
('code', '//imgs.xkcd.com/comics/acceptable_risk.png'), '\n', 'The only thing you need to add is ', 
('code', 'http:'), ' , remember it is ', ('code', 'http:'), ' and not ', 
('code', 'http://'), ' as some folks said earlier because already the url contatin double slashes.\nso please change the code to', '\n', 
('code', "\nres = requests.get('http:' + comicElem[0].get('src'))\n"), '\n', 'or', '\n',
('code', "\ncomicUrl = 'http:' + comicElem[0].get('src')\n\nres = requests.get(comicUrl)\n"), '\n', 'Happy coding', '\n'], 
['\n', 'Id just like to chime in here that I had this exact same error and used @Ajay recommended answer above but even after adding that I as still getting problems, right after the program downloaded the first image it would stop and return this error:','\n', 
('code', '\nValueError: Unsupported or invalid CSS selector: "a[rel"\n'), '\n', "this was referring to one of the last lines in the program where it uses the 'Prev button' to go to the next image to download. ", '\n',
'Anyway after going through the bs4 docs I made a slight change as follows and it seems to work just fine now:', '\n',
('code', '\nprevLink = soup.select(\'a[rel^="prev"]\')[0]\n'), '\n', 'Someone else might run into the same problem so thought Id add this comment.', '\n']]
awnser = ['\n', "No schema means you haven't supplied the ", 
('code', 'http://'), ' or ',
('code', 'https://'), ' supply these and it will do the trick.', '\n', 'Edit: Look at this URL string!:', '\n',
('code', "\nURL '//imgs.xkcd.com/comics/the_martian.png':"), '\n']
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
    #ResultWindow.clear()
   
    ResultWindow.immedok(True)
    ResultWindow.box()
    ResultWindow.border()
    buttom_menu(stdscr)
    
    top_menu =(menu[idx]).encode('utf-8').center(columns - 4)
    ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
    rows, columns = ResultWindow.getmaxyx()
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
    
    if ans:
        answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in awnsers]
        [stylize_print(mypad,x,columns-4) for x in answer_text]
    elif des:
        description_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
        stylize_print(mypad,description_text,columns-4)
    
    while True:
        y,x = stdscr.getmaxyx()
        rows, columns = ResultWindow.getmaxyx()
        if mypad_pos==0:
           mypad.refresh(mypad_pos, mypad_shift, 3, 6, y-6, x-1) 
        top_menu = ("Line %d to %d of 10000 of %s" % (mypad_pos + 1, mypad_pos + rows,'new window Title')).encode('utf-8').center(columns - 4)
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
            #get description and pass it here 
            mypad.clear()
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            new_text = list(filter(lambda x : False if x=='\n' else x, QDescription))
            stylize_print(mypad,new_text,columns-4)
        elif cmd == ord('a'):
            mypad.clear()
            mypad_pos =  0
            mypad_shift = 0
            mypad.refresh(mypad_pos, mypad_shift, 3, 6, rows-1, columns-1)
            answer_text = [list(filter(lambda f : False if f=='\n' else f, x)) for x in awnsers]
            [stylize_print(mypad,x,columns-4) for x in answer_text]
            #stylize_print(mypad,new_text,columns-4)
    curses.mousemask(1)






    
     # y1=round(y/5)
    # x1=round(x/5)
    #ResultWindow = curses.newwin(3*y1,3*x1,1,x1)
    #stdscr.clear()
    #buttom_menu(stdscr)
    #menu=["Boy",'girl','games','last','emememememememem','exitttttttt','nowwwwwwwwwwww','assssssasakasas','asaassa','assajkas','asaskas','sklasas','klas','sajsaj',
    # 'asjask','kslas','jsskjs','assalsakl','sasssakl','ssasskl','dhdhddj','djkdskjdsds','dsjdkjdsdskds','dhdsjs']
    #bottom_menu = "(↓)Next line | (↑)Previous line | (→)Next page | (←)Previouspage | (q)Quit"
    #ResultWindow.addstr(rows - 1, 2, bottom_menu, curses.A_REVERSE)
    # out = stdscr.subwin(rows - 3, columns - 4, 3, 6)
    # out_rows, out_columns = out.getmaxyx()
    # out_rows -= 1
    # lines = list(map(lambda x: x, reduce(lambda x, y: x + y, [[x[i:i+out_columns] for i in range(0, len(x), out_columns)] for x in new_list])))
    
    #print(lines)
    #stdscr.refresh()
    #line = 0        
    #ResultWindow.move(1,1)
    #ResultWindow.addstr(text)
    #curses.cbreak()
    # new_list = []
    # divider='*'*(x-10)
    # regex = re.compile(r'(\n\n+)')
    # for i in description:
    #     if type(i) is tuple:
    #         p= i[1].lstrip('\n')
    #         p = p.rstrip('\n')
    #         new_list.append(p)
    #     elif i =='\n': 
    #         pass        
    #     else:
    #         i= i.lstrip('\n')
    #         i = i.rstrip('\n')
            
    #         new_list.append(i)
    # new_list.append(divider)
    
    #print(new_list)          
    # 2\n is -1 line
    # 3\n is -2 lines
    # 6\n -3lines
    # 9\n -6lines
        #elif cmd==curses.KEY_LEFT:
        #    mypadshift-=1
        #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)
        #elif cmd == curses.KEY_RIGHT:    
        #    mypadshift+=1
        #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)  
    
    #print("".join(lines[line:line+out_rows]))
    # while True:
    #     # spaces = 0
    #     # for l in lines[line:line+out_rows]:
    #     #     matches = regex.finditer(l)
    #     #     for i in matches:
    #     #         result = i.groups()
    #     #         if result[0]=='\n\n':
    #     #            spaces+=1
    #     #         else:
    #     #             spaces+=2
    #     # #print(spaces)            
    #     # spaces = line - spaces
    #     # print("".join(lines[line:out_rows+spaces]))
    #     # print(len(lines[line:out_rows+spaces]))
    #     # print(lines[line:out_rows+spaces])

    #     #print(spaces-13)        
    #     top_menu = ("Lines %d to %d of %d of %s" % (line + 1, min(len(lines), line + out_rows), len(lines),'new window Title')).encode('utf-8').center(columns - 4)
    #     ResultWindow.addstr(0, 2, top_menu, curses.A_REVERSE)
    #     out.addstr(0, 0, "".join(lines[line:out_rows+spaces]))
    #     #stdscr.refresh()
    #     out.refresh()
    #     c = ResultWindow.getch()
    #     if c in [ord("q"),27,curses.KEY_LEFT]:
    #         break
    #     elif c == ord("b"):
    #          print('open webrowser')
    #     elif c == curses.KEY_DOWN:
    #         if len(lines) - line > out_rows:
    #             line += 1
    #     elif c == curses.KEY_UP:
    #         if line > 0:
    #             line -= 1
    #     elif c == curses.KEY_RIGHT:
    #         if len(lines) - line >= 2 * out_rows:
    #             line += out_rows
    #     # elif c == :
    #     #     breaks
    #         # if line >= out_rows:
    #         #     line -= out_rows
    #   #panel = curses.panel.new_panel(stdscr)
    
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
    #check if its the last or the first
    men2 = menu.copy()
    if len_menu>max_y:
        if rw_idx>=max_y:
           diff = (rw_idx-max_y) +1
           print(len(menu))    
           menu = menu[diff:max_y+diff]
           print(len(menu))
           print(diff)

        else:
            menu = menu[0:max_y]   

    #y,x = stdscr.getmaxyx()
    for idx,row in enumerate(menu):
        idf=idx
        idx = idx+diff
        if len(men2[idx])>max_x:
            new_text= men2[idx][:max_x-3]+'...'
        else:
            new_text = False    
        x1 = 3 #divide by the lenght of each text that will be the start
        y1 = 1 +idf
        #y1 = round(y/len(menu) + idx +1)
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

# def panel(stdscr):
#     y,x = stdscr.getmaxyx()
#     PanelWindow = curses.newwin(3,x-1,0,1)
#     PanelWindow.box()
#     PanelWindow.refresh()
#     PanelWindow.move(1,1)
#     PanelWindow.addstr('Reserved Panel')
#     PanelWindow.refresh()
    
    #PanelWindow.getch()

def text_pad(stdscr):
    h,w = stdscr.getmaxyx()
    box = [[0,2],[h-2,w-2]]
    textpad.rectangle(stdscr,box[0][0],box[0][1],box[1][0],box[1][1])

def buttom_menu(stdscr):
    h,w = stdscr.getmaxyx()
    # top_menu = ("DeBuggy").encode('utf-8').center(w - 4)
    # stdscr.addstr(0, 2, top_menu, curses.A_REVERSE)
    bottom_menu = "(↓)Next(↑)Prev Line|(→)Next(←)Prev Page|(q)Quit|(esc)Back|(b)Browser|(d)Description|(a)Answers".encode('utf-8').center(w - 4)
    try:
        stdscr.addstr(h - 1, 2, bottom_menu, curses.A_REVERSE|curses.A_BOLD)
    except:
        stdscr.clear()
        stdscr.addstr(h - 1, 2,'...', curses.A_REVERSE)    

def App(stdscr): 
      #print(SResult)
      
      menu=["Boy",'girl','now','asasakasas','asasa','asajkas','asaskas','sklasas','klas','sajsaj',
      'asjask','kslas','jskjs','asadsakl','sasakl','saskl']
      #menu=titles
      #menu=["Boy",'girl','games','last','emememememememem','exitttttttt','nowwwwwwwwwwww','assssssasakasas','asaassa','assajkas','asaskas','sklasas','klas','sajsaj',
      #'asjask','kslas','jsskjs','assalsakl','sasssakl','ssasskl','dhdhddj','djkdskjdsds','dsjdkjdsdskds','dhdsjs']
      curses.curs_set(False)
      stdscr.immedok(True)
      stdscr.keypad(True)
      text_pad(stdscr)
      curses.mousemask(1)
      #stdscr.nodelay(1)

      h,w = stdscr.getmaxyx()
      #box = [[3,3],[h-3,w-3]]

    #   mypad=curses.newpad(40,60)
    #   mypad_pos = 0
    #   mypad.refresh(mypad_pos,0,5,5,10,60)
    #   stdscr.scrollok(1)
    # for result in links:
    #  
    #   #   menu.append(result["title"])
    #color pair init with i d,foreground,backgroud 
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
      curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
      #height,width of windows(size of the windows),start(shifts down as value increases) and end(shift left as value increases) position
      current_row = 0   
      print_menu(stdscr,current_row,menu)
      #panel(stdscr)
      while True:
           key = stdscr.getch()
           #stdscr.clear()
           if key == curses.KEY_UP and current_row-1 is not -1:
               current_row-=1
               print_menu(stdscr,current_row,menu)
               #print(current_row)
           elif key == curses.KEY_DOWN and current_row+1 is not len(menu):
               current_row+=1
               print_menu(stdscr,current_row,menu)
               #print(current_row)
           elif key in [10,13,curses.KEY_RIGHT,curses.KEY_ENTER]:
               CreateWindow(stdscr,menu[current_row])
               print_menu(stdscr,current_row,menu)
           elif key == ord("q"):
             break     
               #QTitle,QDescription,QStatus,answers = SoF(links[current_row])   
           elif key == ord("b"):
             print('open webrowser')
        #    elif key == :
        #        CreateWindow(stdscr,menu[current_row])
        #        print_menu(stdscr,current_row,menu)         
               #stdscr.getch()
           elif key == curses.KEY_MOUSE:
               _,x,y,_,_ = curses.getmouse()
               start_y = 1
               #start_y = round(h/len(menu)+1)
               #end_y = len(menu)+start_y
               end_y = h-3
               if len(menu)> end_y:
                   continue
               else:
                   index = y-start_y
               try:
                 if y in range(start_y,end_y+1) and  x in range(3,len(menu[index])+5):
                    current_row=index
                    CreateWindow(stdscr,[menu[current_row]])
                    print_menu(stdscr,current_row,menu)  
               except:
                   pass
           #else:
                #print_menu(stdscr,current_row,menu)
                



                #stdscr.addstr(0,0,)
            #starts at 4 max value of y-3 should be greater than len(menu)+4   

                 
           ##print_menu(stdscr,current_row,menu)
      #stdscr.refresh()            
      # ([
      #               u'\n',
      #               ("menu", u" ESC "), ("light gray", u" Go back "),
      #               ("menu", u" B "), ("light gray", u" Open browser "),
      #               ("menu", u" Q "), ("light gray", u" Quit"),
      #           ])             
    
      #stdscr.addstr(y,x,'home')

wrapper(App)