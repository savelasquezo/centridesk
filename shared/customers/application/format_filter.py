def format_filters(filters):
    keys = filters.keys()
    if 'name' in keys:
        filters['display_name'] = filters['name']
        del filters['name']
    if 'gdpr' in keys:
        filters['gdpr'] = int(filters['gdpr'])
    return filters


def format_operator(operator):
    return {
        'type': 'operator',
        'operator': operator
    }


def format_condition(field, value):
    return {
        'type': 'condition',
        'field': field,
        'value': value,
        'condition': 'like'
    }


def format_complete_fields(fields, generic_value):
    query = [format_operator('(')]
    for f in fields:
        query.append(format_condition(f, generic_value))
        query.append(format_operator('||'))
    # remove last operator of fields
    query.pop()
    query.append(format_operator(')'))
    return query


def check_field(field):
    return 'display_name' if field == 'name' else field
