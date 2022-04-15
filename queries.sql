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


--Q2 TODO format for remote access
SELECT ce.tstart STIME, round(avg(hr.hrvalue)) AVGHR, max(hr.hrvalue) MAXHR ,min(hr.hrvalue) MINHR
FROM (
    SELECT ROW_NUMBER() OVER (ORDER BY tstart) i1, tstart, cat, userid, tend
    FROM crichardson5.beat_event 
    WHERE cat = :catone or cat = :cattwo ) ce
    INNER JOIN 
    (SELECT ROW_NUMBER() OVER (ORDER BY tstart) i2, tstart, cat, userid 
    FROM crichardson5.beat_event 
    WHERE cat=:catone or cat = :cattwo ) pe 
    ON ce.i1 = pe.i2 + 1,
    crichardson5.beat_heartrate hr
WHERE
    ce.userid = pe.userid AND
    ce.userid = hr.userid AND
    ce.userid = :uuid AND
    pe.cat = :catone AND 
    ce.cat = :cattwo AND 
    ce.tstart BETWEEN :daystart AND :dayend AND
    hr.time_stamp BETWEEN ce.tstart AND ce.tend      
GROUP BY ce.tstart 
ORDER BY ce.tstart
                        
--Q3
SELECT TO_TIMESTAMP(TSTART, 'YYYY-MM-DD HH24:MI:SS') AS start_time, TO_TIMESTAMP(TEND, 'YYYY-MM-DD HH24:MI:SS') AS end_time, MAX(HRVALUE), TO_TIMESTAMP(MAX(TEND), 'YYYY-MM-DD HH24:MI:SS') - TO_TIMESTAMP(MIN(TSTART), 'YYYY-MM-DD HH24:MI:SS') AS Duration 
FROM crichardson5.beat_heartrate , crichardson5.beat_event
WHERE crichardson5.beat_event.USERID = crichardson5.beat_heartrate.USERID AND
    crichardson5.beat_event.USERID = '0.26777655249889387' AND
    crichardson5.beat_event.CAT = 'fitness' AND
    crichardson5.beat_event.TSTART BETWEEN '2020-06-21 00:00:00' AND '2020-06-29 23:59:59' AND
    crichardson5.beat_heartrate.TIME_STAMP BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
GROUP BY crichardson5.beat_event.tstart, crichardson5.beat_event.tend
ORDER BY crichardson5.beat_event.tstart ASC


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
SELECT 
ROUND(100 - (((avghr_d-avghr_r)/avghr_r)*100)) as recovery_score,
DAY 
FROM
    -- resting HR avg for all days in the given range
    (SELECT 
            ROUND(AVG(hrvalue)) AS avghr_r, 
            crichardson5.beat_heartrate.userid AS id
        FROM crichardson5.beat_heartrate, crichardson5.beat_event
        WHERE
            crichardson5.beat_heartrate.userid = %s AND
            cat='rest' AND
            crichardson5.beat_heartrate.time_stamp BETWEEN %s AND %s
    GROUP BY crichardson5.beat_heartrate.userid
    ),
    -- avg HR values per day in the given range
    ( SELECT ROUND(AVG(hrvalue)) as avghr_d,USERID, DAY
        FROM( SELECT crichardson5.beat_heartrate.USERID USERID,crichardson5.beat_heartrate.HRVALUE HRVALUE,SUBSTR(TSTART, 1, 10) AS DAY
            FROM crichardson5.beat_heartrate, crichardson5.beat_event
            WHERE crichardson5.beat_event.tstart BETWEEN %s AND %s AND
                    crichardson5.beat_heartrate.time_stamp BETWEEN crichardson5.beat_event.TSTART AND crichardson5.beat_event.TEND
                    AND cat='rest' 
                    AND crichardson5.beat_heartrate.userid = %s) new_dates
            GROUP BY USERID, DAY ORDER BY DAY ASC)
WHERE id = %s