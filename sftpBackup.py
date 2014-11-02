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

read_correctly, prefs = util.read_prefs()

util.log(prefs)
util.log(read_correctly)

print "Welcome to sftpBackup, a folder backup system written in python"
if read_correctly:
    print "Your previous preferences have been read"
else:
    print "No preference file was detected or there was an error loading it"
    print "You will now be asked to enter some information about the server you would like to sync with"

util.backup_folder(prefs)
        
print "Your files should have been moved successfully" #hopefully
store = raw_input("Would you like to store your preferences? [Y/n] ")
if store.lower() == 'y':
    print "Please note, storing your password is VERY insecure"
    store_pass = raw_input("Would you like to store your password? [Y/n] ")
    util.store_prefs(store_pass.lower() == 'y')
        
