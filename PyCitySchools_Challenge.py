#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies and Setup
import pandas as pd


# Files to Load (Remember to change the path if needed.)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read the School Data and Student Data and store into a Pandas DataFrame
school_data_df = pd.read_csv(school_data_to_load)
student_data_df = pd.read_csv(student_data_to_load)

# Cleaning Student Names and Replacing Substrings in a Python String
# Add each prefix and suffix to remove to a list.
prefixes_suffixes = ["Dr. ", "Mr. ","Ms. ", "Mrs. ", "Miss ", " MD", " DDS", " DVM", " PhD"]

# Iterate through the words in the "prefixes_suffixes" list and replace them with an empty space, "".
for word in prefixes_suffixes:
    student_data_df["student_name"] = student_data_df["student_name"].str.replace(word,"")

# Check names.
student_data_df.head(10)


# In[2]:


# Deliverable 1: Replace the reading and math scores


# Install numpy using conda install numpy or pip install numpy. 
# Step 1. Import numpy as np.
import numpy as np


# In[3]:


# Step 2. Use the loc method on the student_data_df to select all the reading scores from the 9th grade at Thomas High School and replace them with NaN.
student_data_df.loc[(student_data_df["grade"]== "9th") & (student_data_df["school_name"]=="Thomas High School") ,
                    "reading_score"] = np.nan


# In[4]:


#  Step 3. Refactor the code in Step 2 to replace the math scores with NaN.
student_data_df.loc[(student_data_df["grade"]== "9th") & (student_data_df["school_name"]=="Thomas High School") ,
                    "math_score"] = np.nan


# In[5]:


#  Step 4. Check the student data for NaN's. 
student_data_df.tail()


# In[6]:


# Deliverable 2: Repeat the school district analysis


# Combine the data into a single dataset
school_data_complete_df = pd.merge(student_data_df, school_data_df, how="left", on=["school_name", "school_name"])
school_data_complete_df.head()


# In[7]:


# Calculate the Totals (Schools and Students)
school_count = len(school_data_complete_df["school_name"].unique())
student_count = school_data_complete_df["Student ID"].count()

# Calculate the Total Budget
total_budget = school_data_df["budget"].sum()


# In[8]:


# Calculate the Average Scores using the "clean_student_data".
average_reading_score = school_data_complete_df["reading_score"].mean()
average_math_score = school_data_complete_df["math_score"].mean()


# In[9]:


# Step 1. Get the number of students that are in ninth grade at Thomas High School.
# These students have no grades.
ninth_grade_thomas = student_data_df.loc[(student_data_df["grade"]== "9th")
                                         &(student_data_df["school_name"]=="Thomas High School")].count()['Student ID']

# Get the total student count
student_count = school_data_complete_df["Student ID"].count()

# Step 2. Subtract the number of students that are in ninth grade at 
# Thomas High School from the total student count to get the new total student count.
new_count = student_count - ninth_grade_thomas       
print(new_count)


# In[10]:


# Calculate the passing rates using the "clean_student_data".
passing_math_count = school_data_complete_df[(school_data_complete_df["math_score"] >= 70)].count()["student_name"]
passing_reading_count = school_data_complete_df[(school_data_complete_df["reading_score"] >= 70)].count()["student_name"]


# In[11]:


# Step 3. Calculate the passing percentages with the new total student count.
passing_math_percentage = passing_math_count / new_count * 100
passing_reading_percentage =  passing_reading_count / new_count *100


# In[12]:


# Calculate the students who passed both reading and math.
passing_math_reading = school_data_complete_df[(school_data_complete_df["math_score"] >= 70)
                                               & (school_data_complete_df["reading_score"] >= 70)]

# Calculate the number of students that passed both reading and math.
overall_passing_math_reading_count = passing_math_reading["student_name"].count()


# Step 4.Calculate the overall passing percentage with new total student count.
overall_passing_percentage = overall_passing_math_reading_count / new_count *100


# In[13]:


