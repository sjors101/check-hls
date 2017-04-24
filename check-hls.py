#!/usr/bin/python
"""
This Nagios check can be used to fetch a HLS playlist

Author: Sjors101 <https://github.com/sjors101/>, 12/04/2017
"""

import argparse, sys, os, urllib2

parser=argparse.ArgumentParser()
parser.add_argument("-u", "--url", help="insert destination url", type=str)
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args=parser.parse_args()

if args.url:
    req = urllib2.Request(args.url)

    try:
        response = urllib2.urlopen(req)
    except ValueError:
        print "UNKNOWN - probably a wrong url"
    except urllib2.HTTPError as e:
        print 'CRITICAL - The server couldn\'t fulfill the request. Error code: ',e.code
        sys.exit(2)
    except urllib2.URLError as e:
        print 'CRITICAL - We failed to reach a server. Reason: ',e.reason
        sys.exit(2)
    else:
        readR = response.read(8)
        if 'EXTM3U' in readR:
            print 'OK - able to read playlist'
            sys.exit(0)
        else:
            print 'WARNING - not a HLS-playlist: ',response.read(100)
            sys.exit(1)

else:
    print "UNKOWN - something went wrong"
    sys.exit(3)
