--1

 select f.title,c.first_name,c.last_name,count(r.rental_id) 
 from rental r 
 inner join customer c
 on r.customer_id = c.customer_id
 inner join inventory i
 on i.inventory_id = r.inventory_id
 inner join film f
 on f.film_id = i.film_id
 group by c.first_name,f.title,c.last_name
 having count(r.rental_id)>1 order by count(r.rental_id) desc;

--2

select sum(p.amount),f.title 
from rental r 
inner join payment p
on p.rental_id = r.rental_id
inner join inventory i
on i.inventory_id = r.inventory_id
inner join film f
on f.film_id = i.film_id group by f.title
order by sum(p.amount) desc limit 10;

--3

select s.staff_id,sum(p.amount),min(s.first_name),min(s.last_name)
from payment p
inner join staff s
on s.staff_id = p.staff_id
group by s.staff_id
having sum(p.amount)>=31000;

--4

select r.customer_id,c.first_name || ' ' || c.last_name as name, extract( year from r.rental_date) as rental_year 
from rental r 
inner join customer c
on r.customer_id=c.customer_id
where
(r.return_date is null 
and 
extract(year from r.rental_date) <2006)
or
(extract(year from r.rental_date) <2006 
and
extract(year from r.return_date)>3000);

--5

select ct.city,count(ct.city_id) 
from rental r 
inner join customer c
on r.customer_id = c.customer_id
inner join address a
on a.address_id = c.address_id
inner join city ct
on ct.city_id = a.city_id
group by ct.city
order by count(ct.city_id) desc limit 1;

--6
--part a
--Sold out

select film_id,count(inventory_id),sum(difference)
from 
(select i.film_id,i.inventory_id,(count(i.inventory_id)-count(r.return_date)) as difference
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id
order by i.film_id,i.inventory_id) TD
group by film_id having count(inventory_id)-sum(difference) = 0;

--part b
--Out of stock
select i.film_id,f.title, i.inventory_id
from inventory i
full outer join film f
on f.film_id = i.film_id
where i.inventory_id is null;

--7

select TD.film_id,cnt,name_film,lang_name,first_name,last_name from
( 
select count(distinct r.rental_id) as cnt, i.film_id, 
max(f.title) as name_film,max(l.name) as lang_name 
from rental r 
inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
inner join language l
on f.language_id = l.language_id
group by i.film_id 
order by count(r.rental_id) desc limit 1) TD
inner join film_actor fa
on fa.film_id = TD.film_id
inner join actor a
on a.actor_id = fa.actor_id;

--8

select * from 
(select row_number() over (order by count(r.rental_id) desc) as alias, 
count(r.rental_id), i.film_id,max(f.title) 
from rental r 
inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
group by i.film_id 
order by count(r.rental_id) desc) dt 
where alias = 2;