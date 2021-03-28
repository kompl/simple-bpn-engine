"""
add method configs
"""

from yoyo import step

__depends__ = {'20210328_02_RhcGq-add-method-models'}

steps = [
    step("""CREATE TABLE plane_job_method_config (
                    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    method_uuid UUID REFERENCES method(uuid) ON DELETE CASCADE, 
                    plane_execution_date_time TIMESTAMPTZ,
                    completed BOOLEAN DEFAULT FALSE 
        )"""),
    step("""CREATE TABLE periodic_job_config (
                    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    method_uuid UUID REFERENCES method(uuid) ON DELETE CASCADE, 
                    last_call TIMESTAMPTZ,
                    interval INT 
        )""")
]
