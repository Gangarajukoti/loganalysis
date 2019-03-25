#!/usr/bin/env python3
import psycopg2

DBNAME = "news"


def get_data(query1):
    # fetch data from database
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query1)
    data = c.fetchall()
    db.close()
    return data


def popular_articles():
    # The most popular three articles is?
    query1 = """
    select title, count(*) as num
    from articles, log
    where log.path like '%' || articles.slug
    group by title
    order by num desc
    """
    result = get_data(query1)[:3]
    print('The most popular three articles is::')
    printdata(result)


def popular_authors():
    # 2.Who are the most popular article authors
    query1 = """
    select name, count(*) as num
    from authors, articles, log
    where authors.id = articles.author and log.path like '%' || articles.slug
    group by name
    order by num desc
    """
    result = get_data(query1)
    print('The most popular article authors:')
    printdata(result)


def error_days():
    # 3. On which days did more than 1% of requests lead to errors?
    per = "1"
    query1 = """ with result as (select date(time) as day,
                 round(100.0 * sum(case log.status when '404 NOT FOUND'
                 then 1 else 0 end)/count(log.status),3)
                 as error from log group by date(time) order by error desc)
                 select day,error from result where error >1;"""

    result = get_data(query1)
    print('Days with error rate more than ' + per + '%:')
    for record in result:
        print('{} - {}% errors'.format(record[0], record[1]))


def printdata(result):
    for i in result:
        print('{} - {}views'.format(i[0], i[1]))
        print('')
if __name__ == '__main__':
    popular_articles()
    popular_authors()
    error_days()
