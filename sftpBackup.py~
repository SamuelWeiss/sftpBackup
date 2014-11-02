###############################################################################
# sftpBackup.py
#
# by Sam Weiss
#
# a preliminary file to test the feasability of this project
###############################################################################

import sftpbackup_util as util
import getpass
import pysftp
import pdb

read_correctly = util.read_prefs()


print "Welcome to sftpBackup, a folder backup system written in python"
if read_correctly:
    print "Your previous preferences have been read"
else:
    print "No preference file was detected or there was an error loading it"
    print "You will now be asked to enter some information about the server you would like to sync with"



util.get_unknown()

#open a connection to the server
connected = False
while not connected:
    try:
        sftp = pysftp.Connection(util.prefs['server'],
                                 username=util.prefs['user'],
                                 password=util.prefs['pass'])
        connected = True
    except Exception as e:
        print "The details you entered were not correct, please try again"
        for key in util.prefs.keys():
            util.prefs[key] = "None"
        util.get_unknown()


if not sftp.isdir(util.prefs['destination']):
    sftp.mkdir(util.prefs['destination'])
sftp.cd(util.prefs['destination']);

files = util.get_files_to_move(sftp, '.')

#check if the file exists on the remote server and if it has been upated
#this sync is 1 way, newer files will not be downloaded
pdb.set_trace()
for e in files:
    print e
    try:
        sftp.put_r(e,e,preserve_mtime=True)
    except Exception as error:
        pdb.set_trace()
        #attemped to move non directory with directory move
        sftp.put(e,e, preserve_mtime=True)
        
print "Your files should have been moved successfully" #hopefully
store = raw_input("Would you like to store your preferences? [Y/n] ")
if store.lower() == 'y':
    print "Please note, storing your password is VERY insecure"
    store_pass = raw_input("Would you like to store your password? [Y/n] ")
    util.store_prefs(store_pass.lower() == 'y')
        
