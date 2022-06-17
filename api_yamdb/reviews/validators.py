import datetime as dt


def validate_year(year):
    current_year = dt.date.today()
    if year > current_year.year or year <= 0:
        raise ValueError(f'Некорректный год {year}')