# Create a DataFrame
district_summary_df = pd.DataFrame(
          [{"Total Schools": school_count, 
            "Total Students": new_count, 
            "Total Budget": total_budget,
            "Average Math Score": average_math_score, 
            "Average Reading Score": average_reading_score,
            "% Passing Math": passing_math_percentage,
            "% Passing Reading": passing_reading_percentage,
            "% Overall Passing": overall_passing_percentage}])

# Format the "Total Students" to have the comma for a thousands separator.
district_summary_df["Total Students"] = district_summary_df["Total Students"].map("{:,}".format)

# Format the "Total Budget" to have the comma for a thousands separator, a decimal separator and a "$".
district_summary_df["Total Budget"] = district_summary_df["Total Budget"].map("${:,.2f}".format)

# Format the columns.
district_summary_df["Average Math Score"] = district_summary_df["Average Math Score"].map("{:.1f}".format)
district_summary_df["Average Reading Score"] = district_summary_df["Average Reading Score"].map("{:.1f}".format)
district_summary_df["% Passing Math"] = district_summary_df["% Passing Math"].map("{:.1f}".format)
district_summary_df["% Passing Reading"] = district_summary_df["% Passing Reading"].map("{:.1f}".format)
district_summary_df["% Overall Passing"] = district_summary_df["% Overall Passing"].map("{:.1f}".format)

# Display the data frame
district_summary_df


# In[14]:


# Determine the School Type
per_school_types = school_data_df.set_index(["school_name"])["type"]

# Calculate the total student count.
per_school_counts = school_data_complete_df["school_name"].value_counts()

# Calculate the total school budget and per capita spending
per_school_budget = school_data_complete_df.groupby(["school_name"]).mean()["budget"]

# Calculate the per capita spending.
per_school_capita = per_school_budget / per_school_counts

# Calculate the average test scores.
per_school_math = school_data_complete_df.groupby(["school_name"]).mean()["math_score"]
per_school_reading = school_data_complete_df.groupby(["school_name"]).mean()["reading_score"]

# Calculate the passing scores by creating a filtered DataFrame.
per_school_passing_math = school_data_complete_df[(school_data_complete_df["math_score"] >= 70)]
per_school_passing_reading = school_data_complete_df[(school_data_complete_df["reading_score"] >= 70)]

# Calculate the number of students passing math and passing reading by school.
per_school_passing_math = per_school_passing_math.groupby(["school_name"]).count()["student_name"]
per_school_passing_reading = per_school_passing_reading.groupby(["school_name"]).count()["student_name"]

# Calculate the percentage of passing math and reading scores per school.
per_school_passing_math = per_school_passing_math / per_school_counts * 100
per_school_passing_reading = per_school_passing_reading / per_school_counts * 100

# Calculate the students who passed both reading and math.
per_passing_math_reading = school_data_complete_df[(school_data_complete_df["reading_score"] >= 70)
                                               & (school_data_complete_df["math_score"] >= 70)]

# Calculate the number of students passing math and passing reading by school.
per_passing_math_reading = per_passing_math_reading.groupby(["school_name"]).count()["student_name"]

# Calculate the percentage of passing math and reading scores per school.
per_overall_passing_percentage = per_passing_math_reading / per_school_counts * 100


# In[15]:


# Create the DataFrame
per_school_summary_df = pd.DataFrame({
    "School Type": per_school_types,
    "Total Students": per_school_counts,
    "Total School Budget": per_school_budget,
    "Per Student Budget": per_school_capita,
    "Average Math Score": per_school_math,
    "Average Reading Score": per_school_reading,
    "% Passing Math": per_school_passing_math,
    "% Passing Reading": per_school_passing_reading,
    "% Overall Passing": per_overall_passing_percentage})

# per_school_summary_df.head()


# In[16]:


# Format the Total School Budget and the Per Student Budget
per_school_summary_df["Total School Budget"] = per_school_summary_df["Total School Budget"].map("${:,.2f}".format)
per_school_summary_df["Per Student Budget"] = per_school_summary_df["Per Student Budget"].map("${:,.2f}".format)

