import json
import tkinter as tk
# from tkinter import ttk
# override above w bootstrap for styling
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog


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



def submit():
    title = title_input.get()
    year = year_input.get()
    director = director_input.get()
    comments = comments_input.get()
    watched = watched_input.instate(['selected'])
    rating = rating_var.get()
    film = Film(title=title, year=year, director=director, rating=rating, watched=watched, comments=comments)
    film.save_data()

    # clear user inputs after submitting data
    title_input.delete(0, tk.END)
    year_input.delete(0, tk.END)
    director_input.delete(0, tk.END)
    # rating_input.invoke() #TODO set 0
    watched_input.invoke() # TODO TEST
    comments_input.delete(0, tk.END)


# main window
# window = tk.Tk()
window = ttk.Window(themename="vapor")  # themes: darkly, journal, cyborg,
window.title("movie weasel")
# window.position_center()
window.place_window_center()
# window.geometry('800x500')

# ---------- LABELS -------------

# main label
main_label = ttk.Label(text="Add New Film", font=("Calibri", 24, "bold"))
main_label.grid(column=1, row=0, pady=10)

# title label
title_label = ttk.Label(master=window, text="Film Title", font='Calibri 14')
title_label.grid(column=0, row=1, pady=10)
title_label.focus_set()

# year label
year_label = ttk.Label(master=window, text="Year Released", font='Calibri 14')
year_label.grid(column=0, row=2, pady=10)

# director label
director_label = tk.Label(text="Director", font="Calibri 14")
director_label.grid(column=0, row=3, pady=10)

# rating label
rating_label = tk.Label(text="Rating", font=("Calibri", 14,))
rating_label.grid(column=0, row=5, pady=10)

# watched label
watched_label = tk.Label(text="Watched", font=("Calibri", 14,))
watched_label.grid(column=0, row=4, pady=10)

# comments label
comments_label = tk.Label(text="Comments", font=("Calibri", 14))
comments_label.grid(column=0, row=6, pady=10, padx=20)

# -------- INPUTS ------------------

#title entry
title_input = ttk.Entry(width=20)
title_input.grid(column=2, row=1, pady=10)
title_input.focus()

# year entry
year_input = ttk.Entry(width=20)
year_input.grid(column=2, row=2, pady=10)

# director entry
director_input = ttk.Entry(width=20)
director_input.grid(column=2, row=3, pady=10)


# rating dropdown
ratings = [1, 2, 3, 4, 5]
rating_var = tk.IntVar(window)
rating_input = tk.OptionMenu(window, rating_var, *ratings)
rating_input.grid(column=2, row=5, pady=10)

# watched toggle
watched_input = ttk.Checkbutton(bootstyle="success-square-toggle")
watched_input.grid(column=2, row=4)

# comments textfield
comments_input = ttk.Entry(width=30)
comments_input.grid(column=2, row=6, pady=10, padx=20)

# submit button
button = ttk.Button(text="Submit", command=submit, bootstyle="info")
button.grid(column=1, row=7, pady=10, padx=20, sticky='EW')

# ---------- SEARCH -------------------------

sep = ttk.Separator(window, orient='horizontal', style="info")
sep.grid(row=8, columnspan=3, pady=20, padx=20, sticky='EW')


def search():
    """searches json file for gives search-term"""
    search_term = search_input.get()
    print(f"[+] Searching for {search_term}...")
    search_input.delete(0, tk.END)
    try:
        with open('films.json', 'r') as file:
            data = json.load(file)
            for i in data:
                if i in search_term:
                    display_search_results(data=data[i], title=search_term)
    except FileNotFoundError:
        print("[-] No previous data found.")


def display_search_results(data: dict, title: str):
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


# search button
search_button = ttk.Button(text="search", command=search, bootstyle="info-outline")
search_button.grid(column=1, row=9, pady=10, sticky='w')

# search box
search_input = ttk.Entry(width=30)
search_input.grid(column=0, row=9, pady=10, padx=20, sticky='ew')

#-------------------------------

# keep window open
window.mainloop()
