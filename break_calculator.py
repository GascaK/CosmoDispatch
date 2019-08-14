import automate_it
import load_orders
import tkinter


class BreakCalculator():
    def __init__(self, break_orders):
        """ Calculate engineer break lengths and type of breaks.

        Calculate engineer break length and type from a Hotel_Orders
        db query.

        Noteable Variables
        ------------------------------
        break_orders - dictionary
        sqlite DB query of all engineer break times in dict format.

        engineer_list - list
        List of engineers to verify. Helps in lowering time to calculate

        order_list - list
        List to save data for sorting algorithm.
        """
        self.ait = automate_it.AutomateIt()
        self.engineer_list = ['John Doe', 'Jane Doe']
        order_list = []

        for each in break_orders:
            if each['Assigned'] not in self.engineer_list:
                continue

            self.ait.move_order_number()
            self.ait.type_info(each['Order_Num'])
            self.ait.type_info('enter')
            try:
                self.ait.find('screens/labor_tab_hot.png',
                              reg=(200, 685, 725, 345),
                              attempt_amount=15)
            except self.automate_it.UnableToLocateError:
                return False, 'Unable to locate.'

            for com in ['tab', 'space', 'tab', 'tab', 'tab']:
                self.ait.type_info(com)

            automate_it.pyg.hotkey('ctrl', 'c')
            break_length = tkinter.Tk().clipboard_get()
            order_list.append(f"{each['Assigned']} took a {break_length} minute {each['Issue']}.")
            self.ait.type_info('esc')

        save_info(order_list.sort())

    def save_info(self, values):
        """ Save info to text file breaks.txt

        Check if 'breaks.txt' exists, if it does not create file, if it does
        append to end of file.

        Noteable Variables
        ------------------------------
        values - list
        Iterable list to append to end of file.
        """
        try:
            f = open('breaks.txt', 'a')
        except FileNotFoundError:
            f = open('breaks.txt', 'w')
        for each in values:
            f.write(values)


if __name__ == '__main__':
    lo = load_orders.HotOrders()
    lo.update_orders()

    bc = BreakCalculator(lo.all_orders_as_dict('Issue', 'Break - Casino Shop'))
