import psycopg2

DBNAME = "news"


def get_popular_articles():
    ''' Get the most popular three articles of all time '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select format('%s --- %s views', title, count(*)) slug, path, \
              count(path) as views \
              from articles, log where path = '/article/' || slug \
              group by slug, path, title \
              order by views desc limit 3")
    pop_articles = c.fetchall()
    db.close()
    return pop_articles


def get_popular_authors():
    ''' Get the most popular authors of all time '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from authors")
    pop_authors = c.fetchall()
    db.close()
    return pop_authors


def get_errors():
    ''' On which days did more than 1% of requests lead to errors '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select * from log limit 10")
    errs = c.fetchall()
    db.close()
    return errs

print("\nThe most popular articles of all time are:\n")
print(get_popular_articles())
print("\nThe most popular authors of all time are:\n")
print(get_popular_authors())
print("\nThe days on which more than 1% of request"
      "lead to errors were:\n")
print(get_errors())
