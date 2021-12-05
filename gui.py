import curses
import re
text = '\n# Saves the XKCD comic page for offline read\n\nimport requests, os, bs4, shutil\n\nurl = \'http://xkcd.com/\'\n\nif os.path.isdir(\'xkcd\') == True: # If xkcd folder already exists\n    shutil.rmtree(\'xkcd\') #delete it\nelse: # otherwise\n    os.makedirs(\'xkcd\') # Creates xkcd foulder.\n\n\nwhile not url.endswith(\'#\'): # If there are no more posts, it url will endswith #, exist while loop\n    # Download the page\n    print \'Downloading %s page...\' % url\n    res = requests.get(url) # Get the page\n    res.raise_for_status() # Check for errors\n\n    soup = bs4.BeautifulSoup(res.text) # Dowload the page\n    # Find the URL of the comic im age\n    comicElem = soup.select(\'#comic img\') # Any #comic img it finds will be saved as a list in comicElem \n    if comicElem == []: # if the list is empty\n        print \'Couldn\\\'t find the image!\'\n    else:\n      comicUrl = comicElem[0].get(\'src\') # Get the first index in comicElem (the image) and save to\n        #comicUrl\n\n        # Download the image\n        print \'Downloading the %s image...\' % (comicUrl)\nres = requests.get(comicUrl) # Get the image. Getting something will always use requests.get()\n        res.raise_for_status() # Check for errors\n\n        # Save image to ./xkcd\n        imageFile = open(os.path.join(\'xkcd\', os.path.basename(comicUrl)), \'wb\')\n        for chunk in res.iter_content(10000):\n            imageFile.write(chunk)\n        imageFile.close()\n    # Get the Prev btn\'s URL\n    prevLink = soup.select(\'a[rel="prev"]\')[0]\n    # The Previous button is first <a rel="prev" href="/1535/" accesskey="p">&lt; Prev</a>\n    url = \'http://xkcd.com/\' + prevLink.get(\'href\')\n    # adds /1535/ to http://xkcd.com/\n\nprint \'Done!\'\n'


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
regex=re.compile(r'(\n\n+)')
spaces  =0
k = text.split("\n")



def text_spaces(text):
             spaces = 0
             #global spaces
         #for l in text:
             if type(text) is tuple:
                text = text[1]
             matches = regex.finditer(text)
             for i in matches:
                 result = i.groups()
                 if result[0]=='\n\n':
                     spaces+=1
                 elif result[0]=='\n\n\n':
                     spaces+=2
                 else:
                     spaces+=0
             return spaces


#spaces = sum(list(text_spaces(x) for x in description))
new_text = list(filter(lambda x : False if x=='\n' else x, description))

#print(len(text))
# def remove_new_line(text,divider):
#     #new_list=[]    
#     #for i in description:
#         if type(i) is tuple:
#             p= i[1].lstrip('\n')
#             new_list.append(p)
#         elif i =='\n': 
#             pass        
#         else:
#             new_list.append(i)
#     new_list.append(divider)

max_scroll = len(k)+spaces+20
#print(k)
print(len(k))
print(len(description))
print(len(new_text))






def main(stdscr):
    curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
    curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_RED,curses.COLOR_YELLOW)
    mypad_pos = 0
    y,x =stdscr.getmaxyx() 
    mypad = curses.newpad(len(text),x)
    #print(x)
    #new_pad= []
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
        # for i,j in enumerate(k):
    #     try:
    #         mypad.addstr(j)
    #         mypad.addstr("\n")
    #     except:
    #         st+=1
    #         new_pad = text[st:i+st]
    #         break
    #print(''.join(new_pad)) 
    #         
    mypadshift = 0
    mypad.refresh(mypad_pos, 0, 0, 0,y-1,x-1)
    #stdscr.refresh()        
    while True:
        #print(mypad_pos)
        #mypad.refresh(1, 0, 0, 0,y-1,x-1)
        cmd = stdscr.getch()
        if  cmd == curses.KEY_DOWN:
            mypad_pos += 1
            mypad.refresh(mypad_pos, mypadshift, 0, 0, y-1, x-1)
        elif cmd == curses.KEY_UP and mypad_pos!=0:
            mypad_pos -= 1
            mypad.refresh(mypad_pos, mypadshift, 0, 0, y-1, x-1)
        #elif cmd==curses.KEY_LEFT:
        #    mypadshift-=1
        #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)
        #elif cmd == curses.KEY_RIGHT:    
        #    mypadshift+=1
        #    mypad.refresh(mypad_pos, mypadshift,0, 0, y-1, x-1)
        elif cmd == ord('q'):
            break  


curses.wrapper(main)        