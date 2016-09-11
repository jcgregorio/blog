from sqlalchemy import *
import dbconfig

recipe = Table('recipe', dbconfig.metadata,
             Column('id', Integer, primary_key=True),
             Column('title', String(200)),
             Column('instructions', String(30000)),
         )

