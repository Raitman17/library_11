import psycopg
from os import getenv
from dotenv import load_dotenv
from random import randint

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

# genres = (
#     ('fiction', 'students hand in their homeworks in time'),
#     ('novel', 'big book'),
#     ('detective', 'try and find out how students hw works'),
#     ('horror', 'first flake8 experience'),
# )
# insert_genre = 'INSERT INTO library.genre (name, description) VALUES (%s, %s)'
# for genre in genres:
#     cursor.execute(insert_genre, genre)

select_genre_ids = 'SELECT id from library.genre'
cursor.execute(select_genre_ids)
genres_ids = [row[0] for row in cursor.fetchall()]

select_book_ids = 'SELECT id from library.book'
cursor.execute(select_book_ids)
books_ids = [row[0] for row in cursor.fetchall()]

insert_link = 'INSERT into library.book_genre (book_id, genre_id) VALUES (%s, %s)'

for book_id in books_ids:
    genres = genres_ids.copy()
    for _ in range(randint(1, 3)):
        cursor.execute(insert_link, (book_id, genres.pop(randint(0, len(genres) - 1))))

cursor.close()
connection.commit()
connection.close()
