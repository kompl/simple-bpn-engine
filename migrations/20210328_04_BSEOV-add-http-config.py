"""
add http config
"""

from yoyo import step

__depends__ = {'20210328_03_QXhrf-add-method-configs'}

steps = [
    step("""CREATE TABLE http_responses (
                        uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        status smallint, 
                        headers text,
                        body text 
            )""")
]
