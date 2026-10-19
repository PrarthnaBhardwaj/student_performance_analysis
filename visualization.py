import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("student_data.csv")
subjects = ['Maths' ,'Python' ,'DBMS']
subject_averages = df[subjects].mean()
print("Subject-wise averages:")
print(subject_averages)
plt.bar(subject_averages.index, subject_averages.values)
plt.title("Subject-wise Average Marks")
plt.xlabel("Subjects")
plt.ylabel("Average Marks")
plt.ylim(0, 100)
plt.show()
# Compare the marks of individual students by graph (python,dbms,maths):
def student_graph(df):
    fig, ax = plt.subplots()
    name = df['Name'].tolist()
    maths_marks= df['Maths'].tolist()
    python_marks= df['Python'].tolist()
    dbms_marks = df['DBMS'].tolist()
    x = np.arange(len(name))
    width = 0.2
    ## now asiging bar:
    plt.bar(x-0.2,maths_marks,width,color = '#F4A7BB')
    plt.bar(x,python_marks,width,color = '#C3B1E1')
    plt.bar(x+0.2,dbms_marks,width,color = '#A8DADC')
    plt.title("Each student subject wise marks:")
    plt.xlabel("Student name")
    plt.ylabel("Marks")
    plt.xticks(x , name)
    plt.legend(subjects)
    plt.ylim(0,100)
    fig.tight_layout()
    return fig
## Highlight the students who need academic support:


