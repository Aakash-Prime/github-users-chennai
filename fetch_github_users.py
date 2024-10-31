import requests
import pandas as pd

def fetch_users(location='Chennai', min_followers=50):
    url = 'https://api.github.com/search/users'
    params = {
        'q': f'location:{location} followers:>{min_followers}',
        'per_page': 100,
        'page': 1
    }

    users = []
    while True:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break

        data = response.json()
        users.extend(data['items'])

        if 'next' in response.links:
            params['page'] += 1
        else:
            break

    return users

# Fetch users and save to CSV
users = fetch_users()
print(users)  # Print the raw user data to inspect it

users_df = pd.DataFrame(users)
print(users_df.columns)  # Check what columns were returned

# Safely access the 'company' column, filling with empty strings if it doesn't exist
if 'company' in users_df.columns:
    users_df['company'] = users_df['company'].str.strip().str.lstrip('@').str.upper()
else:
    users_df['company'] = ''  # Set to empty string if 'company' does not exist

users_df.to_csv('users.csv', index=False)

print("User data saved to users.csv")
