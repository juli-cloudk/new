# added on bucket name
#Create s3 bucket
import boto3

bucket_name = "jck2011-s3bucket" 
region_name = 'us-east-1' 

# --- 2. Getting Ready ---
s3 = boto3.client('s3', region_name=region_name)

# --- 3. Making the Bucket ---
try:
    print(f"Trying to create bucket: {bucket_name}")
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': region_name
        }
    )
    print(f"🎉 Success! The bucket '{bucket_name}' is ready!")

except Exception as e:
    # If the name wasn't unique, or you made a mistake, the 'except' part handles the error.
    print(f"❌ Could not create bucket. Error: {e}")
