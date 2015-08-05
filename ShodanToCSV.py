#!/usr/bin/env python
#
# Search shodan, output to CSV
# To ensure comma as seperator, all comma's in os and header field (if any) are replaced for ;;;
# To ensure row integrity all newlines (\n) are replaced by #NWLN
# Author: Jeroen

import shodan
import sys
import os
from optparse import OptionParser

#Initialize userinput
oparser = OptionParser("usage: %prog [options] [command]*", version="v%d.%d.%d" % (1, 0, 0))
oparser.add_option("-d", "--debug", dest="debug", action = "store_true", help="Be extremely verbose", default=False)
oparser.add_option("-k", "--key", dest="AKEY", help="Use your personal API key",default="GETYOUROWNKEY")
oparser.add_option("-s", "--search", dest="searchQuery", help="Insert shodan search query",default=False)
oparser.add_option("-o", "--output", dest="outputFileName", help="output filename",default="output.csv")

(options,args) = oparser.parse_args(sys.argv)

if (options.searchQuery == False):
print 'Type shodanToCSV.py --help for syntax'
sys.exit(1)

try:
# Setup the api
api = shodan.WebAPI(options.AKEY)

# Perform the search
result = api.search(options.searchQuery)
csvHeader = "ip,port,os,country,lastupdate,header\n"
fo = open(options.outputFileName, 'w')
fo.write(str(csvHeader))
# Loop through the matches and print each IP
for result in result['matches']:
row = result['ip'] + ',' + str(result['port']) + ',' + str(result['os']).replace(",",";;;") + ',' + result['country_name'] + ',' + result['updated'] + ',' + str(result['data']).replace(",",";;;")
row = row.replace("\r\n","").replace("\n","") + str(os.linesep)
if(options.debug != False):
print str(row)
fo.write(str(row))
fo.close()
except Exception, e:
print 'Error: %s' % e
exit(1)
