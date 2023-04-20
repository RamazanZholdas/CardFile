import boto3
from datetime import datetime, timedelta

iam = boto3.client('iam')
threshold = timedelta(days=60)
threshold2 = timedelta(days=180)
now = datetime.utcnow()
users = iam.list_users()['Users']


def grants_administrator_access(policy_document):
    for statement in policy_document['Statement']:
        if 'Effect' in statement and statement['Effect'] == 'Allow':
            if 'Action' in statement and statement['Action'] == '*':
                if 'Resource' in statement and statement['Resource'] == '*':
                    return True
    return False


for user in users:
    user_name = user['UserName']
    managed_policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
    has_administrator_access = any(policy['PolicyName'] == 'AdministratorAccess' for policy in managed_policies)

    if not has_administrator_access:
        inline_policies = iam.list_user_policies(UserName=user_name)['PolicyNames']

        for policy_name in inline_policies:
            policy_document = iam.get_user_policy(UserName=user_name, PolicyName=policy_name)['PolicyDocument']

            if grants_administrator_access(policy_document):
                has_administrator_access = True
                break

    if not has_administrator_access:
        groups = iam.list_groups_for_user(UserName=user_name)['Groups']

        for group in groups:
            group_managed_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']

            if any(policy['PolicyName'] == 'AdministratorAccess' for policy in group_managed_policies):
                has_administrator_access = True
                break

            if not has_administrator_access:
                group_inline_policies = iam.list_group_policies(GroupName=group['GroupName'])['PolicyNames']

                for policy_name in group_inline_policies:
                    policy_document = iam.get_group_policy(GroupName=group['GroupName'], PolicyName=policy_name)[
                        'PolicyDocument']

                    if grants_administrator_access(policy_document):
                        has_administrator_access = True
                        break

    if has_administrator_access:
        continue

    job_id = iam.generate_service_last_accessed_details(Arn=user['Arn'])['JobId']
    while iam.get_service_last_accessed_details(JobId=job_id)['JobStatus'] != 'COMPLETED':
        continue

    services_last_accessed = iam.get_service_last_accessed_details(JobId=job_id)['ServicesLastAccessed']

    for service in services_last_accessed:
        if 'LastAuthenticated' not in service or service['LastAuthenticated'] is None:
            print(f"The service {service['ServiceName']} was never accessed by the user {user_name}.")
        elif now - service['LastAuthenticated'].replace(tzinfo=None) > threshold2:
            print(f"The service {service['ServiceName']} was last accessed more than 180 days ago by the user {user_name}.")
        elif now - service['LastAuthenticated'].replace(tzinfo=None) > threshold:
            print(f"The service {service['ServiceName']} was last accessed more than 60 days ago by the user {user_name}.")
