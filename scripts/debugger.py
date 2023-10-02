'''Short description'''

# Author: Luke Henderson

import time
from datetime import datetime
import sys

import colors as cl
import debugTools as dt
import utils as ut

cl.green('Program Start')

if 3!=None:
    print('SUCCESSSSS')
exit()

obj = ['']*8
dt.info(obj, 'obj')
exit()

try:
    time.sleep(2)
    raise TypeError
    raise KeyboardInterrupt
except TypeError:
    print('my TypeError handler')


cl.green('Program End')