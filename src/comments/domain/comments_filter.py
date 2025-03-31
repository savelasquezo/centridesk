from shared.value_objects.order import Order
from shared.value_objects.sort import Sort


class CommentsFilter:

    def __init__(self, sort=None, order=None):
        self.__valid_sort_customer_fields = ['created_at']
        self.sort = sort
        self.order = order

    @property
    def sort(self):
        return self.__sort

    @sort.setter
    def sort(self, sort):
        self.__sort = Sort(sort, self.__valid_sort_customer_fields).sort

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        self.__order = Order(order).order if self.sort else None
