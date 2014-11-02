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
prefs = {'max_size':1000000,
         'server':"None",
         'user':"None",
         'pass':"None",
         'destination':'None'}


def read_prefs():
    try:
        f = open('sftpBackup_prefs', 'r')
    except Exception as e:
        log("No preference file found")
        return False
    temp = json.loads(f)
    if not 'max_size' in test:
        log("Error reading preference file, returning to defaults")
        return False
    prefs = temp
    return True

def store_prefs(store_pass):
    if not store_pass:
        prefs['pass'] = "None"
    f = open('sftpBackup_prefs', 'w')
    output = json.dumps(prefs)

def get_unknown():
    for key in prefs.keys():
        if prefs[key] == 'None':
            if key == 'pass':
                prefs[key] = getpass.getpass("Please enter your password: ")
            else:
                #maybe a way to print this pretty, can figure that out later
                prefs[key] = raw_input("Please enter the " + key + " : ")
            
    '''
    #not super pretty, we can do better in python
    if util.prefs['server'] == "None":
        util.prefs['server'] = raw_input("Please enter the server name or ip: ")
    if util.prefs['user'] == "None":
        util.prefs['user'] = raw_input("Please enter your username: ")
    if prefs['pass'] == "None":
        prefs['pass'] = getpass.getpass("Please enter your password: ")
    if prefs['destination'] == "None":
        util.prefs['destination'] = getpass.getpass("Please enter your password: ")
    '''

def get_target_dir_clean(dir):
    if not os.path.isdir(dir):
        log("Attempted to scan a dir that did not exist \n " + dir)
        sys.exit(1)
    currentdir = os.listdir(dir)
    for e in currentdir:
        if e[0] == '.' or e[0] == '#':
            currentdir.remove(e)
            continue
        if os.path.getsize(e) > prefs['max_size']:
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
    #TODO: figure out some better way to do this
    print "--------------------------------------"
    print string
    print "--------------------------------------"
