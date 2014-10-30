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

util.read_prefs()

if util.prefs['server'] == "None":
    util.prefs['server'] = raw_input("Please enter the server name or ip: ")
if util.prefs['user'] == "None":
    util.prefs['user'] = raw_input("Please enter your username: ")
if util.prefs['pass'] == "None":
    util.prefs['pass'] = getpass.getpass("Please enter your password: ")

#open a connection to the server
sftp = pysftp.Connection(server, username=username, password=passwd)

if not sftp.isdir("Desktop/sftptesting"):
    sftp.mkdir("Desktop/sftptesting")
sftp.cd("Desktop/sftptesting");

files = get_files_to_move(sftp, dir)

#check if the file exists on the remote server and if it has been upated
#this sync is 1 way, newer files will not be downloaded
for e in files:
    print e
    try:
        sftp.put_r(e,e,preserve_mtime=True)
    except Exception as error:
        pdb.set_trace()
        #attemped to move non directory with directory move
        sftp.put(e,e, preserve_mtime=True)
        
print "success!" #hopefully

