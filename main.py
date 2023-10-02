# ~~~ movie weasel ~~~
# this program keeps track of movies a user has watched and data aboutthe movie.
# a user can record their rating and comments about a movie for later review.
# a user can perform queries to view previously-entered data.

# sql database setup
import sqlite3

# styling and components for gui interface
import tkinter as tk

# wrapper method to use with tkinter buttons
from functools import partial
from tkinter import messagebox

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview


class Film:
    def __init__(self, title, year, director, rating, watched, comments):
        self.title:str = title
        self.year:str = year
        self.director:str = director
        self.rating: int = rating
        self.watched: str = "yes" if int(watched) else "no"  # convert boolean value to string
        self.comments:str = comments


# ----------------- SQL DATABASE ----------------------
class Database():
    def __init__(self):
        # create connection to database
        self.conn = sqlite3.connect('films.db')
        # Create a cursor object
        self.cur = self.conn.cursor()

    def create_database(self):
        """create database if it does not already exist"""
        self.cur.execute("CREATE TABLE IF NOT EXISTS film(title TEXT, year TEXT, director TEXT, rating INTEGER, watched INTEGER, comments TEXT)")
        print("[+] database created.")

    def query(self):
        """search database for user-supplied query"""
        thing = window.search_input.get()
        print(f"searching for {thing}...\n")
        rows = self.cur.execute("SELECT * FROM film WHERE title = ?", (thing,)).fetchall()
        print(rows)

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
        self.cur.execute("INSERT INTO film VALUES(:title, :year, :director, :rating, :watched, :comments)", data)
        # save changes
        self.conn.commit()


