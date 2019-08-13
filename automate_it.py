# autoit file
import os
import pyautogui as pyg
import autoit
from time import sleep


class UnableToLocateError(Exception):
    """ UnableToLocateError - Exception

    Return unable to find on screen error.
    """
    def __init__(self):
        pass


class AutomateIt():
    def __init__(self):
        """ Automation script that sends specific information to hotSOS window.

        AutomateIt provides specific commands to be sent through the hotSOS
        application. Each function has documentation to provide further
        information to what is accomplished.
        """
        pyg.PAUSE = .2

    def mouse_click(self, button, x=None, y=None):
        """ Click parametered button at x and y coordinates

        Click either 'left' or 'right' mousebutton at x and y coordinates.
        If No parametered values are provided, click at current mouse position.
        does not return any values.
        """
        x = int(x)
        y = int(y)

        if x is None or y is None:
            pyg.click(button=button)
        elif button is None:
            pyg.moveTo(x, y)
        else:
            pyg.click(x, y, button=button)

    def move_order_number(self, wait=0):
        """ Select to Order Number box in hotsos.

        Move mouse to the OrderNumber section of hotSOS and click.
        """
        self.window_activate()
        for _ in range(2):
            self.mouse_click('left', x=340, y=175)
        sleep(wait)

    def reset_hotsos_window(self, wait=0):
        """ Reset hotSOS back to original window screen

        Reset hotSOS back to how it was before finding Hotel_Orders
        Order_Num.
        """
        self.window_activate()
        self.move_order_number()
        self.type_info('backspace')
        self.type_info('esc')
        self.type_info('enter')

    def type_info(self, text, wait=0):
        """ Type info using pyautogui's type command.

        Type the 'text' into the current view. Wait a certain number of seconds
        then continue. Any commands must be entered through the 'press'
        function. Add any commands to commands variable.

        Noteable Variables
        ------------------------------
        text - string
        Text to send through the pyautogui library.

        wait - int
        Time in seconds to wait after input command to allow for delay
        after entering information.

        commands - list
        List of commands that should be entered through the press function
        of pyautogui. If exact strings are to be typed, enter each letter
        individually instead.
        """
        commands = ['tab', 'enter', 'esc', 'alt', 'command', 'option', 
                    'select', 'backspace']
        if text in commands:
            pyg.press(text)
        else:
            pyg.typewrite(text)
        sleep(wait)

    def insert_new_issue(self, new_issue, issue_location, wait=1, engineer=None):
        """ Insert new issue inside hotSOS window.

        Insert new issue in hotsos window. Takes information passed and
        inputs into hotSOS utilizing precise mouse and button combinations.

        Noteable Variables
        ------------------------------
        new_issue - string
        Issue to be typed into hotSOS window. Must be exactly as shown
        in hotSOS. Verify before sending to function.

        issue_location - string
        Location of issue to be typed into hotSOS window. Must be exactly
        as shown in hotSOS. Verify before sending to function.

        wait - int
        Time in seconds to wait after input command to allow for delay
        after entering information.

        engineer - string
        Name of engineer to attach to hotSOS order created. If empty skip
        entire section.


        Returns
        ------------------------------
        Success - boolean
        Returns successful insert or otherwise.

        message_list - list
        List of messages to send to upper function. Useful for deciphering
        where things have gone awry.
        """
        self.window_activate()
        # return message_list to upper handler.
        message_list = []
        try:
            self.find('screens/new_button_hot.png')
            self.find('screens/issue_entry_hot.png',
                      reg=(200, 685, 725, 345),
                      attempt_amount=20)
            pyg.typewrite(new_issue)
            pyg.press('enter')
            self.find('screens/where_entry_hot.png',
                      reg=(200, 685, 725, 345))
            pyg.typewrite(issue_location)
            pyg.press('enter')

            if engineer is not None:
                self.find('screens/additional_tab_hot.png',
                          reg=(200, 685, 725, 345))
                self.find('screens/direct_to_entry_hot.png',
                          reg=(200, 685, 725, 345))
                pyg.typewrite(engineer)
                for _ in range(4):
                    pyg.press('tab')
                pyg.typewrite(engineer)
                pyg.press('enter')

            self.find('screens/ok_button_hot.png')
            sleep(wait)
            message_list.append(f'Successful insert: {new_issue} @ {issue_location}')
            # return successful and message_list for issue inserted.
            return True, message_list

        # catch TypeError or Not found in screen list. Usually not
        # raised as unable to locate error is more accurate.
        except TypeError:
            sleep(wait)
            message_list.append('TypeError!')
            return False, message_list

        # catch UnableToLocateError, limit reached and was unable to locate
        # screen shot on screen. Return warning message to upper handler
        # for processing.
        except UnableToLocateError as e:
            message_list.append(f'Unable to locate {e.message}.')
            return False, message_list

    def find(self, item_locate, reg=None, attempt_amount=5):
        """ find(item_locate, reg=None, attempt_amount=5)

        Locate screenshot on screen. If not found after certain attempts
        raise Unable to Locate Error with error message. Region to scan,
        set to None to search entire screen. Screen size affects photo
        resolution. Attempt_Amount set to 5 standard, increase if region
        not set to None.

        Noteable Variables
        ------------------------------
        item_locate - string
        Location of screenshot to search on screen for. Warning screen
        size affects resolution. Image must be pixel perfect. The fewer
        the pixels the better

        reg - tuple
        4 Integer tuple to limit the screen search size. Set to None to
        search entire window.

        attempt_amount - int
        Number of times to search screen. The higher the number the longer
        the wait. This is used due to lag time between search and hotSOS
        loading times.
        """
        if not os.path.exists(item_locate):
            raise FileNotFoundError

        attempt = 0

        while attempt <= attempt_amount:
            if reg is not None:
                try:
                    x, y = pyg.locateCenterOnScreen(item_locate, region=reg)
                    self.mouse_click('left', x=x, y=y)
                    return True
                # Catch TypeError, add attempts and continue if valid.
                except TypeError:
                    attempt += 1
            else:
                try:
                    x, y = pyg.locateCenterOnScreen(item_locate)
                    self.mouse_click('left', x=x, y=y)
                    return True
                # Catch TypeError, add attempts and continue if valid.
                except TypeError:
                    attempt += 1
        # Raise Unable to Locate back to upper function
        raise UnableToLocateError

    def export_orders(self, wait=0):
        """ Exports hotSOS Orders to csv/orders.csv

        Exports the current hotSOS Orders list to the orders csv value
        inside the csv folder in the main script path. This will allow
        other classes to load data of all current running calls.

        Returns
        ------------------------------
        Success - Boolean
        Returns True if successful completion or otherwise with error
        message.
        """
        self.window_activate()
        try:
            self.find('screens/export.png')
        # If unable to locate return False and with error.
        except UnableToLocateError as e:
            return False, f'Unable to Locate: {e}'
        # Save prompt script
        for e in [f'{os.path}\\csv\\orders.csv', 'tab', '.csv', 'enter']:
            self.type_info(e)
        sleep(wait)
        return True, None

    def window_activate(self, window='Hotel Service Optimization System - HotSOS', wait=0):
        """ Activate window before continuing

        Activate Window using autoit. Default search window is hotSOS,
        due to frequency of use througout application.

        Noteable Variables
        ------------------------------
        window - string
        Name of window to find, using pyautoit. Pyautoit allows for
        semi matching strings and wild cards.

        wait - int
        Time in seconds to wait after input command to allow for delay
        after entering information.


        Returns
        ------------------------------
        Success - Boolean
        Return if window was either found successfully or otherwise.
        """
        print(f'Locating window: {window}')
        try:
            autoit.win_activate(window)
            print('Found!')
            sleep(wait)
            return True
        # Bare accept because autoit won't tell me what the error actually is.
        except:
            print('Unable to locate')
            sleep(wait)
            return False
