from shared.value_objects.filter import Filter
from shared.value_objects.order import Order
from shared.value_objects.sort import Sort


class CustomerFilter:

    def __init__(self, filters, sort=None, order=None):
        self.__valid_customer_fields = ['phone', 'email', 'centribot_external_id', 'display_name', 'company', 'agent_id',
                                        'delegation', 'external_id', 'gdpr']
        self.__valid_sort_customer_fields = ['phone', 'email', 'centribot_external_id', 'display_name', 'company',
                                             'agent_id', 'created_at', 'updated_at', 'last_comment_at', 'delegation',
                                             'external_id']
        self.filters = filters
        self.sort = sort
        self.order = order

    @property
    def filters(self):
        return self.__filters

    @filters.setter
    def filters(self, filters):
        self.__filters = Filter(filters, self.__valid_customer_fields).filters

    @property
    def sort(self):
        return self.__sort

    @sort.setter
    def sort(self, sort):
        __sort = sort.split(',') if sort else []

        self.__sort = []
        for s in __sort:
            s = s.strip()
            if s == 'name':
                s = 'display_name'
            self.__sort.append(Sort(s, self.__valid_sort_customer_fields).sort)

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        __order = order.split(',') if order else []
        self.__order = [Order(o).order for o in __order] if self.sort else None
