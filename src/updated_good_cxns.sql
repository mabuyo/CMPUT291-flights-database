drop view good_connections;
create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price, dep_time, arr_time, seats) as
SELECT DISTINCT ff.src, ff.dst, ff.dep_date, ff.no1, ff.no2, ff.layover, ff.price, ff.dep_time, ff.arr_time , least(a3.seats, a4.seats) 
FROM
(select a1.src, a2.dst, a1.dep_date, a1.flightno AS no1, a2.flightno AS no2, a2.dep_time-a1.arr_time as layover,
  min(a1.price+a2.price) AS price, a1.dep_time, a2.arr_time, a2.dep_date as date2 
from available_flights a1, available_flights a2
where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time, a1.dep_time, a2.arr_time, a2.dep_date
) ff,  
available_flights a3, available_flights a4
WHERE a3.dep_date = ff.dep_date and a3.flightno = ff.no1 AND a4.flightno = ff.no2 AND a4.dep_date = ff.date2 AND a3.dep_time = ff.dep_time AND a4.arr_time = ff.arr_time;
