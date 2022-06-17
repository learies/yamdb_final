import csv
import sqlite3

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

with open("static/data/category.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_category "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

with open("static/data/comments.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        review_id = row['review_id']
        text = row['text']
        author_id = row['author']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO reviews_comment "
            "(id, text, pub_date, author_id, review_id) "
            "VALUES(?, ?, ?, ?, ?)",
            (id, text, pub_date, author_id, review_id)
        )
        conn.commit()

with open("static/data/genre.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        slug = row['slug']
        c.execute(
            "INSERT INTO reviews_genre "
            "(id, name, slug) "
            "VALUES(?, ?, ?)",
            (id, name, slug)
        )
        conn.commit()

with open("static/data/genre_title.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        genre_id = row['genre_id']
        c.execute(
            "INSERT INTO reviews_title_genre "
            "(id, title_id, genre_id) "
            "VALUES(?, ?, ?)",
            (id, title_id, genre_id)
        )
        conn.commit()

with open("static/data/review.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        title_id = row['title_id']
        text = row['text']
        author_id = row['author']
        score = row['score']
        pub_date = row['pub_date']
        c.execute(
            "INSERT INTO reviews_review "
            "(id, text, score, pub_date, author_id, title_id) "
            "VALUES(?, ?, ?, ?, ?, ?)",
            (id, text, score, pub_date, author_id, title_id)
        )
        conn.commit()

with open("static/data/titles.csv", "r", encoding="utf-8") as data:
    reader = csv.DictReader(data)
    for row in reader:
        id = row['id']
        name = row['name']
        year = row['year']
        category_id = row['category']
        c.execute(
            "INSERT INTO reviews_title "
            "(id, name, year, category_id, description) "
            "VALUES(?, ?, ?, ?, '')",
            (id, name, year, category_id)
        )
        conn.commit()

conn.close()
