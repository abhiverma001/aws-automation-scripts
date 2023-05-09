import boto3
import csv

# Create a Boto3 client for API GatewayV2
client = boto3.client('apigatewayv2')

# Retrieve all VPC-links
response = client.get_vpc_links()
print(response)

# Create a list to store the VPC-link details
vpc_links = []

# Iterate over the VPC-links and retrieve their tags
for vpc_link in response['Items']:
    print(vpc_link)
    # Retrieve the tags for the VPC-link
    tags = client.get_tags(ResourceArn=vpc_link['VpcLinkId'])['Tags']

    # Add the VPC-link details to the list
    vpc_link_details = {
        'Name': vpc_link['Name'],
        'VpcLinkId': vpc_link['VpcLinkId'],
        'VpcLinkStatus': vpc_link['VpcLinkStatus'],
    }
    # Add each tag key as a separate column
    for tag in tags:
        vpc_link_details[tag['Key']] = tag['Value']
    
    vpc_links.append(vpc_link_details)

# Write the VPC-link details to a CSV file
with open('vpc_links.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write header row with column names
    header_row = ['Name', 'VpcLinkId', 'VpcLinkStatus']
    # Add each tag key as a separate column
    tag_keys = set([tag['Key'] for vpc_link in vpc_links for tag in vpc_link.get('Tags', [])])
    for tag_key in tag_keys:
        header_row.append(tag_key)
    writer.writerow(header_row)

    # Write data rows with VPC-link details
    for vpc_link in vpc_links:
        # Combine tags into a single string
        row = [
            vpc_link['Name'],
            vpc_link['VpcLinkId'],
            vpc_link['VpcLinkStatus'],
        ]
        # Add tag values as separate columns
        for tag_key in tag_keys:
            row.append(vpc_link.get(tag_key, ''))
        writer.writerow(row)
