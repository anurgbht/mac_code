''1''
select count(rental_id),customer_id from rental group by customer_id having count(rental_id) > 40;
 
select count(rental_id),customer_id from rental group by 
customer_id order by count(rental_id) desc limit 10;

select r.rental_id, i.film_id,c.first_name,c.last_name from
rental r inner join customer c
on r.customer_id = c.customer_id
inner join inventory i
on i.inventory_id = r.inventory_id
limit 10;

select r.rental_id, i.film_id,f.title,c.first_name,c.last_name from
rental r inner join customer c
on r.customer_id = c.customer_id
inner join inventory i
on i.inventory_id = r.inventory_id
inner join film f
on f.film_id = i.film_id
limit 10;

select f.title,c.first_name,c.last_name,count(r.rental_id) from
rental r inner join customer c
on r.customer_id = c.customer_id
inner join inventory i
on i.inventory_id = r.inventory_id
inner join film f
on f.film_id = i.film_id
group by c.first_name,f.title,c.last_name
order by count(r.rental_id) desc limit 10;

 select f.title,c.first_name,c.last_name,count(r.rental_id) 
 from rental r 
 inner join customer c
 on r.customer_id = c.customer_id
 inner join inventory i
 on i.inventory_id = r.inventory_id
 inner join film f
 on f.film_id = i.film_id
 group by c.first_name,f.title,c.last_name
 having count(r.rental_id)>1;

''2''

select sum(p.amount),f.title from
rental r inner join payment p
on p.rental_id = r.rental_id
inner join inventory i
on i.inventory_id = r.inventory_id
inner join film f
on f.film_id = i.film_id group by f.title
limit 10;

 select sum(p.amount),f.title from
rental r inner join payment p
on p.rental_id = r.rental_id
inner join inventory i
on i.inventory_id = r.inventory_id
inner join film f
on f.film_id = i.film_id group by f.title
order by sum(p.amount) desc limit 10;

''3''

select r.staff_id,sum(p.amount),min(s.first_name),min(s.last_name) from
payment p inner join rental r
on r.rental_id = p.rental_id
inner join staff s
on s.staff_id = r.staff_id
group by r.staff_id
having sum(p.amount)>=31000;

''4''

select * from rental where
 extract(year from rental_date) <2007 and
extract(year from return_date)>3000;

select customer_id from rental
where return_date is null or
(extract(year from rental_date) <2007 and extract(year from return_date)>3000) limit 10;

select r.customer_id,c.first_name || ' ' || c.last_name as name 
from rental r 
inner join customer c
on r.customer_id=c.customer_id
where return_date is null 
or
(extract(year from rental_date) <2007 
and
extract(year from return_date)>3000) limit 10;

''5''

select ct.city,count(ct.city_id) from
rental r inner join
customer c
on r.customer_id = c.customer_id
inner join address a
on a.address_id = c.address_id
inner join city ct
on ct.city_id = a.city_id
group by ct.city
order by count(ct.city_id) desc limit 1;

''6''

select i.film_id,r.rental_date,r.return_date
from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
where r.return_date is null
order by i.film_id limit 10;

 select i.film_id,f.title
from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
where r.return_date is null
left join film f
on f.film_id = i.film_id
;

select i.film_id,f.title
from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
left join film f
on f.film_id = i.film_id
where r.return_date is null
;

select film_id from film where film_id not in
(select i.film_id
from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
where r.return_date is null) limit 10;

select i.film_id,case when r.return_date is null then 'not returned'else 'returned' end as ret_status from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
limit 10;

 select avg(i.film_id),f.title,count(r.return_date is null) from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
full outer join film f
on f.film_id = i.film_id
group by f.title order by f.title limit 10;

''------------------------second approach----------------''

select i.film_id,f.title, i.inventory_id 
from inventory i
full outer join film f
on f.film_id = i.film_id
where i.inventory_id is null
order by title
limit 10;

 select i.film_id,f.title, i.inventory_id
from inventory i
full outer join film f
on f.film_id = i.film_id
order by title
limit 50;

''movies out of stock''
select i.film_id,f.title, i.inventory_id
from inventory i
full outer join film f
on f.film_id = i.film_id
where i.inventory_id is null;

''movies sold out''

select i.film_id,f.title, i.inventory_id,r.return_date
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
order by f.film_id
limit 10;

 select i.film_id,f.title, i.inventory_id,r.return_date
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
order by f.film_id,i.inventory_id,r.return_date;


 select i.film_id,count( i.inventory_id),count(r.return_date is null)
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id;

select i.film_id,count( i.inventory_id),count(r.return_date)
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id order by i.film_id,i.inventory_id;


 select i.film_id,f.title
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id 
having (count( i.inventory_id)-count(r.return_date))>0 
order by i.film_id,i.inventory_id;


 select i.film_id,max(f.title)
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id
having (count( i.inventory_id)-count(r.return_date))>0
order by i.film_id,i.inventory_id;

select i.film_id,max(f.title)
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id
having count(r.return_date)=0
order by i.film_id,i.inventory_id;


select film_id,count(inventory_id),sum(difference) from 
(select i.film_id,i.inventory_id,(count(i.inventory_id)-count(r.return_date)) as difference
from inventory i
inner join film f
on f.film_id = i.film_id
inner join rental r
on r.inventory_id = i.inventory_id
group by i.film_id,i.inventory_id
order by i.film_id,i.inventory_id) TD
group by film_id having count(inventory_id)-sum(difference) = 0;

''7''

 select count(r.rental_id), i.film_id from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
group by i.film_id order by count(r.rental_id) desc limit 10;

select count(r.rental_id), i.film_id,max(f.title) from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.filmm_id = i.film_id
group by i.film_id order by count(r.rental_id) desc limit 10;

select count(r.rental_id), i.film_id,max(f.title) from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
group by i.film_id order by count(r.rental_id) desc limit 1;

select TD.film_id,cnt,name_film,lang_name,first_name,last_name from
( 
select count(distinct r.rental_id) as cnt, i.film_id,max(f.title) as name_film,max(l.name) as lang_name from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
inner join language l
on f.language_id = l.language_id
group by i.film_id order by count(r.rental_id) desc limit 1) TD
inner join film_actor fa
on fa.film_id = TD.film_id
inner join actor a
on a.actor_id = fa.actor_id;



select r.rental_id, i.film_id,f.title,l.name,a.first_name from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
inner join language l
on f.language_id = l.language_id
inner join film_actor fa
on fa.film_id = f.film_id
inner join actor a
on a.actor_id = fa.actor_id limit 10;

select TD.film_id,cnt,name_film,lang_name,first_name,last_name from
( 
select count(distinct r.rental_id) as cnt, i.film_id,max(f.title) as name_film,max(l.name) as lang_name from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
inner join language l
on f.language_id = l.language_id
group by i.film_id order by count(r.rental_id) desc limit 1) TD
inner join film_actor fa
on fa.film_id = TD.film_id
inner join actor a
on a.actor_id = fa.actor_id;



''8''

select row_number() over (order by count(r.rental_id) desc), count(r.rental_id), i.film_id,max(f.title) from
rental r inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
group by i.film_id order by count(r.rental_id) desc limit 2;

select * from 
(select row_number() over (order by count(r.rental_id) desc) as alias, count(r.rental_id), i.film_id,max(f.title) 
from rental r 
inner join inventory i
on r.inventory_id = i.inventory_id
inner join film f
on f.film_id = i.film_id
group by i.film_id order by count(r.rental_id) desc) dt where alias = 2;
