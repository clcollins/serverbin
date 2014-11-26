#!/usr/bin/env python

# Version 1.04 - 20141126
# https://github.com/clcollins/serverbin/wp_report

import sys
import os
import urllib
import subprocess
import socket
import json

webpath = "/srv/web"
wpcliurl = "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
php = "php -d error_reporting=32759"
wpcli = webpath + "/bin/wp-cli.phar"
wpconfig = "wp-includes/version.php"
drusettings = "sites/default/settings.php"


def err(message):
    print ("ERROR: %s \n" % message)
    sys.exit(1)


def check_for_cms(path):
    if os.path.isfile('/'.join([path, wpconfig])):
        return True
    elif os.path.isfile('/'.join([path, drusettings])):
        err("Drupal install found")
    else:
        err("No CMS discovered")


def inspect_wp(path, query):
    wpcliargs = "%s %s --no-color --path=%s" % (php, wpcli, path)
    cmd = ' '.join([wpcliargs, query])
    inspect = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return inspect.stdout.read()


def dictify(blob):
    lines = str(blob).split('\n')
    dict = {}
    for line in lines[1:len(lines) - 3]:
        splitline = line.split()
        print len(splitline)
        if len(splitline) != 0:
            if len(splitline) == 2:
                splitline.append("UNKNOWN")
            dict[splitline[1]] = splitline[2]
    return dict


def main():
    if len(sys.argv) < 2:
        err("No path specified")
    else:
        path = sys.argv[1]
        if path is None:
            err("No path specified")
        elif webpath not in path:
            err("Path must be a subdirectory of %s" % webpath)

    data = dict(hostname=socket.getfqdn())
    data['path'] = path

    if check_for_cms(path):
        if not os.path.isfile(wpcli):
            urllib.urlretrieve(wpcliurl, wpcli)

    data['version'] = inspect_wp(path, "core version")
    plugins = inspect_wp(path, "plugin status")
    data['plugins'] = dictify(plugins)
    themes = inspect_wp(path, "theme status")
    data['themes'] = dictify(themes)

    print json.dumps(data)

main()
