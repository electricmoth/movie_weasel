class Film:
    def __init__(self, title, year, director, rating, watched, comments):
        self.title: str = title
        self.year: str = year
        self.director: str = director
        self.rating: int = rating
        self.watched: str = "yes" if int(watched) else "no"  # convert boolean value to string
        self.comments: str = comments

