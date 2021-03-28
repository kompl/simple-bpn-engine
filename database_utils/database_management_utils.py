
def get_expression(expression_key, field, alias):
    expressions = {
        '': f"{field} = {alias}",
        'exact': f"{field} = {alias}",
        'contains': f"UPPER({field}) LIKE UPPER({alias})",
        'gt': f"{field} > {alias}",
        'lt': f"{field} < {alias}",
        'gte': f"{field} >= {alias}",
        'lte': f"{field} <= {alias}",
        'in': f"{field} IN [{alias}]",
    }
    return expressions[expression_key]


def separate_data_for_dicts_consistently(data, full_fields_string, *models):
    result = []
    mapped_data = dict(zip(full_fields_string, data.values()))
    for model in models:
        initial_data = {key.split('.')[1]: value
                        for key, value in mapped_data.items()
                        if key.startswith(model.__tablename__)}
        result.append(model.__class__(**initial_data))
    return result


def alias_generator():
    count = 0
    while True:
        count += 1
        yield f"${count}"


def get_inner_join(table_name, id_field, filter_group, variables_array, alias_gen):
    query_string_parts = []
    fields = set()
    fields.add(id_field)
    for field_with_method, value in filter_group.items():
        if value:
            field, _, method = field_with_method.rpartition('__')
            fields.add(field)
            variables_array.append(value)
            query_string_parts.append(get_expression(method, field, next(alias_gen)))
    if query_string_parts:
        query_expressions_string = ' AND '.join(query_string_parts)
        fields_string = ', '.join(list(fields))
        return f" INNER JOIN (SELECT {fields_string} \
                FROM {table_name} WHERE {query_expressions_string}) \
                AS {table_name}_{id_field} \
                ON {table_name}_{id_field}.{id_field} = {table_name}.{id_field}"
    else:
        return ''


def get_where(table_name, filter_group, variables_array, alias_gen):
    query_string_parts = []
    for field_with_method, value in filter_group.items():
        if value:
            field, _, method = field_with_method.rpartition('__')
            variables_array.append(value)
            query_string_parts.append(get_expression(method, f'{table_name}.{field}', next(alias_gen)))
    if query_string_parts:
        query_expressions_string = ' AND '.join(query_string_parts)
        return f" WHERE {query_expressions_string}"
    else:
        return ''


def get_ordering_dict(fields, ordering_fields_mapper):
    def get_index(field_string):
        if field_string.startswith('-'):
            return ' DESC', field_string[1:]
        else:
            return '', field_string

    ordering_string = ' ORDER BY'
    for field in fields:
        index, field = get_index(field)
        ordering_string += f' {ordering_fields_mapper[field]}{index}'
    return ordering_string


def get_offsets(page_size, page_number):
    return f' LIMIT {page_size} OFFSET {page_size * page_number - page_size}'
