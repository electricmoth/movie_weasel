# ~~~ movie weasel ~~~
# this program keeps track of movies a user has watched and data aboutthe movie.
# a user can record their rating and comments about a movie for later review.
# a user can perform queries to view previously-entered data.

import json

# sql database setup
import sqlite3

# styling and components for gui interface
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog

# TODO - multiple search results/next, encrypt data.


class Film:
    def __init__(self, title, year, director, rating, watched, comments):
        self.title:str = title
        self.year:str = year
        self.director:str = director
        self.rating: int = rating
        self.watched: int = int(watched)  # convert to int for sqlite3
        self.comments:str = comments

    def save_data(self):
        """save user entered data"""
        new_data = {
                self.title: {
                "year": self.year,
                "director": self.director,
                "rating": self.rating,
                "watched": self.watched,
                "comments": self.comments,
                }
            }
        try:
            with open('films.json', 'r') as file:
                # try to read existing data
                data = json.load(file)

        # if file not found || data file is empty
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"[-] no existing data file found. creating new file.")
            # write new data only
            with open('films.json', 'w') as file:
                json.dump(new_data, file, indent=4)

        else:
            # if existing data found, add new data
            data.update(new_data)
            with open('films.json', 'w') as file:
                json.dump(data, file, indent=4)
        finally:
            print("[+] new data saved.")


# this is the template for the GUI interface the user interacts with
class Interface(ttk.Window):
    def __init__(self):
        """initialize instance of Interface, which extends the Tkinter window"""
        # use "vapor" colorscheme
        super().__init__(themename="vapor")  # more themes: darkly, journal, cyborg,
        # set title of window
        self.title("movie weasel")
        # main "Add New Film" label
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
        self.submit_button = ttk.Button(text="Submit", command=self.submit, bootstyle="info")
        self.submit_button.grid(column=1, row=7, pady=10, padx=20, sticky='EW')
        # search button
        self.search_button = ttk.Button(text="search", command=self.search, bootstyle="info-outline")
        self.search_button.grid(column=1, row=9, pady=10)
        # search input box
        self.search_input = ttk.Entry(width=20)
        self.search_input.grid(column=0, row=9, pady=10, padx=20, sticky='ew')
        # separator line to section off the search part
        self.sep = ttk.Separator(self, orient='horizontal', style="info")
        self.sep.grid(row=8, columnspan=3, pady=20, padx=20, sticky='EW')

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

    def search(self):
        """searches data for user-supplied search-term"""
        self.search_term = self.search_input.get()
        print(f"[+] Searching for {self.search_term}...")
        # clear the search bar when user presses submit
        self.search_input.delete(0, tk.END)
        try:
            # try to read previous data
            with open('films.json', 'r') as file:
                data = json.load(file)
                for i in data:
                    if i in self.search_term:
                        # display search results to user
                        self.display_search_results(data=data[i], title=self.search_term)
                    else:
                        # display a popup that shows no results were found
                        self.not_found()
        # if the data file does not exist
        except FileNotFoundError:
            print("[-] No previous data found.")

    def not_found(self):
        """create popup message box to show that no results were found"""
        # create the message box
        message = "No results found."
        msgbox = MessageDialog(
                message=message,
                title="Not Found!",
                buttons=["OK:success"],
                padding=(50,50))
        # display the message box
        msgbox.show()

    def display_search_results(self, data: dict, title: str):
        """Creates a pop-up message box showing found info from search query"""
        # data to be displayed
        message = f"""
        title: {title}
        year: {data["year"]}
        director: {data["director"]}
        comments: {data["comments"]}
        """
        # create the message box
        msgbox = MessageDialog(
                message=message,
                title="Found!",
                buttons=["OK:success"],
                padding=(50,50))
        # display the message box
        msgbox.show()


# --------- SQL DATABASE ----------------------
class Database():
    def __init__(self):
        print("database init.")

        # create connection to database
        self.conn = sqlite3.connect('films.db')
        # Create a cursor object
        self.cur = self.conn.cursor()

    def create_database(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS film(title TEXT, year TEXT, director TEXT, rating INTEGER, watched INTEGER, comments TEXT)")
        # self.cur.execute("CREATE TABLE IF NOT EXISTS film(id INTEGER PRIMARY KEY, title TEXT, year TEXT, director TEXT, rating INTEGER, watched INTEGER, comments TEXT)")
        print("database created.")

    def query(self):
        """search database for user-supplied query"""
        res = self.cur.execute("SELECT title from film")
        print(res.fetchall())
        print("query")

    def insert_film(self, f: Film):
        """add new film to database"""
        # database fields are: id, title, yr, dir, rating, watched, comments

        # self.cur.execute("""
        # INSERT INTO film (title, year, director, rating, watched, comments) VALUES
        #     ('Monty Python and the Holy Grail', "1975", "unknown", 5, 1, "neeeee")
        # """)

        # data = (

        #     {
        #         "title": f.title,
        #         "year": f.year,
        #         "director": f.director,
        #         "rating": f.rating,
        #         "watched": f.watched,
        #         "comments": f.comments,
        #      }
        #         )

        # self.cur.executemany("INSERT INTO film VALUES(:title, :year, :director, :rating, :watched, :comments)", data)

        # save data
        self.conn.commit()


# -------- MAIN LOOP -------------------

# main program
if __name__ == "__main__":
  # create GUI window
  window = Interface()
  # initialize database
  db = Database()
  # create table in database
  db.create_database()
  # keep window open
  window.mainloop()
  # testing: query all entries
  db.query()

