import os
from dotenv import load_dotenv
import pandas as pd
import time
from contextlib import chdir
from edit_query import edit_query
from get_df_from_sql import get_df_from_sql
from report_editor import report_editor
from make_lda import make_lda
from platform import platform
from datetime import datetime

load_dotenv()

t0 = time.time()

gap_url = 'https://gap.westcliff.edu/'
profile_url = 'https://gap.westcliff.edu/user/profile.php'
recent_attendance_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=7&comp=customsql&courseid=5760'
test_engagement_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=72&comp=customsql&courseid=5760'
test_engagement_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=72&download=1&format=csv'

ir_attendance_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=7&comp=customsql&courseid=1'
ir_attendance_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/managereport.php?courseid=1'

last_meaningful_engagement_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=68&comp=customsql&courseid=5760'
last_meaningful_engagement_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=68&courseid=5760'

engagement_by_student_and_course_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=59&comp=customsql'
engagement_by_student_and_course_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=59'
other_reports_url = 'https://gap.westcliff.edu/blocks/configurable_reports/managereport.php?courseid=5760'

dge_ir_attendance_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=9&comp=customsql&courseid=5760'
dge_ir_attendance_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=9&courseid=5760'

dge_last_meaningful_engagement_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=71&comp=customsql&courseid=5760'
dge_last_meaningful_engagement_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=71&courseid=5760'

dge_engagement_by_student_and_course_url = 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=70&comp=customsql'
dge_engagement_by_student_and_course_dl_url = 'https://gap.westcliff.edu/blocks/configurable_reports/viewreport.php?id=70&courseid=5760'


# it would be nice to have a resource that pulls these from, say, Github
ir_attendance_file = 'ir_attendance.sql'
dge_ir_attendance_file = 'dge_ir_attendance.sql'
last_meaningful_engagement_file = 'last_meaningful_engagement.sql'
dge_last_meaningful_engagement_file = 'dge_last_meaningful_engagement.sql'
engagement_by_student_and_course_file = 'engagement_by_student_and_course.sql'
dge_engagement_by_student_and_course_file = 'dge_engagement_by_student_and_course.sql'

username = os.environ.get('GAP_USER')
password = os.environ.get('GAP_PASS')


dge_ir_attendance_editor = report_editor(
                report_name = "dge_recent_attendance"
                ,report_url = dge_ir_attendance_url
                ,query_file = dge_ir_attendance_file
                ,dl_url = dge_ir_attendance_dl_url
                ,domestic = False
                ,username = username
                ,num_splits = 1
                ,time_restriction = False
                ,need_id_filter = False
                ,password = password)

dge_ir_attendance_editor.login_to_gap()
dge_ir_attendance_editor.fetch_GAP_report()
dge_ir_attendance_editor.quit()

engagement_by_student_and_course_editor = report_editor(
                report_name = "recent_engagement"
                ,report_url = engagement_by_student_and_course_url
                ,query_file = engagement_by_student_and_course_file
                ,dl_url = engagement_by_student_and_course_dl_url
                ,domestic = True
                ,time_restriction = True
                ,need_id_filter = True
                ,username = username
                ,num_splits = 5
                ,password = password)

engagement_by_student_and_course_editor.login_to_gap()
engagement_by_student_and_course_editor.fetch_GAP_report()
engagement_by_student_and_course_editor.quit()

ir_attendance_editor = report_editor(
                report_name = "recent_attendance"
                ,report_url = ir_attendance_url
                ,query_file = ir_attendance_file
                ,dl_url = ir_attendance_dl_url
                ,domestic = True
                ,username = username
                ,num_splits = 4
                ,time_restriction = False
                ,need_id_filter=True
                ,password = password)

ir_attendance_editor.login_to_gap()
ir_attendance_editor.fetch_GAP_report()
ir_attendance_editor.quit()

last_meaningful_engagement_editor = report_editor(
                report_name = "last_meaningful_engagement"
                ,report_url = last_meaningful_engagement_url
                ,query_file = last_meaningful_engagement_file
                ,dl_url = last_meaningful_engagement_dl_url
                ,domestic = True
                ,username = username
                ,num_splits = 5
                ,time_restriction = True
                ,need_id_filter=True
                ,password = password)


