class GetTicketsStatus:

    def __init__(self, status_obj):
        self.status_obj = status_obj

    def get(self):
        return self.status_obj.get_all()
