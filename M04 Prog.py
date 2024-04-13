import csv
import sqlite3
from sqlalchemy import create_engine, select, MetaData, Table, Column, Integer, String

# 16.2
with open('books.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    books = list(reader)

print("Books:", books)

lines = [
    {'title': 'The Weirdstone of Brisingamen', 'author': 'Alan Garner', 'year': 1960},
    {'title': 'Perdido Street Station', 'author': 'China Miéville', 'year': 2000},
    {'title': 'Thud!', 'author': 'Terry Pratchett', 'year': 2005},
    {'title': 'The Spellman Files', 'author': 'Lisa Lutz', 'year': 2007},
    {'title': 'Small Gods', 'author': 'Terry Pratchett', 'year': 1992}
]

with open('books2.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'author', 'year']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(lines)

conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('''CREATE TABLE books
             (title TEXT, author TEXT, year INTEGER)''')
conn.commit()

with open('books2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute("INSERT INTO books VALUES (:title, :author, :year)", row)
conn.commit()

c.execute("SELECT title FROM books ORDER BY title")
print("Titles in alphabetical order:")
for row in c.fetchall():
    print(row[0])

c.execute("SELECT * FROM books ORDER BY year")
print("\nBooks in order of publication:")
for row in c.fetchall():
    print(row)

conn.close()

engine = create_engine('sqlite:///books.db')
metadata = MetaData()
books_table = Table('books', metadata,
                    Column('title', String),
                    Column('author', String),
                    Column('year', Integer))

with engine.connect() as connection:
    stmt = select([books_table.c.title]).order_by(books_table.c.title)
    result = connection.execute(stmt)
    print("\nTitles in alphabetical order (using SQLAlchemy):")
    for row in result:
        print(row[0])