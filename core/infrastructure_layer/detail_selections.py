async def select_board(conn, board_uuid, user_uid):
    data = await conn.fetchrow(
        '''SELECT boards.uuid, 
                  boards.name, 
                  boards.description
        FROM (SELECT uuid, name, description FROM boards WHERE boards.uuid = $1) AS boards
        INNER JOIN (SELECT * FROM boards_users_relations WHERE user_uid = $2) AS boards_users_relations 
            ON boards_users_relations.board_uuid = boards.uuid
        ''', board_uuid, user_uid)
    fields = (
        "boards.uuid",
        "boards.name",
        "boards.description"
    )
    return dict(zip(fields, data.values()))