last_meaningful_engagement_editor.login_to_gap()
last_meaningful_engagement_editor.fetch_GAP_report()
last_meaningful_engagement_editor.quit()


dge_engagement_by_student_and_course_editor = report_editor(
                report_name = "dge_recent_engagement"
                ,report_url = dge_engagement_by_student_and_course_url
                ,query_file = dge_engagement_by_student_and_course_file
                ,dl_url = dge_engagement_by_student_and_course_dl_url
                ,domestic = False
                ,time_restriction = True
                ,need_id_filter = True
                ,username = username
                ,num_splits = 4
                ,password = password)

dge_engagement_by_student_and_course_editor.login_to_gap()
dge_engagement_by_student_and_course_editor.fetch_GAP_report()
dge_engagement_by_student_and_course_editor.quit()

dge_last_meaningful_engagement_editor = report_editor(
                report_name = "dge_last_meaningful_engagement"
                ,report_url = dge_last_meaningful_engagement_url
                ,query_file = dge_last_meaningful_engagement_file
                ,dl_url = dge_last_meaningful_engagement_dl_url
                ,domestic = False
                ,username = username
                ,num_splits = 4
                ,time_restriction = True
                ,need_id_filter = True
                ,password = password)


dge_last_meaningful_engagement_editor.login_to_gap()
dge_last_meaningful_engagement_editor.fetch_GAP_report()
dge_last_meaningful_engagement_editor.quit()

scc = get_df_from_sql("student_course_combos.sql")
dge_scc = get_df_from_sql("dge_student_course_combos.sql")
sis_df = get_df_from_sql('LDA_info.sql')

dge_sis_df = get_df_from_sql('DGE_LDA_info.sql')
course_codes = get_df_from_sql('COURSE_CODES.sql')

if 'Window' in platform():
    data_dir = os.path.abspath(os.pardir + '\\data')
else:
    data_dir = "../data"

with chdir(data_dir):
    
    engagement = pd.read_csv('recent_engagement.csv')
    dge_engagement = pd.read_csv('dge_recent_engagement.csv')

    raw_df = pd.read_csv('old_gap_data.csv')
    raw_df = pd.concat([raw_df, pd.read_csv('recent_attendance.csv')])
    raw_df.to_csv('old_gap_data.csv', index = 0)

    dge_df = pd.read_csv('dge_old_gap_data.csv')
    dge_df = pd.concat([dge_df, pd.read_csv('dge_recent_attendance.csv')])
    dge_df.to_csv('dge_old_gap_data.csv', index = 0)

    gap_lda, lda_by_course = make_lda(raw_df, sis_df, engagement, scc, course_codes)
    dge_gap_lda, dge_lda_by_course = make_lda(dge_df, dge_sis_df, dge_engagement, dge_scc, course_codes)

    output_dir = f'output-{datetime.today().strftime('%Y-%m-%d')}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with chdir(output_dir):
        course_codes.to_csv('COURSE_CODES.csv')
        sis_df.to_csv('LDA_info.csv', index = 0)
        dge_sis_df.to_csv('DGE_LDA_info.csv')
        gap_lda.to_csv('gap_non_absentees_lda.csv', index = 1)
        dge_gap_lda = dge_gap_lda[dge_gap_lda[dge_gap_lda.columns[0]].astype('datetime64[ns]') < datetime.now()]
        dge_gap_lda.to_csv('dge_gap_non_absentees_lda.csv', index = 1)
        lda_by_course.to_csv('lda_by_course.csv', index = 0)
        dge_lda_by_course.to_csv('dge_lda_by_course.csv', index = 0)
        try:
            os.rename('../last_meaningful_engagement.csv', 'last_meaningful_engagement.csv')
        except:
            1
        try:
            os.rename('../dge_last_meaningful_engagement.csv', 'dge_last_meaningful_engagement.csv')
        except:
            1

t1 = time.time()
print(f'Total execution time: {int(100 * (t1 - t0)/60)/100} minutes.')