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
    c.execute("select format('%s --- %s errors', d.date, d.percent) \
               from (select TO_CHAR(time :: DATE, 'Mon dd, yyyy') as date \
               , c.day, to_char(c.percentages, '9.99%') as percent \
               from (select b.day as day, ((b.errors * 100)::float) \
               / (b.ok + b.errors) as percentages \
               from (select a.day as day, (sum(a.status in ('200 OK')::int)) \
               as ok, (sum(a.status in ('404 NOT FOUND')::int)) as errors \
               from (select extract(day from time) as day, time as time, status \
               as status from log) a group by day) as b \
               group by b.day, b.errors, b.ok) c,log \
               where c.day = extract(day from time) and c.percentages >= 1 \
               limit 1) as d")
    errs = c.fetchall()
    db.close()
    return errs

print("\nThe most popular articles of all time are:\n")
print(get_popular_articles())
print("\nThe most popular authors of all time are:\n")
print(get_popular_authors())
print("\nThe day on which more than 1% of request"
      " lead to errors was:\n")
print(get_errors())







"select format('%s --- %s errors', d.date, d.percent) \
 48                from (select TO_CHAR(time :: DATE, 'Mon dd, yyyy') as date \
 49                , c.day, to_char(c.percentages, '9.99%') as percent \
 50                from (select b.day as day, ((b.errors * 100)::float) \
 51                / (b.ok + b.errors) as percentages \
 52                from (select a.day as day, (sum(a.status in ('200 OK')::int)) \
 53                as ok, (sum(a.status in ('404 NOT FOUND')::int)) as errors \
 54                from (select extract(day from time) as day, time as time, status \
 55                as status from log) a group by day) as b \
 56                group by b.day, b.errors, b.ok) c,log \
 57                where c.day = extract(day from time) and c.percentages >= 1 \
 58                limit 1) as d"
