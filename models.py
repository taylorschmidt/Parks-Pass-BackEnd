from peewee import *
import datetime
from flask_login import UserMixin
import os 
from playhouse.db_url import connect
import psycopg2

# DATABASE = os.environ['DATABASE_URL']

DATABASE = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
# DATABASE = connect(os.environ.get('DATABASE_URL'))
# DATABASE = PostgresqlDatabase('parks_pass', host='localhost', port=5432)

class BaseModel(Model):
    class Meta:
        database = DATABASE

class Park(BaseModel):
    park_code = CharField(unique=True)

class Person(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()
    
class PersonPark (BaseModel):
    person = ForeignKeyField(Person, backref='sites')
    visited_park = ForeignKeyField(Park, backref='tourist')
    # favorite_park = ForeignKeyField(Park, backref='fav-tourist')

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Person, Park, PersonPark])
    print("Database tables created.")
    DATABASE.close()