#!/usr/bin/env python

# Version 0.6 - 20141202
# https://github.com/clcollins/serverbin/blacklist

import urllib2
import sys
import subprocess
import re

feed = "<SPACE SEPARATED IPs or IP/SUBNET LIST AT SOME URL>"
testCmd = "/sbin/iptables -n -L %s"
flushCmd = "/sbin/iptables -F %s"
makeCmd = "/sbin/iptables -N %s"
insertCmd = "/sbin/iptables -A %s -s %s -m comment --comment \"BLACKLIST\" -j DROP"
chain = "BLACKLIST"


def err(message):
    print ("ERROR: %s \n" % message)
    sys.exit(1)


def makeChain():
    cmd = makeCmd % chain
    make = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    make_stdout, make_stderr = make.communicate()

    if make_stderr:
        err(make_stderr)


def checkChain():
    cmd = testCmd % chain
    check = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    check_stdout, check_stderr = check.communicate()

    gooderror = re.compile('iptables: No chain/target/match by that name.')

    if check_stderr:
        if gooderror.match(check_stderr):
            makeChain()
        else:
            err(check_stderr)
    else:
        pass


def flushRules():
    cmd = flushCmd % chain
    flush = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    flush_stdout, flush_stderr = flush.communicate()

    if flush_stderr:
        err(flush_stderr)


def applyRules(ip):
    cmd = insertCmd % (chain, ip)
    insert = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)

    insert_stdout, insert_stderr = insert.communicate()

    if insert_stderr:
        err(insert_stderr)


def getIps():
    req = urllib2.Request(feed)
    try:
        response = urllib2.urlopen(req)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
    else:

        ips = str.splitlines(response.read())
        return ips


def main():
    checkChain()
    flushRules()
    ips = getIps()
    for ip in ips:
        applyRules(ip)


main()
