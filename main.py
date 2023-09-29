import json
import tkinter as tk
# from tkinter import ttk
# override above w bootstrap for styling
import ttkbootstrap as ttk


class Film:
    def __init__(self, title, year, director, rating, comments):
        self.title = title
        self.year = year
        self.director = director
        self.rating = rating
        self.comments = comments

    def save_data(self):
        new_data = {
                "title": self.title,
                "year": self.year,
                "director": self.director,
                "rating": self.rating,
                "comments": self.comments,
                }
        try:
            with open('./films.json', 'r') as file:
                # try to read old data
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # file not found
            print(f"[-] no existing data file found.")
            data = new_data
        else:
                # update with new data
                data.update(new_data)
        finally:
            # either way:
            with open('./films.json', 'w') as file:
                # save data
                json.dump(data, file, indent=4)
            print("[+] new data saved.")



def submit():
    title = title_input.get()
    year = year_input.get()
    director = director_input.get()
    rating = rating_input.get()
    comments = comments_input.get()
    print(title)
    print(year)
    print(director)
    print(rating)
    print(comments)
    film = Film(title=title, year=year, director=director, rating=rating, comments=comments)
    film.save_data()

    title_input.delete(0, tk.END)
    year_input.delete(0, tk.END)
    director_input.delete(0, tk.END)
    rating_input.delete(0, tk.END)
    comments_input.delete(0, tk.END)


# main window
window = tk.Tk()
# window = ttk.Window()
window.title("movie weasel")
window.minsize(width=500, height=300)
# window.config(padx=100, pady=200)

# ---------- LABELS -------------

# main label
main_label = ttk.Label(text="add new film", font=("Calibri", 24, "bold"))
main_label.grid(column=0, row=0)
# main_label.config(padx=50, pady=50)

# title label
title_label = ttk.Label(master=window, text="film title", font='Calibri 14')
title_label.grid(column=0, row=1)
# title_label.config(padx=20, pady=20)

# year label
year_label = ttk.Label(master=window, text="year released", font='Calibri 14')
year_label.grid(column=0, row=2)
# year_label.config(padx=20, pady=20)

# director label
director_label = tk.Label(text="director", font="Calibri 14")
director_label.grid(column=0, row=3)
# director_label.config(padx=20, pady=20)

# rating label
rating_label = tk.Label(text="rating", font=("Calibri", 14,))
rating_label.grid(column=0, row=4)
# rating_label.config(padx=20, pady=20)

# comments label
comments_label = tk.Label(text="comments", font=("Calibri", 14))
comments_label.grid(column=0, row=5)
# comments_label.config(padx=20, pady=20)

# -------- INPUTS ------------------

#title entry
title_input = tk.Entry(width=20)
title_input.grid(column=2, row=1)

# year entry
year_input = tk.Entry(width=20)
year_input.grid(column=2, row=2)

# director entry
director_input = tk.Entry(width=20)
director_input.grid(column=2, row=3)

# rating dropdown  # TODO dropdown
rating_input = tk.Entry(width=20)
rating_input.grid(column=2, row=4)

# comments textfield
comments_input = tk.Entry(width=50)
comments_input.grid(column=2, row=5)

# submit button
button = tk.Button(text="submit", command=submit)
button.grid(column=1, row=6)





# keep window open
window.mainloop()
