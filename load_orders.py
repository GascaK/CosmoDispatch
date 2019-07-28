import csv
import sqlite3
from automate_it import AutomateIt


class HotOrders():
    def __init__(self):
        ait = AutomateIt()
        self.conn = sqlite3.connect('hotsos_orders.db')
        self.tracker = self.conn.cursor()
        self.is_updated()

    def run(self):
        pass

    def is_updated(self):
        """ Check if hotsos orders.csv is saved and will update if not.

            asdf
        """
        try:
            read = open('C:/Users/OptimusMine/Desktop/orders.csv')
        # Catch File not found, and create file using ait.
        except FileNotFoundError:
            print('File was not found. Saving data now.')
            cont, mess = ait.save_orders()
            if cont:
                read = open('C:/Users/OptimusMine/Desktop/orders.csv')
            else:
                print(mess)
                raise FileNotFoundError
        # Get to the column headers. First 4 lines are garbage parcers.
        for _ in range(4):
            read.readline()
        reader = csv.reader(read)
        column_headers = (read.readline()).split(',')
        print('CH: ', column_headers)

        # Loop through Column Names and change to proper sql
        i = 0
        while i < len(column_headers):
            if column_headers[i] == 'Order #':
                column_headers[i] = 'Order_Num integer PRIMARY KEY'
            elif column_headers[i] == 'Room/Eq':
                column_headers[i] = 'Room text NOT NULL'
            elif column_headers[i] == 'Status':
                column_headers[i] = 'Status text'
            elif column_headers[i] == 'Priority':
                column_headers[i] = 'Priority integer'
            elif column_headers[i] == 'Trade':
                column_headers[i] = 'Trade text'
            elif column_headers[i] == 'Issue':
                column_headers[i] = 'Issue text'
            elif column_headers[i] == 'Requestor':
                column_headers[i] = 'Requestor text'
            elif column_headers[i] == 'Assigned':
                column_headers[i] = 'Assigned'
            elif column_headers[i] == 'A':
                column_headers[i] = 'A text'
            elif column_headers[i] == 'Occupancy\n':
                column_headers[i] = 'Occupancy text'
            i += 1

        print('CH: ', column_headers)

        print('{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(*column_headers))

        self.tracker.execute('''CREATE TABLE IF NOT EXISTS Hotel_Orders
                        ({}, {}, {}, {}, {}, {}, {}, {},
                        {}, {}, {})'''.format(*column_headers))
        for row in reader:
            self.tracker.execute("""INSERT INTO Hotel_Orders
                            values ('{}', '{}', '{}', '{}', '{}',
                            '{}', '{}', '{}', '{}', '{}', '{}')""".format(*row))

        self.conn.commit()
        t = ('In Progress',)
        self.tracker.execute('SELECT * FROM Hotel_Orders WHERE Status=?', t)
        print(self.tracker.fetchone())


if __name__ == '__main__':
    obj = HotOrders()
    obj.is_updated()
