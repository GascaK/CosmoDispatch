from load_orders import HotOrders


class BreakCalculator:
    def __init__(self):
        self.engineer_list = ['John Doe', 'Jane Doe']
        self.orders = HotOrders()

        self.orders.update_orders(filepath=r'C:\Users\OptimusMine\Desktop\orders.csv', wait=3)

        break_orders = self.orders.return_all_orders('Issue', 'Timelox: Door Ajar')
        print(break_orders)

if __name__ == '__main__':
    bc = BreakCalculator()
