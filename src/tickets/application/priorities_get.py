class GetTicketPriorities:

    def __init__(self, priorities_obj):
        self.priorities_obj = priorities_obj

    def get(self):
        return self.priorities_obj.get_all()
