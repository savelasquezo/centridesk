from shared.exceptions.not_found import NotFound


class GetCustomer:

    def __init__(self, customer_id, account_id, customers_obj):
        self.customer_id = customer_id
        self.account_id = account_id
        self.customers_obj = customers_obj

    def get(self):
        self.customers_obj.customer_id = self.customer_id
        self.customers_obj.account_id = self.account_id
        customer = self.customers_obj.get_by_id()

        if not customer:
            raise NotFound('customer')

        return customer
