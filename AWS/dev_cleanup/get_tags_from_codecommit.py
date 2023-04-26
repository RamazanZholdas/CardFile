import boto3

codecommit = boto3.client('codecommit')
tag_key = 'Team'

paginator = codecommit.get_paginator('list_repositories')
for page in paginator.paginate():
    for repository in page['repositories']:
        repository_name = repository['repositoryName']
        response = codecommit.list_tags_for_resource(
            resourceArn=f'arn:aws:codecommit:us-east-1:022587608743:{repository_name}'
        )

        tag_value = response['tags'].get(tag_key)
        print(f'Repository: {repository_name}')
        print(f'Tag value: {tag_value}')