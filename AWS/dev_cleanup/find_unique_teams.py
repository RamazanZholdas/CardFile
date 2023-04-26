file_name = 'code_commit_tags.txt'

unique_tags = set()

with open(file_name, 'r') as file:
    for line in file:
        if line.startswith('Tag value:'):
            tag_value = line.split(': ')[1].strip()
            unique_tags.add(tag_value)

print(f'Number of unique tag values: {len(unique_tags)}')
print(unique_tags)