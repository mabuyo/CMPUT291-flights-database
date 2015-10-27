
select src, dst, flightno1, flightno2, dep_time, arr_time,  layover, price 
from (select flightno1, flightno2, layover, price, row_number() over (order by price asc) rn 
      from (select src, dst, flightno1, flightno2, dep_time, arr_time, 1 numOfStops, layover, price
            from good_connections)
    union
    select src, dst, flightno flightno1, '' flightno2, dep_time, arr_time, 0 numOfStops, 0 layover, price
    from available_flights);


