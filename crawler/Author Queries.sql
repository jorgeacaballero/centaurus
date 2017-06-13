select count(*) from data;
select count(*) from author;
select count(*) from author_data;

select top(3) author_id, count(data_id) as count_papers from author_data group by author_id order by count_papers desc;

select * from author where id = 4377;

select data_id from author_data where author_id = 4377;

select * from data where id in (select data_id from author_data where author_id = 4377)

select top(3) * from data where year = 16 and month = 12 order by id desc;

select * from data where abstract like '%Honduras%';