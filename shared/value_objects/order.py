from shared.exceptions.invalid_order import InvalidOrder
from shared.exceptions.type_error import TypeErrorValue


class Order:

    def __init__(self, order):
        self.__name = 'order'
        self.order = order

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        if order and not isinstance(order, str):
            raise TypeErrorValue(self.__name)

        order = order.strip() if order else None
        if order not in ['asc', 'desc']:
            raise InvalidOrder()

        self.__order = order
