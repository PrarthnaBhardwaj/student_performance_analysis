import numpy as np
import pandas as pd
## reading the csv file:
df = pd.read_csv('student_data.csv')
subjects = ['Maths' , 'Python' , 'DBMS']
df['average'] = df[subjects].mean(axis = 1) ## calculation row wise:
df['Grades'] = np.select(
    [
         df['average']>=85,
         df['average']>=70,
         df['average']>=50,
    ],
    ["A","B","C"],
    default = "D"
)

print("Total students:",len(df))
print("Class average",round(df['average'].mean(), 2))
print("Highest average",round(df['average'].max(), 2))
print("Minimum average",round(df['average'].min(), 2))

at_risk = df[
   (df['average']<50) |
        (df['Attendance']<75)
]

print("\nStudents needing academic support:")
print(at_risk[['Name','average','Attendance']])

# Display all analyzed records
print("\nStudent analysis:")
print(df[["Name", "average", "Grades"]])
# Calculating marks:

## Validate missing marks:
print(df[df[subjects].isna().any()])
## For duplicated Id:
print(df[df['Student_ID'].duplicated(keep =False)]) ## it returns atleast one true if present otherwise false:
## For Invalid values:
## check for invalid marks:
invalid_marks = df[((df[subjects]<0) | (df[subjects]>100)).any(axis = 1)]
invalid_id = df[(df['Student_ID']<=0)]
invalid_name = df[(df['Name'].isna() |~ df['Name'].astype('string').str.strip().str.replace(' ','',regex=False).str.isalpha().fillna(False))]
