"""
Add constrain to user
"""

from yoyo import step

__depends__ = {'20210325_01_UVqF5-init-models'}

steps = [
    step("ALTER TABLE users ADD CONSTRAINT user_name_uniq UNIQUE (user_name)")
]
