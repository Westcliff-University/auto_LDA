import pandas as pd
import pyodbc
from create_query_string import create_query_string

def make_lda(gap_df, sis_df, engagement_df, scc, course_codes):
    """
    Creates the Last Day of Attendance report components. They still need to be manually
    imported into Google Sheets, however.

    Keyword arguments:
    gap_df -- A pandas dataframe consisting of recent attendance data. See 'https://gap.westcliff.edu/blocks/configurable_reports/editcomp.php?id=7&comp=customsql&courseid=1' for example column headers.
    sis_df -- A pandas dataframe consisting of basic student information. 

    """  
    max_number_of_courses = 0
    for i in range(len(course_codes)):
        max_number_of_courses = max(1 + course_codes.iloc[i].values[1].count(','), max_number_of_courses)
    
    non_absentees = gap_df.loc[(gap_df['attendance status'] != 'V') & (gap_df['attendance status'] != 'A')]
    #non_absentees = non_absentees[non_absentees['course name'].str.contains(r'253|254')]
    last_attendance = {}
    
    lda_columns = ['student id']
    for i in range(max_number_of_courses):
        lda_columns += [f'course {i + 1} code', f'course {i + 1} GAP LDA']
    
    lda_df = pd.DataFrame(columns = lda_columns)
    
    non_absentees = non_absentees.sort_values(by = ['meeting date'], ascending = False)
   
    i = 0
    # for course in non_absentees.loc[non_absentees['student id'] == non_absentees['student id'].unique()[0]]['course name'].unique():
        # print(course)
        
    
    non_absentees = non_absentees.drop_duplicates(subset=['student id', 'course name'])
    
    non_absentees['student id'] = non_absentees['student id'].apply(str.upper)
    
    non_absentees['student_course_combo'] = non_absentees['student id'] + non_absentees['course code']

    #scc = pd.read_csv('student_course_combos.csv')
    scc['student_course_combo'] = scc['StudentIdentifier'] + scc['SectionCode']
    
    test_df = pd.merge(scc, non_absentees, left_on = 'student_course_combo', right_on = 'student_course_combo', how = 'left')
    test_df_clean = test_df[['student_course_combo', 'student id', 'StudentIdentifier', 'course code', 'SectionCode', 'meeting date']].dropna(subset = ['meeting date'])

    sis_df = sis_df.rename(columns = {'StudentAssignedID': 'student id'})

    # display(test_df_clean)
    # display(sis_df)
    
    new_out_df = pd.merge(test_df_clean, sis_df, left_on = 'student id', right_on = 'student id', how = 'left')
    engagement_df['user'] = engagement_df['user'].apply(str.upper)
    
    engagement_df['student_course_combo'] = engagement_df['user'] + engagement_df['course_name']
    
    new_out_df = pd.merge(new_out_df, engagement_df, left_on = 'student_course_combo', right_on = 'student_course_combo', how = 'left')
    
    
    new_out_df['meeting date'] = new_out_df['meeting date'].astype('datetime64[ns]')
    
    new_out_df['lastengagementpoint'] = new_out_df['time_pst'].astype('datetime64[ns]')
    
    new_out_df['LDA'] = new_out_df[['meeting date', 'lastengagementpoint']].max(axis = 1)
    
    new_out_df['GAP Difference'] = (pd.Timestamp.now() - pd.to_datetime(new_out_df['LDA'], dayfirst=True)).dt.days
    
        # If your original date fields have invalid dates and you would like this number of days to be an integer:
    new_out_df['GAP Difference'] = new_out_df['GAP Difference'].astype('Int64')   
    
    new_out_df['GAP LDA < 7'] = new_out_df['GAP Difference'] < 7
    new_out_df['7 <= GAP LDA <= 14'] = ((new_out_df['GAP Difference'] <= 14) == True) & ((new_out_df['GAP Difference'] >= 7) == True)
    new_out_df['14 < GAP LDA'] = new_out_df['GAP Difference'] > 14
    
    
    
    for student in non_absentees['student id'].unique():
        course_df = non_absentees[non_absentees['student id'] == student]
        student_records = {}
        try:
            len(last_attendance[student])
        except:
            last_attendance[student] = max(non_absentees.loc[non_absentees['student id'] == student]['meeting date'])
    
    out_df = pd.DataFrame(last_attendance.values(), index = last_attendance.keys())
    return out_df, new_out_df[['student id',
           'course code', 'meeting date', 'Campus', 'AdvisorName',
           'LastName', 'FirstName', 'Phone', 'Email', 'StudentStatus',
           'CurrentProgramName', 'ProgramStart', 'LastDateAttended',
           'TitleIV', 'InternationalStudent',
           'lastengagementpoint', 'LDA', 'GAP Difference', 'GAP LDA < 7',
           '7 <= GAP LDA <= 14', '14 < GAP LDA']]
    