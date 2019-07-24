import autoit
import time
import csv


class BreakCalculator:
    """ Deprecated Break Calculator function.

        Break Calculator to show all engineers break times, break lengths
        and break amounts.

        TODO
        ------------------------------
        Convert to new automate_it format for ease of use.
    """
    def __init__(self):
        self.engineer_list = ['John Doe', 'Jane Doe']
        self.break_num = []
        self.break_type = []
        self.engineer = []
        self.start_time = []
        self.end_time = []

        try:
            with open('csv/breaks.csv', mode='r') as csv_load:
                for _ in range(4):
                    csv_load.readline()

                csv_read = csv.DictReader(csv_load)
                for i, row in enumerate(csv_read):
                    if row['Assigned'] in self.engineer_list and \
                            row['Issue'].find('No Power') == -1:
                        self.break_num.append(row['Order #'])
                        if 'Lunch' in row['Issue']:
                            self.break_type.append('Lunch Break')
                        else:
                            self.break_type.append('Break')
                    if i > 30:
                        break
        except FileNotFoundError:
            print('File not found, verify saved info as breaks.csv')
            raise

    def calculate_time(self):
        hotsos = 'Hotel Service Optimization System - HotSOS'
        hwnd = autoit.win_activate(hotsos)
        print(self.break_num)
        for each in self.break_num:
            self.tabs()
            autoit.send(each)
            autoit.send('{ENTER}')
            self.extract_time()

    def tabs(self):
        autoit.mouse_move(0, 0)
        autoit.mouse_click('primary', 340, 175)
        time.sleep(0.2)
        autoit.mouse_click('primary', 340, 175)

    def extract_time(self):
        time.sleep(3.5)
        autoit.mouse_click('primary', 220, 900)
        time.sleep(1)
        autoit.send('{TAB}{SPACE}')
        autoit.send('{CTRLDOWN}c{CTRLUP}')
        self.engineer.append(autoit.clip_get())
        autoit.send('{TAB}')
        autoit.send('{CTRLDOWN}c{CTRLUP}')
        temp = autoit.clip_get()
        self.start_time.append(temp[9:])
        time.sleep(0.2)
        autoit.send('{TAB}')
        autoit.send('{CTRLDOWN}c{CTRLUP}')
        temp = autoit.clip_get()
        self.end_time.append(temp[9:])
        autoit.send('{ESC}')

    def save_to_text1(self):
        lunch_list = []
        break_list = []

        for i in range(len(self.break_num)):
            if 'Lunch' in self.break_type[i]:
                lunch_list.append('{} - {} - {} ({}) / '.format(self.engineer[i],
                    self.start_time[i], self.end_time[i], self.break_type[i]))
            else:
                break_list.append('{} - {}, {}'.format(self.engineer[i],
                    self.break_type[i], self.start_time[i]))

    def save_to_text(self):
        temp_list = []
        for i in range(len(self.break_num)):
            temp_list.append('{} - ({}){} - {}'.format(self.engineer[i], self.break_type[i],
                self.start_time[i], self.end_time[i]))
        temp_list.sort()

        with open('breaks.txt', 'w') as file:
            for each in temp_list:
                print(each)
                file.write(each + '\n')


if __name__ == '__main__':
    bc = BreakCalculator()
    bc.calculate_time()
    bc.save_to_text()
