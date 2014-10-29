###############################################################################
# sftpBackup.py
#
# by Sam Weiss
#
# a preliminary file to test the feasability of this project
###############################################################################

import pysftp
import getpass
import os
import pdb
import json


#get information to connect to test server
server = "50.168.87.85"
username="Sam"
passwd = getpass.getpass("Please enter your password: ")

#list what's in our current directory
currentdir = os.listdir('.')
for e in currentdir:
    if e[0] == '.' or e[0] == '#':
        currentdir.remove(e)
    else:
        print e

#open a connection to the server
sftp = pysftp.Connection(server, username=username, password=passwd)

if not sftp.isdir("Desktop/sftptesting"):
    sftp.mkdir("Desktop/sftptesting")
sftp.cd("Desktop/sftptesting");

#pull down information on the remote files
#only look at files we want and put them in a dictionary for later
remote_files = sftp.listdir_attr()
remote_modified = {}
for e in remote_files:
    name = e.filename
    if name[0] != '.' and name[0] != '#':
        remote_modified[name] = e.st_mtime

#check if the file exists on the remote server and if it has been upated
#this sync is 1 way, newer files will not be downloaded
for e in currentdir:
    if sftp.isfile(e):
        local_mod = os.stat(e).st_mtime
        remote_mod = remote_modified[e]
        if local_mod <= remote_mod:
            currentdir.remove(e)
    else:
        #push to the remote
        print e
        try:
            sftp.put_r(e,e,preserve_mtime=True)
        except Exception as error:
            pdb.set_trace()
            #attemped to move non directory with directory move
            sftp.put(e,e)

print "success!" #hopefully

