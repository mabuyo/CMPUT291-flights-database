-- SEARCH FOR FLIGHTS using src, dest and departure date with available seats 
-- available_flights view returns: flight number, the fare type, the number of available seats and the seat price.
-- good_connections view returns: src, dst, dep_date, flightno1, flightno2, layover, and price
-- flight_results: flight number, source and destination airport codes, departure and arrival times, the number of stops, the layover time for non-direct flights, the price, and the number of seats at that price. 
-- sort based on price, highest to lowest



-- MAKE A BOOKING
-- The system should get the name of the passenger and check if the name is listed in the passenger table with the user email. If not, the name and the country of the passenger should be added to the passenger table with the user email. 
SELECT email
FROM passengers p
WHERE p.email = 







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
	u.email = 'mabuyo@ualberta.ca';
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










