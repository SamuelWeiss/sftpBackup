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
import time
import logging

#-----------------------------------------------------------------------------#
#
# If this file is being run as main then we want to print out log messages.
# This is useful for debugging, but in standard cases when this file is not
# main we want our messages to be logged to a file.
#
#-----------------------------------------------------------------------------#
if __name__ != '__main__':
    logging.basicConfig(filename='backup.log', level=logging.DEBUG)


#-----------------------------------------------------------------------------#
# pref
#
# Below is the prototype preferences object, it contains all of the information
# needed to connect to a server and backup a folder. If any of its values are
# "None", then it is not considered complete and cannot be used. It contains:
#
#  * max_size: the maximum size in bytes of a file that is considered ok to move
#  * server: the ip or address of the destination ssh server
#  * user: the username of the user to try and connect to the server as
#  * pass: the password that should be used when trying to connect
#  * destination: the destination folder on the remote server to move the files to
#  * folder: the local folder to move files to and from
#
# Usage: This data structure is designed to be passed to one of the backup
# functions and therefore does not contain the information as to which function
# it is to be used with.
#-----------------------------------------------------------------------------#
prefs = {'max_size':1000000,
         'server':"None",
         'user':"None",
         'pass':"None",
         'destination':'None',
         'folder':'None'}

#-----------------------------------------------------------------------------#
# backup_folder_simple(connection_prefs):
#
# performs a single simple backup to a remote server moving all new files in
# accordance with the preference object given. It is called in sftpBackup.py
#
# connection_prefs: contains the information stated above
#
# TODO: check prefs to make sure they're ok
#-----------------------------------------------------------------------------#
def backup_folder_simple(connection_prefs):
    #open a connection to the server
    try:
        sftp = pysftp.Connection(connection_prefs['server'],
                                 username=connection_prefs['user'],
                                 password=connection_prefs['pass'])
    except Exception as e:
        log("Something went wrong!")
        log(e)

    if not sftp.isdir(connection_prefs['destination']):
        sftp.mkdir(connection_prefs['destination'])
    sftp.cd(connection_prefs['destination']);
        
    files = get_files_to_move(sftp, connection_prefs['folder'])

        #check if the file exists on the remote server and if it has been upated
        #this sync is 1 way, newer files will not be downloaded
    for e in files:
        print e
        try:
            sftp.put_r(e,e,preserve_mtime=True)
        except Exception as error:
                #attemped to move non directory with directory move
            sftp.put(e,e, preserve_mtime=True)

#-----------------------------------------------------------------------------#
# backup_folder_history(connection_prefs):
#
# performs a backup of the local folder to the remote server in a new folder
# indicating the date and time of the backup. It is called as a process in
# sftpBackup.py
#
# connection_prefs: a connection preference object as specified above.
#
# TODO: add some sort of total size limit/old version clearing
#-----------------------------------------------------------------------------#
def backup_folder_history(connection_prefs):

    #open a connection to the server
    try:
        sftp = pysftp.Connection(connection_prefs['server'],
                                 username=connection_prefs['user'],
                                 password=connection_prefs['pass'])
    except Exception as e:
        log("Something went wrong!")
        log(e)
        #made sure the base folder is there
    if not sftp.isdir(connection_prefs['destination']):
        sftp.mkdir(connection_prefs['destination'])
    sftp.cd(connection_prefs['destination']);
        
        #make a folder with the time of the backup
    temp_dest = connection_prefs['destination'] + "/" + time.asctime().replace(' ', '_')
    if not sftp.isdir(temp_dest):
        sftp.mkdir(temp_dest)
    sftp.cd(temp_dest);

    files = get_target_dir_clean(connection_prefs['folder'])

        #check if the file exists on the remote server and if it has been upated
        #this sync is 1 way, newer files will not be downloaded
        #pdb.set_trace()
    for e in files:
        try:
            sftp.put_r(e,e,preserve_mtime=True)
        except Exception as error:
                #attemped to move non directory with directory move
            sftp.put(e,e, preserve_mtime=True)

#-----------------------------------------------------------------------------#
# read_prefs():
#
# Reads the JSON preference file if one exists. Called in main():
#
# 
# returns:
#    * True, then an array containing a list of preference dictionaries
#                                  -- or --
#    * False, then an empty array
#-----------------------------------------------------------------------------#
def read_prefs():
    prefs = {}
    try:
        f = open('.sftpBackup_prefs', 'r')
    except Exception as e:
        log("No preference file found", type='info')
        return False, prefs
    try:
        temp = json.loads(f)
    except Exception as e:
        log("Error reading preference file", type='warn')
        log(e)
        return False, prefs
    if not 'max_size' in test: #TODO: What is this doing?
        log("Error reading preference file, returning to defaults", type='warn')
        return False, prefs
    prefs = temp
    return True, prefs

#-----------------------------------------------------------------------------#
# store_prefs(object):
#
# Stores the provided object as json in a file called .sftpBackup_prefs.
# Called in main():
#
# returns nothing
#-----------------------------------------------------------------------------#
def store_prefs(object):
    f = open('.sftpBackup_prefs', 'w')
    output = json.dumps(object, f)

#-----------------------------------------------------------------------------#
# get_target_dir_clean(dir):
#
# Gets a list of files in a specified directory that can be moved. Called by
# get_files_to_move().
#
# dir: a string that indicates which directory to look at
#
# returns: an array containing all of the valid filenames in the specified
# directory.
#-----------------------------------------------------------------------------#    
def get_target_dir_clean(dir):
    if not os.path.isdir(dir):
        log("Attempted to scan a dir that did not exist \n " + dir, type='warn')
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

#-----------------------------------------------------------------------------#
# get_files_to_move(sftp, dir):
# 
# Gets a list of files which need to be moved to the remote server. Called by
# the backup functions.
#
# sftp: an sftp connection object pointing to the target directory on the remote
# server.
# dir: the local directory that is going to be synced.
#
# returns: a list of files in the local directory that are valid to move and have
# newer versions on the local machine than their server conterparts.
#
# TODO: add some way to omit specific files
#-----------------------------------------------------------------------------#
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
    return target


#-----------------------------------------------------------------------------#
# log(string, type):
# 
# Logs a given string with a given type. Called when different messages are 
# generated.
#
# string: the string to be logged
# type: the type or level at which to log the string, defaults to warn
#
# TODO: add more types
# TODO: Do we even need this?
#-----------------------------------------------------------------------------#
def log(string, type='warn'):
    if type == 'warn':
        logging.warning(string)
    else:
        logging.info(string)
