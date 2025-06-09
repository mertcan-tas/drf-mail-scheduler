from django.core.management.base import BaseCommand
from django.conf import settings
from decouple import config
from django.utils import termcolors
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Reset the MongoDB database and delete all collections.'

    def handle(self, *args, **options):
        MONGO_HOST = config('MONGO_HOST', default="localhost", cast=str)
        MONGO_PORT = config('MONGO_PORT', default=27017, cast=int)
        MONGO_DB_NAME = config('MONGO_DB_NAME', default="logs", cast=str)
        MONGO_USERNAME = config('MONGO_ROOT_USERNAME', default="mongo", cast=str)
        MONGO_PASSWORD = config('MONGO_ROOT_PASSWORD', default="password", cast=str)

        MONGO_URI = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"

        try:
            client = MongoClient(MONGO_URI)
            db = client[MONGO_DB_NAME]

            for collection_name in db.list_collection_names():
                db[collection_name].drop()
                self.stdout.write(termcolors.make_style(fg="green")(f"Collection '{collection_name}' has been deleted."))

            client.close()
            self.stdout.write(termcolors.make_style(fg="green")(f"✓ MongoDB database '{MONGO_DB_NAME}' has been successfully reset."))

        except Exception as e:
            self.stdout.write(termcolors.make_style(fg="red")(f"✘ An error occurred while resetting MongoDB: {e}"))
