async def select_board(conn, uuid):
    data = await conn.fetchrow(
        '''SELECT boards.uuid, 
                  boards.name, 
                  boards.description,
                  boards_users_relations.user_uid
        FROM (SELECT uuid, name, description FROM boards WHERE boards.uuid = $1) AS boards
        LEFT JOIN boards_users_relations ON boards_users_relations.board_uuid = boards.uuid
        ''', uuid)
    fields = (
        "boards.uuid",
        "boards.name",
        "boards.description",
        "users.uid"
    )
    if data:
        return dict(zip(fields, data.values()))
