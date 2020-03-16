import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:q@localhost/project1")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, author, title, year) VALUES (:isbn, :author, :title, :year)",
                   {"isbn": isbn, "author": author, "title": title, "year": year})
        #print(f"Added book named {title} by {author} in {year} (ISBN:{isbn}).")
    db.commit()

if __name__ == "__main__":
    main()
