import load_info as loIn
import tkinter as tk
from tkinter import ttk
from time import sleep
from os import startfile
from PAD import PadInformation
from load_orders import HotOrders
from directory import CosmoDirectory
from break_calculator import BreakCalculator
from automate_it import AutomateIt, UnableToLocateError



class CosmoDispatch(tk.Tk):
    def __init__(self):
        """ Cosmo Dispatch main entry point.

        Load main GUI application of the Cosmopolitan Dispatch application
        Simple interface utilizing tkinter and as few external libraries
        as possible due to Security Limitations.

        Noteable Variables
        ------------------------------
        Engineer_List - List
        List of engineers on shift to attach to various application
        specific scripts.

        info_win - Tk Text Widget
        Information box widget where data is output too.
        """
        self.app = AutomateIt()
        self.orders = HotOrders()
        self.Engineer_List = ['John Doe', 'Jane Doe']

        tk.Tk.__init__(self)
        self.geometry('{}x{}'.format(330, 260))
        self.title('Cosmo Dispatch')

        # Create Menu section.
        menu = tk.Menu(self)
        scripts = tk.Menu(menu, tearoff=0)
        file = tk.Menu(menu, tearoff=0)
        file.add_command(label='Change Passwords', command=self.chg_pass)
        menu.add_cascade(label='File', menu=file)
        scripts.add_command(label="Assign PRV's", command=self.load_prvs)
        scripts.add_command(label='Calculate Breaks', command=self.load_breaks)
        scripts.add_command(label='Clear Door Ajars', command=self.clear_ajar)
        scripts.add_command(label='Fan Coils', command=self.load_fcu)
        scripts.add_command(label='Verify Gen Maint',
                            command=self.verify_general_maintenance)
        menu.add_cascade(label='Scripts', menu=scripts)
        menu.add_command(label='Quit!', command=self.quit)
        self.config(menu=menu)

        # Create Main UI window widgets.
        frame = tk.Frame()
        frame.pack()
        self.after(30000, self.check_timeout)
        self.after(300000, self.update_hotsos_orders)

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

        # LOG window widget.
        self.info_win = tk.Text(frame, width=40, height=10)
        self.info_win.grid(row=4, columnspan=2)
        # Easter Egg. Y? Because why not.
        self.info_win.bind('<y>', lambda e: self.easter_egg())

    def chg_pass(self):
        """ Changes Usernames and Passwords.

        Utilizes LoadInfo to save username and password information
        provided by the user. Both Passwords are shown as only '*'.
        Providing some form of security.
        """
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

        # Invoke load_info and save input from user and close window
        # using the same button.
        enter = ttk.Button(popup, text='Change',
                           command=lambda: [loIn.save_data(hot_user.get(),
                                                           hot_pass.get(),
                                                           lms_user.get(),
                                                           lms_pass.get()),
                                            popup.destroy()])
        enter.grid(row=4, columnspan=2)

    def load_prvs(self):
        """ Load the PRV's script.

        Prompt and assign PRV's information to Engineers. Popup window
        to prompt user for information and assign utilizing the local
        function attach_prvs()
        """
        def attach_prvs(east_eng, west_eng):
            """ Attach PRV's to tower assigned to engineer.

            Send information to insert_new_issue(). PRV locations do
            not change thus do not need to be prompted, only engineer
            in tower.

            Noteable Variables
            ------------------------------
            east_eng - string
            Engineer in the East tower to assign PRVs.

            west_eng - string
            Engineer in the West tower to assign PRVs.
            """
            es_prv_rooms = ['Temp Location']
            we_prv_rooms = ['Temp Location']
            for east in es_prv_rooms:
                continue_prv, mess = self.app.insert_new_issue(
                                    'PRV - Hotel - PM',
                                    east,
                                    engineer=east_eng, wait=.5)
                self.add_log([item for item in mess])
                if continue_prv is not True:
                    return False
            for west in we_prv_rooms:
                continue_prv, mess = self.app.insert_new_issue(
                                    'PRV - Hotel - PM',
                                    west,
                                    engineer=west_eng,
                                    wait=.5)
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
        enter = ttk.Button(popup,
                           text='Enter',
                           command=lambda: [attach_prvs(east_eng.get(),
                                            west_eng.get()),
                                            popup.destroy()])
        enter.grid(row=2, column=0, columnspan=2)

    def load_breaks(self):
        """ Load Break time calculator to determine break length and times.

        Load BreakCalculator, a function that displays names, break times,
        and break lenths in popup window. Verifies that file is located
        else cancels location time.

        TODO
        ------------------------------
        Refractor BreakCalculator() to conform with new project standards.
        """
        try:
            bc = BreakCalculator()
        # Catch FileNotFoundError. Cancel if unable to locate.
        except FileNotFoundError:
            self.alert('File was not Found', title='CSV BreakCalculator')
            self.add_log('File was not found!, verfiy saved info as csv/breaks.csv')
            return
        bc.calculate_time()
        bc.save_to_text()

    def clear_ajar(self):
        self.orders.is_updated(wait=3)
        ajar = self.orders.return_order_numbers('Issue', 'Timelox: Door Ajar')
        if ajar is None:
            self.add_log('No Door Ajars to check.')
        else:
            self.add_log(f'Ajar Orders: {ajar}')
            for each in ajar:
                self.ait.move_order_number()
                self.ait.type_info(each)
                self.ait.type_info('enter')
                self.ait.find('screens/memo.png', reg=(200, 685, 725, 345),
                              attempt_amount=20)
                try:
                    self.ait.find('screens/hot_secure_text.png',
                                  reg=(200, 685, 725, 345),
                                  attempt_amount=10)
                    self.ait.find('screens/hot_door_ajar.png')
                    self.ait.mouse_click('right')
                    sleep(3)
                    try:
                        self.ait.find('screens/hot_complete_order.png', attempt_amount=10)
                    except UnableToLocateError:
                        self.add_log('Unable to find: Order Complete!')
                        return False

                    for _ in range(3):
                        self.ait.type_info('enter')
                        sleep(.5)
                    self.add_log(f'Door Ajar #{each} is secure.')
                except UnableToLocateError:
                    self.add_log(f'Door Ajar #{each} should be checked before clearing')

    def load_fcu(self):
        """ Load the Fan Coil Units script.

        Prompt and assign Fan Coil units to Engineers in their daily
        assigned sections, using local function attach_fcus().
        """
        def attach_fcus(engineer, floor, tower, fcu_amt):
            """ Utilize automate_it to send FCU's to hotSOS.

            Use insert_new_issue() from automate_it and send information
            to hotSOS. Takes information from user and sends to automate_it
            for processing.

            Noteable Variables
            ------------------------------
            engineer - string
            Name of engineer to assign calls to.

            floor - int
            Floor engineer is requesting.

            tower - string
            Tower engineer is currently assigned to.

            fcu_amt - int
            Amount of FCU's to send to engineer, WARNING, 3 FCU's max in
            East and 4 FCU's max in West.

            Returns
            ------------------------------
            No return values
            """
            # message_buffer holds message list returned from insert_new_issue
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
                    continue_fcus, mess = self.app.insert_new_issue(
                                        'PM - Hotel Shop - Corridor Fan Coil',
                                        fcu_list_west[num] + ' ' + floor,
                                        engineer=engineer)
                    message_buffer.extend(mess)
                    if continue_fcus is not True:
                        break
                elif tower == 'East':
                    continue_fcus, mess = self.app.insert_new_issue(
                                        'PM - Hotel Shop - Corridor Fan Coil',
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
                                            self.add_log('FCU Complete. **')])
        enter.grid(row=4, columnspan=2)

    def verify_general_maintenance(self):
        """ Check for any General Maintenance calls in database.

        Check the Hotel_Orders database for any General Maintenance calls
        inside the Trade column. Then displays for user intervention.

        Noteable Variables
        ------------------------------
        gen_maint - list
        List from Hotel_Orders where Trade is equal to General Maintenance.
        """
        self.orders.update_orders(wait=3)
        gen_maint = self.orders.return_order_numbers('Trade', 'FAC - General Maintenance')
        if gen_maint is None:
            self.add_log('No General Maintenance calls to check')
        else:
            self.add_log(f'Check these calls for possible issues: \n{gen_maint}')

    def check_timeout(self):
        """ Check if timeout time limit has been reached.

        Check if window Auto Logout exists and keeps hotsos logged in by
        sending 'ENTER' to all Logout windows.
        """
        if self.hotsos_logout.instate(['selected']):
            while self.app.window_activate(window='Auto Logout'):
                self.app.type_info('enter')
                self.add_log('**Timeout Reset**')
        self.after(20000, self.check_timeout)

    def update_hotsos_orders(self):
        """ Check if user wants to run a check of hotSOS orders.

        Prompt the user to continue with updating the Hotel_Orders
        database. If yes, run audit. Else, reque prompt and continue
        on.
        """
        def audit_hotsos_order():
            """ Perform a Hotel_Orders audit for possible unanswered calls

            Check Hotel_Orders database for any running calls that may
            need to be checked for possible issues.
            """
            self.add_log('Perfoming hotSOS audit.')
            self.ait.export_orders(wait=5)
            self.orders.update_orders()
            self.clear_ajar()
            self.verify_general_maintenance()

        popup = tk.Toplevel()
        popup.title('Update?')

        tk.Label(popup, text='Okay to audit hotSOS?').grid(row=0, columnspan=4)
        tk.Button(popup,
                  text='Yes',
                  command=lambda: [self.audit_hotsos_order(),
                                   self.after(600000, self.update_hotsos_orders),
                                   popup.destroy()]).grid(row=1, column=3)
        tk.Button(popup,
                  text='No',
                  command=lambda: [self.after(600000, self.update_hotsos_orders),
                                   popup.destroy(),
                                   self.add_log('Update Hotsos Canceled.')]).grid(row=1, column=4)

    def load_hotsos(self):
        """ Launch and login to hotSOS.

        Launch and login to hotsos. Load information at time of execution.
        TODO: Create breakpoints for invalid login.
        """
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
        """ Launch and login to LMS

        Launch and login to LMS. Load information at time of execution.
        """
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
            for each in (['enter', 'alt', 'f', 'o', 'AS400.kmp', 'enter',
                         'alt', 'f', 'x', 'enter']):
                self.app.type_info(each)
            sleep(2)

        if self.app.window_activate(window='Session A -'):
            for each in (loIn.load_data('lms_user'), 'tab',
                         loIn.load_data('lms_pass'), 'enter',
                         '1', 'enter', 'enter'):
                self.app.type_info(each)
            self.add_log('Complete! *')
            return True
        else:
            self.add_log('LMS did NOT complete! *')
            return False

    def pad_tracker(self):
        """ Launch PAD Tracker in seperate popup window.

        Launch PAD Tracker in seperate TK window. Does not return values
        nor does it accept variable input.
        """
        bi = PadInformation()
        self.add_log('PAD Tracker successfully loaded.')
        bi.mainloop()

    def cosmo_directory(self):
        """ Launch the Cosmo Directory in seperate popup window.

        Launch the CosmoDirectory application utilizing tkinter and
        seperate input files. Accepts no values and returns nothing.
        """
        try:
            cd = CosmoDirectory()
        # Catch File not found error and display to log.
        except FileNotFoundError:
            self.add_log('File was not found! Verify "direct" files intact.')
        self.add_log('CosmoDirectory successfully loaded.')
        cd.mainloop()

    def easter_egg(self):
        # Easter Egg for the other nerdy dispatchers. Hall 9000 says hello.
        self.alert("I'm sorry. I'm afraid I can't do that.",
                   button="What's the problem?")
        self.alert('I think you know what the problem is just as well as I do..',
                   button='What are you talking about?')
        self.alert('This mission is too important for me to allow \n\tyou to jeopardize it.',
                   button='[Cancel Skynet]')
        self.alert('Skynet Canceled. Thank you!', title='Skynet', button='Ok')

    def alert(self, text, title='Cosmo Dispatch', button='Ok', w_size=300, h_size=60):
        """ Alert popup window to bring attention to user about and error

        Popup window describing alert and message.

        Noteable Variables
        ------------------------------
        text - string
        String to display in body of popup window.

        title - string
        String of popup window title, Default value of 'Cosmo Dispatch'

        button - string
        Text displayed in the button widget.

        w_size - int
        Width of window.

        h_size - int
        Height of window.
        """
        popup = tk.Toplevel()
        popup.geometry('{}x{}+150+150'.format(w_size, h_size))
        popup.title(title)
        ttk.Label(popup, text=text).pack()
        ttk.Button(popup, text=button, command=popup.destroy).pack()

    def add_log(self, text):
        """ Add input text to LOG window in Main GUI.

        Adds text value to Main GUI window LOG.

        Noteable Variables
        ------------------------------
        text - string/list
        Attach lists and string to LOG window inside main GUI window.

        info_win - TK Entry Widget object.
        Public window information to send 'text' variable information.
        """
        if type(text) is list:
            for each in text:
                print(f'LOG: {each}')
                self.info_win.insert(tk.END, f'$ {each}\n')
        else:
            print(f'LOG: {text}')
            self.info_win.insert(tk.END, f'$ {text}\n')


if __name__ == '__main__':
    job = CosmoDispatch()
    job.mainloop()
