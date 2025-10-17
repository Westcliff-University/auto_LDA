# auto_LDA
For producing the Last Day of Attendance report automatically

Import the contents of `data/output-...` into Google sheets. Here are the most recent links for each. Produce a copy for each, maintaining the `YYMMDD` date format at the beginning.
 - Normal LDA Report: https://docs.google.com/spreadsheets/d/1Ux7-M0HBAyope79z6umSOR-Au3u2hn32gXL4K_hotUg/edit?gid=819407507#gid=819407507
 - DGE/AI LDA Report: https://docs.google.com/spreadsheets/d/1Bqge5sLIGcTxB32m6DnsFvZ91HrWe73rhKgOhtct58o/edit?gid=415666902#gid=415666902

# Important: Do not overwrite data on old sheets. Make the copy, change the dates in the titles of the copies, which will become the new editions to be sent out.

Once you have made the copies, both of these sheets are updated in almost the exact same way. Considering the tabs from left to right, the update process (or lack thereof) shall be detailed, with one possible step of going from right to left in order to update the main list of students on the main tab.

 - Sheet1: Update cells in row 1 (near column `Q`) to reflect the current day. You may be tempted to replace these with something that references the current date and updates automatically, but this report computes static differences in days between the "current date" and the last date of attendance, so we must perform a manual update to these cells.
 - LDA by Student-Course Combination: Import `lda_by_course.csv` or `dge_lda_by_course.csv` as appropriate from this directory.
 - Filter View FA: Ignore this. If you receive questions about it, the details of its construction are embedded in the formula in cell `A1`.
 - Sheet19: I don't know why this is here. It's a query tab anyway, so there's no manual process involved.
 - DO NOT TOUCH - IR UPDATE: Import `sis_dump.csv` or `dge_sis_dump.csv` as appropriate from this directory.
# Important: At the start of a session, it is a good idea to copy the entire list of IDs from DO NOT TOUCH - IR UPDATE to Sheet1 column `A` and paste it down. Then remove all duplicate rows, analyzing only column `A`. Then copy all of the formulas down so all of the rows with new students' IDs have populated information.

Continuing to the right now...
   
 - last_meaningful_engagement: Import `Engagement Report by Student-2025...` or `DGE Engagement Report by Student-2025...` as appropriate.
 - course_codes: Import `course_codes.csv`.
 - Brian course_codes: Who knows why that's there? I don't recall putting that one there, but maybe I've gone senile.
 - DO NOT TOUCH - GAP_NON_ABSENTEES: Import `gap_non_absentees_lda.csv` or `dge_gap_non_absentees_lda.csv` as appropriate from this directory.
 - Sheet22: I don't know why this is here. It's a query tab anyway, so there's no manual process involved.
 - Adam: I don't know why this is here. I've never had to update it.

Once each LDA report is complete, send it to the appropriate mailing list, either lda@westcliff.edu or ai-lda@westcliff.edu.
Once the emails are sent out, you should be done.


