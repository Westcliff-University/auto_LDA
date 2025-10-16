/*
// PC=Pending Confirmation
// AS=Active / Scheduled
// AC=Active / Current
// AL=Active / Leave Of Absence
// ID=Inactive / Dropped
// IW=Inactive / Withdrawn
// IC=Inactive / Cancelled
// CN=Complete / Not graded
// CG=Complete / Graded
*/

WITH sections AS (
select people.studentidentifier,termCourseSections.SectionCode,termCourseSections.StartDate,termCourseSections.EndDate,terms.Name as TermName
    ,studentTermCourseSections.Status
    /*,letterGrades.Code
    ,studentTermCourseSections.NumericGrade*/
    from academics.studentTermCourseSections
    join academics.students on students.id = studenttermcoursesections.studentid
    join config.people on people.id = students.personid
    join academics.termCourseSections on termCourseSections.id = studentTermCourseSections.TermCourseSectionId
    join academics.terms on terms.id = termCourseSections.TermId
    join academics.courses on courses.id = termCourseSections.CourseId
    /* join academics.letterGrades on letterGrades.id = studentTermCourseSections.LetterGradeId */
    where students.InstitutionId in (1,31,32)
    /*AND (studentTermCourseSections.Status LIKE 'AC%' OR studentTermCourseSections.Status LIKE 'AS%')*/
)

SELECT DISTINCT p.StudentIdentifier, sections.SectionCode
FROM academics.Students s
LEFT JOIN config.People p ON p.ID = s.PersonID
LEFT JOIN sections ON sections.StudentIdentifier = p.StudentIdentifier
LEFT JOIN config.statuses st ON st.ID = s.StatusID
LEFT JOIN config.Campuses c ON c.ID = s.CampusID
WHERE p.StudentIdentifier IS NOT NULL
/* AND s.InstitutionID = 1 */
AND sections.SectionCode IS NOT NULL
AND st.Name IN ('Active', 'Active not attending', 're-entry' ,'Enrollment confirmed','Leave of Absence', 're-admit')
AND NOT (
c.Name NOT LIKE '%PREPARATORY%'
AND c.Name NOT LIKE '%KING%'
AND c.Name NOT LIKE '%PRESIDENT%'
AND c.Name NOT LIKE '%MAJ%'
AND c.Name NOT LIKE '%DUBAI%'
AND c.Name NOT LIKE '%UNICOLLEGE%'
AND c.Name NOT LIKE '%WESTERN STATE%'
AND c.Name NOT LIKE '%PREMIER%'
AND c.Name NOT LIKE '%CAPITOL%')
AND c.Name NOT LIKE '%Corona%'
AND s.StartDate NOT LIKE '%TRANSFER%' 
AND (sections.SectionCode LIKE '%255%' OR sections.SectionCode LIKE '%256%' OR sections.SectionCode LIKE '%251%' OR sections.SectionCode LIKE '%252%')
ORDER BY p.StudentIdentifier


