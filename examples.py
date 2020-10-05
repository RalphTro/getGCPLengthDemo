#! /usr/bin/env python3

import getGCPLength as gcl

## Valid examples 

print (gcl.getGCPLength('00', '340123453111111115'))
print (gcl.getGCPLength('01', '04150999999994'))
print (gcl.getGCPLength('253', '4602443000331XYZ'))
print (gcl.getGCPLength('255', '0811625999996554433'))
print (gcl.getGCPLength('401', '6270029876'))
print (gcl.getGCPLength('402', '59090020241111113'))
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
12
10
9
6
11
9
10
10
10
8
7
9
"""

## Invalid examples 

# SSCC has 17 instead of 18 characters
# print (gcl.getGCPLength('00', '34012345311111111'))
# Expected result:
# The GS1 Key has an incorrect length or impermissible characters.

# No prefix available
# print (gcl.getGCPLength('01', '09999999999994'))
# Expected result:
# There is no matching value. Try GEPIR (https://gepir.gs1.org/) or contact local GS1 MO.