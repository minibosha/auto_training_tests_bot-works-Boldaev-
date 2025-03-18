-- 1 Задание
SELECT TrackId, Composer from Track

where TrackId = 51;


-- 2 Задание
SELECT * from Track

ORDER BY Name

Limit 52-48 OFfset 48;


-- 3 Задание
SELECT * from Track

where Name like '%Hit%';


-- 4 Задание
SELECT * from Track

where Milliseconds BETWEEN 1000*350 and 1000*360;


-- 5 Задание
SELECT * from Track
where Composer is NULL;


-- 6 Задание
SELECT * from Track

where AlbumId = 108;


-- 7 Задание
SELECT SUM(Milliseconds) AS total_duration FROM Track
WHERE TrackId = 77;


-- 8 Задание
SELECT * from Track

ORDER BY UnitPrice DESc, UnitPrice

limit 1;


-- 9 Задание
SELECT Sum(UnitPrice) FROM Track;


-- 10 Задание
SELECT SUM(Track.Milliseconds) / 1000 AS total_duration_seconds
FROM Track
JOIN Album ON Track.AlbumId = Album.AlbumId
WHERE Album.Title = 'Greatest Hits I';


-- 11 Задание
SELECT Customer.CustomerId, Customer.FirstName, Customer.LastName, MAX(Invoice.Total) AS max_total
FROM Invoice
JOIN Customer ON Invoice.CustomerId = Customer.CustomerId
GROUP BY Customer.CustomerId
ORDER BY max_total DESC
LIMIT 1;


-- 12 Задание
SELECT Genre.Name AS GenreName, COUNT(Track.TrackId) AS TrackCount
FROM Track
JOIN Genre ON Track.GenreId = Genre.GenreId
GROUP BY Genre.Name
ORDER BY TrackCount DESC;


-- 13 Задание
SELECT Track.TrackId, Track.Name AS TrackName, Customer.FirstName, Customer.LastName FROM Customer
JOIN Invoice ON Customer.CustomerId = Invoice.CustomerId
JOIN InvoiceLine ON Invoice.InvoiceId = InvoiceLine.InvoiceId
JOIN Track ON InvoiceLine.TrackId = Track.TrackId
WHERE Customer.FirstName = 'Dan' AND Customer.LastName = 'Miller';