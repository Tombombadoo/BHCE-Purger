import requests
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="A script to purge all data from Bloodhound-CE")
    parser.add_argument('url', type=str, help='The Bloodhound URL including httpx and port if non-standard')
    parser.add_argument('id', type=str, help='The Bloodhound API ID')
    parser.add_argument('key', type=str, help='The Bloodhound API Key')
    args = parser.parse_args()

    # First API call (login)
    login_url = f"{args.url}/api/v2/login"
    login_data = {
        "login_method": "secret",
        "username": args.id,
        "secret": args.key
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(login_url, json=login_data, headers=headers)

    # Check if login was successful and extract the token
    if response.status_code == 200:
        try:
            data = response.json().get('data')
            print(data)
            token = data["session_token"]
            if token:
                print("Authentication successful, token obtained.")
            else:
                print("Token not found in response.")
                exit(1)
        except ValueError:
            print("Failed to parse JSON response.")
            exit(1)
    else:
        print(f"Authentication failed with status code {response.status_code}")
        exit(1)

    # Second API call (clear database)
    clear_db_url = f"{args.url}/api/v2/clear-database"
    clear_db_data = {
        "deleteCollectedGraphData": True,
        "deleteFileIngestHistory": True,
        "deleteDataQualityHistory": True,
        "deleteAssetGroupSelectors": [0]
    }

    # Add token to headers for authorization
    clear_db_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    clear_db_response = requests.post(clear_db_url, json=clear_db_data, headers=clear_db_headers)

    # Check if the second request was successful
    if clear_db_response.status_code == 204:
        print("Database cleared successfully.")
    else:
        print(f"Failed to clear database with status code {clear_db_response.status_code}")

if __name__ == "__main__":
    main()