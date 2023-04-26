import boto3
from datetime import datetime, timedelta
from dateutil.tz import tzlocal


def get_list_of_inactive_users(days):
    iam = boto3.client('iam', region_name='us-east-1')
    threshold = datetime.now(tzlocal()) - timedelta(days=days)

    inactive_users = []
    paginator = iam.get_paginator('list_users')
    for page in paginator.paginate():
        for user in page['Users']:
            if '.' not in user['UserName'] and ('-' in user['UserName'] or '_' in user['UserName']):
                continue

            user_tags = iam.list_user_tags(UserName=user['UserName'])['Tags']
            if any(tag['Key'] == 'InactiveWarningSent' for tag in user_tags):
                continue

            if 'PasswordLastUsed' in user:
                last_console_access = user['PasswordLastUsed']
            else:
                last_console_access = None

            access_keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
            last_used_dates = []
            for key in access_keys:
                last_used = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])['AccessKeyLastUsed']
                if 'LastUsedDate' in last_used:
                    last_used_dates.append(last_used['LastUsedDate'])
            if last_used_dates:
                last_programmatic_access = max(last_used_dates)
            else:
                last_programmatic_access = None

            if (last_console_access is None or last_console_access < threshold) and (
                    last_programmatic_access is None or last_programmatic_access < threshold):
                inactive_users.append(user['UserName'])
                warning_tag = {'Key': 'InactiveWarningSent', 'Value': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                iam.tag_user(UserName=user['UserName'], Tags=[warning_tag])

    return inactive_users


def send_warning(user_name, inactive_users):
    ses_client = boto3.client('ses', region_name='us-east-1')

    users = 'List of inactive users: '
    for idx, user in enumerate(inactive_users):
        if idx == len(inactive_users) - 1:
            users += user + "."
            break
        users += user + ", "

    email_body = 'You have not been active in AWS for 6 months. \n'
    email_body += 'If you don\'t log in within a week, your account will be deleted. \n'
    email_body += users + "\n"
    response = ses_client.send_email(
        Source='ramazan.zholdas@edetek.com',
        Destination={
            'ToAddresses': [user_name]
        },
        Message={
            'Subject': {
                'Charset': 'UTF-8',
                'Data': 'AWS User deletion warning'
            },
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': email_body
                }
            }
        }
    )

    return response


def lambda_handler():
    inactive_users = get_list_of_inactive_users(180)
    print(send_warning("ramazan.zholdas@edetek.com", inactive_users))


lambda_handler()
