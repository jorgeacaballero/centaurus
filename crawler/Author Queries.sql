select count(*) from data;
select count(*) from author;
select count(*) from author_data;

select author_id, count(data_id) as count_papers from author_data group by author_id order by count_papers desc;

select * from author where id = 6890;

select data_id from author_data where author_id = 6890;

select * from data where id in (select data_id from author_data where author_id = 2818)