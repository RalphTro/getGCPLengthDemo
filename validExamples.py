#! /usr/bin/env python3

import getGCPLength as gcl

print (gcl.getGCPLength('00', '340123453111111115'))
print (gcl.getGCPLength('01', '04012345123456'))
print (gcl.getGCPLength('00', '340123453111111115'))
print (gcl.getGCPLength('01', '04012345123456'))
print (gcl.getGCPLength('253', '4602443000331XYZ'))
print (gcl.getGCPLength('255', '0811625999996554433'))
print (gcl.getGCPLength('414', '4226350800008'))
print (gcl.getGCPLength('417', '4280000000002'))
print (gcl.getGCPLength('8003', '03870585000552987'))
print (gcl.getGCPLength('8004', '0180451111ABC987'))
print (gcl.getGCPLength('8010', '0628165987'))
print (gcl.getGCPLength('8017', '440018922222222226'))
print (gcl.getGCPLength('8018', '385888700111111111'))

""" 
Expected results:
7
7
10
9
9
10
10
10
8
7
9
7
"""