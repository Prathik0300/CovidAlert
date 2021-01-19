from __future__ import print_function
import pickle as pkl
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def GettingPhoneNumber():


    SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']
    """Shows basic usage of the People API.
        Prints the name of the first 10 connections.
    """
    creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pkl.load(token)
        # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pkl.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

        # Call the People API
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses,phoneNumbers').execute()
    connections = results.get('connections', [])
    phoneDir = {}
    for person in connections:
            
        names = person.get('names', [])
        print(names)
        no = person.get('phoneNumbers', [])
        if names:
            name = names[0].get('displayName')
            print(name)
if __name__ == "__main__":
    GettingPhoneNumber()