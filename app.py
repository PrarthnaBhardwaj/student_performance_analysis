## Streamlit dashboard.

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from visualization import student_graph
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
        (df['Attendance']<75)
]

print("\nStudents needing academic support:")
print(at_risk[['Name','Average','Attendance']])

## Highlight the students who need academic support:
st.subheader('Students Who need Academic Support:')
st.dataframe(at_risk,width='stretch')