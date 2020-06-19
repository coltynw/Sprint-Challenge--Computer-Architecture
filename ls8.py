# '/examples/print8.ls8'

"""Main."""

import sys
from cpu import *

cpu = CPU()


# thing = sys.argv[1]

# print(sys.argv)
# thing = open('/examples/print8.ls8')
cpu.load('sctest.ls8')
cpu.run()

# v = cpu.ram_read(125)
# print(v)
# heyyyy it works