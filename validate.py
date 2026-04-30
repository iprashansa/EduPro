from data_processing import load_and_merge_data, calculate_kpis, generate_teacher_stats
import pandas as pd

def validate_data():
    print("Loading data...")
    df_merged, df_teachers, df_courses, df_transactions = load_and_merge_data("EduPro_Data.xlsx")
    
    print(f"Loaded {len(df_merged)} merged records.")
    print("Calculating KPIs...")
    kpis = calculate_kpis(df_merged, df_teachers, df_courses)
    for k, v in kpis.items():
        print(f"  {k}: {v}")
        
    print("Generating Teacher Stats...")
    stats = generate_teacher_stats(df_merged, df_teachers)
    print(f"Generated stats for {len(stats)} teachers.")
    
    print("All validations completed successfully!")

if __name__ == "__main__":
    validate_data()
