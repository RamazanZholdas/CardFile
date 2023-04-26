import boto3

iam = boto3.client('iam')
group_users = {}
paginator = iam.get_paginator('list_groups')
for page in paginator.paginate():
    for group in page['Groups']:
        group_name = group['GroupName']
        users = iam.get_group(GroupName=group_name)['Users']
        group_users[group_name] = len(users)

sorted_groups = dict(sorted(group_users.items(), key=lambda item: item[1]))

for group_name, user_count in sorted_groups.items():
    print(f'Group: {group_name}, Users: {user_count}')