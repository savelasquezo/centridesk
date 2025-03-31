from src.search.domain.generic_search import GenericSearch


class SearchTicket(GenericSearch):

    def __init__(self, query=None, sort=None, order=None):
        super().__init__(
            query=query,
            fields=['status_id', 'priority_id', 'author_id', 'assignee_id', 'channel_id', 'external_id',
                    'centribot_project_id', 'centribot_channel_id'],
            sort=sort,
            order=order,
            valid_sort_fields=['status_id', 'priority_id', 'author_id', 'assignee_id', 'channel_id', 'external_id',
                               'centribot_project_id', 'centribot_channel_id', 'created_at', 'updated_at', 'closed_at']
        )
