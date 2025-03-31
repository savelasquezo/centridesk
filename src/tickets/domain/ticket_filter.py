from shared.value_objects.filter import Filter
from shared.value_objects.order import Order
from shared.value_objects.sort import Sort


class TicketFilter:

    def __init__(self, filters, sort=None, order=None):
        self.__valid_ticket_fields = ['status_id', 'priority_id', 'author_id', 'assignee_id', 'channel_id',
                                      'external_id', 'centribot_project_id', 'centribot_channel_id', 'created_at',
                                      'updated_at', 'closed_at']
        self.filters = filters
        self.sort = sort
        self.order = order

    @property
    def filters(self):
        return self.__filters

    @filters.setter
    def filters(self, filters):
        self.__filters = Filter(filters, self.__valid_ticket_fields).filters

    @property
    def sort(self):
        return self.__sort

    @sort.setter
    def sort(self, sort):
        __sort = sort.split(',') if sort else []
        self.__sort = [Sort(s, self.__valid_ticket_fields).sort for s in __sort]

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        __order = order.split(',') if order else []
        self.__order = [Order(o).order for o in __order] if self.sort else None
