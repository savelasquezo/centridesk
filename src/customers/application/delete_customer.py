class DeleteCustomer:
    def __init__(self, customer_id, account_id, customers_obj):
        self.customer_id = customer_id
        self.account_id = account_id
        self.customers_obj = customers_obj

    def delete(self):
        self.customers_obj.account_id = self.account_id
        self.customers_obj.customer_id = self.customer_id
        self.customers_obj.get_by_id()

        self.customers_obj.delete()
