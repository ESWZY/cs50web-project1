# Project 1

Web Programming with Python and JavaScript

# introduction

[This website](http://serboo-eswzy.herokuapp.com/) provides 5000 books information for users to search, label or review. You can search book login-free. After log in, you can leave a review about certain books. If you don't want to review, you could just label the book as READ. Feel free to explore!

# Project Structure

## Main Page

In the [main page](http://serboo-eswzy.herokuapp.com/), you can search books by title/author/ISBN when you input any info in the center input box, and click "SerBoo Search" button. Besides, if you don't have some idea about any book you want, just click "I am feeling lucky" button, and you will get a book randomly. Additionally, you mustn't log in for above actions. 

![Main page](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/main-page.png) 

## Result Page

In the [result page](http://serboo-eswzy.herokuapp.com/search?book=the), you can get books with cover, title, author, publish year as a list. The boom items are arranged as five books a row. If you can't see the cover, don't worry, it just because that the book is too unpopular to have an user-uploaded cover picture in book.douban.com (Because the information is from Douban, a website related to film, books, music and activities in China). When you click "more" button, you will enter the book page.

![Result page](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/result-page.png) 

If there is on book meets the request, an error page will be returned.

![No result page](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/no-result-page.png)

## Book Page

### Book Information

In the [book page](http://serboo-eswzy.herokuapp.com/search?lucky=True), you can see all of information about a book. The first line is the title. The left column is the cover of the book, and the right column is the key information of the book, including author, publication year, ISBN-10, Douban page link, the number of reviews in Douban, the average rating in Douban, and the summary of the book. Exceptionally, if you see "Douban_rate_limit_exceeded..", don't be panic, just wait a minute (The Douban API we used is free, so it has a request limit).

![Book page](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/book-page.png) 

### Your Review

After a drop-down divider, you can leave a review here. In the drop down form, 1~5 stars can be selected for your choice. And in the input box below, you can input whatever you want about the book. What? You don't want to show what you want? Just input rating or review or neither both, all of those are not required. However, before leaving review, you must log in. If you don't have an account, click the green button in the navigation bar to register. Note that you cannot comment after registration.

![Review part](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/review-part.png) 

### Users Review

The next part is the review list in the website. Always, there is nothing because few people know the website. The nickname will become "You", if you have had a review.

![Review list](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/review-list.png) 

## API

This part is the interface to get book information by ISBN. The details are in the [API page](https://serboo-eswzy.herokuapp.com/api). 

![API page](https://github.com/ESWZY/cs50web-project1/blob/master/screenshot/API-page.png) 

# Back End

The project is based on Flask. HTML files are in the template directory, CSS files are in the static directory.

Database tables and their structure as following:

```
               List of relations
 Schema |      Name      |   Type   |  Owner
--------+----------------+----------+----------
 public | books          | table    | postgres
 public | books_id_seq   | sequence | postgres
 public | reviews        | table    | postgres
 public | reviews_id_seq | sequence | postgres
 public | users          | table    | postgres
 public | users_id_seq   | sequence | postgres
```

```books```:
```
                                 Table "public.books"
 Column |       Type        | Collation | Nullable |              Default
--------+-------------------+-----------+----------+-----------------------------------
 id     | integer           |           | not null | nextval('books_id_seq'::regclass)
 isbn   | character varying |           |          |
 title  | character varying |           |          |
 author | character varying |           |          |
 year   | character varying |           |          |
Indexes:
    "books_pkey" PRIMARY KEY, btree (id)
```

```users```:

```
                                 Table "public.books"
 Column |       Type        | Collation | Nullable |              Default
--------+-------------------+-----------+----------+-----------------------------------
 id     | integer           |           | not null | nextval('books_id_seq'::regclass)
 isbn   | character varying |           |          |
 title  | character varying |           |          |
 author | character varying |           |          |
 year   | character varying |           |          |
Indexes:
    "books_pkey" PRIMARY KEY, btree (id)
```

```reviews```:

```
                                  Table "public.reviews"
 Column  |       Type        | Collation | Nullable |               Default
---------+-------------------+-----------+----------+-------------------------------------
 id      | integer           |           | not null | nextval('reviews_id_seq'::regclass)
 book_id | integer           |           | not null |
 user_id | integer           |           | not null |
 comment | character varying |           |          |
 rating  | integer           |           |          |
 time    | date              |           |          |
Indexes:
    "reviews_pkey" PRIMARY KEY, btree (id)
```

# Deploy 

## On Heroku

The full process I following is narrated by a [video](https://www.youtube.com/watch?v=FKy21FnjKS0) in YouTube channel Pretty Printed. 

Specially, you should set an environment variable `DATABASE_URL` as your database link. And use ```heroku run import.py``` to import books information.

## Locally

First:

```pip -r requirements.txt```

And then, run create table commands in ```table.sql``` for your database. Run ```python import.py``` to import books information.

Finally, run:

```flask run```

# Others

The directory "lecture2" ~ "lecture4" in the repo are for course studying. If you want to deploy the project, you can delete them directly.

In the search page, you can provide two parameter ```begin``` and ```end``` in the get method to designate the search position. The default: ```/search?begin=0&end=20&book=```

Application error maybe occur when returned search result is too many.
