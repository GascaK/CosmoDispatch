import tkinter as tk
from tkinter import ttk


class CosmoDirectory(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Cosmopolitan Directory')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        directory = ttk.Notebook(self)
        f1 = ttk.Frame(directory)
        f2 = ttk.Frame(directory)
        f3 = ttk.Frame(directory)
        f4 = ttk.Frame(directory)
        directory.add(f1, text='A - D')
        directory.add(f2, text='E - J')
        directory.add(f3, text='L - R')
        directory.add(f4, text='S - Z')

        self.a_d = tk.Text(f1, height=30, width=70)
        self.a_d.pack()
        self.a_d.insert(tk.END, self.load_file('direct/a_d.txt'))

        self.e_j = tk.Text(f2, height=30, width=70)
        self.e_j.pack()
        self.e_j.insert(tk.END, self.load_file('direct/e_j.txt'))

        self.l_r = tk.Text(f3, height=30, width=70)
        self.l_r.pack()
        self.l_r.insert(tk.END, self.load_file('direct/l_r.txt'))

        self.s_z = tk.Text(f4, height=30, width=70)
        self.s_z.pack()
        self.s_z.insert(tk.END, self.load_file('direct/s_z.txt'))

        directory.pack()

    def load_file(self, filepath):
        try:
            with open(filepath, mode='r') as in_read:
                return in_read.read()
        except FileNotFoundError as e:
            return f'Info Not FOUND. Check {filepath}'

    def save_file(self, filepath, info):
        try:
            with open(filepath, mode='w') as file:
                file.write(info)
        except FileNotFoundError:
            print('Unable to save to file. Verify file is not open?')

    def on_closing(self):
        self.save_file('direct/a_d.txt', self.a_d.get(1.0, 'end-1c'))
        self.save_file('direct/e_j.txt', self.e_j.get(1.0, 'end-1c'))
        self.save_file('direct/l_r.txt', self.l_r.get(1.0, 'end-1c'))
        self.save_file('direct/s_z.txt', self.s_z.get(1.0, 'end-1c'))
        self.destroy()


if __name__ == '__main__':
    cd = CosmoDirectory()
    cd.mainloop()
