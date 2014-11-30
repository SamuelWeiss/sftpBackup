from Tkinter import *
import ttk
import multiprocessing
import sftpbackup_util as util
import tkFileDialog

#------------------------------------------------------------------------------#
# It is a limitation of Tk that functions attached to widgets as commands may
# not be called with any arguements. Therefore, it is necessary for any
# variable that must be accessed within these functions to have global scope.
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                             global declarations
#------------------------------------------------------------------------------#

root = Tk()
mainframe = ttk.Frame(root, padding="3 3 12 12")

connection = {}


servername_var      = StringVar() # the name of the server to which files will
                                  # be backed up
destination_var     = StringVar() # the folder within the server to which files
                                  # will be backed up
username_var        = StringVar() # the username for the server connection
password_var        = StringVar() # the password for the server connection
pattern_var         = StringVar() # the backup pattern
function_var        = StringVar() # the backup function


frequency_var       = IntVar()    # the frequency with which the files should
                                  # be backed up
frequency_units_var = StringVar() # the units for frequency_var


maxsize_var         = StringVar() # the maximum total filesize the user wants
                                  # allow to be backed up
maxsize_units_var   = StringVar() # the units for maxsize_var

store_var           = BooleanVar() # the store var

folder_var          = StringVar() # the folder to be backed up
folder = ttk.Label(mainframe, text=folder_var)

#------------------------------------------------------------------------------#
#                            auxiliary functions
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
# submit():
#
# Packs a response in the correct format to send to the main thread, and sends
# the response. Called when the user presses the submit button.
#
# return value: no return value
#------------------------------------------------------------------------------#
def submit():
        response = pack_response()
        connection['connection'].send(response)

#------------------------------------------------------------------------------#
# browse():
#
# Opens a file dialogue (i.e. finder on apple products, explorer on windows
# products) and allows the user to select which folder he or she wishes to back
# up. Called when the user presses the browse button.
#
# return value: no return value
#------------------------------------------------------------------------------#
def browse():
        filename = tkFileDialog.askdirectory(parent=mainframe, title="Select Folder to Back Up")
        folder_var = filename
        folder.configure(text=filename)

#------------------------------------------------------------------------------#
# pack_response():
#
# Constructs a response to be sent to the main thread. Called by submit().
#
# return value: response, a dictionary containing the settings indicated by the
#               user, to be sent to the main thread.
#------------------------------------------------------------------------------#
def pack_response():
        response = {#'pattern'   : pattern_var.get(),
                    'pattern'   : "one-time",
                    'time'      : to_seconds(int(frequency_var.get())),
                    #'function'  : function_var.get(),
                    'function'  : util.backup_folder_simple,
                    'store'     : store_var.get(),
                    'prefs'     : pack_prefs() }
        return response

#------------------------------------------------------------------------------#
# pack_prefs():
#
# Constructs preferences to be stored in a response. Called by pack_response().
#
# return value: preferences, a dictionary containing settings indicated by the
#               by the user, to be added to a response
#------------------------------------------------------------------------------#
def pack_prefs():
        preferences = {'maxsize': to_bytes(int(maxsize_var.get())),
                       'server' : servername_var.get(),
                       'user'   : username_var.get(),
                       'pass'   : password_var.get(),
                   'destination': destination_var.get(),
                       'folder' : folder_var.get() }

        return preferences

#------------------------------------------------------------------------------#
# to_seconds(time):
#
# Converts time from whichever unit the user has indicated to seconds. Called
# by pack_response().
#
# time: the value to be converted to seconds
#
# return value: time converted to seconds
#------------------------------------------------------------------------------#
def to_seconds(time):
        convert = {'seconds'    : 1,
                   'minutes'    : 60,
                   'hours'      : 60*60,
                   'days'       : 60*60*24,
                   'weeks'      : 60*60*24*7,
                   'months'     : 60*60*24*7*4,
                   'years'      : 60*60*24*7*4*12 }

        return time/convert[frequency_units_var.get()]

