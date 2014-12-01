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
#-----------------------------------------------------------------------------#
#
# For a complete explanation of this data structure please see the util file
#
#-----------------------------------------------------------------------------#
example_prefs = {'max_size':1000000,
                 'server':"None",
                 'user':"None",
                 'pass':"None",
                 'destination':'None',
                 'folder':'None'}

#-----------------------------------------------------------------------------#
# example_schedule
#
# This is an example of what a schedule object should contain. It is an array
# containing individual backups, which each contain the following:
#  * pattern: either repeating or one time, this is a string
#  * time: indicated the number of seconds between backups to sleep for
#  * function: stores the function that should be called when the backup is
#      performed
#  * store: a boolean value indicating if the preferences should be stored
#  * prefs: a connection preference like the one given above
#
# TODO: make this an object - why did I not do that to start?
#-----------------------------------------------------------------------------#
example_schedule = [{'pattern':'repeating',
                     'time':3600, #in seconds - ?
                     'function':util.backup_folder_history,
                     'store':True,
                     'prefs':example_prefs
                     },
                    {'pattern':'one-time',
                     'time':0,
                     'funciton':util.backup_folder_simple,
                     'store':False,
                     'prefs':example_prefs
                     }]

#-----------------------------------------------------------------------------#
#
# These three variables contain all of the possible values for some other variables
# They are used to make sure that the fields are valid.
#
#-----------------------------------------------------------------------------#
valid_patterns = ['repeating', 'one-time']
prefs_needed = ['max_size', 'server', 'user', 'pass', 'destination','folder']
task_elements = ['pattern', 'time', 'function', 'prefs', 'store']

#-----------------------------------------------------------------------------#
# main():
#
# A central process that manages all of the other processes that go on. There
# are three types of processes that can run, a process that drives the Graphical
# User Interface, which is called interface, worker processes, and this process,
# which directs all of the other processes. We chose this structure because it
# allows for our interface to close and be killed without interupting our
# backup functionality, so backups will continue even if the user has quit the
# interface. It also has led to a more modular design where each connection and
# each backup is isolated in its own process, with limited communication with 
# the main thread. The purpose of the main thread is to wait for input from the
# interface and to start new processes when valid input has been given.
# when the interface exit, this process is considered compelte and this function
# will exit, storing preferences that have been marked accordingly.
#-----------------------------------------------------------------------------#
def main():
    parent_connection, child_connection = multiprocessing.Pipe()
    #launch the GUI first, we want to look responsive
    interface = multiprocessing.Process(target=gui.start, args=(child_connection,))
    interface.start()
    #try to read preferences
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

#-----------------------------------------------------------------------------#
# confirm_schedule(testing):
#
# makes sure that a given schedule is valid. Called in main()
#
# testing: the schedule data that is to be tested
#
# returns: either a string containing an error message or None
#
# TODO: should this go in the util file?
#-----------------------------------------------------------------------------#
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

#-----------------------------------------------------------------------------#
# scheduler(schedule, worker_list):
#
# Creates processes to handle a given schedule and makes sure they run called by main()
#
# schedule: a list of schedules like the example above.
# worker_list: either a list of workers who have already been started or nothing
# 
# returns: an array containing all of the processes
#-----------------------------------------------------------------------------#
def scheduler(schedule, worker_list=None):
    if not worker_list:
        worker_list = []
    for e in schedule:
        p = multiprocessing.Process(target=worker, args=(e))
        p.start()
        worker_list.append(p)
        #schedule.remove(e)
    return worker_list

#-----------------------------------------------------------------------------#
# worker(task):
#
# A simple function designed to handle a single task. It exists so that the
# scheduler can simply spin up a thread of a single function, after which the
# the process will be able to handle itself. Called by scheduler()
#
# task: a schedule data structure as seen above.
#
# returns: nothing
#-----------------------------------------------------------------------------#
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