# this is the template for the GUI interface the user interacts with
class Interface(ttk.Window):
    def __init__(self):
        """initialize instance of Interface, which extends the Tkinter window"""
        # use "vapor" colorscheme
        super().__init__(themename="vapor")  # more themes: darkly, journal, cyborg,
        # set title of window
        self.title("movie weasel")
        # main "Add New Film" label

    def add_screen(self):
        """displays widgets on screen that allow user to enter film data"""
        self.clear_widgets()
        self.main_label = ttk.Label(text="Add New Film", font=("Calibri", 24, "bold"))
        self.main_label.grid(column=1, row=0, pady=10)
        # label for 'film title' input box
        self.title_label = ttk.Label(text="Film Title", font='Calibri 14')
        self.title_label.grid(column=0, row=1, pady=10)
        self.title_label.focus_set()
        # label for 'year released' input box
        self.year_label = ttk.Label(text="Year Released", font='Calibri 14')
        self.year_label.grid(column=0, row=2, pady=10)
        # label for 'director' input box
        self.director_label = tk.Label(text="Director", font="Calibri 14")
        self.director_label.grid(column=0, row=3, pady=10)
        # label for 'rating' dropdown menu
        self.rating_label = tk.Label(text="Rating", font=("Calibri", 14,))
        self.rating_label.grid(column=0, row=5, pady=10)
        # label for 'watched' toggle button
        self.watched_label = tk.Label(text="Watched", font=("Calibri", 14,))
        self.watched_label.grid(column=0, row=4, pady=10)
        # label for 'comments' input box
        self.comments_label = tk.Label(text="Comments", font=("Calibri", 14))
        self.comments_label.grid(column=0, row=6, pady=10, padx=20)
        # -------- INPUTS ------------------
        #title input box
        self.title_input = ttk.Entry(width=20)
        self.title_input.grid(column=2, row=1, pady=10)
        self.title_input.focus()
        # year input box
        self.year_input = ttk.Entry(width=20)
        self.year_input.grid(column=2, row=2, pady=10)
        # director input box
        self.director_input = ttk.Entry(width=20)
        self.director_input.grid(column=2, row=3, pady=10)
        # rating dropdown menu
        # rating can be 1-5
        self.ratings = [1, 2, 3, 4, 5]
        self.rating_var = tk.IntVar()
        self.rating_input = tk.OptionMenu(self, self.rating_var, *self.ratings)
        self.rating_input.grid(column=2, row=5, pady=10)
        # watched toggle button
        self.watched_input = ttk.Checkbutton(bootstyle="success-square-toggle")
        self.watched_input.grid(column=2, row=4)
        # comments input box
        self.comments_input = ttk.Entry(width=30)
        self.comments_input.grid(column=2, row=6, pady=10, padx=20)
        # submit button
        self.submit_button = ttk.Button(text="Submit", command=self.submit, bootstyle="light")
        self.submit_button.grid(column=1, row=7, pady=10, padx=20, sticky='EW')
        # search input box
        # self.search_input = ttk.Entry(width=20)
        # self.search_input.grid(column=0, row=9, pady=10, padx=20, sticky='ew')
        # search button
        # command=partial(db.query, self.search_input.get()),
        #self.search_button = ttk.Button(text="search", command=partial(db.query, (self.search_input.get(),)), bootstyle="info-outline")
        self.search_button = ttk.Button(text="show data", command=self.show_data, bootstyle="secondary-outline")
        self.search_button.grid(column=1, row=9, pady=10)
        # separator line to section off the search part
        self.sep = ttk.Separator(self, orient='horizontal', style="light")
        self.sep.grid(row=8, columnspan=3, pady=20, padx=20, sticky='EW')

    def clear_widgets(self):
        """clears all widgets from screen"""
        for widget in self.winfo_children():
            widget.destroy()

    def submit(self):
        """gets user input from input boxes/buttons. creates new Film object, saves data"""
        # get text input entered by user
        title = self.title_input.get()
        year = self.year_input.get()
        director = self.director_input.get()
        comments = self.comments_input.get()
        # check if watched toggle button is set on or off
        watched = self.watched_input.instate(['selected'])
        # check what the rating dropdown was set to
        rating = self.rating_var.get()
        # create a new instance of Film class
        film = Film(title=title, year=year, director=director, rating=rating, watched=watched, comments=comments)
        # save data
        db.insert_film(film)
        # clear user inputs after submitting data
        self.title_input.delete(0, tk.END)
        self.year_input.delete(0, tk.END)
        self.director_input.delete(0, tk.END)
        # self.rating_input.invoke() #TODO set 0
        self.watched_input.invoke() # TODO TEST
        self.comments_input.delete(0, tk.END)

    # def not_found(self):
    #     """create popup message box to show that no results were found"""
    #     # create the message box
    #     messagebox.showinfo("Not Found!", "No results for that query.")

    def show_data(self):
       """clears home screen widgets and shows table of user's data"""
       # clear screen
       self.clear_widgets()
       # home button
       self.home_button = ttk.Button(text="Back", command=self.add_screen, bootstyle="light-outline")
       self.home_button.grid(column=0, row=0, pady=10, padx=20, sticky='W')

       films = db.cur.execute("SELECT * FROM film").fetchall()
       coldata = [
            {"text": "title", "stretch": True},
            {"text": "year", "stretch": False, "width": 55},
            {"text": "director", "stretch": False},
            {"text": "rating", "stretch": False, "width": 55, "anchor": 'center'},
            {"text": "seen", "stretch": False,"width": 75},
            {"text": "comment", "stretch": True},
        ]
       rowdata = list(films)

       dt = Tableview(
            master=self,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
        )
       dt.grid(padx=10, pady=10, column=0, row=1)
       dt.focus_set()


# -------- MAIN LOOP -------------------
# main program
if __name__ == "__main__":
  try:
    # initialize database
    db = Database()
    # create table in database
    db.create_database()
    # create GUI window
    window = Interface()
    # show add new film screen
    window.add_screen()
    # keep window open
    window.mainloop()
    # close database
    db.close()
  # exit if program receives keyboard interrupt/ control-C
  except KeyboardInterrupt:
    print("\nGoodbye.\n")

