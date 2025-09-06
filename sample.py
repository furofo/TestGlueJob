#!/usr/bin/env python3
"""
AWS Glue PySpark Script - Sample ETL Job
This script demonstrates reading parquet files and basic data processing using AWS Glue libraries
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Get job arguments (if any)
    args = getResolvedOptions(sys.argv, ['JOB_NAME'])
    
    # Initialize Spark and Glue contexts
    sc = SparkContext()
    glueContext = GlueContext(sc)
    spark = glueContext.spark_session
    
    # Initialize the job
    job = Job(glueContext)
    job.init(args['JOB_NAME'], args)
    
    logger.info("Starting AWS Glue PySpark ETL Job")
    logger.info(f"Job Name: {args['JOB_NAME']}")
    
    try:
        # Path to the sample parquet file
        input_path = "data/employees.parquet"
        
        logger.info(f"Reading parquet file from: {input_path}")
        
        # Read parquet file using Spark
        df = spark.read.parquet(input_path)
        
        # Log basic information about the dataset
        logger.info(f"Total records read: {df.count()}")
        logger.info(f"Schema:")
        df.printSchema()
        
        # Show sample data
        logger.info("Sample data (first 10 rows):")
        df.show(10)
        
        # Perform some basic transformations
        logger.info("Performing data transformations...")
        
        # Add a new column for salary grade
        df_transformed = df.withColumn(
            "salary_grade",
            when(col("salary") >= 70000, "High")
            .when(col("salary") >= 60000, "Medium")
            .otherwise("Low")
        )
        
        # Group by department and calculate statistics
        dept_stats = df_transformed.groupBy("department") \
            .agg(
                count("employee_id").alias("employee_count"),
                avg("salary").alias("avg_salary"),
                max("salary").alias("max_salary"),
                min("salary").alias("min_salary")
            ).orderBy("department")
        
        logger.info("Department Statistics:")
        dept_stats.show()
        
        # Show salary grade distribution
        salary_grade_dist = df_transformed.groupBy("salary_grade") \
            .agg(count("employee_id").alias("count")) \
            .orderBy("salary_grade")
        
        logger.info("Salary Grade Distribution:")
        salary_grade_dist.show()
        
        # Convert to Glue DynamicFrame for demonstration
        logger.info("Converting to Glue DynamicFrame...")
        dynamic_frame = glueContext.create_dynamic_frame.from_rdd(
            df_transformed.rdd, 
            "transformed_employees"
        )
        
        logger.info(f"DynamicFrame record count: {dynamic_frame.count()}")
        logger.info("DynamicFrame schema:")
        dynamic_frame.printSchema()
        
        # You could write the results to another location here
        # For now, we'll just log the completion
        logger.info("ETL job completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in ETL job: {str(e)}")
        raise e
    
    finally:
        # Commit the job
        job.commit()
        logger.info("Job committed successfully")

if __name__ == "__main__":
    main()
