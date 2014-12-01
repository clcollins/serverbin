#!/usr/bin/env python

# Version 0.5 - 20141201
# https://github.com/clcollins/serverbin/blacklist

import urllib2
import sys
import subprocess

feed = "<SPACE SEPARATED IPs or IP/SUBNET LIST AT SOME URL>"
inputPos = "5"
testCmd = "/sbin/iptables -n -L %s"
flushCmd = "/sbin/iptables -F %s"
makeCmd = "/sbin/iptables -N %s"
insertCmd = "/sbin/iptables -A %s -s %s -m comment --comment \"BLACKLIST\" -j DROP"
chain = "BLACKLIST"


def err(message):
    print ("ERROR: %s \n" % message)
    sys.exit(1)


def makeChain():
    print "Making chain"
    cmd = makeCmd % chain
    make = subprocess.Popen(cmd,
                            shell=True,
                            stderr=subprocess.PIPE)

    make_error = make.stderr.read()
    if make_error:
        err(make_error)


def checkChain():
    cmd = testCmd % chain
    print "Checking chain"
    print cmd
    check = subprocess.Popen(cmd,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    # I don't know why, but check.stdout.read() needs to be given to something
    # or the whole thing freezes
    check_stdout = check.stdout.read()

    check_error = check.stderr.read()
    if check_error:
        print (check_error + "\n")
        makeChain()
    else:
        print "No errors"


def flushRules():
    cmd = flushCmd % chain
    print "Flushing chain"
    flush = subprocess.Popen(cmd,
                             shell=True,
                             stderr=subprocess.PIPE)

    flush_error = flush.stderr.read()
    if flush_error:
        err(flush_error)


def applyRules(ip):
    cmd = insertCmd % (chain, ip)
    insert = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
    insert_error = insert.stderr.read()
    if insert_error:
        err(insert_error)


def getIps():
    req = urllib2.Request(feed)
    try:
        print "Getting IPs"
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
    print "checkchain1"
    checkChain()
    print "checkchain2"
    print "flushrules1"
    flushRules()
    print "flushrules2"

    print "applying rules"
    ips = getIps()
    for ip in ips:
        applyRules(ip)


main()
