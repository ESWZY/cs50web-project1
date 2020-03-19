create table users( 
	id SERIAL PRIMARY KEY, 
	username varchar not null, 
	password varchar not null, 
	name varchar
);

create table books( 
	id SERIAL PRIMARY KEY, 
	isbn varchar,
	title varchar,
	author varchar,
	year varchar 
);

create table reviews( 
	id SERIAL PRIMARY KEY, 
	book_id INTEGER not null ,
	user_id INTEGER not null,
	comment VARCHAR,
	rating INTEGER,
	time date
);


--INSERT INTO users (usearname, password, name) VALUES ('admin', ' pbkdf2:sha256:150000$uZdY9dcA$f7ac40c2a852d55860d8c2aab4be576767d764eb16b8d1e1710923a05ced57e1', 'admin');

SELECT * FROM books WHERE LOWER(title) LIKE '%year%';


--INSERT INTO reviews (book_id, user_id, comment, rating, time) VALUES (3891, 1, 'I really like Shakespeare', 5, '2020-03-17');

SELECT name, comment, rating, time FROM reviews JOIN users ON reviews.user_id=users.id ;

SELECT title, author, year, isbn, COUNT(reviews.id) as review_count, AVG(reviews.rating) as average_score FROM books left JOIN reviews ON books.id = reviews.book_id WHERE isbn = '0375508325' GROUP BY title, author, year, isbn;