#------------------------------------------------------------------------------#
# to_bytes(size):
#
# Converts size from whichever unit the user has indicated to bytes. Called by
# pack_prefs().
#
# size: the value to be converted to bytes
#
# return value: size converted to bytes
#------------------------------------------------------------------------------#
def to_bytes(size):
        convert = {'bytes'      : 1,
                   'kilobytes'  : 1000,
                   'megabytes'  : 1000000,
                   'gigabytes'  : 1000000000,
                   'terabytes'  : 1000000000000 }

        return int(maxsize_var.get())/convert[maxsize_units_var.get()]

#------------------------------------------------------------------------------#
# start(child_connection):
#
# Invoked by the main thread; generates the GUI.
#
# child_connection: the connection passed from the main thread -- a response
#                   will be sent to this connection using
#                   child_connection.send(response)
#
# return value: no return value
#------------------------------------------------------------------------------#

def start(child_connection):
        root.title("SFTP Backup")
        connection['connection'] = child_connection
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="-- Server information --").grid(column=1, row=1)


        ttk.Label(mainframe, text="Server Name").grid(row=2, column=1)
        ttk.Entry(mainframe, textvariable=servername_var).grid(row=3, column=1, sticky=E)

        ttk.Label(mainframe, text="Destination").grid(row=2, column=2)
        ttk.Entry(mainframe, textvariable=destination_var).grid(row=3, column=2, sticky=W)

        ttk.Label(mainframe, text="Username").grid(row=5, column=1)
        ttk.Entry(mainframe, textvariable=username_var).grid(row=6, column=1)

        ttk.Label(mainframe, text="Password").grid(row=5, column=2)
        ttk.Entry(mainframe, textvariable=password_var, show="*").grid(row=6, column=2)


        ttk.Label(mainframe, text="-- Backup Settings --").grid(column=3, row=1)


        ttk.Label(mainframe, text="Pattern").grid(row=2, column=3)
        pattern_box = ttk.Combobox(mainframe, textvariable=pattern_var)
        pattern_box.grid(row=3, column=3)
        pattern_box['values']=('repeating', 'one-time')

        ttk.Label(mainframe, text="Function").grid(row=2, column=4)
        function_box = ttk.Combobox(mainframe, textvariable=function_var)
        function_box.grid(row=3, column=4)
        function_box['values'] = ('backup folder history', 'backup folder simple')

        ttk.Label(mainframe, text="Frequency").grid(row=5, column=3)
        ttk.Entry(mainframe,textvariable=frequency_var).grid(row=6, column=3)
        frequency_units = ttk.Combobox(mainframe, textvariable=frequency_units_var)
        frequency_units.grid(row=7, column=3)
        frequency_units['values'] = ('seconds', 'minutes', 'hours', 'weeks', 'months')

        ttk.Label(mainframe, text="Max Size").grid(row=5, column=4)
        ttk.Entry(mainframe,textvariable=maxsize_var).grid(row=6, column=4)
        maxsize_units = ttk.Combobox(mainframe, textvariable=maxsize_units_var)
        maxsize_units.grid(row=7, column=4)
        maxsize_units['values'] = ('bytes', 'kilobytes', 'megabytes', 'gigabytes', 'terabytes')

        ttk.Label(mainframe, text="Folder to back up").grid(row=2, column=5)
        folder.grid(row=3, column=5)
        folder.configure(text="")

        ttk.Button(mainframe, text="Browse", command=browse).grid(row=4, column=5)

        ttk.Label(mainframe, text="Valid?").grid(row=6, column=5, sticky=W)
        ttk.Label(mainframe, text="IDK!").grid(row=6, column=5)

        ttk.Button(mainframe, text="EXECUTE", command=submit).grid(row=7, column=5)

        ttk.Radiobutton(mainframe, text="yes", variable=store_var, value=True).grid(row=5, column=5)
        ttk.Radiobutton(mainframe, text="no", variable=store_var, value=False).grid(row=5,column=5, sticky=E)
        ttk.Label(mainframe, text="Store?").grid(row=5, column=5, sticky=W)

        for child in mainframe.winfo_children():
                child.grid_configure(padx=5, pady=5)

        root.mainloop()

#------------------------------------------------------------------------------#
# if gui.py is run directly, manually generate the GUI
#------------------------------------------------------------------------------#
if __name__ == '__main__':
	start(0)
