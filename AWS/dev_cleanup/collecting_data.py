result = {}
with open('access_advisor_report.txt', 'r') as f:
    for line in f:
        line = line.strip()
        parts = line.split(' ')
        service = ' '.join(parts[2:parts.index('was')])
        user = parts[parts.index('user')+1].replace('.', '.')
        if user not in result:
            result[user] = []
        result[user].append(service)

for user, services in result.items():
    result[user] = ', '.join(services)

print("{")
for user, services in result.items():
    print(f'"{user}": "{services}",')
print("}")