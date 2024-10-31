import requests
import pandas as pd
import time

# Replace with your personal access token
TOKEN = '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'

# Function to fetch users based on location and follower count
def fetch_users(location, min_followers):
    url = 'https://api.github.com/search/users'
    params = {
        'q': f'location:{location} followers:>{min_followers}',
        'per_page': 100,
        'page': 1
    }
    headers = {'Authorization': f'token {TOKEN}'}

    users = []
    while True:
        response = requests.get(url, params=params, headers=headers)
        
        # Log the status code for debugging
        print(f"Fetching users: {response.status_code}")

        if response.status_code == 403:  # Rate limit exceeded
            print("Rate limit exceeded. Waiting for reset...")
            reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
            wait_time = reset_time - int(time.time())
            print(f"Waiting for {wait_time} seconds.")
            time.sleep(wait_time)
            continue
        
        response.raise_for_status()  # Ensure the request was successful
        data = response.json()

        if not data['items']:
            break  # Exit loop if no more users are found

        users.extend(data['items'])
        
        if 'next' in response.links:
            params['page'] += 1
        else:
            break

    return users

# Function to fetch repositories for each user
def fetch_repositories(user_logins):
    repositories = []
    headers = {'Authorization': f'token {TOKEN}'}

    for user in user_logins:
        repo_url = f'https://api.github.com/users/{user}/repos'
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()  # Ensure the request was successful

        # Check for rate limiting
        if repo_response.status_code == 403:
            print("Rate limit exceeded for user repos. Exiting...")
            break
        
        repo_data = repo_response.json()
        
        for repo in repo_data:
            license_name = repo['license']['name'] if repo.get('license') else ''
            repositories.append({
                'login': user,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'],
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': license_name
            })

        time.sleep(1)  # Delay to avoid hitting rate limits

    return repositories

# Fetch users
location = 'Chennai'
min_followers = 50
try:
    users = fetch_users(location, min_followers)

    # Create a DataFrame from the user data
    users_df = pd.DataFrame(users)

    # Print the columns to check available fields
    print("Available user columns:", users_df.columns)

    # Check if 'company' exists before processing
    if 'company' in users_df.columns:
        users_df['company'] = users_df['company'].str.strip().str.lstrip('@').str.upper()
    else:
        users_df['company'] = None

    # Save the users DataFrame to a CSV file
    users_df.to_csv('users.csv', index=False)

    # Fetch repositories for each user
    repositories = fetch_repositories(users_df['login'])

    # Create a DataFrame for repositories and save to CSV
    repositories_df = pd.DataFrame(repositories)
    repositories_df.to_csv('repositories.csv', index=False)

    print(f"Retrieved {len(users_df)} users and {len(repositories_df)} repositories, saved to 'users.csv' and 'repositories.csv'")

except Exception as e:
    print(f"An error occurred: {e}")
