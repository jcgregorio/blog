from sqlalchemy import Table, Column, Integer, String, VARCHAR
import dbconfig

table = Table('bin', dbconfig.metadata,
        Column('id', Integer(), primary_key=True),
        Column('code', VARCHAR()),
        Column('language', String(50)),
        Column('filename', String(50))
        )

