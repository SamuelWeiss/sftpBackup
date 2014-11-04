###############################################################################
# sftpBackup.py
#
# by Sam Weiss
#
# a preliminary file to test the feasability of this project
###############################################################################

#our files
import sftpbackup_util as util
import gui

#standard lib
import pysftp
import pdb
import os
import sys
import time
import multiprocessing


#schedules should be in this form
example_prefs = {'max_size':1000000,
                 'server':"None",
                 'user':"None",
                 'pass':"None",
                 'destination':'None',
                 'folder':'None'}
example_schedule = [{'pattern':'repeating',
                    'time':3600, #in seconds - ?
                    'function':util.backup_folder_history,
                     'store':True,
                    'prefs':example_prefs},
                    {'pattern':'one-time',
                     'time':0,
                     'funciton':util.backup_folder_simple,
                     'store':False,
                     'prefs':example_prefs
                     }]

valid_patterns = ['repeating', 'one-time']
prefs_needed = ['max_size', 'server', 'user', 'pass', 'destination','folder']
task_elements = ['pattern', 'time', 'function', 'prefs', 'store']

def stand_in(var):
    print "hurr durr"

def main():
    parent_connection, child_connection = multiprocessing.Pipe()
    #launch the GUI first, we want to look responsive
    interface = multiprocessing.Process(target=gui.start, args=(child_connection,))
    #interface.start()
    #try to read preferences
    print "still running"
    read_success, schedule = util.read_prefs()
    worker_list=[]
    to_store=[]
    if read_success:
        worker_list = scheduler(schedule, worker_list)
    while interface.is_alive():
        temp = parent_connection.recv()
        message = confirm_schedule(temp)
        if message:
            parent_connection.send(message)
        else:
            if temp['store']:
                to_store=[]
            scheduler(temp, worker_list)
            worker_list = schedule.append(temp)
    util.store_prefs(to_store)

def confirm_schedule(testing):
    if testing.keys() != task_elements:
        return "task array was malformed"
    if testing['time'] < 0:
        #we can't handle negative times, that doesn't make sense
        return "Time is less than zero"
    if testing['pattern'] not in valid_patterns:
        #we don't support the given pattern
        return "Unsupported Pattern"
    if type(testing['function']) != type(main):
        return "Function error, wrong type: " + string(testing['function'])
    if testing['prefs'].keys() != prefs_needed:
        return "Preference array was malformed"
    if testing['prefs']['max_size'] < 100:
        return "Nonsense maximum file size"
    if not os.exists(testing['prefs']['folder']):
        return "Path does not exist"

    #create a test ssh connection
    try:
        test = pysftp.Connection(testing['prefs']['server'],
                                 username=testing['prefs']['user'],
                                 password=testing['prefs']['pass'])
    except Exception as e:
        util.log(e)
        return "Connection with given arguments failed"
    
    return None


def scheduler(schedule, worker_list=None):
    if not worker_list:
        worker_list = []
    for e in schedule:
        p = multiprocessing.Process(target=worker, args=(e))
        p.start()
        worker_list.append(p)
        #schedule.remove(e)
    return worker_list

def worker(task):
    if task['pattern'] == 'repeating' and task['time']>0:
        while True:
            task['function'](task['prefs'])
            time.sleep(task['time'])
            #TODO: change this to sleep until a time, not just sleep a certain amount of time
    elif task['pattern'] == 'one-time' and task['time']==0:
        task['function'](task['prefs'])
    else:
        util.log("Got something I couldn't handle!")
        util.log(task)

        
if __name__ == '__main__':
    main()


#old stuff I didn't quite feel like throwing away yet
    
'''
read_correctly, prefs = util.read_prefs()

util.log(prefs)
util.log(read_correctly)

print "Welcome to sftpBackup, a folder backup system written in python"
if read_correctly:
    print "Your previous preferences have been read"
else:
    print "No preference file was detected or there was an error loading it"
    print "You will now be asked to enter some information about the server you would like to sync with"

util.backup_folder_simple(prefs)
        
print "Your files should have been moved successfully" #hopefully
store = raw_input("Would you like to store your preferences? [Y/n] ")
if store.lower() == 'y':
    print "Please note, storing your password is VERY insecure"
    store_pass = raw_input("Would you like to store your password? [Y/n] ")
    util.store_prefs(store_pass.lower() == 'y')
'''
