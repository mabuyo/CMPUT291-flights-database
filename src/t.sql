SELECT * FROM temp WHERE flightno1='' AND flightno2={1} AND dep_time={2} AND price = min(SELECT price FROM temp WHERE flightno1={0} AND flightno2={1} AND dep_time={2})