# Display the data frame
per_school_summary_df


# In[17]:


# Step 5.  Get the number of 10th-12th graders from Thomas High School (THS).
tenth_graders = school_data_complete_df.loc[(school_data_complete_df["grade"]== "10th")&(school_data_complete_df["school_name"]=="Thomas High School")].count()['Student ID']
eleventh_graders = school_data_complete_df.loc[(school_data_complete_df["grade"]== "11th")&(school_data_complete_df["school_name"]=="Thomas High School")].count()['Student ID']
twelfth_graders = school_data_complete_df.loc[(school_data_complete_df["grade"]== "12th")&(school_data_complete_df["school_name"]=="Thomas High School")].count()['Student ID']

total_students = tenth_graders + eleventh_graders + twelfth_graders
total_students


# In[18]:


# Step 6. Get all the students passing math from THS
passing_math = school_data_complete_df.loc[(school_data_complete_df["school_name"]=="Thomas High School") & (school_data_complete_df["math_score"] >= 70)].count()["Student ID"]
passing_math


# In[19]:


# Step 7. Get all the students passing reading from THS
passing_reading = school_data_complete_df.loc[(school_data_complete_df["school_name"]=="Thomas High School")&(school_data_complete_df["reading_score"] >= 70)].count()["Student ID"]
passing_reading


# In[20]:


# Step 8. Get all the students passing math and reading from THS
THS_students_passing_math_and_reading = school_data_complete_df.loc[(school_data_complete_df["math_score"] >= 70)&(school_data_complete_df["reading_score"] >= 70)&(school_data_complete_df["school_name"]=="Thomas High School")]
THS_students_passing_math_and_reading


# In[21]:


THS_students_passing_math_and_reading.count()


# In[22]:


# Step 9. Calculate the percentage of 10th-12th grade students passing math from Thomas High School.
THS_passing_math_10th_11th_12th = school_data_complete_df.loc[(school_data_complete_df["grade"]!= "9th")
                                                              &(school_data_complete_df["school_name"]=="Thomas High School") 
                                                              & (school_data_complete_df["math_score"] >= 70)].count()["Student ID"]
THS_passing_math_10th_11th_12th_percentage = THS_passing_math_10th_11th_12th / total_students *100
THS_passing_math_10th_11th_12th_percentage


# In[23]:


# Step 10. Calculate the percentage of 10th-12th grade students passing reading from Thomas High School.
THS_passing_reading_10th_11th_12th = school_data_complete_df.loc[(school_data_complete_df["grade"]!= "9th")
                                                                 &(school_data_complete_df["school_name"]=="Thomas High School") 
                                                                 & (school_data_complete_df["reading_score"] >= 70)].count()["Student ID"]
THS_passing_reading_10th_11th_12th_percentage = THS_passing_reading_10th_11th_12th / total_students *100
THS_passing_reading_10th_11th_12th_percentage


# In[24]:


# Step 11. Calculate the overall passing percentage of 10th-12th grade from Thomas High School.
total_grades = THS_students_passing_math_and_reading["student_name"].count()

overall_passing_percentage =  total_grades / total_students *100
overall_passing_percentage


# In[25]:


# Step 12. Replace the passing math percent for Thomas High School in the per_school_summary_df.
per_school_summary_df.loc[["Thomas High School"],['% Passing Math']]= THS_passing_math_10th_11th_12th_percentage


# In[26]:


# Step 13. Replace the passing reading percentage for Thomas High School in the per_school_summary_df.
per_school_summary_df.loc[["Thomas High School"],['% Passing Reading']]= THS_passing_reading_10th_11th_12th_percentage


# In[27]:


# Step 14. Replace the overall passing percentage for Thomas High School in the per_school_summary_df.
per_school_summary_df.loc[["Thomas High School"],['% Overall Passing']]= overall_passing_percentage


# In[28]:


# per_school_summary_df
per_school_summary_df


# In[29]:


