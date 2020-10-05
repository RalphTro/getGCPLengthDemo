#! /usr/bin/env python3
"""Get GS1 Company Prefix (GCP) Length.

IMPORTANT: this script was developed for DEMONSTRATION purposes only. 
It is NOT RECOMMENDED implementing it 1:1 in a productive environment.
Particularly, I recommend companies to use a local copy of the GCP Length Table 
that is updated in regular (e.g. daily) intervals. 
If companies also have a separate file containing own GCP length entries, 
the latter should ideally be 
(a) formatted similarly and 
(b) kept separately to ease maintenance of the two files.
The latter approach is faster and far more efficient than triggering an online 
lookup every time the function is called. 
In this regard, note that the GCP length table at the time of writing this software
(July 2020) already is > 5 MB in size.
The function supports all GS1 Keys applicable to construct EPC values, specifically: 
SSCC, GTIN, GDTI, GCN, GINC, GSIN, GLN (for parties and physical locations), 
GRAI, GIAI, ITIP, CPID, GSRN-P, and GSRN."""

from re import match
import requests
import json

gs1KeyRegEx = {
    '00': "^(\d{18})$",
    '01': "^(\d{14})$",
    '253': "^(\d{13})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,17})$",
    '255': "^(\d{13})(\d{0,12})$",
    '401': "^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$",
    '402': "^(\d{17})$",
    '414': "^(\d{13})$",
    '417': "^(\d{13})$",
    '8003': "^(\d{14})([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,16})$",
    '8004': "^([\x21-\x22\x25-\x2F\x30-\x39\x3A-\x3F\x41-\x5A\x5F\x61-\x7A]{0,30})$",
    '8006': "^(\d{14})(\d{2})(\d{2})$",
    '8010': "^([\x23\x2D\x2F\x30-\x39\x41-\x5A]{0,30})$",
    '8017': "^(\d{18})$",
    '8018': "^(\d{18})$"
}

keyStartsWithGCP = {
    '00': False,
    '01': False,
    '253': True,
    '255': True,
    '401': True,
    '402': True,
    '414': True,
    '417': True,
    '8003': False,
    '8004': True,
    '8006': False,
    '8010': True,
    '8017': True,
    '8018': True
}

# Fetch GCP Length Table data from GS1 Website:
allGCPs = json.loads(requests.get(
    'https://www.gs1.org/sites/default/files/docs/gcp_length/gcpprefixformatlist.json').text)

# Transform JSON structure into list of dictionaries:
gcpDict = allGCPs["GCPPrefixFormatList"]["entry"]

def getGCPLength(aI, gs1Key):
    """Returns the length of a given GS1 Key.

    Function 'getGCPLength' expects a GS1 Key, prepended with its corresponding GS1 Application Identifier, and returns the corresponding GS1 Company Prefix (GCP) length.
    hereby, the function triggers an online lookup at GS1's GCP length table residing at https://www.gs1.org/sites/default/files/docs/gcp_length/gcpprefixformatlist.json
    Prior to that, it also performs a basic syntax check.
    
    Parameters
    ----------
    aI : str
        The GS1 Application Identifier (AI) of the GS1 Key.
    gs1Key : str
        The value of the GS1 Key.

    Returns
    -------
    int
        The length of the GS1 Company Prefix.
    str 
        Human readable error message.
    """

    # Check if GS1 Key complies with its corresponding RegEx
    if match(gs1KeyRegEx[aI], gs1Key) is None:
        exit('The GS1 Key has an incorrect length or impermissible characters.')
    # Variables storing identified gcp length and specifying prefix length/search string
    gcpLength = ""
    j = 12
    # Normalise input string so that function works consistently for all GS1 keys
    if (keyStartsWithGCP[aI] == True):
        gs1Key = '0' + gs1Key
    # Check if there are matching 12-digit prefix values. If not, iterate further (i.e. decrease GCP length) until there is a match.
    # Then, return corresponding GCP Length Value
    while (j > 2 and not gcpLength):  # 'not' checks if gcpLength is an empty string (yes/no)
        for i in range(len(gcpDict)):
            if (len(gcpDict[i]["prefix"]) == j and gcpDict[i]["prefix"] in gs1Key[1:(j+1)]):
                gcpLength = gcpDict[i]["gcpLength"]
                return (gcpLength)
            else:
                continue
        j -= 1
    if not gcpLength:
        exit('There is no matching value. Try GEPIR (https://gepir.gs1.org/) or contact local GS1 MO.')