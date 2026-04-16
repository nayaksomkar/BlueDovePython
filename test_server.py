import requests

try:
    r = requests.get('http://localhost:8000/')
    print('Status:', r.status_code)
    print('Content:', r.text[:500])
except Exception as e:
    print('Error:', e)

try:
    r = requests.get('http://localhost:8000/api/info')
    print('\nAPI Info:', r.json())
except Exception as e:
    print('API Error:', e)
