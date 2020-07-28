#! /usr/bin/env python3

import getGCPLength as gcl

# SSCC has 17 instead of 18 characters
print (gcl.getGCPLength('00', '34012345311111111'))

# No prefix available
print (gcl.getGCPLength('01', '09999999999994'))

""" 
Expected results:
The GS1 Key has an incorrect length or impermissible characters.
There is no matching value. Try GEPIR (https://gepir.gs1.org/) or contact local GS1 MO.
"""