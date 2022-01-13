import curses
from colorama import init

class bcolors:
      init()
      bold='\033[1m'
      underline='\033[4m'
      reverse='\033[7m'
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

def curses_default_color(stdscr):
      curses.start_color()
      curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_MAGENTA)
      curses.init_pair(2,curses.COLOR_BLUE,curses.COLOR_RED)
      curses.init_pair(4,curses.COLOR_CYAN,curses.COLOR_BLACK)
      curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)


