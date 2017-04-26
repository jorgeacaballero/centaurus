insert into data (title,authors,abstract,url, year, month) 
values ('Title', 'Author','Abstract', 'https://arxiv.org/abs/1009.0004', 10,10) 
on conflict (url) do nothing 