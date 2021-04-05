from fastapi_async_db_utils.utils import alias_generator, get_expression


class DoesNotExist(Exception):
    pass


async def simple_read(conn, model):
    init_data = model.dict()
    fields = list(init_data.keys())
    fields_string = ', '.join([field for field in fields])
    data = await conn.fetch(
        f'''SELECT {fields_string} FROM {model.__tablename__}'''
    )
    if data:
        return [dict(zip(fields, row.values())) for row in data]
    else:
        raise DoesNotExist


async def read_by_params(conn, model, **filters):
    alias_gen = alias_generator()
    init_data = model.dict()
    fields = list(init_data.keys())
    values = list(filters.values())
    filters_string = ' AND '.join([get_expression(field__exp_key.partition('__')[2],
                                                  field__exp_key.partition('__')[0],
                                                  next(alias_gen))
                                   for field__exp_key, value in filters.items()])
    fields_string = ', '.join([field for field in fields])
    data = await conn.fetch(f'''SELECT {fields_string} FROM {model.__table__} WHERE {filters_string}''', *values)
    if data:
        return [model.construct(**dict(row)) for row in data]
    else:
        raise DoesNotExist


async def create(conn, model):
    init_data = model.dict()
    returning_fields = ', '.join(list(init_data.keys()))
    if not getattr(model, model.__pk__):
        init_data.pop(model.__pk__)
    values = list(init_data.values())
    fields_string = ', '.join(list(init_data.keys()))
    aliases = ', '.join([f"${num + 1}" for num in range(len(values))])
    data = await conn.fetchrow(
        f'''INSERT INTO {model.__table__} ({fields_string}) VALUES ({aliases}) RETURNING {returning_fields}''', *values
    )
    if data:
        return model.construct(**dict(data))
    else:
        raise DoesNotExist


async def bulk_create(conn, models):
    alias_gen = alias_generator()
    fields_list = [field for field in dir(models[0]) if not field.startswith('_') and field != 'metadata']
    variables = [getattr(model, field) for model in models for field in fields_list]
    aliases = [[next(alias_gen) for i in range(len(fields_list))] for rows in range(len(models))]
    fields = ', '.join([field for field in fields_list])
    aliases_string = '(' + '), ('.join([', '.join(aliases_row) for aliases_row in aliases]) + ')'
    data = await conn.fetch(
        f'''INSERT INTO {models[0].__tablename__} ({fields}) VALUES {aliases_string} RETURNING {fields}''', *variables
    )
    if data:
        return [models[0].__class__(**dict(row)) for row in data]
    else:
        raise DoesNotExist


async def update_by_params(conn, model, *excluded, **filters):
    alias_gen = alias_generator()
    fields = [field for field in dir(model)
              if not field.startswith('_') and field != 'metadata' and field not in excluded]
    set_list = ', '.join([f'{field} = {next(alias_gen)}' for field in fields])
    fields_string = ', '.join([field for field in fields + list(excluded)])
    filters_string = ' AND '.join([get_expression(field__exp_key.partition('__')[2],
                                                  field__exp_key.partition('__')[0],
                                                  next(alias_gen))
                                   for field__exp_key, value in filters.items()])
    values = [getattr(model, field) for field in fields] + [value for value in filters.values()]
    data = await conn.fetchrow(
        f'''UPDATE {model.__tablename__} SET {set_list} WHERE {filters_string} RETURNING {fields_string}''', *values
    )
    if data:
        return model.__class__(**dict(data))
    else:
        raise DoesNotExist


async def delete_by_params(conn, model, **filters):
    alias_gen = alias_generator()
    fields = [field for field in dir(model) if not field.startswith('_') and field != 'metadata']
    fields_string = ', '.join([field for field in fields])
    filters_string = ' AND '.join([get_expression(field__exp_key.partition('__')[2],
                                                  field__exp_key.partition('__')[0],
                                                  next(alias_gen))
                                   for field__exp_key, value in filters.items()])
    values = [value for value in filters.values()]
    data = await conn.fetch(
        f'''DELETE FROM {model.__tablename__} WHERE {filters_string} RETURNING {fields_string}''', *values
    )
    if data:
        return [model.__class__(**dict(row)) for row in data]
    else:
        return []
