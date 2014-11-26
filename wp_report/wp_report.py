#!/usr/bin/env python

# Version 1.1 - 20141126
# https://github.com/clcollins/serverbin/wp_report

import sys
import os
import urllib
import subprocess
import socket
import json

run_as_user = "apache"
webpath = "/srv/web"
wpcliurl = "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
php = "sudo -u %s php -d error_reporting=32759" % run_as_user
wpcli = webpath + "/bin/wp-cli.phar"
wpversion = "wp-includes/version.php"
drusettings = "sites/default/settings.php"

report_errors = False
report_drupal = False


def err(message):
    print ("ERROR: %s \n" % message)
    sys.exit(1)


def check_for_cms(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if wpversion in os.path.join(root, file):
                wproot = os.path.dirname(root)
                wp_found(wproot)
            elif drusettings in os.path.join(root, file):
                if report_drupal:
                    druroot = os.path.dirname(os.path.dirname(root))
                    data = dict(hostname=socket.getfqdn())
                    data['path'] = druroot
                    data['cms'] = 'Drupal'
                    print json.dumps(data)


def inspect_wp(path, query):
    wpcliargs = "%s %s --no-color --path=%s" % (php, wpcli, path)
    cmd = ' '.join([wpcliargs, query])
    inspect = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if report_errors:
        inspect_error = inspect.stderr.read()
        if inspect_error:
            data = dict(hostname=socket.getfqdn())
            data['path'] = path
            data['cms'] = 'WordPress'
            data['ERROR'] = inspect_error
            print json.dumps(data)
    return inspect.stdout.read()


def dictify(blob):
    lines = str(blob).split('\n')
    dict = {}
    for line in lines[1:len(lines) - 3]:
        splitline = line.split()
        if len(splitline) != 0:
            if len(splitline) == 2:
                splitline.append("UNKNOWN")
            dict[splitline[1]] = splitline[2]
    return dict


def wp_found(path):
    data = dict(hostname=socket.getfqdn())
    data['path'] = path
    data['cms'] = 'WordPress'
    if not os.path.isfile(wpcli):
        urllib.urlretrieve(wpcliurl, wpcli)

    version = inspect_wp(path, "core version")
    data['version'] = version.replace("\n", "")
    plugins = inspect_wp(path, "plugin status")
    data['plugins'] = dictify(plugins)
    themes = inspect_wp(path, "theme status")
    data['themes'] = dictify(themes)

    print json.dumps(data)


def main():
    if len(sys.argv) < 2:
        err("No path specified")
    else:
        path = sys.argv[1]
        if path is None:
            err("No path specified")
        elif webpath not in path:
            err("Path must be a subdirectory of %s" % webpath)

    check_for_cms(path)

main()
