import pandas as pd

# create an empty dataframe
df = pd.DataFrame(columns=['Username', 'ServiceNamespace', 'PolicyName', 'PolicyType', 'PolicyArn', 'EntityType', 'EntityName'])

# example response data
response_data = [{'ServiceNamespace': 'autoscaling', 'Policies': [{'PolicyName': 'CloudWatchReadOnlyAccess', 'PolicyType': 'MANAGED', 'PolicyArn': 'arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess'}]}, {'ServiceNamespace': 'events', 'Policies': [{'PolicyName': 'CloudWatchEventsReadOnlyAccess', 'PolicyType': 'MANAGED', 'PolicyArn': 'arn:aws:iam::aws:policy/CloudWatchEventsReadOnlyAccess'}]}, {'ServiceNamespace': 'kms', 'Policies': [{'PolicyName': 'kms-secrets-keys', 'PolicyType': 'INLINE', 'EntityType': 'GROUP', 'EntityName': 'conform5-support-team'}]}, {'ServiceNamespace': 'schemas', 'Policies': [{'PolicyName': 'CloudWatchEventsReadOnlyAccess', 'PolicyType': 'MANAGED', 'PolicyArn': 'arn:aws:iam::aws:policy/CloudWatchEventsReadOnlyAccess'}]}, {'ServiceNamespace': 'secretsmanager', 'Policies': [{'PolicyName': 'integrations-secrets-rw', 'PolicyType': 'INLINE', 'EntityType': 'GROUP', 'EntityName': 'conform5-support-team'}]}, {'ServiceNamespace': 'sns', 'Policies': [{'PolicyName': 'CloudWatchReadOnlyAccess', 'PolicyType': 'MANAGED', 'PolicyArn': 'arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess'}]}, {'ServiceNamespace': 'sqs', 'Policies': [{'PolicyName': 'AmazonSQSReadOnlyAccess', 'PolicyType': 'MANAGED', 'PolicyArn': 'arn:aws:iam::aws:policy/AmazonSQSReadOnlyAccess'}]}]

# example username
username = 'alex.gutnik'

# loop through the response data
for item in response_data:
    # loop through the policies
    for policy in item['Policies']:
        # add a new row to the dataframe with the relevant data
        df = pd.concat([df, pd.DataFrame({'Username': [username],
                                           'ServiceNamespace': [item['ServiceNamespace']],
                                           'PolicyName': [policy['PolicyName']],
                                           'PolicyType': [policy['PolicyType']],
                                           'PolicyArn': [policy.get('PolicyArn', '')],
                                           'EntityType': [policy.get('EntityType', '')],
                                           'EntityName': [policy.get('EntityName', '')]})], ignore_index=True)

# output the dataframe
df.to_excel('data.xlsx', index=False)
