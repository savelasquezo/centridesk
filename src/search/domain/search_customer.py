from src.search.domain.generic_search import GenericSearch


class SearchCustomer(GenericSearch):

    def __init__(self, query=None, sort=None, order=None):
        super().__init__(
            query=query,
            fields=['phone', 'email', 'centribot_external_id', 'display_name', 'company', 'agent_id', 'delegation',
                    'external_id'],
            sort=sort,
            order=order,
            valid_sort_fields=['phone', 'email', 'centribot_external_id', 'display_name', 'company', 'agent_id',
                               'created_at', 'updated_at', 'last_comment_at', 'delegation', 'external_id']
        )
