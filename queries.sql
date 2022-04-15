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
SELECT ce.tstart, avg(hr.hrvalue) avgHR, max(hr.hrvalue) maxHR,min(hr.hrvalue) minHR
FROM (--PSEUDO: sort by tstart and label the indexes of each row. For rows in table CE and PE, join CE[i] w PE[i+1]
    SELECT ROW_NUMBER() OVER (ORDER BY tstart) i1, tstart, cat, userid, tend
    FROM beat_event 
    WHERE cat='rest' or cat = 'fitness' ) ce --Current Event = Activity 2
    INNER JOIN 
    (SELECT ROW_NUMBER() OVER (ORDER BY tstart) i2, tstart, cat, userid 
    FROM beat_event 
    WHERE cat='rest' or cat = 'fitness' ) pe --Previous Event = Activity 1
    ON ce.i1 = pe.i2 + 1,
    beat_heartrate hr
WHERE pe.cat = 'fitness' AND --Activity 1
      ce.cat = 'rest' AND --Activity 2
      ce.userid = pe.userid AND
      ce.userid = hr.userid AND
      ce.tstart BETWEEN '2021-02-11 00:00:00' AND '2022-02-11 23:59:59' AND
      --ce.userid = '<SPECIFIC_USERID>' AND
      hr.TIME_STAMP BETWEEN ce.tstart AND ce.tend      
GROUP BY ce.tstart --Get all relevant HR data for each rest session
ORDER BY ce.tstart;



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