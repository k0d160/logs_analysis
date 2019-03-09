#!/usr/bin/python3.5

import psycopg2

DBNAME = "news"


def create_popular_articles_view():
    # Get the most popular three articles of all time
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("create view pop_articles as\
               select \
               format('\"%s\" --- %s views', title, views) \
               from (select title, articles.author, count(author) \
               as views from articles, log \
               where path = '/article/' || slug \
               group by title, author \
               order by views desc \
               limit 3) as t")
    db.commit()
    db.close()


def create_popular_authors_view():
    # Get the most popular authors of all time
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("create view popular_authors as\
               select format('%s --- %s views', d.name, d.total) as total \
               from (select sum(t.views) as total, t.no as name \
               from (select title, articles.author, authors.id as aid, \
               name as no, count(author) as views from authors, articles, log \
               where authors.id = articles.author and \
               path = '/article/' || slug group by title, author,\
               authors.id, name) as t \
               group by t.no, aid \
               order by total desc) \
               as d group by d.total, d.name \
               order by d.total desc")
    db.commit()
    db.close()


def create_errors_view():
    # On which days did more than 1% of requests lead to errors
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("create view errors as \
               select format('%s --- %s errors', d.date, d.percent) \
               from (select TO_CHAR(time :: DATE, 'Mon dd, yyyy') as date \
               , c.day, to_char(c.percentages, '9.99%') as percent \
               from (select b.day as day, ((b.errors * 100)::float) \
               / (b.ok + b.errors) as percentages \
               from (select a.day as day, (sum(a.status in ('200 OK')::int)) \
               as ok, (sum(a.status in ('404 NOT FOUND')::int)) as errors \
               from (select extract(day from time) as day, \
               time as time, status as status from log) a group by day) as b \
               group by b.day, b.errors, b.ok) c,log \
               where c.day = extract(day from time) and c.percentages >= 1 \
               limit 1) as d")
    db.commit()
    db.close()


create_popular_articles_view()
print("popular_articles view is ready")
create_popular_authors_view()
print("popular_authors view is ready")
create_errors_view()
print("errors view is ready")
print("\n\nCONGRATULATIONS!!! ... All views are ready to be used\n\n")
print('''To see the result of each view simply execute the file: report.py
       using the command::python report.py from a new terminal window.
       Alternatively you can execute each individual view by first executing
       the command::python queries.py. After you have entered the news
       database you can execute each view by simply typing:: SELECT * FROM
       view_name. Example: SELECT * FROM popular_authors\n\n''')
