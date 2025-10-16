/**/

SELECT CONCAT('<a target="_new" href="gap.westcliff.edu/course/view.php?id=',a.course,'">', a.course, '</a>') AS 'Course link',
c.fullname AS 'Course Name',
c.shortname AS 'Course Code',
u.username AS 'Student ID',
u.firstname AS 'First Name',
u.lastname AS 'Last Name',
#DATE_FORMAT(FROM_UNIXTIME(att.sessdate),'%d %M %Y') AS 'Meeting Date',
FROM_UNIXTIME(att.sessdate) AS 'Meeting Date',
attst.acronym AS 'Attendance Status',
(SELECT name FROM prefix_role WHERE id = en.roleid) AS 'Role Name'

FROM prefix_attendance_sessions AS att
JOIN prefix_attendance_log AS attlog ON att.id = attlog.sessionid
JOIN prefix_attendance_statuses AS attst ON attlog.statusid = attst.id
JOIN prefix_attendance AS a ON att.attendanceid = a.id
JOIN prefix_course AS c ON a.course = c.id
JOIN prefix_enrol AS en ON en.courseid = c.id
JOIN prefix_user_enrolments AS ue ON ue.enrolid = en.id
JOIN prefix_user AS u ON attlog.studentid = u.id AND ue.userid = u.id
WHERE (c.fullname like '%KINGS%' OR c.fullname LIKE '%PGS%' OR c.fullname LIKE '%PBS%')
AND c.fullname NOT IN ('Westcliff_Library')
AND c.fullname NOT LIKE '%Orientation%'
AND c.fullname NOT LIKE '%NSO%'
%%FILTER_STARTTIME:att.sessdate:>%% %%FILTER_ENDTIME:att.sessdate:<%%
%%FILTER_COURSES:c.fullname%%

# Some temporary lines while the .csv functions are being fixed
# AND c.shortname LIKE '%246%'
AND DATEDIFF(NOW(), FROM_UNIXTIME(att.sessdate)) < 15

# End of temporary lines