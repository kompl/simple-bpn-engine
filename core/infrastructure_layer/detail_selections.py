async def select_board(conn, uuid, user_uid):
    data = await conn.fetchrow(
        '''SELECT boards.uuid, 
                  boards.name, 
                  boards.description,
                  boards_users_relations.user_uid
        FROM (SELECT uuid, name, description FROM boards WHERE boards.uuid = $1) AS boards
        LEFT JOIN (SELECT * FROM boards_users_relations WHERE user_uid = $2) AS boards_users_relations 
            ON boards_users_relations.board_uuid = boards.uuid
        ''', uuid, user_uid)
    fields = (
        "boards.uuid",
        "boards.name",
        "boards.description",
        "users.uid"
    )
    if data:
        return dict(zip(fields, data.values()))
    else:
        raise For
