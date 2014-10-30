###############################################################################
# sftpbacup_util.py
#
# by Sam Weiss
#
# Contains function that will be run in the main file
###############################################################################

import pysftp
import getpass
import os
import pdb
import json
import sys

#excluded_files = [
#how to implement this, we want to exclude some formats, but also
#maybe ignore . files and # files


#we don't want to try and move files over 1 MB
prefs = {'max_size':1000000, 'server':"None", 'user':"None", 'pass':"None"}


def read_prefs():
    try:
        f = open('sftpBackup_prefs', 'r')
    except Exception as e:
        log("No preference file found")
        return
    temp = json.loads(f)
    if not 'max_size' in test:
        log("Error reading preference file, returning to defaults")
        return
    prefs = temp

def store_prefs(store_pass):
    if not store_pass:
        prefs['pass'] = "None"
    f = open('sftpBackup_prefs', 'w')
    output = json.dumps(prefs)

def get_target_dir_clean(dir):
    if not os.path.isdir(dir):
        log("Attempted to scan a dir that did not exist /n " + dir)
        sys.exit(1)
    currentdir = os.listdir(dir)
    for e in currentdir:
        if e[0] == '.' or e[0] == '#':
            currentdir.remove(e)
            continue
        if os.path.getsize(e) > max_size:
            currentdir.remove(e)
            continue
    return currentdir

def get_files_to_move(sftp, dir):
    target = get_target_dir_clean(dir)
    remote_files = sftp.listdir_attr()
    remote_modified = {}
    for e in remote_files:
        name = e.filename
        if name[0] != '.' and name[0] != '#':
            remote_modified[name] = e.st_mtime
    for e in target:
        if sftp.isfile(e):
            local_mod = os.stat(e).st_mtime
            remote_mod = remote_modified[e]
            if local_mod <= remote_mod:
                target.remove(e)

def log(string):
    print "--------------------------------------"
    print string
    print "--------------------------------------"
