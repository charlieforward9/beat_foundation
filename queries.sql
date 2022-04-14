--Put queries here
--Q1
SELECT ROUND(AVG(CRICHARDSON5.beat_heartrate.HRVALUE)) AS AVG_HR, MIN(CRICHARDSON5.beat_heartrate.HRVALUE) as MIN_HR, MAX(CRICHARDSON5.beat_heartrate.HRVALUE) AS MAX_HR
FROM CRICHARDSON5.beat_event JOIN CRICHARDSON5.beat_heartrate
ON (
    crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
    crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
    )
WHERE crichardson5.beat_event.USERID = '0.8302870117189518' AND
      crichardson5.beat_event.TSTART BETWEEN  '2021-06-1 00:00:00' AND '2021-06-5 23:59:59' AND
        crichardson5.beat_event.CAT = 'work';


--Q2



--Q3
SELECT TO_TIMESTAMP(TSTART, 'YYYY-MM-DD HH24:MI:SS') AS time, MAX(HRVALUE), TO_TIMESTAMP(MAX(TEND), 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(MIN(TSTART), 'YYYY-MM-DD HH24:MI:SS') AS Duration
FROM crichardson5.beat_heartrate , crichardson5.beat_event
WHERE crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
    crichardson5.beat_event.USERID = crichardson5.beat_event.USERID AND 
    crichardson5.beat_event.CAT = 'rest' AND
    crichardson5.beat_event.TSTART BETWEEN '2020-06-21 00:00:00' AND '2020-06-29 23:59:59' AND
    crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
GROUP BY crichardson5.beat_event.tstart
ORDER BY crichardson5.beat_event.tstart ASC;


--Q4
SELECT TEND, ROUND(AVG(HRVALUE)), MIN(HRVALUE), MAX(HRVALUE), TO_TIMESTAMP(MAX(TEND), 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(MIN(TSTART), 'YYYY-MM-DD HH24:MI:SS') AS Duration
FROM (
SELECT *
FROM CRICHARDSON5.beat_event E, CRICHARDSON5.beat_heartrate H
WHERE E.CAT = 'rest' AND
      E.USERID = H.USERID AND
      E.USERID = '0.26777655249889387' AND
      H.time_stamp BETWEEN E.TSTART AND E.TEND AND
      E.TEND BETWEEN '2020-06-21 00:00:00' AND '2020-06-30 23:59:59'

)
GROUP BY TEND;


--Q5




