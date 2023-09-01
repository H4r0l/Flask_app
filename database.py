from peewee import MySQLDatabase, Model, TextField, DateTimeField, IntegerField, ForeignKeyField, CharField
from os import environ
import datetime


db = MySQLDatabase(
    environ.get("DB_NAME"),
    user=environ.get("DB_USER"),
    password=environ.get("DB_PASSWORD"),
    port=int(environ.get("DB_PORT")),
    host=environ.get("DB_HOST")
)


class User(Model):  # Tables
    username = CharField()
    password = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = "users"

    @classmethod
    def create_user(cls, _username, _password):
        _password = "encrypt_" + _password
        return User.create(username=_username, password=_password)


# Migrations
class Product(Model):  # Tables
    name = TextField()
    price = IntegerField()
    user = ForeignKeyField(User, backref="products")
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        db_table = "products"


db.create_tables([User, Product])