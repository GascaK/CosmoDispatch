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
        pyg.PAUSE = .2

    def move_order_number(self, wait=0):
        '''move_order_number(wait=0)
            Move to the OrderNumber section of Hotsos.
        '''
        self.window_activate()
        pyg.click(x=340, y=175)
        sleep(wait)

    def type_info(self, text, wait=0):
        '''type_info(text, wait=0)
            Type the 'text' into the current view. Wait a certain number of seconds
            then continue.
        '''
        # commands accepted and must be entered seperately as 'press' command 
        # by pyautogui.
        commands = ['tab', 'enter', 'esc', 'alt']
        if text in commands:
            pyg.press(text)
        else:
            pyg.typewrite(text)
        sleep(wait)

    def insert_new_issue(self, new_issue, issue_location, wait=1, engineer=None):
        '''insert_new_issue(new_issue, issue_location, wait=1, engineer=None)
            Insert new issue in hotsos window. New Issue = type of issue, issue_location
            must be exact to issue location in hotsos. Verify before applying.
            Wait time of 1 second, standard due to input lag of hotsos application.
            Engineer = none. Must match name exactly to hotsos. Verify before applying.
        '''
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

        except TypeError:
            # catch TypeError or Not found in screen list. Usually not
            # raised as unable to locate error is more accurate.
            sleep(wait)
            message_list.append('TypeError!')
            return False, message_list

        except UnableToLocateError as e:
            # catch UnableToLocateError, limit reached and was unable to locate
            # screen shot on screen. Return warning message to upper handler
            # for processing.
            message_list.append(f'Unable to locate {e.message}.')
            return False, message_list

    def find(self, item_locate, reg=None, attempt_amount=5):
        '''find(item_locate, reg=None, attempt_amount=5)
            Locate screenshot on screen. If not found after certain attempts
            raise Unable to Locate Error with error message.
            Region to scan, set to None to search entire screen. Screen size
            affects photo resolution.
            Attempt_Amount set to 5 standard, increase if region not set to
            None.
        '''
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
                # Catch TypeError, but continue if not past attempt_amount
                except TypeError:
                    print(f'TypeError {attempt}')
                    attempt += 1
        # Raise Unable to Locate back to upper function
        raise UnableToLocateError(f'{item_locate}')

    def window_activate(self, window='Hotel Service Optimization System - HotSOS', wait=0):
        '''window_activate(window='* - HotSOS', wait=0)
            Activate Window using autoit.
        '''
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
