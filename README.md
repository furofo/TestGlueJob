# AWS Glue PySpark Sample Script

This repository contains a simple AWS Glue PySpark script that demonstrates reading parquet files and performing basic ETL operations using AWS Glue Docker containers. Mock data and parquet files no rela data or s3 bucket used ye

## Files

- `sample.py` - Main AWS Glue PySpark script
- `create_sample_data.py` - Helper script to create sample parquet data
- `data/employees.parquet` - Sample parquet file with employee data
- `requirements.txt` - Python dependencies for data creation
- `.vscode/launch.json` - VS Code debug configuration

## Sample Data

The script works with a sample employee dataset containing:
- employee_id
- name
- department
- salary
- hire_date

## Features Demonstrated

1. **Reading Parquet Files**: Uses Spark to read parquet data
2. **Data Transformations**: Adds salary grade categorization
3. **Aggregations**: Calculates department-wise statistics
4. **Glue DynamicFrames**: Converts Spark DataFrame to Glue DynamicFrame
5. **Logging**: Comprehensive logging throughout the process

## Setting up AWS Glue Docker Container with Visual Studio Code

### Prerequisites

1. **Install Visual Studio Code**: Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. **Install Python**: Ensure Python 3.11+ is installed
3. **Install Docker**: Download from [https://www.docker.com/](https://www.docker.com/)
4. **Install VS Code Extensions**:
   - Python
   - Python Debugger
   - Remote - Containers (Dev Containers)

### Step 1: Pull the AWS Glue Docker Image

```bash
# Pull the latest AWS Glue 5.0 Docker image
docker pull public.ecr.aws/glue/aws-glue-libs:5
```

### Step 2: Run the Docker Container

```bash

# Optional: Set AWS profile if you have AWS credentials
export PROFILE_NAME=default

# Run the container with workspace mounted current working directory
docker run -it --rm \
    -v ~/.aws:/home/hadoop/.aws \
    -v $(pwd):/home/hadoop/workspace/ \
    -e AWS_PROFILE=$PROFILE_NAME \
    --name glue5_pyspark \
    public.ecr.aws/glue/aws-glue-libs:5 \
    pyspark
```

### Step 3: Attach VS Code to the Running Container

1. **Start Visual Studio Code**
2. **Open Remote Explorer**:
   - Click on the Remote Explorer icon in the left sidebar
   - Or press `Ctrl+Shift+P` and type "Remote Explorer"

3. **Find and Attach to Container**:
   - Look for `glue5_pyspark` in the Containers section
   - Right-click on the container
   - Select **"Attach in Current Window"**

4. **Handle Security Warning**:
   - If a dialog appears warning about "Attaching to a container may execute arbitrary code"
   - Choose **"Got it"** to proceed

### Step 4: Open the Workspace in the Container

1. **Open Folder**: Click "Open Folder" or press `Ctrl+K Ctrl+O`
2. **Navigate to**: `/home/hadoop/workspace/`
3. **Select the workspace folder**

### Step 5: Configure VS Code for AWS Glue Development

1. **Open Workspace Settings**:
   - Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
   - Type: `Preferences: Open Workspace Settings (JSON)`
   - Press Enter

2. **Add Configuration**: Paste the following JSON and save:

```json
{
    "python.defaultInterpreterPath": "/usr/bin/python3.11",
    "python.analysis.extraPaths": [
        "/usr/lib/spark/python/lib/py4j-0.10.9.7-src.zip:/usr/lib/spark/python/:/usr/lib/spark/python/lib/"
    ]
}
```

### Step 6: Run the AWS Glue Script with Debugger

1. **Open the Run and Debug View**:
   - Click on the Run and Debug icon in the left sidebar
   - Or press `Ctrl+Shift+D`

2. **Select Configuration**:
   - Choose "Run Glue Script" from the dropdown menu

3. **Start Debugging**:
   - Click the green play button or press `F5`
   - The script will run with full debugging capabilities

## Running the Script

### Alternative Methods:

#### Method 1: Direct Terminal Execution in Container
```bash
# Inside the container terminal
cd /home/hadoop/workspace
python3 sample.py --JOB_NAME my-test-job
```

#### Method 2: Using spark-submit (Recommended)
```bash
# Inside the container terminal
cd /home/hadoop/workspace
spark-submit sample.py --JOB_NAME my-test-job
```

#### Method 3: Make Script Executable
```bash
# Make executable
chmod +x sample.py

# Run directly
./sample.py --JOB_NAME my-test-job
```

## Troubleshooting

### Common Issues:

1. **Container Not Found in Remote Explorer**:
   - Ensure the container is running: `docker ps`
   - Restart the container if needed

2. **Python Path Issues**:
   - Verify the workspace settings JSON is correctly configured
   - Check that `/usr/bin/python3.11` exists in the container

3. **Permission Issues**:
   - Ensure the workspace directory has proper permissions
   - Use `sudo` if necessary when mounting volumes

4. **AWS Glue Libraries Not Found**:
   - Verify you're using the correct Docker image: `public.ecr.aws/glue/aws-glue-libs:5`
   - Check that the container has all required libraries

### Debugging Tips:

- **Set Breakpoints**: Click on line numbers in VS Code to set breakpoints
- **Inspect Variables**: Use the Variables panel in the Debug view
- **Step Through Code**: Use F10 (step over) and F11 (step into)
- **Debug Console**: Use the Debug Console for interactive Python commands

## Key Differences: AWS Glue 4.0 vs 5.0 Docker Image

- **Single Container Image**: AWS Glue 5.0 provides one container for both batch and streaming jobs
- **Updated Dependencies**: Latest versions of Spark, Python, and AWS libraries
- **Improved Performance**: Better memory management and execution optimization
- **Enhanced Debugging**: Better integration with development tools

## Expected Output

When you run the script successfully, you'll see console output showing:
- Dataset information (row count, schema)
- Sample data preview
- Department-wise statistics (employee count, avg/max/min salary by department)
- Salary grade distribution
- DynamicFrame information
- Job completion confirmation

## Next Steps

To extend this script for production use:
- **Connect to S3**: Replace local file paths with S3 URLs
- **Add Data Quality Checks**: Implement validation and error handling
- **Implement Complex Transformations**: Add joins, aggregations, and data cleansing
- **Add Error Handling**: Comprehensive exception handling and logging
- **Integrate with AWS Glue Catalog**: Use Glue Data Catalog for schema management
- **Deploy to AWS Glue**: Upload script to AWS Glue Studio for production execution
