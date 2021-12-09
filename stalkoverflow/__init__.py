import pyfiglet
import sys
from stalkoverflow.color import bcolors

DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
print(bcolors.cyan+DebuggyAnimation,file=sys.stdout)