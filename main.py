 import load_info as loIn
import tkinter as tk
from tkinter import ttk
from time import sleep
from os import startfile
from PAD import PadInformation
from directory import CosmoDirectory
from automate_it import AutomateIt, UnableToLocateError
from breakCalculator import BreakCalculator


class CosmoDispatch(tk.Tk):
    def __init__(self):

        self.app = AutomateIt()
        self.Engineer_List = ['John Doe', 'Jane Doe']

        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(330, 260))
        self.title('Cosmo Dispatch')

        menu = tk.Menu(self)
        scripts = tk.Menu(menu, tearoff=0)
        file = tk.Menu(menu, tearoff=0)
        file.add_command(label='Change Passwords',command=self.chg_pass)
        menu.add_cascade(label='File', menu=file)
        scripts.add_command(label="Assign PRV's", command=self.load_prvs)
        scripts.add_command(label='Fan Coils', command=self.load_fcu)
        scripts.add_command(label='Calculate Breaks', command=self.load_breaks)
        menu.add_cascade(label='Scripts', menu=scripts)
        menu.add_command(label='Quit!', command=self.quit)
        self.config(menu=menu)

        frame = tk.Frame()
        frame.pack()
        self.after(30000, self.check_timeout)
        
        ttk.Label(frame, text='Click to Launch').grid(row=0, column=0, columnspan=2)
        hotsos_but = ttk.Button(frame, text='HotSOS', command=self.load_hotsos)
        hotsos_but.grid(row=1, column=0)

        lms_but = ttk.Button(frame, text='LMS', command=self.load_lms)
        lms_but.grid(row=1, column=1)

        pad_track = ttk.Button(frame, text='PAD Tracker', command=self.pad_tracker)
        pad_track.grid(row=2, column=0)

        cosmo_direct = ttk.Button(frame, text='Directory', command=self.cosmo_directory)
        cosmo_direct.grid(row=2, column=1)

        self.hotsos_logout = ttk.Checkbutton(frame, text='Prevent Logoff')
        self.hotsos_logout.grid(row=3, columnspan=2)

        self.info_win = tk.Text(frame, width=40, height=10)
        self.info_win.grid(row=4, columnspan=2)

    def chg_pass(self):
        ''' chg_pass()
            Change Username and password information.
        '''
        popup = tk.Toplevel()
        popup.title('Change Login Info')

        ttk.Label(popup, text='Hotsos User').grid(row=0, column=0)
        hot_user = ttk.Entry(popup, width=15)
        hot_user.grid(row=0, column=1)

        ttk.Label(popup, text='Hotsos Pass').grid(row=1, column=0)
        hot_pass = ttk.Entry(popup, show='*', width=15)
        hot_pass.grid(row=1, column=1)

        ttk.Label(popup, text='LMS User').grid(row=2, column=0)
        lms_user = ttk.Entry(popup, width=15)
        lms_user.grid(row=2, column=1)

        ttk.Label(popup, text='LMS Pass').grid(row=3, column=0)
        lms_pass = ttk.Entry(popup, show='*', width=15)
        lms_pass.grid(row=3, column=1)

        enter = ttk.Button(popup, text='Change', 
                           command=lambda: [loIn.save_data(hot_user.get(),
                                                           hot_pass.get(),
                                                           lms_user.get(),
                                                           lms_pass.get()),
                                            popup.destroy()])
        enter.grid(row=4, columnspan=2)

    def load_hotsos(self):
        '''load_hotsos()
            Launch and login to hotsos. Load information at time of execution.
            TODO: Create breakpoints for invalid login.
        '''
        self.add_log('* Standby...\nLoading Hotsos.')
        startfile(r'C:\Program Files (x86)\MTech\hotsos\client_na2\HotSOS.exe')
        sleep(1)
        self.app.window_activate(window='Login')
        self.app.type_info(loIn.load_data('hot_user'), wait=2)
        self.app.type_info('tab')
        self.app.type_info(loIn.load_data('hot_pass'))
        self.app.type_info('enter', wait=3)
        self.app.find('screens/orders_console_hot.png')
        self.app.type_info('tab')
        self.app.type_info('FAC - *')
        self.app.type_info('enter')
        self.app.type_info('enter')
        self.add_log('Complete!')

    def load_lms(self):
        '''load_lms()

        '''
        self.add_log('* Standby...\nLoading LMS')
        startfile(r'C:\Users\Public\Desktop\LMS.ws')
        sleep(2)
        if self.app.window_activate('IBM i signon'):
            self.app.type_info(loIn.load_data('lms_pass'))
            sleep(1)

        if self.app.window_activate(window='PC5250'):
            self.app.type_info('enter')
            sleep(1)
            self.app.window_activate(window='Session A -')
            try:
                self.app.find('screens/as400.png')
            except UnableToLocateError as e:
                self.add_log(f'Unable to Locate: {e}\nLMS did NOT complete. *')
                return False
            for each in (['enter', 'alt', 'f', 'o', 'AS400.kmp', 'enter', 'alt',
                         'f', 'x', 'enter']):
                self.app.type_info(each)
            sleep(2)

        if self.app.window_activate(window='Session A -'):
            for each in (loIn.load_data('lms_user'), 'tab', loIn.load_data('lms_pass'),
                         'enter', '1', 'enter', 'enter'):
                self.app.type_info(each)
            self.add_log('Complete! *')
            return True
        else:
            self.add_log('LMS did NOT complete! *')
            return False

    def check_timeout(self):
        '''check_timeout()
            Check if window Auto Logout exists and keeps hotsos logged in.
        '''
        if self.hotsos_logout.instate(['selected']) and self.app.window_activate(window='Auto Logout'):
            self.app.type_info('enter')
            self.add_log('**Timeout Reset**')
        self.after(25000, self.check_timeout)

    def load_fcu(self):
        '''load_fcu()
            Prompt and assign Fan Coil units to Engineers.
        '''
        def attach_fcus(engineer, floor, tower, fcu_amt):
            '''attach_fcus(engineer, floor, tower, fcu_amt)
                Send insert_new_issue information for FCU input.
            '''
            message_buffer = []
            fcu_list_east = ['East Tower - Fan Coil - North Corridor - Floor',
                             'East Tower - Fan Coil - South Corridor - Floor',
                             'ES - Corridor - Floor']
            fcu_list_west = ['West Tower - Fan Coil - Center Corridor - Floor',
                             'West Tower - Fan Coil - East Corridor - Floor',
                             'West Tower - Fan Coil - West Corridor - Floor',
                             'West Tower - Fan Coil - Storage Room - Floor',
                             'WE - Corridor - Floor']
            for num in range(int(fcu_amt)):
                if tower == 'West':
                    continue_fcus, mess = self.app.insert_new_issue('PM - Hotel Shop - Corridor Fan Coil',
                                              fcu_list_west[num] + ' ' + floor,
                                              engineer=engineer)
                    message_buffer.extend(mess)
                    if continue_fcus is not True:
                        break
                elif tower == 'East':
                    continue_fcus, mess = self.app.insert_new_issue('PM - Hotel Shop - Corridor Fan Coil',
                                              fcu_list_east[num] + ' ' + floor,
                                              engineer=engineer)
                    message_buffer.extend(mess)
                    if continue_fcus is not True:
                        break
            self.add_log(message_buffer)

        popup = tk.Toplevel()
        popup.title('FCU Assignment')
        self.add_log('** Loading FCU **')

        ttk.Label(popup, text='Engineer:').grid(row=0, column=0)
        engineer = ttk.Combobox(popup, value=self.Engineer_List)
        engineer.grid(row=0, column=1)
        engineer.current(0)

        ttk.Label(popup, text='Floor: ').grid(row=1, column=0)
        floor = ttk.Entry(popup, width=25)
        floor.grid(row=1, column=1)

        ttk.Label(popup, text='Tower: ').grid(row=2, column=0)
        tower = ttk.Combobox(popup, value=['West', 'East'])
        tower.grid(row=2, column=1)
        tower.current(0)

        ttk.Label(popup, text='FCU AMT: ').grid(row=3, column=0)
        fcu = ttk.Entry(popup, width=25)
        fcu.grid(row=3, column=1)

        enter = ttk.Button(popup, 
                           text='Enter', 
                           command=lambda: [attach_fcus(engineer.get(),
                                                        floor.get(),
                                                        tower.get(),
                                                        fcu.get()),
                                            popup.destroy(),
                                            self.add_log ('FCU Complete. **')])
        enter.grid(row=4, columnspan=2)

    def load_breaks(self):
        '''load_breaks()
            Launch BreakCalculator
        '''
        try:
            bc = BreakCalculator()
        except FileNotFoundError:
            self.alert('File was not Found', title='CSV BreakCalculator')
            self.add_log('File was not found!, verfiy saved info as csv/breaks.csv')
            return
        bc.calculate_time()
        bc.save_to_text()

    def pad_tracker(self):
        bi = PadInformation()
        self.add_log('PAD Tracker successfully loaded.')
        bi.mainloop()

    def cosmo_directory(self):
        try:
            cd = CosmoDirectory()
        except FileNotFoundError:
            self.add_log('File was not found! Verify "direct" files intact.')
        self.add_log('CosmoDirectory successfully loaded.')
        cd.mainloop()

    def add_log(self, text):
        '''add_log(text)
            Adds either list or string to TK widget in main window.
        '''
        if type(text) is list:
            for each in text:
                print(f'LOG: {each}')
                self.info_win.insert(tk.END, f'$ {each}\n')
        else:
            print(f'LOG: {text}')
            self.info_win.insert(tk.END, f'$ {text}\n')

    def load_prvs(self):
        '''load_prvs()
            Prompt and assign PRV's information to Engineers
        '''
        def attach_prvs(east_eng, west_eng):
            '''attach_prvs(east_eng, west_eng)
                Send infomration to insert_new_issue.
            '''
            es_prv_rooms = ['Temp Location']
            we_prv_rooms = ['Temp Location']
            for east in es_prv_rooms:
                continue_prv, mess = self.app.insert_new_issue('PRV - Hotel - PM', east, engineer=east_eng, wait=.5)
                self.add_log([item for item in mess])
                if continue_prv is not True:
                    return False
            for west in we_prv_rooms:
                continue_prv, mess = self.app.insert_new_issue('PRV - Hotel - PM', west, engineer=west_eng, wait=.5)
                self.add_log([item for item in mess])
                if continue_prv is not True:
                    return False

        popup = tk.Toplevel()
        popup.title('PRV Selection')
        ttk.Label(popup, text='East Tower:').grid(row=0, column=0)
        east_eng = ttk.Combobox(popup, value=self.Engineer_List)
        east_eng.grid(row=0, column=1)
        east_eng.current(0)
        ttk.Label(popup, text='West Tower:').grid(row=1, column=0)
        west_eng = ttk.Combobox(popup, value=self.Engineer_List)
        west_eng.grid(row=1, column=1)
        west_eng.current(0)
        enter = ttk.Button(popup, text='Enter', command=lambda: [attach_prvs(east_eng.get(), west_eng.get()),
                                                                 popup.destroy()] )
        enter.grid(row=2, column=0, columnspan=2)

    def alert(self, text, title='CosmoDispatch.py', button='Ok'):
        popup = tk.Toplevel()
        popup.title(title)
        ttk.Label(popup, text=text).pack()
        ttk.Button(popup, text=button, command=popup.destroy).pack()
        popup.mainloop()

if __name__ == '__main__':
    job = CosmoDispatch()
    job.mainloop()

