async def create_boards_user_relation(conn, board_uuid, user_uid):
    await conn.fetch(
        f'''INSERT INTO boards_users_relations (board_uuid, user_uid) VALUES ($1, $2)''', board_uuid, user_uid
    )
