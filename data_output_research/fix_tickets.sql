select t.tno, p.name, t.email, t.paid_price
FROM passengers p, tickets t
where p.email = t.email;
