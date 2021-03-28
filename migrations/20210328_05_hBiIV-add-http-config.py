"""
add http config
"""

from yoyo import step

__depends__ = {'20210328_04_BSEOV-add-http-config'}

steps = [
    step("""CREATE TABLE http_method_config (
                        uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        method_uuid UUID REFERENCES method(uuid) ON DELETE CASCADE, 
                        uri_pattern text,
                        method varchar(64),
                        body text,
                        headers text,
                        expected_response_uuid UUID NULL REFERENCES http_responses(uuid) ON DELETE CASCADE
            )""")
]
