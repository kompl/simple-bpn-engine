"""
add http config
"""

from yoyo import step

__depends__ = {'20210328_05_hBiIV-add-http-config'}

steps = [
    step("""CREATE TABLE boards_users_relations (
                board_uuid UUID REFERENCES boards(uuid) ON DELETE CASCADE,
                user_uid UUID REFERENCES users(uid) ON DELETE CASCADE,
                CONSTRAINT boards_users_composite_pkey PRIMARY KEY(board_uuid, user_uid) 
    )""")
]
