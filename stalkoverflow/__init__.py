import pyfiglet
import sys
from stalkoverflow.color import *

DebuggyAnimation = pyfiglet.figlet_format("Debuggy",font="letters")
print(cyan+DebuggyAnimation,file=sys.stdout)