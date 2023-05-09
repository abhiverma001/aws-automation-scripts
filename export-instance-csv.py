import boto3
import csv

# Create an EC2 client
ec2 = boto3.client('ec2')

# Retrieve all running instances
instances = ec2.describe_instances(Filters=[
    {
        'Name': 'instance-state-name',
        'Values': ['running', 'stopped']
    }
])['Reservations']

# Create a CSV file and write the headers
with open('instance_details.csv', 'w', newline='') as csvfile:
    fieldnames = ['InstanceId', 'InstanceName', 'InstanceType', 'InstanceState', 'Region']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Write each instance's details to the CSV file
    for instance in instances:
        instance_data = instance['Instances'][0]
        instance_id = instance_data['InstanceId']
        instance_type = instance_data['InstanceType']
        instance_state = instance_data['State']['Name']
        region = ec2.meta.region_name
        instance_name = [tag['Value'] for tag in instance_data['Tags'] if tag['Key'] == 'Name']
        instance_name = instance_name[0] if instance_name else ''

        # Write the instance's details to the CSV file
        writer.writerow({
            'InstanceId': instance_id,
            'InstanceName': instance_name,
            'InstanceType': instance_type,
            'InstanceState': instance_state,
            'Region': region
        })

print('Instance details exported to instance_details.csv')
