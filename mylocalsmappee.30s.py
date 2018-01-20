#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# <bitbar.title>MySmappee</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>pvdabeel@mac.com</bitbar.author>
# <bitbar.author.github>pvdabeel</bitbar.author.github>
# <bitbar.desc>Show your home power consumption and solar production in the Mac OS X menubar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# Licence: GPL v3

# Installation instructions: 
# -------------------------- 
# Execute in terminal.app before running : 
#    sudo easy_install keyring
#
# Ensure you have bitbar installed https://github.com/matryer/bitbar/releases/latest
# Ensure your bitbar plugins directory does not have a space in the path (known bitbar bug)
# Copy this file to your bitbar plugins folder and chmod +x the file from your terminal in that folder
# Run bitbar


try:   # Python 3 dependencies
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen, build_opener
    from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPError, URLError
except: # Python 2 dependencies
    from urllib import urlencode
    from urllib2 import Request, urlopen, build_opener
    from urllib2 import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler, HTTPError, URLError

import ast
import json
import sys
import datetime
import calendar
import base64
import math
import keyring      # Access token is stored in OS X keychain
import getpass      # Getting password without showing chars in terminal.app
import time
import os
import subprocess
import smappy


from datetime import date

# Streaming - requires bitbar v2 beta10 or higher

STREAMING = True

# Nice ANSI colors
CEND    = '\33[0m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'

# Support for OS X Dark Mode
DARK_MODE=os.getenv('BitBarDarkMode',0)

# Logo for both dark mode and regular mode
def app_print_logo():
    if bool(DARK_MODE):
        print ('|image=iVBORw0KGgoAAAANSUhEUgAAAA8AAAAWCAYAAAAfD8YZAAAAAXNSR0IArs4c6QAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpMwidZAAABZElEQVQ4EbWSuUoEQRCGZ93FA8TFIxOExczIUF/CdzAUcxMzwUDBRzA2MxMMfAFjQQVRQcQDFTxW1nPb75/p6u0ZNliDKfimjq6/errpJCnDnHNVqEOtjPndZ7JbPyzCESzDYPfOQpXGCizBA8ieYAXqhdZ8SkMNFuAWZL+Zc6/4NRjIK8hUhGFYhUeIre2TT/wGjMFQGEIyClvQBJkJsqzzbRFuw3hRfOV77Fc7kiyygRowIXFfmJAkVR9XolocWl3ndlowsZK2Cj3YNz05sYRfPQjV8g7pRvHOTS9Op/o4dlZ/NrG92x8Kb77TmsyrbOdVrE3UH878QXwG+nVrlNcAywnT9Qt8S0kwrn8a9EhOQHYPO3CqBHuBTZgJojhgYRL2QLYLDVhXgmnYfNxvF2a1KYKGT87x13Dpcz0M/V04hl2Y3vcIi3Nw4znE62KOYR/0nmfhAO4gs3ia1eT/W4+15cZ/df1h8Ce1/SgAAAAASUVORK5CYII=')
    else:
        print ('|image=iVBORw0KGgoAAAANSUhEUgAAAA8AAAAWCAYAAAAfD8YZAAAAAXNSR0IArs4c6QAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAACXBIWXMAAAsTAAALEwEAmpwYAAABWWlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNS40LjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyI+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgIDwvcmRmOkRlc2NyaXB0aW9uPgogICA8L3JkZjpSREY+CjwveDp4bXBtZXRhPgpMwidZAAABWklEQVQ4EbWTOUpEURBF21lBFIdEBEFchZtwCeZuwMRMMDDo0NDIXBB0Iw6RqCCiOIFoi/NwzutfD9putA3+hWPVq19Vb+iyUilJXfQdhu5S+tu9lXoJzsMGdMIevMOf6iBjAa7hC25hEbzCr/J+c3ABFn4U9h67DH3QJIODsAQ3YGHwWfgv2FUYhQHIGsGrQg0sioJoEPaJb+swBlkWn4JJcdQoCBsNbTAO6SW1Kl7eB2uliHtFG+ZiF3ZuR28kNRRb+NpOJTmPkDZyAJSdfCyVutbdhr8RvyOaimNunZ6HIjWSwhqO++q7SZq22PmZwCF49EjU2iDWuOn7MdYXzy+svw+O4iT4U1zBNvQUa0+2Bs6Do9skC3fAHTdhGlaK9SV2FrLi2BGYwrFAHcEZnLhAnmYG8jViMPw4BP5TTIAFW3AA/eCJzsFX3oUaZOVuOVJ3/hv/UV7W8ht0klql7W4ncwAAAABJRU5ErkJggg==')
    print('---')


# The init function: Called to store your username and access_code in OS X Keychain on first launch

def init():
    # Here we do the setup
    # Store access_token in OS X keychain on first run
    print ('Enter your local smappee hostname (by default this is \"smappee.local\"):')
    init_hostname = raw_input()
    print ('Enter your local smappee password (by default this is \"admin\")')
    init_password = getpass.getpass()

    try:
        c = smappy.LocalSmappee(init_hostname)
        c.logon(init_password)
    except HTTPError as e:
        print ('Error contacting local Smappee appliance. Try again later.')
        print e
        time.sleep(0.5)
        return
    except URLError as e:
        print ('Error: Unable to connect. Check your connection settings.')
        print e
        return
    except Exception as e:
        print ('Error: Something went wrong:')
        print e
        return
    keyring.set_password("mylocalsmappee-bitbar","hostname",init_hostname)
    keyring.set_password("mylocalsmappee-bitbar","password",init_password)


# The main function

def main(argv):

    # CASE 1: init was called 
    if 'init' in argv:
       init()
       return
  

    # CASE 2: init was not called, keyring not initialized
    if DARK_MODE:
        color = '#FFDEDEDE'
        info_color = '#808080'
    else:
        color = 'black' 
        info_color = '#808080'

    HOSTNAME = keyring.get_password("mylocalsmappee-bitbar","hostname")
    PASSWORD = keyring.get_password("mylocalsmappee-bitbar","password")
    
    if not HOSTNAME:   
       # restart in terminal calling init 
       app_print_logo()
       print ('Login to your local Smappee | refresh=true terminal=true bash="\'%s\'" param1="%s" color=%s' % (sys.argv[0], 'init', color))
       return


    # CASE 3: init was not called, keyring initialized, no connection (access code not valid)
    try:
       # create connection to smappee using token
       c = smappy.LocalSmappee(HOSTNAME)
       c.logon(PASSWORD)
    except: 
       app_print_logo()
       print ('Login to your local Smappee | refresh=true terminal=true bash="\'%s\'" param1="%s" color=%s' % (sys.argv[0], 'init', color))
       return


    # CASE 4: all ok, all other cases
    if STREAMING:
       while True:

          # get the data for the location      
          load = c.active_power()

          # print the data for the Smappee appliance
          print ('%s Watt | color=%s' % (load,color))
          print ('---')
          print ('Expert Mode | href=http://%s/smappee.html color=%s' % (HOSTNAME,color))
          print ('~~~')
          time.sleep(0.5)
    else:
       app_print_logo()
       prefix = ''

       # get the data for the location      
       load = c.active_power()

       # print the data for the Smappee appliance
       print ('%sCurrent Load:  %s Watt | color=%s' % (prefix, load,color))
       print ('%s---' % prefix)
       print ('%sExpert Mode | href=http://%s/smappee.html color=%s' % (prefix, HOSTNAME,color))

def run_script(script):
    return subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()


if __name__ == '__main__':
    main(sys.argv)
