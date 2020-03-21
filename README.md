# Project 1

Web Programming with Python and JavaScript

# introduction

This website provides 5000 books information for users to search, label or review. You can search book login-free. After log in, you can leave a review about certain books. If you don't want to review, you could just label the book as READ. Feel free to explore!

# Project Structure

## Main Page

In the main page, you can search books by title/author/ISBN when you input any info in the center input box, and click "SerBoo Search" button. Besides, if you don't have some idea about any book you want, just click "I am feeling lucky" button, and you will get a book randomly. Additionally, you mustn't log in for above actions. 

![Main page]() 

## Result Page

In the result page, you can get books with cover, title, author, publish year as a list. The boom items are arranged as five books a row. If you can't see the cover, don't worry, it just because that the book is too unpopular to have an user-uploaded cover picture in book.douban.com (Because those information is from Douban, a websitw related to film, books, music and activities in China). When you click "more" button, you will enter the book page.

![Result page]() 

## Book Page

### Book Information

In the book page, you can see all of information about a book. The first line is the title. The left column is the cover of the book, and the right column is the key information of the book, including author, publication year, ISBN-10, Douban page link, the number of reviews in Douban, the average rating in Douban, and the summary of the book. Exceptionally, if you see "Douban?rate?limit?exceeded..", don't be panic, just wait a minute (The Douban API we used is free, so it has a request limit).

![Book page]() 

### Your Review

After a dropdown divider, you can leave a review here. In the drop down form, 1~5 stars can be selected for your choice. And in the input box below, you can input whatever you want about the book. What? You don't want to show what you want? Just input rating or review or neither bothboth, all of those are not required. However, before leaving review, you must log in. If you don't have an account, click the green button in the navigation bar to register. Note that you cannot comment after registration.

![Review part]() 

### Users Review

The next part is the review list in the website. Always, there is nothing because few people know the website. The nickname will become "You", if you have had a review.

![Review list]() 

## API

This part is the interface to get book information by ISBN. The details are in the API page. 

![API page]() 

# Back End

The project is based on Flask. The HTML files are in the template directory

# Deploy on Heroku

The full process I following is narrated by YouTube channel [Pretty Printed](https://www.youtube.com/watch?v=FKy21FnjKS0). 

Specially, you should set an environment variable `DATABASE_URL` as your database link.
