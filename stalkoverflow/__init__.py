import pyfiglet
import sys
from stalkoverflow.color import bcolors

DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
print(bcolors.cyan+DebuggyAnimation+bcolors.end,file=sys.stdout)