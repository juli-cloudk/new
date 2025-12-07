import boto3
import json

# AWS Settings
REGION = 'us-east-1'  # Where we want to create things
AMI_ID = 'ami-053b0d53c27927909'  # The type of server we want (like a template)
INSTANCE_TYPE = 't2.micro'  # This is a small server
KEY_PAIR_NAME = 'my-provisioning-key'  # Name of our key for access
SECURITY_GROUP_NAME = 'provioning_Server_SG'  # Name for our security group
S3_BUCKET_NAME = 'my-provisioning-bucket-2024'  # Unique name for our bucket

# Create the AWS clients
ec2_client = boto3.client('ec2', region_name=REGION)
s3_client = boto3.client('s3', region_name=REGION)

def create_s3_bucket(bucket_name):
    """Create a storage space (bucket) on S3."""
    try:
        s3_client.create_bucket(Bucket=bucket_name,
                                 CreateBucketConfiguration={'LocationConstraint': REGION})
        print(f"Created S3 bucket: {bucket_name}")
    except Exception as e:
        print(f"Couldn't create the bucket: {e}")

def create_security_group():
    """Make a group that controls access to our server."""
    try:
        vpc = ec2_client.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
        vpc_id = vpc['Vpcs'][0]['VpcId']  # Get the ID of the default network

        sg_response = ec2_client.create_security_group(
            GroupName=PROVISIONING_SECURITY_GROUP
            Description='Allow SSH and HTTP access',
            VpcId=vpc_id
        )
        security_group_id = sg_response['GroupId']
        print(f"Created Security Group ID: {security_group_id}")

        # Allow access for SSH and HTTP
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},  # SSH
                {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}   # HTTP
            ]
        )
        return security_group_id
    except Exception as e:
        print(f"Couldn't create Security Group: {e}")

def launch_ec2_instance(security_group_id):
    """Launch a virtual server on AWS."""
    try:
        instance = ec2_client.run_instances(
            ImageId=AMI_ID,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_PAIR_NAME,
            SecurityGroupIds=[security_group_id]
        )
        instance_id = instance['Instances'][0]['InstanceId']
        print(f"Launched EC2 Instance ID: {instance_id}")

        # Wait for the server to start up and get its public IP
        waiter = ec2_client.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        public_ip = ec2_client.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0].get('PublicIpAddress')
        print(f"Instance is running. Public IP: {public_ip}")
        return instance_id
    except Exception as e:
        print(f"Couldn't launch EC2 instance: {e}")


if __name__ == "__main__":
    create_s3_bucket(S3_BUCKET_NAME)  # Create the S3 bucket
    sg_id = create_security_group()  # Make the security group
    if sg_id:
        instance_id = launch_ec2_instance(sg_id)  # Start the server
        if instance_id:
            print("✅ Provisioning Complete!")
            print(f"EC2 Instance ID: {instance_id}")
            print(f"S3 Bucket: s3://{S3_BUCKET_NAME}")
    else:
        print("❌ Provisioning failed.")
