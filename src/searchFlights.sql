drop view available_flights;
create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats, price) as 
select f.flightno, sf.dep_date, f.src, f.dst, f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time)), 
   f.dep_time+(trunc(sf.dep_date)-trunc(f.dep_time))+(f.est_dur/60+a2.tzone-a1.tzone)/24, 
       fa.fare, fa.limit-count(tno), fa.price
from flights f, flight_fares fa, sch_flights sf, bookings b, airports a1, airports a2
where f.flightno=sf.flightno and f.flightno=fa.flightno and f.src=a1.acode and
  f.dst=a2.acode and fa.flightno=b.flightno(+) and fa.fare=b.fare(+) and
  sf.dep_date=b.dep_date(+)
group by f.flightno, sf.dep_date, f.src, f.dst, f.dep_time, f.est_dur,a2.tzone,
  a1.tzone, fa.fare, fa.limit, fa.price
having fa.limit-count(tno) > 0;


select * from available_flights;


drop view good_connections;
create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price, dep_time, arr_time, seats) as
SELECT DISTINCT ff.src, ff.dst, ff.dep_date, ff.no1, ff.no2, ff.layover, ff.price, ff.dep_time, ff.arr_time , CASE WHEN a3.seats <= a4.seats then a3.seats else a4.seats end 
FROM
(select a1.src, a2.dst, a1.dep_date, a1.flightno AS no1, a2.flightno AS no2, a2.dep_time-a1.arr_time as layover,
  min(a1.price+a2.price) AS price, a1.dep_time, a2.arr_time, a2.dep_date as date2 
from available_flights a1, available_flights a2
where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time, a1.dep_time, a2.arr_time, a2.dep_date
) ff,  
available_flights a3, available_flights a4
WHERE a3.dep_date = ff.dep_date and a3.flightno = ff.no1 AND a4.flightno = ff.no2 AND a4.dep_date = ff.date2 AND a3.dep_time = ff.dep_time AND a4.arr_time = ff.arr_time;

spool new_gc2.txt
select * from good_connections;
spool off;

select flightno1, flightno2, layover, price 
from (
select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn 
from 
(select flightno1, flightno2, layover, price
from good_connections
where to_char(dep_date,'DD/MM/YYYY')='22/12/2015' and src='YEG' and dst='LAX'
union
select flightno flightno1, '' flightno2, 0 layover, price
from available_flights
where to_char(dep_date,'DD/MM/YYYY')='22/12/2015' and src='YEG' and dst='LAX'));
