"""
add method models
"""

from yoyo import step

__depends__ = {'20210328_01_aECcO-init-core-models'}

steps = [
    step("""CREATE TABLE methods (
                    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(47), 
                    description VARCHAR(1024),
                    disabled BOOLEAN DEFAULT FALSE,
                    status_id INT REFERENCES method_statuses(id) ON DELETE CASCADE, 
                    next_method_uuid UUID REFERENCES methods(uuid) ON DELETE CASCADE,
                    prev_method_uuid UUID REFERENCES methods(uuid) ON DELETE CASCADE
                    )""")
]
