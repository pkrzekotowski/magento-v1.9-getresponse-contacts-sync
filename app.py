import requests
import json
import schedule
import time

# Set your API keys here
MAGENTO_API_KEY = 'your_magento_api_key'
GETRESPONSE_API_KEY = 'your_getresponse_api_key'

# Set the Magento and GetResponse API endpoints
MAGENTO_API_URL = 'https://yourmagentostore.com/api/rest/customers'
GETRESPONSE_API_URL = 'https://api.getresponse.com/v3/contacts'

# Set the GetResponse contact list IDs where you want to add the contacts
GETRESPONSE_ENGLISH_LIST_ID = 'your_getresponse_english_list_id'
GETRESPONSE_SPANISH_LIST_ID = 'your_getresponse_spanish_list_id'

def get_magento_contacts():
    # Make a request to the Magento API to get the email contacts and language
    headers = {'Authorization': 'Bearer ' + MAGENTO_API_KEY}
    response = requests.get(MAGENTO_API_URL, headers=headers)

    if response.status_code == 200:
        # Extract the email addresses and language from the response
        contacts = json.loads(response.text)
        contact_list = [
            {'email': contact['email'], 'language': contact['language']}
            for contact in contacts
        ]
        return contact_list
    else:
        print('Error fetching Magento contacts:', response.status_code)
        return []

def send_to_getresponse(contact_list):
    # Send the contact list to GetResponse
    headers = {
        'Authorization': 'Bearer ' + GETRESPONSE_API_KEY,
        'Content-Type': 'application/json'
    }

    for contact in contact_list:
        # Choose the GetResponse list based on language
        if contact['language'] == 'English':
            list_id = GETRESPONSE_ENGLISH_LIST_ID
        elif contact['language'] == 'Spanish':
            list_id = GETRESPONSE_SPANISH_LIST_ID
        else:
            # Skip if the language is neither English nor Spanish
            continue

        # Create the payload for each contact
        payload = json.dumps({
            'email': contact['email'],
            'campaign': {'campaignId': list_id}
        })
        # Make a POST request to the GetResponse API to add the contact
        response = requests.post(GETRESPONSE_API_URL, headers=headers, data=payload)

        if response.status_code != 201:
            print('Error adding contact to GetResponse:', response.status_code)

def job():
    # Get the contacts from Magento
    contact_list = get_magento_contacts()
    # Send the contacts to GetResponse
    send_to_getresponse(contact_list)

# Schedule the job to run every 20 minutes
schedule.every(20).minutes.do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
