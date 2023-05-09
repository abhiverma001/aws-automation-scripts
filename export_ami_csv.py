import boto3
import csv

session = boto3.Session()
region = session.region_name
client = boto3.client('ec2')

# Retrieve all available AMIs
response = client.describe_images(Owners=['self'])

# Extract the relevant details and write to CSV
with open('ami_details.csv', mode='w', newline='') as csv_file:
    fieldnames = ['ImageId', 'Name', 'CreationDate', 'OwnerId', 'State', 'Region']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for image in response['Images']:
        writer.writerow({'ImageId': image['ImageId'], 
                         'Name': image['Name'], 
                         'CreationDate': image['CreationDate'], 
                         'OwnerId': image['OwnerId'],
                         'Region' : region, 
                         'State': image['State']})
