import pyfiglet
import sys
from stalkoverflow.color import bcolors

def start():
    DebuggyAnimation = pyfiglet.figlet_format("DeBuggy",font="letters")
    print(bcolors.cyan+DebuggyAnimation+bcolors.end,file=sys.stdout)
def aprint(text):
    print(bcolors.green+text+bcolors.end)    