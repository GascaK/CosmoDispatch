#!/usr/bin/env python
import os
import tkinter as tk
from tkinter import ttk


class CDUpdate(tk.Tk):
    def __init__(self, update_file):
        """ Cosmo Dispatch Update/Installer class.

        Update the CosmoDispatch application source code
        with information provided in predefined format from
        inside CD_update.txt file. This is to circumvent
        limitations in the ability to send .py extensions
        over email.

        Noteable Variables
        ------------------------------
        update_file - string
        File to load for update. Usually 'CD_update.txt'
        """
        # Standard location of local.
        location = ''
        tk.Tk.__init__(self)
        frame = tk.Frame()
        frame.pack()
        entry = tk.Text(frame, width=50, height=10)
        entry.pack()
        update_notes = False
        try:
            with open(update_file, 'r') as u_file:
                for line in u_file:
                    if line[:9] == '[UpNotes]' or update_notes == True:
                        if line[:9] == '[UpNotes]':
                            update_notes = True
                            version = line[9:]
                            self.title(f'Update # {version}')
                            continue
                        elif line[:9] == '[DnNotes]':
                            update_notes = False
                            continue
                        # Display Update Notes.
                        entry.insert(tk.END, line)
                    # Locate File Load location. Will return
                    elif line[:4] == '[FL]':
                        location = line[4:]
                        try:
                            os.remove(location[:-1])
                        # Catch FileNotFoundError while attempting to delete
                        # file at location. Continue as this works out.
                        except FileNotFoundError:
                            continue
                        continue  # skip the location line
                    # If location is not empty continue. Otherwise skip
                    # line assignment.
                    if location is not '':
                        self.run_update(location[:-1], line)
        # Catch FileNotFoundError while attempting to open CD_update.txt
        except FileNotFoundError:
            print('File was not located. Verify CD_update.'
                  'txt was downloaded correctly')

    def run_update(self, location, line):
        """ Update file at location with line

        Write line by line to the specific location listed.
        Point of friction as opening and closing the file seems
        tedious and may need refractoring.

        Noteable Variables
        ------------------------------
        location - string
        Location of file to be updated. If not found, create file
        then add 'line'.

        line - string
        String to append to file.
        """
        try:
            up_file = open(location, 'a')
        # Catch FileNotFoundError, if true then Create file first then
        # write line.
        except FileNotFoundError:
            result = location.find('\\')
            if not os.path.exists(location[:result]):
                print(f'Creating Directory: {location[:result]}')
                os.makedirs(location[:result])
            # Create file
            up_file = open(location, 'w')
        finally:
            up_file.write(line)
            up_file.close()


if __name__ == '__main__':
    cdi = CDUpdate('CD_update.txt')
    cdi.mainloop()
