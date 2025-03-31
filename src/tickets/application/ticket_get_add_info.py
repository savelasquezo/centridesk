def add_ticket_info(account_id, ticket, customers_obj, agents_obj, status_dict=None, priorities_dict=None,
                    channels_dict=None):
    if status_dict:
        ticket['status'] = status_dict[ticket['status_id']]

    if status_dict:
        ticket['priority'] = priorities_dict[ticket['priority_id']]

    if ticket['is_agent'] is False:
        customers_obj.account_id = account_id
        customers_obj.customer_id = ticket['author_id']
        ticket['author'] = customers_obj.get_by_id()

    else:
        agents_obj.agent_id = ticket['author_id']
        ticket['author'] = agents_obj.get_by_id()

    if channels_dict:
        ticket['channel_name'] = channels_dict.get(ticket['channel_id'])

    return ticket
