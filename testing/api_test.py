
import requests

r = requests.get('https://movies.expectedbehaviors.com/api')
print(r.json)
