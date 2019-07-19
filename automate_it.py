# autoit file
import pyautogui as pyg
import autoit
from time import sleep

class UnableToLocateError(Exception):
    '''UnableToLocateError - Exception
        Return unable to find on screen error.
    '''
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class AutomateIt():
    def __init__(self):
        self.hot_hwd = 'Hotel Service Optimization System - HotSOS'
        pyg.PAUSE = .2

    def move_order_number(self, wait=0):
        self.window_activate()
        pyg.click(x=340, y=175)
        sleep(wait)

    def type_info(self, text, wait=0):
        commands = ['tab', 'enter', 'esc', 'alt']
        if text in commands:
            pyg.press(text)
        else:
            pyg.typewrite(text)
        sleep(wait)

    def insert_new_issue(self, new_issue, issue_location, wait=1, engineer=None):
        self.window_activate()
        message_list = []
        try:
            self.find('screens/new_button_hot.png')
            self.find('screens/issue_entry_hot.png', reg=(200, 685, 725, 345), attempt_amount=20)
            pyg.typewrite(new_issue)
            pyg.press('enter')
            self.find('screens/where_entry_hot.png', reg=(200, 685, 725, 345))
            pyg.typewrite(issue_location)
            pyg.press('enter')

            if engineer is not None:
                self.find('screens/additional_tab_hot.png', reg=(200, 685, 725, 345))
                self.find('screens/direct_to_entry_hot.png', reg=(200, 685, 725, 345))
                pyg.typewrite(engineer)
                for _ in range(4):
                    pyg.press('tab')
                pyg.typewrite(engineer)
                pyg.press('enter')

            self.find('screens/ok_button_hot.png')
            sleep(wait)
            message_list.append(f'Successful insert: {new_issue} @ {issue_location}')
            return True, message_list

        except TypeError:
            sleep(wait)
            message_list.append('TypeError!')
            return False, message_list

        except UnableToLocateError as e:
            message_list.append(f'Unable to locate {e.message}.')
            return False, message_list

    def find(self, item_locate, reg=None, attempt_amount=5):
        attempt = 0
        while attempt <= attempt_amount:
            if reg is not None:
                try:
                    x, y = pyg.locateCenterOnScreen(item_locate, region=reg)
                    pyg.click(x, y)
                    return True
                except TypeError:
                    print(f'TypeError {attempt}')
                    attempt += 1
            else:
                try:
                    x, y = pyg.locateCenterOnScreen(item_locate)
                    pyg.click(x, y)
                    return True
                except TypeError:
                    print(f'TypeError {attempt}')
                    attempt += 1
        # Raise Unable to Locate back to upper function
        raise UnableToLocateError(f'{item_locate}')

    def window_activate(self, window='Hotel Service Optimization System - HotSOS', wait=0):
        print(f'Locating window: {window}')
        try:
            autoit.win_activate(window)
            print('Found!')
            sleep(wait)
            return True
        except:
            print('Unable to locate')
            sleep(wait)
            return False

