
async def select_user(conn, user_name):
    data = await conn.fetch(
        '''SELECT users.uid,
                  users.user_name, 
                  users.disabled,
                  users.hashed_password,
                  boards_users_relations.board_uuid
        FROM (SELECT uid, user_name, disabled, hashed_password FROM users WHERE users.user_name = $1) AS users
        LEFT JOIN boards_users_relations ON boards_users_relations.user_uid = users.uid
        ''', user_name)
    fields = (
        "users.uid",
        "users.user_name",
        "users.disabled",
        "users.hashed_password",
        "boards_users_relations.board_uuid"
    )
    return [dict(zip(fields, row.values())) for row in data if row.get("user_name")]
