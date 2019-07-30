from tkinter import *
from tkinter import ttk
import time


class PadInformation(Tk):
    def __init__(self):
        """ Pad Tracker window.

        Launch the PAD Tracker Application. Saves information to
        padInfo.txt in local directory.

        TODO
        ------------------------------
        Alter source to fit better with current project dynamics.
        """
        super().__init__()
        self.geometry('{}x{}'.format(425, 185))
        self.title('PAD Tracker')
        self.frame = Frame(self)
        self.populateFields()
        self.frame.pack()

    def populateFields(self):
        issue = ttk.Label(self.frame, text='Issue dispatched for PAD:')
        issue.grid(row=1, column=0)

        self.call_type = Text(self.frame,
                              width=50,
                              height=3)
        self.call_type.grid(row=2, column=0)

        place = ttk.Label(self.frame, text='Location dispatched to:')
        place.grid(row=3, column=0)

        self.call_place = Text(self.frame,
                               width=50,
                               height=3)
        self.call_place.grid(row=4, column=0)

        enter = ttk.Button(self.frame,
                           text='Update Records',
                           command=self.on_button)
        enter.grid(row=5, column=0)

        self.call_type.bind('<Tab>', self.ch_focus)
        self.call_type.bind('<Return>', lambda e: 'break')
        self.call_place.bind('<Tab>', lambda e: 'break')
        self.call_place.bind('<Return>', self.on_button)

    def on_button(self, event):
        self.save_text(self.call_type.get(1.0, 'end-1c'),
                       self.call_place.get(1.0, 'end-1c'))
        self.call_type.delete(1.0, 'end')
        self.call_place.delete(1.0, 'end')

        self.call_type.focus()
        return 'break'

    def ch_focus(self, event):
        self.call_place.focus()
        return 'break'

    def save_text(self, types, place):
        with open('padInfo.txt', 'a', encoding='utf8') as padInfo:
            padInfo.write('{} at {} @ {}\n'.format(
                    types,
                    place,
                    time.asctime(time.localtime(time.time()))))


if __name__ == '__main__':
    bi = PadInformation()
    bi.mainloop()
