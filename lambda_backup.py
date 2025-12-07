import boto3  # Import AWS SDK for Python
import json  # For handling JSON data
from datetime import datetime  # For getting the current date and time
import uuid  # For generating unique IDs

# config
BACKUP_BUCKET_NAME = 'my-Privisioning-bucket-2024'  
REGION_NAME = 'us-east-1'  # AWS region

# Create an S3 client
s3 = boto3.client('s3', region_name=REGION_NAME)

def simulate_database_dump():
    """Simulates making a backup of a database."""
    # Create data that represents the backup
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "database_name": "my_database",
        "record_count": 500000,
        "unique_backup_id": str(uuid.uuid4()),  # Generate a unique ID 
        "status": "Simulated successful dump."
    }
    # Convert the data into a JSON string
    return json.dumps(backup_data, indent=4)

def lambda_handler(event, context):
    "Main function that runs the backup process."
    try:
        print(f"--- Starting backup at {datetime.now().isoformat()} ---")

        # 1. Simulate getting the database dump
        db_dump_content = simulate_database_dump()
        file_size_bytes = len(db_dump_content.encode('utf-8'))  # Get the size of the backup data

        # 2. Create a unique file name based on the current date and time
        date_str = datetime.now().strftime("%Y/%m/%d")
        s3_key = f"{date_str}/db_backup_{datetime.now().strftime('%H%M%S')}.json"

        # 3. Upload the backup to S3
        s3.put_object(
            Bucket=BACKUP_BUCKET_NAME,
            Key=s3_key,
            Body=db_dump_content,
            ContentType='application/json'
        )

        print(f"✅ Backup successful!")
        print(f"   Bucket: {BACKUP_BUCKET_NAME}")
        print(f"   File: {s3_key}")
        print(f"   Size: {file_size_bytes} bytes")

        return {
            'statusCode': 200,
            'body': json.dumps('Backup completed successfully.')
        }

    except Exception as e:
        print(f"❌ Backup failed! Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Backup failed with error: {str(e)}')
        }
