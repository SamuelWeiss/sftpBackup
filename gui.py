from Tkinter import *
import ttk
import multiprocessing
import sftpbackup_util as util


def browse():
        print "browsing"

def submit(child_connection):
        response = pack_response()
        child_connection.send(response)

def pack_response():
        response = {'pattern'   : pattern_var.get(),
                    'time'      : frequency_var.get(),
                    'function'  : function_var.get(),
                    'store'     : store_var.get(),
                    'prefs'     : pack_prefs()
                   }
        return response


def pack_prefs():
        prerencesfs = {'maxsize': maxsize_var.get()
                       'server' : servername_var.get()
                       'user'   : username_var.get()
                       'pass'   : password_var.get()
                   'destination': destination_var.get()
                       'folder' : folder_var.get()
                      }

        return prefs

def display_error(error):
        function()

def start(child_connection):
        root = Tk()
        root.title("SFTP Backup")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        servername_var=StringVar()
        destination_var=StringVar()
        username_var=StringVar()
        password_var=StringVar()
        pattern_var=StringVar()
        function_var=StringVar()
        frequency_var=StringVar()
        frequency_units_var=StringVar()
        maxsize_var=StringVar()
        maxsize_units_var=StringVar()
        folder_var=StringVar()
        store_var = StringVar()


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
        pattern_box = ttk.Combobox(mainframe, textvariable=pattern_var).grid(row=3, column=3)

        ttk.Label(mainframe, text="Function").grid(row=2, column=4)
        function_box = ttk.Combobox(mainframe, textvariable=function_var).grid(row=3, column=4)

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

        ttk.Button(mainframe, text="EXECUTE", command=submit).grid(row=6, column=5)



        for child in mainframe.winfo_children():
                child.grid_configure(padx=5, pady=5)




        root.mainloop()


