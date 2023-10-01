# ~~~ movie weasel ~~~
# this program keeps track of movies a user has watched and data aboutthe movie.
# a user can record their rating and comments about a movie for later review.
# a user can perform queries to view previously-entered data.

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
        self.watched: int = int(watched)  # convert to int for sqlite3 which does not support boolean values
        self.comments:str = comments

    def __repr__(self):
        return f"""
        title: {self.title}
        year: {self.year}
        director: {self.director}
        watched: {self.watched}
        rating: {self.rating}
        comments: {self.comments}
        """


# this is the template for the GUI interface the user interacts with
class Interface(ttk.Window):
    def __init__(self):
        """initialize instance of Interface, which extends the Tkinter window"""
        # use "vapor" colorscheme
        super().__init__(themename="vapor")  # more themes: darkly, journal, cyborg,
        # set title of window
        self.title("Movie Weasel")
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
        # ratings dropdown defaults to 1
        self.rating_var.set(self.ratings[0])
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
        self.submit_button.grid(column=2, row=7, pady=10, padx=20, sticky='EW')
        # search button
        self.search_button = ttk.Button(text="search", command=db.query, bootstyle="info-outline")
        self.search_button.grid(column=1, row=9, pady=10)
        # search input box
        self.search_input = ttk.Entry(width=20)
        self.search_input.insert(0, "search here...")
        self.search_input.configure(foreground='gray')
        self.search_input.grid(column=0, row=9, pady=10, padx=20, sticky='ew')
        self.search_input.bind("<FocusIn>", lambda event: self.clear_default_text())  # When focused, clear default text
        self.search_input.bind("<FocusOut>", lambda event: self.restore_default_text())  # When focus is lost, restore default text
        # separator line to section off the search part
        self.sep = ttk.Separator(self, orient='horizontal', style="info")
        self.sep.grid(row=8, columnspan=3, pady=20, padx=20, sticky='EW')

    def clear_default_text(self):
        """clear 'search here...' text when user click on input field"""
        if self.search_input.get() == "search here...":
            # clear default text
            self.search_input.delete(0, tk.END)
            # change text color when user starts typing
            self.search_input.configure(foreground='white')

    def restore_default_text(self):
        if not self.search_input.get():
            self.search_input.insert(0, "search here...")
            # change text color back to gray
            self.search_input.configure(foreground='gray')

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
        self.rating_var.set(self.ratings[0])
        self.comments_input.delete(0, tk.END)

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

    def display_search_results(self, films: list[Film]):
        """Creates a pop-up message box showing found info from search query"""
        message = ""
        print(f"{films=}")
        for f in films:
            print(f)
            print(f"{type(f)=}")
        # data to be displayed
        # TODO make table
        message = f"{f}"
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
        # create connection to database
        self.conn = sqlite3.connect('films.db')
        # Create a cursor object
        self.cur = self.conn.cursor()

    def create_database(self):
        """create database if it does not exist"""
        self.cur.execute("CREATE TABLE IF NOT EXISTS film(title TEXT, year TEXT, director TEXT, rating INTEGER, watched INTEGER, comments TEXT)")
        print("[+] database created.")

    def query(self):
        """search database for user-supplied query"""
        search_term = window.search_input.get()
        # clear search query from search input when user hits search button
        window.restore_default_text()
        print(f"Searching for {search_term}...")
        # TODO multiple results
        res: list = self.cur.execute("SELECT * from film WHERE title = ?", (search_term,)).fetchall()
        if res:
            window.display_search_results(films=res)
        else:
            print("[-] not found.")
            window.not_found()

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
    # keep window open
    window.mainloop()
  # exit if program receives keyboard interrupt/ control-C
  except KeyboardInterrupt:
    print("\nGoodbye.\n")

