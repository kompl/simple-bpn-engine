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


def alias_generator():
    count = 0
    while True:
        count += 1
        yield f"${count}"


class SelectParamsContainer:
    def __init__(self, table_params, filters, **ordering):
        self.alias_generator = alias_generator()
        self.args = []
        self.filters = filters

        for table_name, id_field__filter_group in filters.items():
            id_field, filter_group = id_field__filter_group
            self.filters[table_name] = self._get_where_string(table_name, filter_group)

        self.order_by_list, self.page_size, self.page_number = table_params
        self.pagination_string = self._get_offset_string()
        self.ordering_string = self._get_ordering_string(ordering)

    def _get_where_string(self, table_name, filter_group):
        query_string_parts = []
        for field_with_method, value in filter_group.items():
            if value:
                field, _, method = field_with_method.rpartition('__')
                self.args.append(self._update_arg(method, value))
                query_string_parts.append(get_expression(method, f'{table_name}.{field}', next(self.alias_generator)))
        if query_string_parts:
            query_expressions_string = ' AND '.join(query_string_parts)
            return f" WHERE {query_expressions_string}"
        else:
            return ''

    @staticmethod
    def _update_arg(method, value):
        arg_patterns = {
            'contains': f"%{value}%"
        }
        return arg_patterns.get(method, value)

    def _get_offset_string(self):
        return f' LIMIT {self.page_size} OFFSET {self.page_size * self.page_number - self.page_size}'

    def _get_ordering_string(self, ordering_fields_mapper):
        def get_index(field_string):
            if field_string.startswith('-'):
                return ' DESC', field_string[1:]
            else:
                return '', field_string

        ordering_string = ' ORDER BY'
        for field in self.order_by_list:
            index, field = get_index(field)
            ordering_string += f' {ordering_fields_mapper[field]}{index}'
        return ordering_string


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
