from load_orders import HotOrders


class BreakCalculator:
    def __init__(self):
        self.engineer_list = ['John Doe', 'Jane Doe']
        self.orders = HotOrders()

        self.orders.update_orders(filepath=r'C:\Users\OptimusMine\Desktop\orders.csv', wait=3)

        all_orders = self.orders.all_orders_as_dict('Issue', 'Break')
        all_orders.append(self.orders.all_orders_as_dict('Issue', 'Lunch Break'))

        for each in all_orders:
            order = each['Order_Num']
            


if __name__ == '__main__':
    bc = BreakCalculator()
