import Tkinter
import ttk
import tkFileDialog

# root = Tk()
# l =ttk.Label(root, text="Starting...")
# l.grid()
# l.bind('<Enter>', lambda e: l.configure(text='Moved mouse inside'))
# l.bind('<Leave>', lambda e: l.configure(text='Moved mouse outside'))
# l.bind('<1>', lambda e: l.configure(text='Clicked left mouse button'))
# l.bind('<Double-1>', lambda e: l.configure(text='Double clicked'))
# l.bind('<B3-Motion>', lambda e: l.configure(text='right button drag to %d,%d' % (e.x, e.y)))
# root.mainloop()

root = Tkinter.Tk()
root.withdraw()

filename = tkFileDialog.askopenfilename(parent=root,title='Open file to encrypt')
print filename