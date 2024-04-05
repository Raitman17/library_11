import psycopg
from os import getenv
from dotenv import load_dotenv
from random import randint
from faker import Faker

load_dotenv()

vars = (
    ('host', 'PG_HOST'),
    ('port', 'PG_PORT'),
    ('user', 'PG_USER'),
    ('password', 'PG_PASSWORD'),
    ('dbname', 'PG_DBNAME'),
)
credentials = {var: getenv(env_var) for var, env_var in vars}

connection = psycopg.connect(**credentials)
cursor = connection.cursor()

insert_author = 'INSERT INTO library.author (full_name) VALUES (%s)'
faker = Faker()
for _ in range(500):
    cursor.execute(insert_author, (faker.name(),))

connection.commit()

select_author_ids = 'SELECT id from library.author'
cursor.execute(select_author_ids)
authors_ids = [row[0] for row in cursor.fetchall()]

select_book_ids = 'SELECT id from library.book'
cursor.execute(select_book_ids)
books_ids = [row[0] for row in cursor.fetchall()]

insert_link = 'INSERT into library.book_author (book_id, author_id) VALUES (%s, %s)'

for book_id in books_ids:
    authors = authors_ids.copy()
    for _ in range(randint(1, 3)):
        cursor.execute(insert_link, (book_id, authors.pop(randint(0, len(authors) - 1))))

cursor.close()
connection.commit()
connection.close()
