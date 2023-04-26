import boto3

iam = boto3.client('iam')
is_truncated = True
marker = None
admin_users = []

while is_truncated:
    if marker:
        response = iam.list_users(Marker=marker)
    else:
        response = iam.list_users()

    is_truncated = response['IsTruncated']
    if is_truncated:
        marker = response['Marker']

    for user in response['Users']:
        user_name = user['UserName']

        inline_policies = iam.list_user_policies(UserName=user_name)

        for policy_name in inline_policies['PolicyNames']:
            policy_document = iam.get_user_policy(UserName=user_name, PolicyName=policy_name)
            if 'AdministratorAccess' in policy_document['PolicyDocument']['Statement'][0]['Action']:
                admin_users.append(user_name)
                break

print("Users with AdministratorAccess:")
for user_name in admin_users:
    print(user_name)