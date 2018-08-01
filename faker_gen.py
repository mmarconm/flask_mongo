from pymongo import MongoClient
from faker import Faker
from datetime import datetime
from random import choice
from uuid import uuid4


client = MongoClient("mongodb://mmarconm:admin@localhost/tododb") # defaults to port 27017
db = client.tododb

fake = Faker('pt_BR')

status = ['em_rota', 'entreguar', 'conferir']
languages = ['python', 'ruby', 'java', 'javascript', 'c', 'haskell', 'scala', 'R', 'C++']

def populate(n=10):
    count = 0

    while count < n:

        items_doc = {
            'id': uuid4().hex,
            'name': fake.name(),
            'email': fake.email(),
            'date': fake.date(),
            'status': choice(status),
            'language': choice(languages)
        }

        db.tododb.insert(items_doc)
        count += 1

if __name__ == "__main__":
    print("Populating MongoDB")
    populate(100)
    print('Done...')