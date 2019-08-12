import csv
import sqlite3
from time import sleep
from automate_it import AutomateIt


class HotOrders():
    def __init__(self):
        """ hotSOS Order tracker, saver and updater.

        Function to load and save hotSOS order information into
        memory for use throughout the CosmoDispatch application.

        Noteable Variables
        ------------------------------
        conn - SQLite3 Database Connection
        Connector to the SQLite3 database

        tracker - SQLite3 cursor object
        Cursor object for SQLite3
        """
        self.ait = AutomateIt()
        # SQL database. Saved in memory to load upon every boot up.
        self.conn = sqlite3.connect(':memory:')
        self.tracker = self.conn.cursor()

    def update_orders(self, filepath='csv/orders.csv', wait=0):
        """ Check if hotsos orders.csv is saved and will update if not.

        Update orders attempts to check for the presence of the
        orders.csv inside the csv folder location. If not located
        will attempt to invoke the AutomateIt function export_orders().

        Noteable Variables
        ------------------------------
        filepath - string
        Filepath to load orders from.

        column_headers - string
        Input from the orders.csv. Uses this information to gather column
        names for each individual user. This is due to users being able
        to alter column names inside the hotSOS application

        wait - int
        Time in seconds to wait after input command to allow for delay
        after entering information.
        """
        try:
            read = open(filepath)
        # Catch File not found, and create file using ait.
        except FileNotFoundError:
            print('File was not found. Saving data now.')
            cont, mess = self.ait.export_orders()
            if cont:
                read = open(filepath)
            else:
                print(mess)
                raise FileNotFoundError
        # Get to the column headers. First 4 lines are garbage parcers.
        for _ in range(4):
            read.readline()
        reader = csv.reader(read)
        column_headers = (read.readline()).split(',')

        # Loop through Column Names and change to proper sql
        for i, title in enumerate(column_headers):
            if title == 'Order #':
                column_headers[i] = 'Order_Num integer PRIMARY KEY'
            elif title == 'Room/Eq':
                column_headers[i] = 'Room text NOT NULL'
            elif title == 'Status':
                column_headers[i] = 'Status text'
            elif title == 'Priority':
                column_headers[i] = 'Priority integer'
            elif title == 'Trade':
                column_headers[i] = 'Trade text'
            elif title == 'Issue':
                column_headers[i] = 'Issue text'
            elif title == 'Requestor':
                column_headers[i] = 'Requestor text'
            elif title == 'Assigned':
                column_headers[i] = 'Assigned'
            elif title == 'A':
                column_headers[i] = 'A'
            elif title == 'Occupancy\n':
                column_headers[i] = 'Occupancy text'

        # Drop old TABLE and create new one with newly loaded information.
        self.tracker.execute('''DROP TABLE IF EXISTS Hotel_Orders''')

        self.tracker.execute('''CREATE TABLE IF NOT EXISTS Hotel_Orders
            ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'''.format(*column_headers))
        for row in reader:
            self.tracker.execute('''INSERT INTO Hotel_Orders
                values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                '{}', '{}', '{}')'''.format(*[value.replace("'", ',') for value in row]))
        self.conn.commit()
        sleep(wait)

    def return_order_numbers(self, column, value):
        """ Return the order numbers of value that are in columns

        Return the hotSOS order numbers of all matching values
        inside the provided column name.

        Noteable Variables
        ------------------------------
        column - String
        Column name inside the Hotel_Orders database to compare
        against values.

        value - String
        Value to search for in provided column name

        Returns
        ------------------------------
        Returns the hotSOS order numbers of all matching rows.
        """
        self.tracker.execute('''SELECT Order_Num
            FROM
             Hotel_Orders
            WHERE
             {} = ?
            ORDER BY
             Order_Num'''.format(column), (value,))
        return self.tracker.fetchall()

    def return_all_orders(self, column, value):
        """ Return all values from the db where value is in column

        Return the hotSOS information of all matching values inside
        the provided column name

        Noteable Variables
        ------------------------------
        column - String
        Column name inside the Hotel_Orders database to compare
        against values.

        value - String
        Value to search for in provided column name

        Returns
        ------------------------------
        Returns the hotSOS information of all matching rows.
        """
        self.tracker.execute('''SELECT *
            FROM
             Hotel_Orders
            WHERE
             {} = ?
            ORDER BY
             Order_Num'''.format(column), (value,))
        return self.tracker.fetchall()


if __name__ == '__main__':
    obj = HotOrders()
