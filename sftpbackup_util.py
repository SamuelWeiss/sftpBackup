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
         'destination':'None',
         'folder':'None'}

def backup_folder(connection_prefs):
    get_unknown(connection_prefs)

    #open a connection to the server
    connected = False
    while not connected:
        try:
            sftp = pysftp.Connection(connection_prefs['server'],
                                     username=connection_prefs['user'],
                                     password=connection_prefs['pass'])
            connected = True
        except Exception as e:
            print "The details you entered were not correct, please try again"
            for key in connection_prefs.keys():
                connection_prefs[key] = "None"
            get_unknown()



        if not sftp.isdir(connection_prefs['destination']):
            sftp.mkdir(connection_prefs['destination'])
        sftp.cd(connection_prefs['destination']);
                
        files = get_files_to_move(sftp, connection_prefs['folder'])

        #check if the file exists on the remote server and if it has been upated
        #this sync is 1 way, newer files will not be downloaded
        #pdb.set_trace()
        for e in files:
            print e
            try:
                sftp.put_r(e,e,preserve_mtime=True)
            except Exception as error:
                #attemped to move non directory with directory move
                sftp.put(e,e, preserve_mtime=True)


def read_prefs():
    prefs = {'max_size':1000000,
             'server':"None",
             'user':"None",
             'pass':"None",
             'destination':'None',
             'folder':'None'}

    try:
        f = open('sftpBackup_prefs', 'r')
    except Exception as e:
        log("No preference file found")
        return False, prefs
    temp = json.loads(f)
    if not 'max_size' in test:
        log("Error reading preference file, returning to defaults")
        return False, prefs
    prefs = temp
    return True, prefs

def store_prefs(store_pass):
    if not store_pass:
        prefs['pass'] = "None"
    f = open('sftpBackup_prefs', 'w')
    output = json.dumps(prefs, f)

def get_unknown(dict=prefs):
    for key in dict.keys():
        if dict[key] == 'None':
            if key == 'pass':
                dict[key] = getpass.getpass("Please enter your password: ")
            else:
                #maybe a way to print this pretty, can figure that out later
                dict[key] = raw_input("Please enter the " + key + " : ")
        
    
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
        e = dir + e
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