# Sort and show top five schools.
per_school_summary_df.sort_values(["% Overall Passing"], ascending=False).head(5)


# In[30]:


# Sort and show bottom five schools.
per_school_summary_df.sort_values(["% Overall Passing"], ascending=True).head(5)


# In[31]:


# Create a Series of scores by grade levels using conditionals.
scores_ninth_graders = school_data_complete_df[(school_data_complete_df["grade"] == "9th")]

scores_tenth_graders = school_data_complete_df[(school_data_complete_df["grade"] == "10th")]

scores_eleventh_graders = school_data_complete_df[(school_data_complete_df["grade"] == "11th")]

scores_twelfth_graders = school_data_complete_df[(school_data_complete_df["grade"] == "12th")]

# Group each school Series by the school name for the average math score.
ninth_grade_math_scores = scores_ninth_graders.groupby(["school_name"]).mean()["math_score"]

tenth_grade_math_scores = scores_tenth_graders.groupby(["school_name"]).mean()["math_score"]

eleventh_grade_math_scores = scores_eleventh_graders.groupby(["school_name"]).mean()["math_score"]

twelfth_grade_math_scores = scores_twelfth_graders.groupby(["school_name"]).mean()["math_score"]

# Group each school Series by the school name for the average reading score.
ninth_grade_reading_scores = scores_ninth_graders.groupby(["school_name"]).mean()["reading_score"]

tenth_grade_reading_scores = scores_tenth_graders.groupby(["school_name"]).mean()["reading_score"]

eleventh_grade_reading_scores = scores_eleventh_graders.groupby(["school_name"]).mean()["reading_score"]

twelfth_grade_reading_scores = scores_twelfth_graders.groupby(["school_name"]).mean()["reading_score"]


# In[32]:


# Combine each Series for average math scores by school into single data frame.
math_scores_by_grade = pd.DataFrame({
               "9th": ninth_grade_math_scores,
               "10th": tenth_grade_math_scores,
               "11th": eleventh_grade_math_scores,
               "12th": twelfth_grade_math_scores})
math_scores_by_grade


# In[33]:


# Combine each Series for average reading scores by school into single data frame.
reading_scores_by_grade = pd.DataFrame({
               "9th": ninth_grade_reading_scores,
               "10th": tenth_grade_reading_scores,
               "11th": eleventh_grade_reading_scores,
               "12th": twelfth_grade_reading_scores})
reading_scores_by_grade


# In[34]:


# Format each grade column.
math_scores_by_grade["9th"] = math_scores_by_grade["9th"].map("{:.1f}".format)

math_scores_by_grade["10th"] = math_scores_by_grade["10th"].map("{:.1f}".format)

math_scores_by_grade["11th"] = math_scores_by_grade["11th"].map("{:.1f}".format)

math_scores_by_grade["12th"] = math_scores_by_grade["12th"].map("{:.1f}".format)


# In[35]:


# Remove the index.
math_scores_by_grade.index.name = None

# Display the data frame
math_scores_by_grade.head()


# In[36]:


# Remove the index.
reading_scores_by_grade.index.name = None

# Display the data frame
reading_scores_by_grade.head()


# In[37]:


# Establish the spending bins and group names.
spending_bins = [0, 585, 630, 645, 675]

# Categorize spending based on the bins.
group_names = ["<$584", "$585-629", "$630-644", "$645-675"]

per_school_summary_df["Spending Ranges (Per Student)"] = pd.cut(per_school_capita, spending_bins, labels=group_names)

per_school_summary_df.head()


# In[38]:


# Calculate averages for the desired columns.
spending_math_scores = per_school_summary_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]

spending_reading_scores = per_school_summary_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]

spending_passing_math = per_school_summary_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]

spending_passing_reading = per_school_summary_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]

overall_passing_spending = per_school_summary_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[39]:


# Create the DataFrame
spending_summary_df = pd.DataFrame({
          "Average Math Score" : spending_math_scores,
          "Average Reading Score": spending_reading_scores,
          "% Passing Math": spending_passing_math,
          "% Passing Reading": spending_passing_reading,
          "% Overall Passing": overall_passing_spending})

