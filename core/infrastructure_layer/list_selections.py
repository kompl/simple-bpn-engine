from fastapi_async_db_utils.utils import SelectParamsContainer


async def select_board_list(conn, page_params, filters):
    container = SelectParamsContainer(page_params, filters, name='boards.name', description='boards.description')
    data = await conn.fetch(
        f'''SELECT  boards.uuid, 
                    boards.name, 
                    boards.description
        FROM (SELECT uid FROM users {container.filters['users']}) AS users
        LEFT JOIN boards_users_relations 
            ON boards_users_relations.user_uid = users.uid
        LEFT JOIN (SELECT uuid, name, description FROM boards {container.filters['boards']}) AS boards 
            ON boards_users_relations.board_uuid = boards.uuid
        {container.ordering_string} {container.pagination_string} 
        ''', *container.args)
    fields = (
        "boards.uuid",
        "boards.name",
        "boards.description",
    )
    if data:
        return [dict(zip(fields, row.values())) for row in data if row.get("uuid")]
    else:
        return []
