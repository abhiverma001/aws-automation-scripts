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
