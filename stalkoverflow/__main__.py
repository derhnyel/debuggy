import argparse
import os
from stalkoverflow import (parsers,handler,ui,editor_tui,animation)
import sys


def main():
    if len(sys.argv)>=2:
        """Use system argv"""
        if sys.argv[1]=='editor':
            animation.aprint("Debuggy is Launching Editor...Please wait...")
            file = None if len(sys.argv)<3 else sys.argv[2]
            editor_tui.curses_main(file=file)
            return True  
        elif sys.argv[1]=='q':
            query = ' '.join(sys.argv[2:len(sys.argv)]) #splice to get query
            if query=='':
                raise Exception("Enter a search query")
            if not os.path.isfile(query): #Ensure Query is not a File
                titles,_,links,_=parsers.GSearch(query) #Parse Query
                if len(titles) != 1: #Check to Ensure Result is not Empty 
                    ui.start_app(links,titles) # Opens interface       
                else:
                    print("\n%s%s%s" % (animation.bcolors.red, "No Google results found for query.\n", animation.bcolors.end))  
            else:
                raise Exception("-q takes str and not paths")
            return True       
        elif sys.argv[1]=='s':
            print(animation.bcolors.green+"Debuggy is Running Script...Please wait..."+animation.bcolors.end)
            script = None if len(sys.argv)<3 else sys.argv[2]
            if script is not None:
                handler.ProcessScript(script) #Handle Script Process to catch exceptions
            else:
                raise Exception("Enter a Valid file path")    
            return True            
    """Use Args Parser"""
    parser = argparse.ArgumentParser (prog='DeBuggy',description='Command-line tool that automatically searches Google and displays results in your terminal when you get a compiler error.\n Made by @Derhnyel')
    parser.add_argument('-v','--version', action='version', version='%(prog)s 3.0.0')
    parser.add_argument("-s","--script",help="Run Script from Terminal")
    parser.add_argument('-q','--query',help='Query stackoverflow with Error message ')
    subparser = parser.add_subparsers(dest='command')
    call = subparser.add_parser('call')
    #query_ = subparser.add_parser('q')
    #script_ = subparser.add_parser('s')
    editor_ = subparser.add_parser('editor')

    call.add_argument("-id",'--pid',required=True)
    call.add_argument('-e','--err',required=True)
    call.add_argument('-f','--file',required=True)
    args = parser.parse_args()
    
    if args.command=='call':
        animation.start()
        if os.path.isfile(args.err):
            ProcessId= int(args.pid)
            handler.execute(args.err,ProcessId,filename =args.file)
        else:
            raise Exception("-e takes path to Error logfile Only")        
    elif args.query is not None:
        if not os.path.isfile(args.query):
            # print(sys.argv[2:len(sys.argv)])
            # print(sys.argv[1])
            titles,_,links,_=parsers.GSearch(args.query)
            if len(titles) !=1:
                ui.start_app(links,titles) # Opens interface        
            else:
                print("\n%s%s%s" % (animation.bcolors.red, "No Google results found or Flagged for Too many requests \n", animation.bcolors.end))
        else:
             raise Exception("-q takes str and not paths") #handle paths as query
    elif args.script is not None:
        print(animation.bcolors.green+"Debuggy is Running Script...Please wait..."+animation.bcolors.end)
        handler.ProcessScript(args.script)
    else:
        animation.start()
        parser.print_help(sys.stderr)  

if __name__ == '__main__':
    main()