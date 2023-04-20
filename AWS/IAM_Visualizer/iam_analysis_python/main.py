import boto3
from datetime import datetime, timedelta

# Create an IAM client
iam = boto3.client('iam')

# Set the threshold for unused policies to 60 days
threshold = timedelta(days=60)

# Get the current date and time (offset-naive)
now = datetime.utcnow()

# List all users
users = iam.list_users()['Users']


def grants_administrator_access(policy_document):
    # For each statement in the policy document
    for statement in policy_document['Statement']:
        # If the statement has an "Effect" key with the value "Allow"
        if 'Effect' in statement and statement['Effect'] == 'Allow':
            # If the statement has an "Action" key with the value "*"
            if 'Action' in statement and statement['Action'] == '*':
                # If the statement has a "Resource" key with the value "*"
                if 'Resource' in statement and statement['Resource'] == '*':
                    # Return True
                    return True

    # Return False
    return False


# For each user
for user in users:
    # Get the user name
    user_name = user['UserName']

    # Get the managed policies attached to the user
    managed_policies = iam.list_attached_user_policies(UserName=user_name)['AttachedPolicies']

    # Check if the user has the AdministratorAccess managed policy attached
    has_administrator_access = any(policy['PolicyName'] == 'AdministratorAccess' for policy in managed_policies)

    # If the user doesn't have the AdministratorAccess managed policy attached directly
    if not has_administrator_access:
        # Get the inline policies attached to the user
        inline_policies = iam.list_user_policies(UserName=user_name)['PolicyNames']

        # For each inline policy
        for policy_name in inline_policies:
            # Get the policy document
            policy_document = iam.get_user_policy(UserName=user_name, PolicyName=policy_name)['PolicyDocument']

            # Check if the policy grants administrator access (you need to implement this function)
            if grants_administrator_access(policy_document):
                # Set has_administrator_access to True and break out of the loop
                has_administrator_access = True
                break

    # If the user doesn't have the AdministratorAccess policy attached directly (managed or inline)
    if not has_administrator_access:
        # Get the groups that the user is a member of
        groups = iam.list_groups_for_user(UserName=user_name)['Groups']

        # For each group
        for group in groups:
            # Get the managed policies attached to the group
            group_managed_policies = iam.list_attached_group_policies(GroupName=group['GroupName'])['AttachedPolicies']

            # Check if the group has the AdministratorAccess managed policy attached
            if any(policy['PolicyName'] == 'AdministratorAccess' for policy in group_managed_policies):
                # Set has_administrator_access to True and break out of the loop
                has_administrator_access = True
                break

            # If the group doesn't have the AdministratorAccess managed policy attached
            if not has_administrator_access:
                # Get the inline policies attached to the group
                group_inline_policies = iam.list_group_policies(GroupName=group['GroupName'])['PolicyNames']

                # For each inline policy
                for policy_name in group_inline_policies:
                    # Get the policy document
                    policy_document = iam.get_group_policy(GroupName=group['GroupName'], PolicyName=policy_name)[
                        'PolicyDocument']

                    # Check if the policy grants administrator access (you need to implement this function)
                    if grants_administrator_access(policy_document):
                        # Set has_administrator_access to True and break out of the loop
                        has_administrator_access = True
                        break

    # If the user has the AdministratorAccess policy attached (directly or via a group)
    if has_administrator_access:
        # Ignore the user
        continue

    # Generate a report for the user
    job_id = iam.generate_service_last_accessed_details(Arn=user['Arn'])['JobId']

    # Wait for the report to be generated
    while iam.get_service_last_accessed_details(JobId=job_id)['JobStatus'] != 'COMPLETED':
        continue

    # Get the report details
    services_last_accessed = iam.get_service_last_accessed_details(JobId=job_id)['ServicesLastAccessed']

    # For each service in the report
    for service in services_last_accessed:
        # If the service was never accessed or was last accessed more than 60 days ago
        if 'LastAuthenticated' not in service or service['LastAuthenticated'] is None:
            print(f"The service {service['ServiceName']} was never accessed by the user {user_name}.")
        elif now - service['LastAuthenticated'].replace(tzinfo=None) > threshold:
            # Print the service name and the user name
            print(f"The service {service['ServiceName']} was last accessed more than 60 days ago by the user {user_name}.")
