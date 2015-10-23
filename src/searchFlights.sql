drop view available_flights;
create view available_flights(flightno,dep_date, src,dst,dep_time,arr_time,fare,seats,
  price) as 
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



drop view good_connections;
create view good_connections (src,dst,dep_date,flightno1,flightno2, dep_time, arr_time, layover,price, seats) as
select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a1.dep_time, a2.arr_time, a2.dep_time-a1.arr_time,
  min(a1.price+a2.price), CASE WHEN a1.seats < a2.seats THEN a1.seats ELSE a2.seats END
from available_flights a1, available_flights a2
where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno,a2.arr_time,  a2.dep_time, a1.arr_time, a1.dep_time, a1.seats, a2.seats;



select src, dst, flightno1, flightno2, dep_time, arr_time,  layover, price 
from (
select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn 
from 
(select src, dst, flightno1, flightno2, dep_time, arr_time, 1 numOfStops, layover, price
from good_connections
union
select src, dst, flightno flightno1, '' flightno2, dep_time, arr_time, 0 numOfStops, 0 layover, price
from available_flights