spending_summary_df


# In[40]:


# Format the DataFrame
spending_summary_df["Average Math Score"] = spending_summary_df["Average Math Score"].map("{:.1f}".format)

spending_summary_df["Average Reading Score"] = spending_summary_df["Average Reading Score"].map("{:.1f}".format)

spending_summary_df["% Passing Math"] = spending_summary_df["% Passing Math"].map("{:.0f}".format)

spending_summary_df["% Passing Reading"] = spending_summary_df["% Passing Reading"].map("{:.0f}".format)

spending_summary_df["% Overall Passing"] = spending_summary_df["% Overall Passing"].map("{:.0f}".format)

spending_summary_df


# In[41]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]

# Categorize spending based on the bins.
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
per_school_summary_df["School Size"] = pd.cut(per_school_summary_df["Total Students"], size_bins, labels=group_names)


# In[42]:


# Calculate averages for the desired columns.
size_math_scores = per_school_summary_df.groupby(["School Size"]).mean()["Average Math Score"]

size_reading_scores = per_school_summary_df.groupby(["School Size"]).mean()["Average Reading Score"]

size_passing_math = per_school_summary_df.groupby(["School Size"]).mean()["% Passing Math"]

size_passing_reading = per_school_summary_df.groupby(["School Size"]).mean()["% Passing Reading"]

size_overall_passing = per_school_summary_df.groupby(["School Size"]).mean()["% Overall Passing"]


# In[43]:


# Assemble into DataFrame.
size_summary_df = pd.DataFrame({
          "Average Math Score" : size_math_scores,
          "Average Reading Score": size_reading_scores,
          "% Passing Math": size_passing_math,
          "% Passing Reading": size_passing_reading,
          "% Overall Passing": size_overall_passing})


# In[44]:


# Format the DataFrame
size_summary_df["Average Math Score"] = size_summary_df["Average Math Score"].map("{:.1f}".format)

size_summary_df["Average Reading Score"] = size_summary_df["Average Reading Score"].map("{:.1f}".format)

size_summary_df["% Passing Math"] = size_summary_df["% Passing Math"].map("{:.0f}".format)

size_summary_df["% Passing Reading"] = size_summary_df["% Passing Reading"].map("{:.0f}".format)

size_summary_df["% Overall Passing"] = size_summary_df["% Overall Passing"].map("{:.0f}".format)

size_summary_df


# In[45]:


# Calculate averages for the desired columns. 
type_math_scores = per_school_summary_df.groupby(["School Type"]).mean()["Average Math Score"]

type_reading_scores = per_school_summary_df.groupby(["School Type"]).mean()["Average Reading Score"]

type_passing_math = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Math"]

type_passing_reading = per_school_summary_df.groupby(["School Type"]).mean()["% Passing Reading"]

type_overall_passing = per_school_summary_df.groupby(["School Type"]).mean()["% Overall Passing"]


# In[46]:


# Assemble into DataFrame.
type_summary_df = pd.DataFrame({
          "Average Math Score" : type_math_scores,
          "Average Reading Score": type_reading_scores,
          "% Passing Math": type_passing_math,
          "% Passing Reading": type_passing_reading,
          "% Overall Passing": type_overall_passing})

type_summary_df


# In[47]:


# Format the DataFrame
type_summary_df["Average Math Score"] = type_summary_df["Average Math Score"].map("{:.1f}".format)

type_summary_df["Average Reading Score"] = type_summary_df["Average Reading Score"].map("{:.1f}".format)

type_summary_df["% Passing Math"] = type_summary_df["% Passing Math"].map("{:.0f}".format)

type_summary_df["% Passing Reading"] = type_summary_df["% Passing Reading"].map("{:.0f}".format)

type_summary_df["% Overall Passing"] = type_summary_df["% Overall Passing"].map("{:.0f}".format)

type_summary_df


# In[ ]:




