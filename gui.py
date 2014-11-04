from Tkinter import *
import ttk
import multiprocessing
import sftpbackup_util as util
import tkFileDialog


root = Tk()
root.title("SFTP Backup")
mainframe = ttk.Frame(root, padding="3 3 12 12")

dictionary = {}

servername_var=StringVar()
destination_var=StringVar()
username_var=StringVar()
password_var=StringVar()
pattern_var=StringVar()
function_var=StringVar()
frequency_var=IntVar()
frequency_units_var=StringVar()
maxsize_var=StringVar()
maxsize_units_var=StringVar()
folder_var=StringVar()
store_var = BooleanVar()
bool_var = BooleanVar()
bool_var=False

def submit():
        response = pack_response()
        bool_var = True
        return response

def browse():
        filename = tkFileDialog.askopenfilename(parent=mainframe, title="Select Folder to Back Up")
        root.withdraw()
        folder_var = filename
        folder_var['text'] = filename
        print filename

def pack_response():
        response = {#'pattern'   : pattern_var.get(),
                    'pattern'    : "one-time",
                    'time'      : to_seconds(int(frequency_var.get())),
                    #'function'  : function_var.get(),
                    'function'  : util.backup_folder_simple,
                    'store'     : store_var.get(),
                    'prefs'     : pack_prefs() }
        return response


def pack_prefs():
        preferences = {'maxsize': to_bytes(int(maxsize_var.get())),
                       'server' : servername_var.get(),
                       'user'   : username_var.get(),
                       'pass'   : password_var.get(),
                   'destination': destination_var.get(),
                       'folder' : folder_var.get() }

        return preferences

def to_seconds(time):
        convert = {'seconds'    : 1,
                   'minutes'    : 60,
                   'hours'      : 60*60,
                   'days'       : 60*60*24,
                   'weeks'      : 60*60*24*7,
                   'months'     : 60*60*24*7*4,
                   'years'      : 60*60*24*7*4*12 }

        return time/convert[frequency_units_var.get()]

def to_bytes(size):
        convert = {'bytes'      : 1,
                   'kilobytes'  : 1000,
                   'megabytes'  : 1000000,
                   'gigabytes'  : 1000000000,
                   'terabytes'  : 1000000000000 }

        return int(maxsize_var.get())/convert[maxsize_units_var.get()]

def start(child_connection):


        
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
        ttk.Entry(mainframe, textvariable=folder_var).grid(row=3, column=5)
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
        

start(0)

