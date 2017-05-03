create table data (
	id int not null identity(1,1) primary key,
	title text,
	abstract text,
	url varchar(255) not null unique,
	year int,
	month int
);

create table author (
	id int not null identity(1,1) primary key,
	name varchar(255)
);

create table author_data (
	data_id int,
	author_id int,
	constraint movie_cat_pk primary key (data_id, author_id),
	constraint fk_data
		foreign key (data_id) references data (id),
	constraint fk_author
		foreign key (author_id) references author (id)
);