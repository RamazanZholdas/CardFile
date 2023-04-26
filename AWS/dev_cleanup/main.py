import boto3
from datetime import datetime, timedelta

iam = boto3.client('iam')
threshold = timedelta(days=365)
now = datetime.utcnow()
#users = iam.list_users()['Users']
exception_list = []
all_users = []
def grants_administrator_access(policy_document, user_name):
    for statement in policy_document['Statement']:
        if statement == "Effect":
            exception_list.append(user_name)
            return False
        if 'Effect' in statement and statement['Effect'] == 'Allow':
            if 'Action' in statement and statement['Action'] == '*':
                if 'Resource' in statement and statement['Resource'] == '*':
                    return True
    return False


marker = None
while True:
    if marker:
        response = iam.list_users(Marker=marker)
    else:
        response = iam.list_users()
    users = response['Users']
    for user in users:
        user_name = user['UserName']
        all_users.append(user_name)
        # managed_policies is policy that is directly attached
        managed_policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']
        has_administrator_access = any(policy['PolicyName'] == 'AdministratorAccess' for policy in managed_policies)
    
        if not has_administrator_access:
            inline_policies = iam.list_user_policies(UserName=user_name)['PolicyNames']
    
            for policy_name in inline_policies:
                # policy_document is inline policies
                policy_document = iam.get_user_policy(UserName=user_name, PolicyName=policy_name)['PolicyDocument']

                if grants_administrator_access(policy_document, user_name):
                    has_administrator_access = True
                    break
                
        if not has_administrator_access:
            # list of groups that user belong to
            groups = iam.list_groups_for_user(UserName=user_name)['Groups']
    
            for group in groups:
                group_managed_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']

                if any(policy['PolicyName'] == 'AdministratorAccess' for policy in group_managed_policies):
                    has_administrator_access = True
                    break
                
                if not has_administrator_access:
                    group_inline_policies = iam.list_group_policies(GroupName=group['GroupName'])['PolicyNames']
    
                    for policy_name in group_inline_policies:
                        # policy_document is inline policies
                        policy_document = iam.get_group_policy(GroupName=group['GroupName'], PolicyName=policy_name)[
                            'PolicyDocument']
    
                        if grants_administrator_access(policy_document, user_name):
                            has_administrator_access = True
                            break
                        
        if has_administrator_access:
            continue

        job_id = iam.generate_service_last_accessed_details(Arn=user['Arn'])['JobId']
        while iam.get_service_last_accessed_details(JobId=job_id)['JobStatus'] != 'COMPLETED':
            continue

        services_last_accessed = iam.get_service_last_accessed_details(JobId=job_id)['ServicesLastAccessed']

        with open('access_advisor_report.txt', 'a') as f:
            for service in services_last_accessed:
                if 'LastAuthenticated' not in service or service['LastAuthenticated'] is None:
                    f.write(f"The service {service['ServiceName']} was never accessed by the user {user_name}.\n")
                elif now - service['LastAuthenticated'].replace(tzinfo=None) > threshold:
                    f.write(
                        f"The service {service['ServiceName']} was last accessed more than 365 days ago by the user {user_name}.\n")

    if response['IsTruncated']:
        marker = response['Marker']
    else:
        break


print("Exception list:", exception_list, len(exception_list))
print("All users", all_users, len(all_users))