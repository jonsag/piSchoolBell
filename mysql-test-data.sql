INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('first ring in', '20');

INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('second ring in', '10, 5, 10');

INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('ring out', '10');



INSERT INTO breaks (breakName, startDate, endDate)
VALUES ('testlov', '2018-03-12', '2018-03-13');

INSERT INTO breaks (breakName, startDate, endDate)
VALUES ('testlovdag', '2018-03-15', '2018-03-15');



INSERT INTO extraDays (extraDayName, extraDayDate)
VALUES ('föräldradag', '2018-03-17');



INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('inringning första', '1111100', '08:08', '1');

INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('inringning andra', '1111100', '08:10', '2');

INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('utringning', '1111100', '08:50', '3');


