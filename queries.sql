--Put queries here
--Q1
SELECT AVG(HRvalue), MIN(HRvalue), MAX(HRvalue), a.CAT
FROM (beat_event e JOIN beat_heartrate h (
    ON e.userID = h.userID AND
    h.time_stamp BETWEEN e.tstart AND e.tend)) a
WHERE a.userID='<USERID>' AND
    a.tstart BETWEEN '<START TIMESTAMP>' AND '<END TIMESTAMP>'
GROUP BY a.cat


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
SELECT *
FROM crichardson5.beat_heartrate, crichardson5.beat_event, crichardson5.beat_customer
WHERE crichardson5.beat_heartrate.USERID = crichardson5.beat_event.USERID AND
    crichardson5.beat_customer.USERID = crichardson5.beat_heartrate.USERID AND
    crichardson5.beat_customer.USERID = crichardson5.beat_event.USERID AND 
    crichardson5.beat_event.CAT = 'fitness' AND
    crichardson5.beat_event.TSTART BETWEEN '2021-02-11 00:00:00' AND '2021-02-11 23:59:59' AND
    crichardson5.beat_heartrate.TIME_STAMP BETWEEN '2021-02-11 00:00:00' AND '2021-02-11 23:59:59';


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
SELECT ((oneday.AVG(HRvalue) / sevenday.AVG(HRvalue)) * 100)
FROM
    (SELECT AVG(HRvalue) 
    FROM beat_event e
    WHERE cat='rest') restHR JOIN beat_heartrate ON 
        
        AND 



SELECT *, AVG(HRvalue)
FROM beat_event e JOIN beat_heartrate h
ON h.time_stamp BETWEEN e.tstart AND e.tend 
    AND e.userID=h.userID 
    AND 


cat='rest'