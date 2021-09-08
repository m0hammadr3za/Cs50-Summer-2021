SELECT description FROM crime_scene_reports
WHERE year = 2020
AND month = 7
AND day = 28
AND street = "Chamberlin Street";
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse.
-- Interviews were conducted today with three witnesses who were present at the time —
-- each of their interview transcripts mentions the courthouse.



SELECT name, transcript FROM interviews
WHERE year = 2020
AND month = 7
AND day = 28
AND transcript LIKE "%courthouse%";
-- Ruth | Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and
-- drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that
-- left the parking lot in that time frame.
-- Eugene | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived
-- at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- Raymond | As the thief was leaving the courthouse, they called someone who talked to them for less than a minute.
-- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.



SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25;
-- Ruth clue returns a bunch of license plates



SELECT person_id FROM bank_accounts
WHERE account_number IN (
SELECT account_number FROM atm_transactions
WHERE atm_location LIKE "%Fifer%"
AND year = 2020
AND month = 7
AND day = 28
AND transaction_type = "withdraw");
-- Eugene clue returns a few banck accounts which we can find the owners of those accounts



SELECT caller FROM phone_calls
WHERE year = 2020
AND month = 7
AND day = 28
AND duration < 60;

SELECT passport_number FROM passengers
WHERE flight_id IN (
SELECT id FROM flights
WHERE year = 2020
AND month = 7
AND day = 29
AND origin_airport_id = (
SELECT id FROM airports
WHERE city LIKE "%Fiftyville%")
ORDER BY hour, minute
LIMIT 1);
-- Raymond clue also returns some phone and passport numbers



-- Finding the thief
SELECT name FROM people
WHERE license_plate IN (
SELECT license_plate FROM courthouse_security_logs
WHERE year = 2020
AND month = 7
AND day = 28
AND hour = 10
AND minute BETWEEN 15 AND 25)
AND id IN (
SELECT person_id FROM bank_accounts
WHERE account_number IN (
SELECT account_number FROM atm_transactions
WHERE atm_location LIKE "%Fifer%"
AND year = 2020
AND month = 7
AND day = 28
AND transaction_type = "withdraw"))
AND phone_number IN (
SELECT caller FROM phone_calls
WHERE year = 2020
AND month = 7
AND day = 28
AND duration < 60)
AND passport_number IN (
SELECT passport_number FROM passengers
WHERE flight_id IN (
SELECT id FROM flights
WHERE year = 2020
AND month = 7
AND day = 29
AND origin_airport_id = (
SELECT id FROM airports
WHERE city LIKE "%Fiftyville%")
ORDER BY hour, minute
LIMIT 1));



-- Figuring out where he escaped to
SELECT city FROM airports
WHERE id = (
SELECT destination_airport_id FROM flights
WHERE year = 2020
AND month = 7
AND day = 29
AND origin_airport_id = (
SELECT id FROM airports
WHERE city LIKE "%Fiftyville%")
ORDER BY hour, minute
LIMIT 1);



-- Finding the accomplice
SELECT name FROM people
WHERE phone_number = (
SELECT receiver FROM phone_calls
WHERE year = 2020
AND month = 7
AND day = 28
AND duration < 60
AND caller = (
SELECT phone_number FROM people
WHERE name LIKE "%Ernest%"));