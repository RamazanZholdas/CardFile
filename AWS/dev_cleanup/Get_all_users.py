import boto3

iam = boto3.client('iam')
counter = 0

paginator = iam.get_paginator('list_users')
for page in paginator.paginate():
    for user in page['Users']:
        counter += 1
        print(user['UserName'])

print(counter)