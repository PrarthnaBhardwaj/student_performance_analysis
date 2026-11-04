## Streamlit dashboard.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from visualization import student_graph
from io import StringIO
# Configure the dashboard
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dashboard title
st.title("📊 Student Performance & Academic Insights")
st.write("Analyze student marks, grades, and attendance.")

# Load student data
df = pd.read_csv("student_data.csv")

# Calculate average marks
subjects = ["Maths", "Python", "DBMS"]
df["Average"] = df[subjects].mean(axis=1)

# Assign grades
df["Grade"] = np.select(
    [
        df["Average"] >= 85,
        df["Average"] >= 70,
        df["Average"] >= 50
    ],
    ["A", "B", "C"],
    default="D"
)

# Summary metrics
st.subheader("Class Overview")
st.header("Whole class performance table:")
st.dataframe(df,width = "stretch")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Students", len(df))

with col2:
    st.metric(
        "Class Average",
        f"{df['Average'].mean():.2f}"
    )

with col3:
    st.metric(
        "Highest Average",
        f"{df['Average'].max():.2f}"
    )

with col4:
    pass_rate = (df["Average"] >= 50).mean() * 100
    st.metric("Pass Rate", f"{pass_rate:.1f}%")
# Subject-wise chart
st.subheader("Subject-wise Average Marks")

subject_averages = df[subjects].mean()
colors = []
for value in subject_averages.values:
   if value == subject_averages.max():
        colors.append('#A8D5BA')
else:
        colors.append('#CDB4DB')
 
fig,ax = plt.subplots(figsize = (8,4))
ax.bar(
    subject_averages.index,
    subject_averages.values,
    color = colors,
    width = 0.2
)
ax.set_title("Subject-wise Average Marks")
ax.set_xlabel("Subjects")
ax.set_ylabel("Average Marks")
ax.set_ylim(0,100)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", linestyle="--", alpha=0.3)
ax.set_axisbelow(True)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# Student records
st.subheader("Student Records")
# st.dataframe(df, use_container_width=True)
## Create a student filter:
grade_options = ['all'] + sorted(df['Grade'].unique().tolist())
selected_grade = st.selectbox(
"filter students by grade",
grade_options
)
## Filter students based on the selection:
if selected_grade == 'all':
    filtered_df = df
else:
    filtered_df = df[df['Grade'] == selected_grade]

    ## display the filtered df or filtered_df:
st.dataframe(filtered_df,width  = "stretch")
## show how many students match the filter:
st.write('total student displayed:',len(filtered_df))
## Search student by name:
student_name = st.text_input(
    label = "Searching for student name",
    placeholder= "Type name of student")
student_id = st.number_input(
    label = "Searching for student Id",
    placeholder="Type the student Id",
    step = 1,
    format= "%d"
)
 
def student_search(student_name,student_id,df):
    name_frame = Search_student(student_name,df)
    id_frame = Students_id(student_id,df)
    combined_frame = pd.concat([name_frame,id_frame])
    combined_frame = combined_frame.drop_duplicates()
    if combined_frame.empty:
       st.write("Result not found:")
    else:
        st.dataframe(combined_frame,width='stretch')
   

def Students_id(student_id,df):
 if student_id:
    search_id = df[df['Student_ID'] == student_id]
    if search_id.empty:
        st.write("Result not found")
        return search_id
    else:
        return search_id
 else:
  
    return pd.DataFrame()


def Search_student(student_name,df):
     if student_name:
      search_name = df[(df['Name'].str.contains(student_name,case=False ,na = False))]
      if search_name.empty:
          st.write("Result not found")
          return student_name
      else:
         return search_name
     else:
      return pd.DataFrame()
student_search(student_name,student_id,df)
## Graph of marks of each student in subject wise:
fig = student_graph(df)
st.pyplot(fig)

## Making a table for students who need academic supporyt:
at_risk = df[
   (df['Average']<50) |
        (df['Attendance']<80)
]

print("\nStudents needing academic support:")
print(at_risk[['Name','Average','Attendance']])

## Highlight the students who need academic support:
st.subheader('Students Who need Academic Support:')
st.dataframe(at_risk,width='stretch')
## Checking for invalid inputs:
invalid_marks = df[((df[subjects]<0) | (df[subjects]>100)).any(axis = 1)]
invalid_id = df[(df['Student_ID']<=0)]
invalid_name = df[(df['Name'].isna() |~ df['Name'].astype('string').str.strip().str.replace(' ','',regex=False).str.isalpha().fillna(False))]
st.subheader("Invalid Names:")
st.dataframe(invalid_name)
st.subheader("Invalid Student_Id:")
st.dataframe(invalid_id)
st.subheader("Invalid Marks:")
st.dataframe(invalid_marks)


## Showing the required columns to user:
st.subheader("Your required column:")
req_col=df.columns.tolist()
## displays col name to user:
st.markdown(req_col)
## print this to console
print(req_col)

## Download filtered student records and analysis reports
    ## a:  Filter students by studey_hours,marks,attandace:
## filtered student records
st.subheader("students filter record:")
filter_data = df[(df[subjects]<75).any(axis = 1) | (df['Attendance']<80) | ( df['Study_Hours']<3)]
st.dataframe(filter_data,width='stretch')

## ANALYSIS REPORT:
## a; General Report:
total_students = len(df.index)
maths_avg = df['Maths'].mean(axis = 0)
python_avg = df['Python'].mean(axis = 0)
dbms_avg = df['DBMS'].mean(axis = 0)
attendance_avg = df['Attendance'].mean(axis = 0)
## student performance analysis:
max_avg = df['Average'].max()
low_att = df['Attendance'].min()
high_att = df['Attendance'].max()
min_avg = df['Average'].min()
 
 ## Compare performance across diff subjects:
py_max = df['Python'].max(axis = 0)
maths_max = df['Maths'].max(axis = 0)
dbms_max = df['DBMS'].max(axis = 0)

## Attendance and Study hours analysis:
low_att_no = (df['Attendance']<80).sum()
low_hour_no = (df['Study_Hours']<2).sum()
## at_risk : student need academic support:

st.subheader("Analysis Report:")
class_report = {
    'Total students': total_students,
    'Maths Average': maths_avg,
    'Python average': python_avg,
    'DBMS average': dbms_avg,
    'Attendance average': attendance_avg,
    'Maximum average': max_avg,
    'Minimum average': min_avg,
    'Low Attendance': low_att,
    'Highest Attendance': high_att,
    'Max python': py_max,
    'Max Maths': maths_max,
    'Max DBMS': dbms_max,
    'low Attendance count': low_att_no,
    'low study-hours count': low_hour_no
}
report = pd.DataFrame([class_report])
st.dataframe(report,width='stretch')

## Adding the Download button:
def convert_for_download(df):
    return df.to_csv().encode("utf-8")
csv = convert_for_download(filter_data)
st.download_button(
    label="Download filter record:",
    data=csv,
    file_name="filter record.csv",
    mime="txt/csv",
)
text = convert_for_download(report)
st.download_button(
     label= "Download analysis report",
     data = text,
     file_name = "analysis report.csv",
     mime = "txt/csv", 
  ) 
## Someone's Else wants to upload their csv file:
uploaded_file = st.file_uploader("Choose a file",type = ["csv"])
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.markdown(dataframe)

## 

