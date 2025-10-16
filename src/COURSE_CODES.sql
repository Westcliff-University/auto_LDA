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

SET NOCOUNT ON;

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
    /* where students.InstitutionId in (1,31,32) */
    AND (studentTermCourseSections.Status LIKE 'AS%' OR studentTermCourseSections.Status LIKE 'AC%')
),

dropped_sections AS (
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
    /* where students.InstitutionId in (1,31,32) */
    AND (studentTermCourseSections.Status LIKE 'IW%' OR studentTermCourseSections.Status LIKE 'ID%')
)

SELECT p.StudentIdentifier,
STUFF(
    (
          SELECT DISTINCT ',' + sections.SectionCode
          FROM sections
          WHERE p.StudentIdentifier = sections.StudentIdentifier
          /* AND (sections.SectionCode LIKE '%241%' OR sections.SectionCode LIKE '%242%') */
          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '') AS Courses
, 
    CASE WHEN
    (STUFF(
    (
          SELECT DISTINCT ',' + dropped_sections.SectionCode
          FROM dropped_sections
          WHERE p.StudentIdentifier = dropped_sections.StudentIdentifier
          AND (dropped_sections.SectionCode LIKE '%251%' OR dropped_sections.SectionCode LIKE '%252%')
          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '')) IS NULL THEN 'None'
    ELSE (STUFF(
    (
          SELECT DISTINCT ',' + dropped_sections.SectionCode
          FROM dropped_sections
          WHERE p.StudentIdentifier = dropped_sections.StudentIdentifier
          AND (dropped_sections.SectionCode LIKE '%251%' OR dropped_sections.SectionCode LIKE '%252%')
          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, ''))
    END AS Dropped_Courses
FROM academics.Students s
LEFT JOIN config.People p ON p.ID = s.PersonID
WHERE STUFF(
    (
          SELECT ',' + sections.SectionCode
          FROM sections
          WHERE p.StudentIdentifier = sections.StudentIdentifier
          /* AND (sections.SectionCode LIKE '%241%' OR sections.SectionCode LIKE '%242%') */
          FOR XML PATH(''), TYPE).value('.', 'NVARCHAR(MAX)'), 1, 1, '') IS NOT NULL
GROUP BY p.StudentIdentifier
