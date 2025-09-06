#!/usr/bin/env python3
"""
Script to create sample parquet file for testing AWS Glue PySpark script
"""

import pandas as pd
import os

# Create sample data
sample_data = {
    'employee_id': [1, 2, 3, 4, 5],
    'name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson'],
    'department': ['Engineering', 'Marketing', 'Sales', 'Engineering', 'HR'],
    'salary': [75000, 65000, 55000, 80000, 60000],
    'hire_date': ['2020-01-15', '2019-03-20', '2021-07-10', '2018-11-05', '2022-02-28']
}

# Create DataFrame
df = pd.DataFrame(sample_data)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Save as parquet file
df.to_parquet('data/employees.parquet', index=False)

print("Sample parquet file created at: data/employees.parquet")
print("Sample data preview:")
print(df)
