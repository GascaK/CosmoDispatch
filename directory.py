import tkinter as tk
from tkinter import ttk

class CosmoDirectory(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Cosmopolitan Directory')
        
        directory = ttk.Notebook(self)
        f1 = ttk.Frame(directory)
        f2 = ttk.Frame(directory)
        f3 = ttk.Frame(directory)
        f4 = ttk.Frame(directory)
        directory.add(f1, text='A - D')
        directory.add(f2, text='E - J')
        directory.add(f3, text='L - R')
        directory.add(f4, text='S - Z')

        a_d = tk.Text(f1, height=30, width=70)
        a_d.pack()
        a_d.insert(tk.END, self.load_file('direct/a_d.txt'))

        e_j = tk.Text(f2, height=30, width=70)
        e_j.pack()
        e_j.insert(tk.END, self.load_file('direct/e_j.txt'))

        l_r = tk.Text(f3, height=30, width=70)
        l_r.pack()
        l_r.insert(tk.END, self.load_file('direct/l_r.txt'))

        s_z = tk.Text(f4, height=30, width=70)
        s_z.pack()
        s_z.insert(tk.END, self.load_file('direct/s_z.txt'))

        directory.pack()

    def load_file(self, filepath):
        try:
            with open(filepath, mode='r') as in_read:
                return in_read.read()
        except FileNotFoundError as e:
            raise

if __name__ == '__main__':
    cd = CosmoDirectory()
    cd.mainloop()

