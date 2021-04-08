"""
remove user_uid from boards
"""

from yoyo import step

__depends__ = {'20210328_06_TPTOv-add-http-config'}

steps = [
    step("""ALTER TABLE boards DROP COLUMN users_uid""")
]
