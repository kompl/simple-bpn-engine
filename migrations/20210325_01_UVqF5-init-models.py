"""
init scopes
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""create extension pgcrypto"""),
    step("""CREATE TABLE users (
                        uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        user_name VARCHAR(47), 
                        hashed_password VARCHAR(256),
                        disabled BOOLEAN DEFAULT FALSE 
            )""")
]
