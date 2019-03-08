import psycopg2

DBNAME = "news"


def get_popular_articles():
    ''' Get the most popular three articles of all time '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select \
               format('%s --- %s views', title, views) \
               from (select title, articles.author, count(author) \
               as views from articles, log \
               where path = '/article/' || slug \
               group by title, author \
               order by views desc \
               limit 3) as t;")
    pop_articles = c.fetchall()
    db.close()
    return pop_articles


def get_popular_authors():
    ''' Get the most popular authors of all time '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select format('%s --- %s views', d.name, d.total) as total \
               from (select sum(t.views) as total, t.no as name \
               from (select title, articles.author, authors.id as aid, \
               name as no, count(author) as views from authors, articles, log \
               where authors.id = articles.author and \
               path = '/article/' || slug group by title, author,\
               authors.id, name) as t \
               group by t.no, aid \
               order by total desc) \
               as d group by d.total, d.name \
               order by d.total desc;")
    pop_authors = c.fetchall()
    db.close()
    return pop_authors


def get_errors():
    ''' On which days did more than 1% of requests lead to errors '''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("select b.stat, b.err, b.day, sum(b.ok) as ok_codes, sum(b.err) err_codes from (select a.day as day, a.t as t, a.stat as stat, sum(a.stat in ('200 OK')::int) as ok, sum(a.stat in ('404 NOT FOUND')::int) as err from (select extract(day from time) as day, time as t, status as stat from log group by time, status order by day) a group by a.day, a.t, a.stat) as b group by b.stat, b.err, b.day having sum(b.ok) != b.err order by b.day")
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























#"select d.day, count(d.stat) as num, d.stat from (select extract(day from time    ) as day, time, status as stat from log group by day, time, status order by day    ) as d where d.day = 1 or d.day > 1  group by d.day, d.stat order by d.day"

