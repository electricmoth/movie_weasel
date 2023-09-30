import json
import tkinter as tk
# from tkinter import ttk
# override above w bootstrap for styling
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog

# TODO - sql db, multiple search results/next, encrypt data.


class Film:
    def __init__(self, title, year, director, rating, watched, comments):
        self.title = title
        self.year = year
        self.director = director
        self.rating = rating
        self.watched = watched
        self.comments = comments

    def save_data(self):
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

        except (FileNotFoundError, json.JSONDecodeError):
            # file not found || empty file
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


class Interface(ttk.Window):
    def __init__(self):
        super().__init__(themename="vapor")

        # window = tk.Tk()
        # window = ttk.Window(themename="vapor")  # themes: darkly, journal, cyborg,
        self.title("movie weasel")
        # window.position_center()
        # window.geometry('800x500')

        # main label
        self.main_label = ttk.Label(text="Add New Film", font=("Calibri", 24, "bold"))
        self.main_label.grid(column=1, row=0, pady=10)

        self.title_label = ttk.Label(text="Film Title", font='Calibri 14')
        self.title_label.grid(column=0, row=1, pady=10)
        self.title_label.focus_set()

        # year label
        self.year_label = ttk.Label(text="Year Released", font='Calibri 14')
        self.year_label.grid(column=0, row=2, pady=10)

        # director label
        self.director_label = tk.Label(text="Director", font="Calibri 14")
        self.director_label.grid(column=0, row=3, pady=10)

        # rating label
        self.rating_label = tk.Label(text="Rating", font=("Calibri", 14,))
        self.rating_label.grid(column=0, row=5, pady=10)

        # watched label
        self.watched_label = tk.Label(text="Watched", font=("Calibri", 14,))
        self.watched_label.grid(column=0, row=4, pady=10)

        # comments label
        self.comments_label = tk.Label(text="Comments", font=("Calibri", 14))
        self.comments_label.grid(column=0, row=6, pady=10, padx=20)

        # -------- INPUTS ------------------

        #title entry
        self.title_input = ttk.Entry(width=20)
        self.title_input.grid(column=2, row=1, pady=10)
        self.title_input.focus()

        # year entry
        self.year_input = ttk.Entry(width=20)
        self.year_input.grid(column=2, row=2, pady=10)

        # director entry
        self.director_input = ttk.Entry(width=20)
        self.director_input.grid(column=2, row=3, pady=10)


        # rating dropdown
        self.ratings = [1, 2, 3, 4, 5]
        self.rating_var = tk.IntVar()
        self.rating_input = tk.OptionMenu(self, self.rating_var, *self.ratings)
        self.rating_input.grid(column=2, row=5, pady=10)

        # watched toggle
        self.watched_input = ttk.Checkbutton(bootstyle="success-square-toggle")
        self.watched_input.grid(column=2, row=4)

        # comments textfield
        self.comments_input = ttk.Entry(width=30)
        self.comments_input.grid(column=2, row=6, pady=10, padx=20)

        # submit button
        self.submit_button = ttk.Button(text="Submit", command=self.submit, bootstyle="info")
        self.submit_button.grid(column=1, row=7, pady=10, padx=20, sticky='EW')

        # search button
        self.search_button = ttk.Button(text="search", command=self.search, bootstyle="info-outline")
        self.search_button.grid(column=1, row=9, pady=10)

        # search box
        self.search_input = ttk.Entry(width=20)
        self.search_input.grid(column=0, row=9, pady=10, padx=20, sticky='ew')


        self.sep = ttk.Separator(self, orient='horizontal', style="info")
        self.sep.grid(row=8, columnspan=3, pady=20, padx=20, sticky='EW')


    def submit(self):
        title = self.title_input.get()
        year = self.year_input.get()
        director = self.director_input.get()
        comments = self.comments_input.get()
        watched = self.watched_input.instate(['selected'])
        rating = self.rating_var.get()
        print(self.rating_var)
        print(type(self.rating_var))
        film = Film(title=title, year=year, director=director, rating=rating, watched=watched, comments=comments)
        film.save_data()
        # clear user inputs after submitting data
        self.title_input.delete(0, tk.END)
        self.year_input.delete(0, tk.END)
        self.director_input.delete(0, tk.END)
        # self.rating_input.invoke() #TODO set 0
        self.watched_input.invoke() # TODO TEST
        self.comments_input.delete(0, tk.END)


    def search(self):
        """searches json file for gives search-term"""
        self.search_term = self.search_input.get()
        print(f"[+] Searching for {self.search_term}...")
        self.search_input.delete(0, tk.END)
        try:
            with open('films.json', 'r') as file:
                data = json.load(file)
                for i in data:
                    if i in self.search_term:
                        self.display_search_results(data=data[i], title=self.search_term)
        except FileNotFoundError:
            print("[-] No previous data found.")


    def display_search_results(self, data: dict, title: str):
        """Creates a pop-up box showing found info"""

        message = f"""
        title: {title}
        year: {data["year"]}
        director: {data["director"]}
        comments: {data["comments"]}
        """
        msgbox = MessageDialog(
                message=message,
                title="Found!",
                buttons=["OK:success"],
                padding=(50,50))
        msgbox.show()


#-------------------------------



if __name__ == "__main__":
  window = Interface()
  # keep window open
  window.mainloop()
