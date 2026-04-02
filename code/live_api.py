import requests

response = requests.get(
    'https://oim.108122.xyz/mass',
    headers={'X-Token': 'nidhinidhi'},  # your first name x2
)
print(response.json())