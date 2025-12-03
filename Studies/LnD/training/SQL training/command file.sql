CREATE TABLE bhatt.freshers_bhatt( id          integer,  name    text,    age    integer);

  INSERT INTO bhatt.freshers_bhatt VALUES (1,'Anurag',13);
  INSERT INTO bhatt.freshers_bhatt VALUES (2,'Rakshita',7);
  INSERT INTO bhatt.freshers_bhatt VALUES (3,'Naveen',47);
  INSERT INTO bhatt.freshers_bhatt VALUES (4,'Pragya',69);
  INSERT INTO bhatt.freshers_bhatt VALUES (5,'Aastha',87);
  INSERT INTO bhatt.freshers_bhatt VALUES (6,'Rohit',17);
  INSERT INTO bhatt.freshers_bhatt VALUES (7,'Aakanksha',24);
  INSERT INTO bhatt.freshers_bhatt VALUES (8,'Smita',73);
  INSERT INTO bhatt.freshers_bhatt VALUES (9,'Aditi',97);
  INSERT INTO bhatt.freshers_bhatt VALUES (10,'Arijit',57);
  INSERT INTO bhatt.freshers_bhatt VALUES (11,'Arijit',57);
  INSERT INTO bhatt.freshers_bhatt VALUES (12,'Aditi',57);
  INSERT INTO bhatt.freshers_bhatt VALUES (13,'Aditi',57);
  
  
 
ALTER TABLE bhatt.freshers_bhatt ADD COLUMN Mobile integer;

SELECT * FROM bhatt.freshers_bhatt;

select a.first_name,a.last_name, f.title from
film_actor fa
inner join actor a
on fa.actor_id = a.actor_id
inner join film f
on fa.film_id = f.film_id
limit 20;

CREATE TABLE bhatt.scorecard( id          integer,  name    text, subject text, marks integer);

  INSERT INTO bhatt.scorecard VALUES (1,'Anurag','SQL',23);
  INSERT INTO bhatt.scorecard VALUES (2,'Rakshita','SQL',32);
  INSERT INTO bhatt.scorecard VALUES (3,'Naveen','SQL',23);
  INSERT INTO bhatt.scorecard VALUES (4,'Pragya','SQL',69);
  INSERT INTO bhatt.scorecard VALUES (5,'Aastha','SQL',87);
  INSERT INTO bhatt.scorecard VALUES (6,'Rohit','SQL',17);
  INSERT INTO bhatt.scorecard VALUES (7,'Aakanksha','SQL',24);
  INSERT INTO bhatt.scorecard VALUES (8,'Smita','SQL',73);
  INSERT INTO bhatt.scorecard VALUES (9,'Anurag','SAS',23);
  INSERT INTO bhatt.scorecard VALUES (10,'Rakshita','SAS',32);
  INSERT INTO bhatt.scorecard VALUES (11,'Naveen','SAS',23);
  INSERT INTO bhatt.scorecard VALUES (12,'Pragya','SAS',69);
  INSERT INTO bhatt.scorecard VALUES (13,'Aastha','SAS',87);
  INSERT INTO bhatt.scorecard VALUES (14,'Rohit','SAS',17);
  INSERT INTO bhatt.scorecard VALUES (15,'Aakanksha','SAS',24);
  INSERT INTO bhatt.scorecard VALUES (16,'Smita','SAS',73);
  
  INSERT INTO bhatt.scorecard2 VALUES (1,'Anurag','SQL',23);
  INSERT INTO bhatt.scorecard2 VALUES (2,'Rakshita','SQL',32);
  INSERT INTO bhatt.scorecard2 VALUES (3,'Naveen','SQL',23);
  INSERT INTO bhatt.scorecard2 VALUES (4,'Pragya','SQL',69);
  INSERT INTO bhatt.scorecard2 VALUES (5,'Aastha','SQL',87);
  INSERT INTO bhatt.scorecard2 VALUES (6,'Rohit','SQL',17);
  INSERT INTO bhatt.scorecard2 VALUES (7,'Aakanksha','SQL',24);
  INSERT INTO bhatt.scorecard2 VALUES (8,'Smita','SQL',73);
  
   select count(id),name from bhatt.freshers_bhatt group by name having count(name)>=2;
   select * from bhatt.scorecard2 where marks between 10 and 23 and name not like '%a';
   delete from bhatt.freshers_bhatt  where id =12;
   select * from bhatt.freshers_bhatt where name not in (select name from bhatt.freshers_bhatt group by name having count(name)>1);
   
   create table bhatt.forjoinA(id integer, name text);
   INSERT INTO bhatt.forjoinA VALUES (1,'Anurag');
   INSERT INTO bhatt.forjoinA VALUES (2,'Naveen');
   INSERT INTO bhatt.forjoinA VALUES (3,'Rakshita');
   INSERT INTO bhatt.forjoinA VALUES (4,'Smita');
   INSERT INTO bhatt.forjoinA VALUES (5,'Arijit');
   INSERT INTO bhatt.forjoinA VALUES (6,'Pragya');
   INSERT INTO bhatt.forjoinA VALUES (7,'Aakanksha');

   create table bhatt.forjoinB(id integer, amount integer);
   INSERT INTO bhatt.forjoinB VALUES (2,23);
   INSERT INTO bhatt.forjoinB VALUES (3,300);
   INSERT INTO bhatt.forjoinB VALUES (4,211);
   INSERT INTO bhatt.forjoinB VALUES (5,3434);
   INSERT INTO bhatt.forjoinB VALUES (7,776);
   
   select * from bhatt.forjoinA as A inner join bhatt.forjoinB as B on A.id=B.id;
   
   create table bhatt.forcase(id integer, name text, gender text);
   INSERT INTO bhatt.forcase VALUES (1,'Emma','Female');
   INSERT INTO bhatt.forcase VALUES (2,'kajol','F');
   INSERT INTO bhatt.forcase VALUES (3,'chani','f');
   INSERT INTO bhatt.forcase VALUES (4,'Brad','Male');
   INSERT INTO bhatt.forcase VALUES (5,'Spacey','M');
   INSERT INTO bhatt.forcase VALUES (5,'Bobby','O');
   
   select id,name, case when gender in ('Male','M','m') then 'M' when gender in ('Female','F','f') then 'F' else 'Shit'  end as gnew from bhatt.forcase;
    select *, dense_rank() over(partition by subject order by marks desc) as hello from bhatt.scorecard;