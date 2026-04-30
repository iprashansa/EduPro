import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def load_and_merge_data(filepath="EduPro_Data.xlsx"):
    # Load sheets
    df_teachers = pd.read_excel(filepath, sheet_name="Teachers")
    df_courses = pd.read_excel(filepath, sheet_name="Courses")
    df_transactions = pd.read_excel(filepath, sheet_name="Transactions")
    
    # Merge datasets
    # Transactions maps TeacherID and CourseID
    df_merged = pd.merge(df_transactions, df_teachers, on="TeacherID", how="inner")
    df_merged = pd.merge(df_merged, df_courses, on="CourseID", how="inner")
    
    return df_merged, df_teachers, df_courses, df_transactions

def calculate_kpis(df_merged, df_teachers, df_courses):
    # 1. Average Teacher Rating
    avg_teacher_rating = df_teachers["TeacherRating"].mean()
    
    # 2. Average Course Rating
    avg_course_rating = df_courses["CourseRating"].mean()
    
    # 3. Rating Consistency Index 
    # Can be defined as 1 / (std dev of teacher ratings + 1) or just standard deviation
    rating_std = df_teachers["TeacherRating"].std()
    
    # 4. Experience Impact Score
    # Correlation between YearsOfExperience and TeacherRating
    experience_impact = df_teachers["YearsOfExperience"].corr(df_teachers["TeacherRating"])
    
    # 5. Enrollment Influence Ratio
    # Average enrollments (transactions) per teacher
    enrollment_influence = len(df_merged) / len(df_teachers) 
    
    kpis = {
        "Average Teacher Rating": round(avg_teacher_rating, 2),
        "Average Course Rating": round(avg_course_rating, 2),
        "Rating Std Dev (Consistency)": round(rating_std, 2),
        "Experience Impact (Corr)": round(experience_impact, 2),
        "Avg Enrollments per Teacher": round(enrollment_influence, 2)
    }
    return kpis

def generate_teacher_stats(df_merged, df_teachers):
    # Group by TeacherID to get their distinct metrics
    stats = df_merged.groupby("TeacherID").agg(
        Total_Enrollments=("TransactionID", "count"),
        Avg_Course_Rating=("CourseRating", "mean")
    ).reset_index()
    
    teacher_stats = pd.merge(df_teachers, stats, on="TeacherID", how="left")
    teacher_stats["Total_Enrollments"] = teacher_stats["Total_Enrollments"].fillna(0)
    teacher_stats["Avg_Course_Rating"] = teacher_stats["Avg_Course_Rating"].fillna(0)
    
    return teacher_stats

def train_course_rating_model(df_merged):
    # Prepare data for ML model
    df = df_merged.dropna(subset=['CourseCategory', 'CourseLevel', 'TeacherRating', 'YearsOfExperience', 'CourseRating']).copy()
    
    # Encode categorical features
    le_cat = LabelEncoder()
    le_level = LabelEncoder()
    
    df['Cat_Enc'] = le_cat.fit_transform(df['CourseCategory'])
    df['Level_Enc'] = le_level.fit_transform(df['CourseLevel'])
    
    # Features (X) and Target (y)
    X = df[['Cat_Enc', 'Level_Enc', 'TeacherRating', 'YearsOfExperience']]
    y = df['CourseRating']
    
    # Train Random Forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, le_cat, le_level

