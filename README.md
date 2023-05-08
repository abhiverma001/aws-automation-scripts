# AWS-Automation-Scripts

## Install & Confugure Python Boto3
- Below command is used to install the awscli boto3
```
pip install awscli boto3
```

## Export AWS Auto Scaling Groups Name and Tags in a CSV file.
- We can achive this by below python boto3 script
- Recommended to user AWS CloudShell for this kind of work
- Create a file [export_asg_tags_csv.py](https://github.com/abhiverma001/aws-automation-scripts/blob/main/export_asg_tags_csv.py) and write the below script in this file.
```
import boto3
import csv

# Create an Auto Scaling client
autoscaling = boto3.client('autoscaling')

# Retrieve a list of Auto Scaling groups
paginator = autoscaling.get_paginator('describe_auto_scaling_groups')
groups = []
for response in paginator.paginate():
    groups += response['AutoScalingGroups']

# Write the Auto Scaling group names and tags to a CSV file
with open('autoscaling_groups.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row with column names
    header_row = ['Name']
    tag_keys = set()
    for group in groups:
        for tag in group['Tags']:
            tag_keys.add(tag['Key'])
    header_row += sorted(tag_keys)
    writer.writerow(header_row)

    # Write data rows with Auto Scaling group names and tag values
    for group in groups:
        row = [group['AutoScalingGroupName']]
        for tag_key in sorted(tag_keys):
            tag_value = next((tag['Value'] for tag in group['Tags'] if tag['Key'] == tag_key), '')
            row.append(tag_value)
        writer.writerow(row)
```
- To execute this script run below command in you cloudshell
```
python3 script_file_name.py
```
- A CSV file will be created in the same directory.


## Export AWS AMI Details in a CSV file.
- We can achive this by below python boto3 script
- This script retrieves all the AMIs that are owned by your AWS account (specified by Owners=['self'] in the describe_images() method), and then writes the relevant details to a CSV file named ami_details.csv. You can modify the fieldnames list to include additional details about the AMIs if needed.
```
import boto3
import csv

client = boto3.client('ec2')

# Retrieve all available AMIs
response = client.describe_images(Owners=['self'])

# Extract the relevant details and write to CSV
with open('ami_details.csv', mode='w', newline='') as csv_file:
    fieldnames = ['ImageId', 'Name', 'CreationDate', 'OwnerId', 'State']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for image in response['Images']:
        writer.writerow({'ImageId': image['ImageId'], 
                         'Name': image['Name'], 
                         'CreationDate': image['CreationDate'], 
                         'OwnerId': image['OwnerId'], 
                         'State': image['State']})

```
- A csv file will be created named 'ami_details.csv'.


