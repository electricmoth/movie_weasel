import sqlite3
from film import Film


class Database:
    def __init__(self):
        """initialize a new Database instance"""
        # create connection to database
        with sqlite3.connect('films.db') as self.conn:
            # Create a cursor object
            self.cur = self.conn.cursor()

    def create_database(self):
        """create database if it does not already exist"""
        self.cur.execute("CREATE TABLE IF NOT EXISTS film(title TEXT, year TEXT, director TEXT, rating INTEGER, watched INTEGER, comments TEXT)")
        print("[+] database created.")

    def insert_film(self, f: Film):
        """add new film to database"""
        # database fields are: id, title, yr, dir, rating, watched, comments
        data = (
            {
                "title": f.title,
                "year": f.year,
                "director": f.director,
                "rating": f.rating,
                "watched": f.watched,
                "comments": f.comments,
             }
                )
        # insert data into database
        try:
            self.cur.execute("INSERT INTO film VALUES(:title, :year, :director, :rating, :watched, :comments)", data)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        else:
            # save changes
            self.conn.commit()

