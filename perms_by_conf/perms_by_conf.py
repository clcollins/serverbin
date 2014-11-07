#!/usr/bin/env python

# Version 1.0 - 20141107

# Copyright Information
# ---------------------
#
#
#
# Copyright (C) 2014 Chris Collins
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see http://www.gnu.org/licenses/.

import yaml
import sys
import os
import pwd
import grp
import subprocess

gids = []
admin_group = "admin"
webpath = "/srv/web"

wpconfig = "wp-config.php"
drusettings = "site/default/settings.php"


def err(message):
    print ("ERROR: %s \n" % message)
    sys.exit(1)


def validate_path(path, webpath):
    if path is None:
        err("'base:<path>' must be specified in the yaml file")
    elif webpath not in path:
        err("'base:<path>' must be a subdirectory of %s" % webpath)


def get_uid(user):

    uid = pwd.getpwnam(user).pw_uid
    return uid


def get_gid(group):

    gid = grp.getgrnam(group).gr_gid
    return gid


def setfacl_d(dir, uid, gids):

    d_gidperms = ["u::rwx,", "g::rwx,", "o::r-x,", "u:" + str(uid) + ":rwx,"]
    for gid in gids:
        d_gidperms.append("g:" + str(gid) + ":rwx,")

    d_args = ["/usr/bin/setfacl", "-d", "-m", ''.join(d_gidperms), dir]

    gidperms = ["u::rwx,", "g::rwx,", "o::r-x,", "u:" + str(uid) + ":rwx,"]
    for gid in gids:
        gidperms.append("g:" + str(gid) + ":rwx,")

    args = ["/usr/bin/setfacl", "-m", ''.join(gidperms), dir]

    subprocess.Popen(d_args)
    subprocess.Popen(args)


def setfacl_f(file, uid, gids):

    gidperms = ["u::rw-,", "g::rw-,", "o::r--,", "u:" + str(uid) + ":rw-,"]
    for gid in gids:
        gidperms.append("g:" + str(gid) + ":rw-,")

    args = ["/usr/bin/setfacl", "-m", ''.join(gidperms), file]

    subprocess.Popen(args)


def setfacl_b(path):

    subprocess.Popen(["/usr/bin/setfacl", "-R", "-b", path])


def try_chown(path, uid, gid):
    try:
        os.chown(path, uid, gid)
    except OSError as (errno, strerror):
        err(path + ": {1}".format(errno, strerror))


def recurse_perms(path, uid, gids):

    try_chown(path, uid, gids[0])
    setfacl_d(path, uid, gids)

    for root, dirs, files in os.walk(path, topdown=False):

        for dir in dirs:
            thisdir = os.path.join(root, dir)
            try_chown(thisdir, uid, gids[0])
            setfacl_d(thisdir, uid, gids)

        for file in files:
            thisfile = os.path.join(root, file)
            try_chown(thisfile, uid, gids[0])
            setfacl_f(thisfile, uid, gids)


def do_exceptions(path, exceptions):

    for exception in exceptions:
        epath = exception.get('path', None)
        user = exception.get('user', None)
        group = exception.get('group', None)
        recurse = exception.get('recurse', False)

        if epath is None:
            err("'path:<subdir>' must be specified for exceptions")

        if user is not None:
            uid = get_uid(user)
        else:
            uid = -1

        if group is not None:
            gid = get_gid(group)
        else:
            gid = -1

        item = '/'.join([path, epath])
        if recurse is True:
            for root, dirs, files in os.walk(item, topdown=False):
                for dir in dirs:
                    thisdir = os.path.join(root, dir)
                    try_chown(thisdir, uid, gid)
                for file in files:
                    thisfile = os.path.join(root, file)
                    try_chown(thisfile, uid, gid)
        else:
            try_chown(item, uid, gid)


def check_for_cms(path, exceptions, wp_exceptions, dru_exceptions):
    if os.path.isfile('/'.join([path, wpconfig])):
        for wp_exception in wp_exceptions:
            if os.path.exists('/'.join([path, wp_exception['path']])):
                exceptions.append(wp_exception)
    elif os.path.isfile('/'.join([path, drusettings])):
        for dru_exception in dru_exceptions:
            if os.path.exists('/'.join([path, dru_exception['path']])):
                exceptions.append(dru_exception)

    return exceptions


def main():
    if len(sys.argv) < 2:
        err("No yaml file specified")
    else:
        yaml_file = sys.argv[1]

    with open(yaml_file) as file:
        data = yaml.safe_load(file)

    path = data.get('base', None)
    webserver = data.get('webserver', 'root')
    user = data.get('user', 'root')
    group = data.get('group', 'root')
    altgroups = data.get('altgroups', None)

    wp_exceptions = [
        {'path': '.htaccess', 'user': webserver},
        {'path': 'wp-content', 'user': webserver},
        {'path': 'wp-content/cache', 'user': webserver, 'recurse': True},
        {'path': 'wp-content/blogs.dir', 'user': webserver, 'recurse': True},

    ]

    dru_exceptions = [
        {'path': 'sites/default/files', 'user': webserver, 'recurse': True},
    ]

    validate_path(path, webpath)
    uid = get_uid(user)
    gids.append(get_gid(group))
    altgroups.append(admin_group)

    for group in altgroups:
        gids.append(get_gid(group))

    setfacl_b(path)
    recurse_perms(path, uid, gids)

    exceptions = data.get('exceptions', None)
    check_for_cms(path, exceptions, wp_exceptions, dru_exceptions)

    if exceptions is not None:
        do_exceptions(path, exceptions)


main()
