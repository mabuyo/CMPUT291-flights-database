-- SEARCH FOR FLIGHTS using src, dest and departure date with available seats 
-- available_flights view returns: flight number, the fare type, the number of available seats and the seat price.
-- good_connections view returns: src, dst, dep_date, flightno1, flightno2, layover, and price
-- flight_results: flight number, source and destination airport codes, departure and arrival times, the number of stops, the layover time for non-direct flights, the price, and the number of seats at that price. 
-- sort based on price, highest to lowest
-- FROM ASGN2
SELECT flightno1, flightno2, layover, price 
  from (
  SELECT flightno1, flightno2, layover, price, row_number() over (order by price asc) rn 
  from 
  (SELECT flightno1, flightno2, layover, price
  from good_connections
  where to_char(dep_date,'DD/MM/YYYY')='22/12/2015' and src='YEG' and dst='LAX'
  union
  SELECT flightno flightno1, '' flightno2, 0 layover, price
  from available_flights
  where to_char(dep_date,'DD/MM/YYYY')='22/12/2015' and src='YEG' and dst='LAX'))
  where rn <=5; -- get rid of this top 5

-- FROM ASSGN2
  create view good_connections (src,dst,dep_date,flightno1,flightno2, layover,price) as
  select a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time-a1.arr_time,
	min(a1.price+a2.price)
  from available_flights a1, available_flights a2
  where a1.dst=a2.src and a1.arr_time +1.5/24 <=a2.dep_time and a1.arr_time +5/24 >=a2.dep_time
  group by a1.src, a2.dst, a1.dep_date, a1.flightno, a2.flightno, a2.dep_time, a1.arr_time;

  select src, dst, dep_date, flightno1, flightno2, layover/24, price
  from good_connections;


-- MAKE A BOOKING
-- The system should get the name of the passenger and check if the name is listed in the passenger table with the user email. 
-- TODO: replace p.name with user inputted name and replace p.email with user email
SELECT email
FROM passengers p
WHERE p.name = "Michelle Mabuyo" AND
	p.email = "mabuyo@ualberta.ca";

-- If not listed in the passenger table with the user email, the name and the country of the passenger should be added to the passenger table with the user email. 
-- TODO: email is user email, name is use rinput and country should be user input (?)
INSERT INTO passengers values ('email', 'name', 'country');

-- Your system should add rows to tables bookings and tickets to indicate that the booking is done (a unique ticket number should be generated by the system). 
-- TODO: code should insert values of all of these according to selected flight
INSERT INTO bookings values (tno, flightno, fare, dep_date, seat);
INSERT INTO tickets values(tno, email, paid_price)

-- list existing bookings of user
-- tables needed
	-- users(email, pass, last_login)
	-- passengers(email, name, country)
	-- tickets(tno, name, email, paid_price)
	-- bookings(tno, flightno, fare, dep_date, seat)
-- for each booking: the ticket number, the passenger name, the departure date and the price

SELECT t.tno, p.name, b.dep_date, t.paid_price
FROM users u, passengers p, tickets t, bookings b
WHERE u.email = p.email AND 
	p.email = t.email AND
	t.tno = b.tno AND
	u.email = 'test@gmail.com';
-- TODO: u.email will be replaced with the string for email of current user

-- see details for a booking
-- use ticket number for selection
SELECT tno, flightno, fare, dep_date, seat
FROM bookings
WHERE tno = '8';
-- TODO: tno will be compared with user selected input for ticket number


-- cancel a booking using ticket no
-- need to delete ticket as well, can we do this with an "on delete cascade"??? maybe not since they are populating tables using the original file.
-- TODO: replace tno with user selected input 
DELETE FROM bookings WHERE tno = '8';
DELETE FROM tickets WHERE tno = '8';



-- logout
-- set user last_login to sysdate
UPDATE users SET last_login = '' WHERE email = 'mabuyo@ualberta.ca'
-- TODO: email will be email of current user

-- check if user login is valid
SELECT email from users where email = 'mabuyo@ualberta.ca' AND pass = '1111';

-- record the departure time in act_dep_time if airline agent
UPDATE sch_flights SET act_dep_time = TO_DATE(update, 'DD-MON-YYYY, HH:MI') WHERE flightno = input AND dep_date = TO_DATE(date,'DD-MON-YYYY')
-- UPDATE sch_flights SET act_dep_time = TO_DATE('22-Sep-2015, 08:00', 'DD-MON-YYYY, HH:MI') WHERE flightno = 'AC154' AND dep_date = TO_DATE('22-Sep-2015','DD-MON-YYYY')
'AC154',to_date('22-Sep-2015','DD-Mon-YYYY'),to_date('15:50', 'hh24:mi'),to_date('21:30','hh24:mi')


