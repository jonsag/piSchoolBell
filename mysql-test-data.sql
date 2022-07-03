INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('First ring in', '20');
INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('Second ring in', '10, 5, 10');
INSERT INTO ringPatterns (ringPatternName, ringPattern)
VALUES ('Ring out', '10');
INSERT INTO breaks (breakName, startDate, endDate)
VALUES ('Test break', '2018-03-12', '2018-03-13');
INSERT INTO breaks (breakName, startDate, endDate)
VALUES ('Breakday', '2018-03-15', '2018-03-15');
INSERT INTO extraDays (extraDayName, extraDayDate)
VALUES ('Parents day', '2018-03-17');
INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('1 first lesson in', '1111100', '08:08', '1');
INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('2 first lesson in', '1111100', '08:10', '2');
INSERT INTO ringTimes (ringTimeName, weekDays, ringTime, ringPatternId)
VALUES ('First lesson out', '1111100', '08:50', '3');
