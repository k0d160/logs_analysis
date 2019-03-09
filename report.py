#!/usr/bin/python3.5

import psycopg2


DBNAME = 'news'

# Get the views responses from the database
def get_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from pop_articles")
    pop_articles = c.fetchall()
    db.close()
    return pop_articles


def get_popular_authors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from popular_authors")
    pop_authors = c.fetchall()
    db.close()
    return pop_authors


def get_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from errors")
    errors = c.fetchall()
    db.close()
    return errors

# Store response from views
articles = get_popular_articles()
authors = get_popular_authors()
errors = get_errors()

# Display output from views in plain text
print("\nThe most popular articles of all time are:\n")
print("{0[0]}\n{1[0]}\n{2[0]}".format(*articles))
print("\nThe most popular authors of all time are:\n")
print("{0[0]}\n{1[0]}\n{2[0]}\n{3[0]}".format(*authors))
print("\nThe day on which more than 1% of request"
      " lead to errors was:\n")
print("{0[0]}\n".format(*errors))
