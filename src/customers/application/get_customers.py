class GetCustomers:

    def __init__(self, account_id, customers_obj, page=None, page_size=None):
        self.account_id = account_id
        self.customers_obj = customers_obj
        self.page = page
        self.page_size = page_size

    def get(self):
        self.customers_obj.account_id = self.account_id
        total = self.customers_obj.count()
        return self.customers_obj.get_all(self.page_size, self.page), total
