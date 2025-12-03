1.

 SELECT event_id,SUM(p.amount) FROM transaction t 
 INNER JOIN (SELECT event_id FROM movies m WHERE movie_name="<name>") DT ON DT.event_id=t.event_id
 INNER JOIN payment p ON p.payment_id=t.payment_id 
 GROUP BY event_id ORDER BY SUM(p.amount);
 
2.
    SELECT l.city, SUM(DT.amount) as Revenue,
	( SELECT payment_id,amount
      FROM payment 
      WHERE date_part('year',now())=date_part('year',last_updated) AND date_part('month',now())=date_part('month',last_updated) ) DT
	  INNER JOIN transaction t ON t.payment_id=p.payment_id
	  INNER JOIN location l ON l.location_id=t.location_id
	  INNER JOIN address a ON a.address_id=l.address_id
	  GROUP BY l.city
	  ORDER BY SUM(DT.amount);



3.
 
  SELECT * FROM 
  (SELECT bank,SUM(p.amount),rank() over(partition by p.bank order by sum(p.amount) desc) as rank
  FROM payment p ) DT WHERE rank=1;
  
  SELECT p.bank,SUM(p.amount)
  FROM payment p 
  GROUP BY p.bank
  ORDER BY SUM(p.amount) DESC LIMIT 3;
 
4.

 
  SELECT * FROM 
  (SELECT offer_id,COUNT(p.payment_id),rank() over(partition by p.offer_id order by COUNT(p.payment_id) desc) as rank FROM payment p ) DT WHERE rank=1;


  SELECT  * FROM offers o INNER JOIN 
 (SELECT offer_id,COUNT(payment_id) FROM payment GROUP BY offer_id ORDER BY COUNT(payment_id) DESC LIMIT 1) DT
  ON o.offer_id=DT.offer_id; 
  
5.
  SELECT m.movie_name, DT.ratings FROM Movie m INNER JOIN 
  ( SELECT event_id,AVG(star_feedback) as ratings
  FROM Feedback 
  WHERE Last_updated BETWEEN DATE_SUB(curdate(),7) AND curdate() 
  ORDER BY AVG(star_feedback) DESC LIMIT 5) DT 
  ON DT.event_id=m.event_id;

